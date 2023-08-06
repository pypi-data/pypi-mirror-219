from __future__ import annotations

import contextvars as cv
import enum
import json
from collections.abc import (
    Awaitable,
    Callable,
    Collection,
    Iterable,
    Iterator,
    Mapping,
    Sequence,
    Set,
)
from contextlib import AbstractAsyncContextManager, asynccontextmanager, contextmanager
from datetime import datetime, timedelta
from functools import cached_property, lru_cache, wraps
from itertools import chain, filterfalse, product, repeat, starmap
from pathlib import Path, PurePath
from shutil import move
from tempfile import NamedTemporaryFile
from typing import Literal, TypeVar

import sqlalchemy as sa
from attrs import evolve
from loguru import logger
from typing_extensions import Concatenate, Never, ParamSpec, Self, TypeAlias
from yarl import URL

from . import http, pkg_db, pkg_models
from . import results as R
from ._sources.cfcore import CfCoreResolver
from ._sources.github import GithubResolver
from ._sources.instawow import InstawowResolver
from ._sources.tukui import TukuiResolver
from ._sources.wago import WagoResolver
from ._sources.wowi import WowiResolver
from .cataloguer import (
    CATALOGUE_VERSION,
    ComputedCatalogue,
    ComputedCatalogueEntry,
)
from .common import Defn, Strategy
from .config import Config
from .http import make_generic_progress_ctx, make_pkg_progress_ctx
from .plugins import load_plugins
from .resolvers import HeadersIntent, Resolver
from .utils import (
    StrEnum,
    WeakValueDefaultDictionary,
    bucketise,
    chain_dict,
    file_uri_to_path,
    find_addon_zip_tocs,
    gather,
    is_file_uri,
    make_zip_member_filter_fn,
    normalise_names,
    shasum,
    time_op,
    trash,
    uniq,
)
from .utils import run_in_thread as t

_P = ParamSpec('_P')
_T = TypeVar('_T')

_AsyncNamedTemporaryFile = t(NamedTemporaryFile)
_move_async = t(move)


def bucketise_results(
    values: Iterable[tuple[Defn, R.AnyResult[_T]]],
) -> tuple[Mapping[Defn, _T], Mapping[Defn, R.AnyResult[Never]]]:
    ts: dict[Defn, _T] = {}
    errors: dict[Defn, R.AnyResult[Never]] = {}

    for defn, value in values:
        if isinstance(value, (R.ManagerError, R.InternalError)):
            errors[defn] = value
        else:
            ts[defn] = value

    return ts, errors


@asynccontextmanager
async def _open_temp_writer_async():
    fh = await _AsyncNamedTemporaryFile(delete=False)
    path = Path(fh.name)
    try:
        yield (path, t(fh.write))
    except BaseException:
        await t(fh.close)()
        await t(path.unlink)()
        raise
    else:
        await t(fh.close)()


@contextmanager
def _open_pkg_archive(path: PurePath):
    from zipfile import ZipFile

    with ZipFile(path) as archive:

        def extract(parent: Path) -> None:
            archive.extractall(parent, members=filter(make_zip_member_filter_fn(base_dirs), names))

        names = archive.namelist()
        base_dirs = {h for _, h in find_addon_zip_tocs(names)}
        yield (base_dirs, extract)


@object.__new__
class _DummyResolver:
    async def resolve(self, defns: Sequence[Defn]) -> dict[Defn, R.AnyResult[pkg_models.Pkg]]:
        return dict.fromkeys(defns, R.PkgSourceInvalid())

    async def get_changelog(self, uri: URL) -> str:
        raise R.PkgSourceInvalid


async def capture_manager_exc_async(
    awaitable: Awaitable[_T],
) -> R.AnyResult[_T]:
    "Capture and log an exception raised in a coroutine."
    from aiohttp import ClientError

    try:
        return await awaitable
    except (R.ManagerError, R.InternalError) as error:
        return error
    except ClientError as error:
        logger.opt(exception=True).info('network error')
        return R.InternalError(error)
    except BaseException as error:
        logger.exception('unclassed error')
        return R.InternalError(error)


class _DummyLock:
    async def __aenter__(self):
        pass

    async def __aexit__(self, *args: object):
        pass


def _with_lock(
    lock_name: str,
    *,
    manager_bound: bool = True,
):
    def outer(
        coro_fn: Callable[Concatenate[Manager, _P], Awaitable[_T]]
    ) -> Callable[Concatenate[Manager, _P], Awaitable[_T]]:
        @wraps(coro_fn)
        async def inner(self: Manager, *args: _P.args, **kwargs: _P.kwargs):
            async with self.locks[(lock_name, id(self)) if manager_bound else lock_name]:
                return await coro_fn(self, *args, **kwargs)

        return inner

    return outer


class _StandardLocks(StrEnum):
    LoadCatalogue = enum.auto()
    MutatePkgs = enum.auto()
    DownloadPkg = enum.auto()


class _Resolvers(dict[str, Resolver]):
    @cached_property
    def priority_dict(self) -> _ResolverPriorityDict:
        return _ResolverPriorityDict(self)

    @cached_property
    def addon_toc_key_and_id_pairs(self) -> Collection[tuple[str, str]]:
        return [
            (r.metadata.addon_toc_key, r.metadata.id)
            for r in self.values()
            if r.metadata.addon_toc_key
        ]


class _ResolverPriorityDict(dict[str, float]):
    def __init__(self, resolvers: _Resolvers) -> None:
        super().__init__((n, i) for i, n in enumerate(resolvers))

    def __missing__(self, key: str) -> float:
        return float('inf')


_web_client = cv.ContextVar[http.ClientSessionType]('_web_client')

LocksType: TypeAlias = Mapping[object, AbstractAsyncContextManager[None]]

_locks = cv.ContextVar[LocksType]('_locks', default=WeakValueDefaultDictionary(_DummyLock))


def contextualise(
    *,
    web_client: http.ClientSessionType | None = None,
    locks: LocksType | None = None,
) -> None:
    "Set variables for the current context."
    if web_client is not None:
        _web_client.set(web_client)
    if locks is not None:
        _locks.set(locks)


@lru_cache(1)
def _parse_catalogue(raw_catalogue: bytes):
    with time_op(lambda t: logger.debug(f'parsed catalogue in {t:.3f}s')):
        return ComputedCatalogue.from_base_catalogue(json.loads(raw_catalogue))


class Manager:
    RESOLVERS: Sequence[type[Resolver]] = [
        GithubResolver,
        CfCoreResolver,
        WowiResolver,
        TukuiResolver,
        InstawowResolver,
        WagoResolver,
    ]
    'Default resolvers.'

    _base_catalogue_url = (
        f'https://raw.githubusercontent.com/layday/instawow-data/data/'
        f'base-catalogue-v{CATALOGUE_VERSION}.compact.json'
    )
    _catalogue_ttl = timedelta(hours=4)

    _normalise_search_terms = staticmethod(normalise_names(''))

    def __init__(
        self,
        config: Config,
        database: sa.Engine,
    ) -> None:
        self.config: Config = config
        self.database: sa.Engine = database

        builtin_resolver_classes = list(self.RESOLVERS)

        for resolver, access_token in (
            (r, getattr(self.config.global_config.access_tokens, r.requires_access_token, None))
            for r in self.RESOLVERS
            if r.requires_access_token is not None
        ):
            if access_token is None:
                builtin_resolver_classes.remove(resolver)

        plugin_hook = load_plugins()
        resolver_classes = chain(
            (r for g in plugin_hook.instawow_add_resolvers() for r in g), builtin_resolver_classes
        )
        self.resolvers = _Resolvers((r.metadata.id, r(self)) for r in resolver_classes)

    @classmethod
    def from_config(cls, config: Config) -> Self:
        "Instantiate the manager from a configuration object."
        return cls(config, pkg_db.prepare_database(config.db_uri))

    @property
    def locks(self) -> LocksType:
        "Lock factory used to synchronise async operations."
        return _locks.get()

    @property
    def web_client(self) -> http.ClientSessionType:
        return _web_client.get()

    def pair_uri(self, value: str) -> tuple[str, str] | None:
        "Attempt to extract a valid ``Defn`` source and alias from a URL."
        aliases_from_url = (
            (r.metadata.id, a)
            for r in self.resolvers.values()
            for a in (r.get_alias_from_url(URL(value)),)
            if a
        )
        return next(aliases_from_url, None)

    def check_pkg_exists(self, defn: Defn) -> bool:
        "Check that a package exists in the database."
        with self.database.connect() as connection:
            return (
                connection.execute(
                    sa.select(sa.text('1'))
                    .select_from(pkg_db.pkg)
                    .where(
                        pkg_db.pkg.c.source == defn.source,
                        (pkg_db.pkg.c.id == defn.alias)
                        | (pkg_db.pkg.c.id == defn.id)
                        | (sa.func.lower(pkg_db.pkg.c.slug) == sa.func.lower(defn.alias)),
                    )
                ).scalar()
                == 1
            )

    def get_pkg(self, defn: Defn, partial_match: bool = False) -> pkg_models.Pkg | None:
        "Retrieve a package from the database."
        with self.database.connect() as connection:
            maybe_row_mapping = (
                connection.execute(
                    sa.select(pkg_db.pkg).where(
                        pkg_db.pkg.c.source == defn.source,
                        (pkg_db.pkg.c.id == defn.alias)
                        | (pkg_db.pkg.c.id == defn.id)
                        | (sa.func.lower(pkg_db.pkg.c.slug) == sa.func.lower(defn.alias)),
                    )
                )
                .mappings()
                .one_or_none()
            )
            if maybe_row_mapping is None and partial_match:
                maybe_row_mapping = (
                    connection.execute(
                        sa.select(pkg_db.pkg)
                        .where(pkg_db.pkg.c.slug.contains(defn.alias))
                        .order_by(pkg_db.pkg.c.name)
                    )
                    .mappings()
                    .first()
                )
            if maybe_row_mapping is not None:
                return pkg_models.Pkg.from_row_mapping(connection, maybe_row_mapping)

    @t
    def _install_pkg(self, pkg: pkg_models.Pkg, archive: Path, replace: bool) -> R.PkgInstalled:
        with _open_pkg_archive(archive) as (top_level_folders, extract):
            with self.database.connect() as connection:
                installed_conflicts = connection.execute(
                    sa.select(pkg_db.pkg)
                    .distinct()
                    .join(pkg_db.pkg_folder)
                    .where(pkg_db.pkg_folder.c.name.in_(top_level_folders))
                ).all()
            if installed_conflicts:
                raise R.PkgConflictsWithInstalled(installed_conflicts)

            if replace:
                trash(
                    (self.config.addon_dir / f for f in top_level_folders),
                    dest=self.config.global_config.temp_dir,
                    missing_ok=True,
                )
            else:
                unreconciled_conflicts = top_level_folders & {
                    f.name for f in self.config.addon_dir.iterdir()
                }
                if unreconciled_conflicts:
                    raise R.PkgConflictsWithUnreconciled(unreconciled_conflicts)

            extract(self.config.addon_dir)

        pkg = evolve(
            pkg, folders=[pkg_models.PkgFolder(name=f) for f in sorted(top_level_folders)]
        )
        with self.database.begin() as transaction:
            pkg.insert(transaction)

        return R.PkgInstalled(pkg)

    @t
    def _update_pkg(
        self, old_pkg: pkg_models.Pkg, new_pkg: pkg_models.Pkg, archive: Path
    ) -> R.PkgUpdated:
        with _open_pkg_archive(archive) as (top_level_folders, extract):
            with self.database.connect() as connection:
                installed_conflicts = connection.execute(
                    sa.select(pkg_db.pkg)
                    .distinct()
                    .join(pkg_db.pkg_folder)
                    .where(
                        pkg_db.pkg_folder.c.pkg_source != new_pkg.source,
                        pkg_db.pkg_folder.c.pkg_id != new_pkg.id,
                        pkg_db.pkg_folder.c.name.in_(top_level_folders),
                    )
                ).all()
            if installed_conflicts:
                raise R.PkgConflictsWithInstalled(installed_conflicts)

            unreconciled_conflicts = top_level_folders - {f.name for f in old_pkg.folders} & {
                f.name for f in self.config.addon_dir.iterdir()
            }
            if unreconciled_conflicts:
                raise R.PkgConflictsWithUnreconciled(unreconciled_conflicts)

            trash(
                (self.config.addon_dir / f.name for f in old_pkg.folders),
                dest=self.config.global_config.temp_dir,
                missing_ok=True,
            )
            extract(self.config.addon_dir)

        new_pkg = evolve(
            new_pkg, folders=[pkg_models.PkgFolder(name=f) for f in sorted(top_level_folders)]
        )
        with self.database.begin() as transaction:
            old_pkg.delete(transaction)
            new_pkg.insert(transaction)

        return R.PkgUpdated(old_pkg, new_pkg)

    @t
    def _remove_pkg(self, pkg: pkg_models.Pkg, keep_folders: bool) -> R.PkgRemoved:
        if not keep_folders:
            trash(
                (self.config.addon_dir / f.name for f in pkg.folders),
                dest=self.config.global_config.temp_dir,
                missing_ok=True,
            )

        with self.database.begin() as transaction:
            pkg.delete(transaction)

        return R.PkgRemoved(pkg)

    @_with_lock(_StandardLocks.LoadCatalogue, manager_bound=False)
    async def synchronise(self) -> ComputedCatalogue:
        "Fetch the catalogue from the interwebs and load it."
        async with self.web_client.get(
            self._base_catalogue_url,
            expire_after=self._catalogue_ttl,
            raise_for_status=True,
            trace_request_ctx=make_generic_progress_ctx('Synchronising catalogue'),
        ) as response:
            raw_catalogue = await response.read()
        return _parse_catalogue(raw_catalogue)

    async def find_equivalent_pkg_defns(
        self, pkgs: Collection[pkg_models.Pkg]
    ) -> dict[pkg_models.Pkg, list[Defn]]:
        "Given a list of packages, find ``Defn``s of each package from other sources."
        from .matchers import AddonFolder

        catalogue = await self.synchronise()

        @t
        def collect_addon_folders():
            return {
                p: frozenset(
                    a
                    for f in p.folders
                    for a in (
                        AddonFolder.from_addon_path(
                            self.config.game_flavour, self.config.addon_dir / f.name
                        ),
                    )
                    if a
                )
                for p in pkgs
            }

        async def collect_hashed_folder_defns():
            matches = [
                m
                for r in self.resolvers.values()
                for m in await r.get_folder_hash_matches(
                    [a for p, f in folders_per_pkg.items() if p.source != r.metadata.id for a in f]
                )
            ]

            defns_per_pkg: dict[pkg_models.Pkg, frozenset[Defn]] = {
                p: frozenset() for p in folders_per_pkg
            }
            for (pkg, orig_folders), (defn, matched_folders) in product(
                folders_per_pkg.items(), matches
            ):
                if orig_folders == matched_folders:
                    defns_per_pkg[pkg] |= frozenset((defn,))

            return defns_per_pkg

        def get_catalogue_defns(pkg: pkg_models.Pkg) -> frozenset[Defn]:
            entry = catalogue.keyed_entries.get((pkg.source, pkg.id))
            if entry:
                return frozenset(Defn(s.source, s.id) for s in entry.same_as)
            else:
                return frozenset()

        def get_addon_toc_defns(pkg_source: str, addon_folders: Collection[AddonFolder]):
            return frozenset(
                d
                for a in addon_folders
                for d in a.get_defns_from_toc_keys(self.resolvers.addon_toc_key_and_id_pairs)
                if d.source != pkg_source
            )

        folders_per_pkg = await collect_addon_folders()

        with time_op(lambda t: logger.debug(f'hashed folder matches found in {t:.3f}s')):
            hashed_folder_defns = await collect_hashed_folder_defns()

        return {
            p: sorted(d, key=lambda d: self.resolvers.priority_dict[d.source])
            for p in pkgs
            for d in (
                get_catalogue_defns(p)
                | get_addon_toc_defns(p.source, folders_per_pkg[p])
                | hashed_folder_defns[p],
            )
            if d
        }

    async def _resolve_deps(
        self, results: Collection[R.AnyResult[pkg_models.Pkg]]
    ) -> Mapping[Defn, R.AnyResult[pkg_models.Pkg]]:
        """Resolve package dependencies.

        The resolver will not follow dependencies
        more than one level deep.  This is to avoid unnecessary
        complexity for something that I would never expect to
        encounter in the wild.
        """
        pkgs = [r for r in results if isinstance(r, pkg_models.Pkg)]
        dep_defns = uniq(
            filterfalse(
                {(p.source, p.id) for p in pkgs}.__contains__,
                ((p.source, d.id) for p in pkgs for d in p.deps),
            )
        )
        if not dep_defns:
            return {}

        deps = await self.resolve(list(starmap(Defn, dep_defns)))
        pretty_deps = {
            evolve(d, alias=r.slug) if isinstance(r, pkg_models.Pkg) else d: r
            for d, r in deps.items()
        }
        return pretty_deps

    async def resolve(
        self, defns: Collection[Defn], with_deps: bool = False
    ) -> Mapping[Defn, R.AnyResult[pkg_models.Pkg]]:
        "Resolve definitions into packages."
        if not defns:
            return {}

        defns_by_source = bucketise(defns, key=lambda v: v.source)
        results = await gather(
            (self.resolvers.get(s, _DummyResolver).resolve(b) for s, b in defns_by_source.items()),
            capture_manager_exc_async,
        )
        results_by_defn = chain_dict(
            defns,
            R.ManagerError(),
            *(
                r.items() if isinstance(r, dict) else zip(d, repeat(r))
                for d, r in zip(defns_by_source.values(), results)
            ),
        )
        if with_deps:
            results_by_defn.update(await self._resolve_deps(results_by_defn.values()))
        return results_by_defn

    async def get_changelog(self, source: str, uri: str) -> str:
        "Retrieve a changelog from a URI."
        return await self.resolvers.get(source, _DummyResolver).get_changelog(URL(uri))

    async def search(
        self,
        search_terms: str,
        *,
        limit: int,
        sources: Set[str] = frozenset(),
        prefer_source: str | None = None,
        start_date: datetime | None = None,
        filter_installed: Literal[
            'ident', 'include_only', 'exclude', 'exclude_from_all_sources'
        ] = 'ident',
    ) -> list[ComputedCatalogueEntry]:
        "Search the catalogue for packages by name."
        import rapidfuzz

        catalogue = await self.synchronise()

        ew = 0.5
        dw = 1 - ew

        threshold = 0 if search_terms == '*' else 70

        if sources:
            unknown_sources = sources - self.resolvers.keys()
            if unknown_sources:
                raise ValueError(f'Unknown sources: {", ".join(unknown_sources)}')

        if prefer_source and prefer_source not in self.resolvers:
            raise ValueError(f'Unknown preferred source: {prefer_source}')

        def get_installed_pkg_keys():
            with self.database.connect() as connection:
                return (
                    connection.execute(sa.select(pkg_db.pkg.c.source, pkg_db.pkg.c.id))
                    .tuples()
                    .all()
                )

        def make_filter_fns() -> Iterator[Callable[[ComputedCatalogueEntry], bool]]:
            yield lambda e: self.config.game_flavour in e.game_flavours

            if sources:
                yield lambda e: e.source in sources

            if start_date is not None:
                start_date_ = start_date
                yield lambda e: e.last_updated >= start_date_

            if filter_installed in {'exclude', 'exclude_from_all_sources'}:
                installed_pkg_keys = set(get_installed_pkg_keys())
                if filter_installed == 'exclude_from_all_sources':
                    installed_pkg_keys |= {
                        (s.source, s.id)
                        for k in installed_pkg_keys
                        for e in (catalogue.keyed_entries.get(k),)
                        if e
                        for s in e.same_as
                    }

                yield lambda e: (e.source, e.id) not in installed_pkg_keys

        filter_fns = list(make_filter_fns())

        entries = catalogue.entries

        if prefer_source:
            entries = (e for e in entries if not any(s.source == prefer_source for s in e.same_as))

        if filter_installed == 'include_only':
            installed_pkg_keys = get_installed_pkg_keys()
            entries = (
                e for k in installed_pkg_keys for e in (catalogue.keyed_entries.get(k),) if e
            )

        s = self._normalise_search_terms(search_terms)

        tokens_to_entries = bucketise(
            ((e.normalised_name, e) for e in entries if all(f(e) for f in filter_fns)),
            key=lambda v: v[0],
        )
        matches = rapidfuzz.process.extract(
            s,
            list(tokens_to_entries),
            scorer=rapidfuzz.fuzz.WRatio,
            limit=limit * 2,
            score_cutoff=threshold,
        )
        weighted_entries = sorted(
            (
                (-((s / 100) * ew + e.derived_download_score * dw), e)
                for m, s, _ in matches
                for _, e in tokens_to_entries[m]
            ),
            key=lambda v: v[0],
        )
        return [e for _, e in weighted_entries[:limit]]

    async def _download_pkg_archive(self, pkg: pkg_models.Pkg, *, chunk_size: int = 4096):
        if is_file_uri(pkg.download_url):
            return Path(file_uri_to_path(pkg.download_url))

        async with self.locks[_StandardLocks.DownloadPkg, pkg.download_url]:
            dest = self.config.global_config.cache_dir / shasum(pkg.download_url)
            if not await t(dest.exists)():
                async with self.web_client.get(
                    pkg.download_url,
                    headers=await self.resolvers[pkg.source].make_request_headers(
                        intent=HeadersIntent.Download
                    ),
                    raise_for_status=True,
                    trace_request_ctx=make_pkg_progress_ctx(self.config.profile, pkg),
                ) as response, _open_temp_writer_async() as (
                    temp_path,
                    write,
                ):
                    async for chunk in response.content.iter_chunked(chunk_size):
                        await write(chunk)

                await _move_async(temp_path, dest)

            return dest

    @t
    def _check_installed_pkg_integrity(self, pkg: pkg_models.Pkg) -> bool:
        return all((self.config.addon_dir / p.name).exists() for p in pkg.folders)

    async def _should_update_pkg(self, old_pkg: pkg_models.Pkg, new_pkg: pkg_models.Pkg) -> bool:
        return old_pkg.version != new_pkg.version or (
            not await self._check_installed_pkg_integrity(old_pkg)
        )

    @_with_lock(_StandardLocks.MutatePkgs)
    async def install(
        self, defns: Sequence[Defn], replace: bool, dry_run: bool = False
    ) -> Mapping[Defn, R.AnyResult[R.PkgInstalled]]:
        "Install packages from a definition list."

        # We'll weed out installed deps from the results after resolving -
        # doing it this way isn't particularly efficient but avoids having to
        # deal with local state in ``resolve``
        resolve_results = await self.resolve(
            [d for d in defns if not self.check_pkg_exists(d)], with_deps=True
        )
        pkgs, resolve_errors = bucketise_results(resolve_results.items())
        new_pkgs = {d: p for d, p in pkgs.items() if not self.check_pkg_exists(p.to_defn())}

        results = dict.fromkeys(defns, R.PkgAlreadyInstalled()) | resolve_errors

        if dry_run:
            return results | {d: R.PkgInstalled(p, dry_run=True) for d, p in new_pkgs.items()}

        download_results = zip(
            new_pkgs,
            await gather(
                (self._download_pkg_archive(r) for r in new_pkgs.values()),
                capture_manager_exc_async,
            ),
        )
        archive_paths, download_errors = bucketise_results(download_results)

        return (
            results
            | download_errors
            | {
                d: await capture_manager_exc_async(self._install_pkg(new_pkgs[d], a, replace))
                for d, a in archive_paths.items()
            }
        )

    @_with_lock(_StandardLocks.MutatePkgs)
    async def update(
        self, defns: Sequence[Defn], retain_defn_strategy: bool, dry_run: bool = False
    ) -> Mapping[Defn, R.AnyResult[R.PkgInstalled | R.PkgUpdated]]:
        """Update installed packages from a definition list.

        A ``retain_defn_strategy`` value of false will instruct ``update``
        to extract the strategy from the installed package; otherwise
        the ``Defn`` strategy will be used.
        """

        defns_to_pkgs = {d: p for d in defns for p in (self.get_pkg(d),) if p}
        resolve_defns = {
            # Attach the source ID to each ``Defn`` from the
            # corresponding installed package.  Using the ID has the benefit
            # of resolving installed-but-renamed packages - the slug is
            # transient but the ID isn't
            evolve(d, id=p.id) if retain_defn_strategy else p.to_defn(): d
            for d, p in defns_to_pkgs.items()
        }
        resolve_results = await self.resolve(resolve_defns, with_deps=True)
        # Discard the reconstructed ``Defn``s
        orig_defn_resolve_results = (
            (resolve_defns.get(d, d), r) for d, r in resolve_results.items()
        )
        pkgs, resolve_errors = bucketise_results(orig_defn_resolve_results)

        updatables = {
            d: (o, n)
            for d, n in pkgs.items()
            for o in (defns_to_pkgs.get(d),)
            if not o or await self._should_update_pkg(o, n)
        }

        results = (
            dict.fromkeys(defns, R.PkgNotInstalled())
            | resolve_errors
            | {
                d: R.PkgUpToDate(is_pinned=pkgs[d].options.version_eq)
                for d in pkgs.keys() - updatables.keys()
            }
        )

        if dry_run:
            return results | {
                d: R.PkgUpdated(o, n, dry_run=True) if o else R.PkgInstalled(n, dry_run=True)
                for d, (o, n) in updatables.items()
            }

        download_results = zip(
            updatables,
            await gather(
                (self._download_pkg_archive(n) for _, n in updatables.values()),
                capture_manager_exc_async,
            ),
        )
        archive_paths, download_errors = bucketise_results(download_results)

        return (
            results
            | download_errors
            | {
                d: await capture_manager_exc_async(
                    self._update_pkg(o, n, a) if o else self._install_pkg(n, a, False)
                )
                for d, a in archive_paths.items()
                for o, n in (updatables[d],)
            }
        )

    @_with_lock(_StandardLocks.MutatePkgs)
    async def remove(
        self, defns: Sequence[Defn], keep_folders: bool
    ) -> Mapping[Defn, R.AnyResult[R.PkgRemoved]]:
        "Remove packages by their definition."
        return {
            d: (
                await capture_manager_exc_async(self._remove_pkg(p, keep_folders))
                if p
                else R.PkgNotInstalled()
            )
            for d in defns
            for p in (self.get_pkg(d),)
        }

    @_with_lock(_StandardLocks.MutatePkgs)
    async def pin(self, defns: Sequence[Defn]) -> Mapping[Defn, R.AnyResult[R.PkgInstalled]]:
        """Pin and unpin installed packages.

        instawow does not have true pinning.  This flips ``Strategy.VersionEq``
        on for installed packages from sources that support it.
        The net effect is the same as if the package
        had been reinstalled with the ``VersionEq`` strategy.
        """

        @t
        def pin(defn: Defn) -> R.PkgInstalled:
            resolver = self.resolvers.get(defn.source)
            if resolver is None:
                raise R.PkgSourceInvalid

            if Strategy.VersionEq not in resolver.metadata.strategies:
                raise R.PkgStrategiesUnsupported({Strategy.VersionEq})

            pkg = self.get_pkg(defn)
            if not pkg:
                raise R.PkgNotInstalled

            version = defn.strategies.version_eq
            if version and pkg.version != version:
                R.PkgFilesNotMatching(defn.strategies)

            with self.database.begin() as transaction:
                transaction.execute(
                    sa.update(pkg_db.pkg_options)
                    .filter_by(pkg_source=pkg.source, pkg_id=pkg.id)
                    .values(version_eq=version is not None)
                )

            new_pkg = evolve(pkg, options=evolve(pkg.options, version_eq=version is not None))
            return R.PkgInstalled(new_pkg)

        return {d: await capture_manager_exc_async(pin(d)) for d in defns}
