"""
PyScript Component for Smart Home - The Next Generation.

Smart Home - TNG is a Home Automation framework for observing the state
of entities and react to changes. It is based on Home Assistant from
home-assistant.io and the Home Assistant Community.

Copyright (c) 2022-2023, Andreas Nixdorf

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program.  If not, see
http://www.gnu.org/licenses/.


This component is based on the custom_component

Pyscript: Python Scripting for Home Assistant, Copyright (c) 2020-2022 Craig Barrat,
which may be freely used and copied according tho the terms of the Apache 2.0 License.

Original source code and documentation can be found under:
https://github.com/custom-components/pyscript
"""

import glob
import logging
import os
import types
import typing

from ... import core
from .ast_eval import AstEval
from .global_context import GlobalContext
from .source_file import SourceFile

if not typing.TYPE_CHECKING:

    class PyscriptComponent:
        pass


if typing.TYPE_CHECKING:
    from .pyscript_component import PyscriptComponent


_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class GlobalContextMgr:
    """Define class for all global contexts."""

    def __init__(
        self,
        owner: PyscriptComponent,
        controller_is_global: bool = False,
    ) -> None:
        """Report an error if GlobalContextMgr in instantiated."""
        self._contexts: dict[str, GlobalContext] = {}
        self._owner = owner
        self._controller_is_global = controller_is_global

        def get_global_ctx_factory(ast_ctx: AstEval) -> typing.Callable[[], str]:
            """Generate a pyscript.get_global_ctx() function with given ast_ctx."""

            async def get_global_ctx():
                return ast_ctx.global_ctx.name

            return get_global_ctx

        def list_global_ctx_factory(ast_ctx: AstEval) -> typing.Callable[[], list[str]]:
            """Generate a pyscript.list_global_ctx() function with given ast_ctx."""

            async def list_global_ctx():
                ctx_names = set(self._contexts.keys())
                curr_ctx_name = ast_ctx.global_ctx.name
                ctx_names.discard(curr_ctx_name)
                return [curr_ctx_name] + sorted(ctx_names)

            return list_global_ctx

        def set_global_ctx_factory(ast_ctx: AstEval) -> typing.Callable[[str], None]:
            """Generate a pyscript.set_global_ctx() function with given ast_ctx."""

            async def set_global_ctx(name: str):
                global_ctx = self._contexts.get(name)
                if global_ctx is None:
                    raise NameError(f"global context '{name}' does not exist")
                ast_ctx.global_ctx = global_ctx
                ast_ctx.set_logger_name(global_ctx.name)

            return set_global_ctx

        ast_funcs = {
            "pyscript.get_global_ctx": get_global_ctx_factory,
            "pyscript.list_global_ctx": list_global_ctx_factory,
            "pyscript.set_global_ctx": set_global_ctx_factory,
        }

        self.pyscript.functions.register_ast(ast_funcs)

    @property
    def controller(self) -> core.SmartHomeController:
        return self._owner.controller

    @property
    def pyscript(self) -> PyscriptComponent:
        return self._owner

    def create_context(
        self,
        name,
        *,
        generate_unique_name: bool = False,
        global_sym_table: dict[str, typing.Any] = None,
        rel_import_path: str = None,
        app_config: dict[str, typing.Any] = None,
        filepath: str = None,
        source: str = None,
        mtime: float = None,
        module: types.ModuleType = None,
        autostart: bool = False,
    ) -> GlobalContext:
        """create a new GlobalContext."""
        if generate_unique_name:
            name = self._new_name(name)
            if not global_sym_table:
                global_sym_table = {"__name__", name}
            else:
                global_sym_table = global_sym_table.copy()
                global_sym_table["__name__"] = name

        ctx_curr = self._contexts.get(name)
        if ctx_curr:
            self._delete(name)
        result = GlobalContext(
            name,
            global_sym_table=global_sym_table,
            manager=self,
            rel_import_path=rel_import_path,
            app_config=app_config,
            filepath=filepath,
            source=source,
            mtime=mtime,
            module=module,
            autostart=autostart,
            controller_is_global=self._controller_is_global,
        )
        self._contexts[name] = result
        return result

    def get(self, name: str) -> GlobalContext:
        """Return the GlobalContext given a name."""
        return self._contexts.get(name, None)

    def _delete(self, name: str) -> None:
        """Delete the given GlobalContext."""
        global_ctx = self._contexts.pop(name, None)
        if global_ctx:
            global_ctx.stop()

    def _new_name(self, root: str) -> str:
        """Find a unique new name by appending a sequence number to root."""
        name_seq = 0
        while True:
            name = f"{root}{name_seq}"
            name_seq += 1
            if name not in self._contexts:
                return name

    async def load_scripts(self, global_ctx_only: str = None):
        """Load all python scripts in FOLDER."""

        load_paths = [
            # path, glob, check_config, autoload
            ("", "*.py", False, True),
            ("apps", "*/__init__.py", True, True),
            ("apps", "*.py", True, True),
            ("apps", "*/**/*.py", False, False),
            ("modules", "*/__init__.py", False, False),
            ("modules", "*.py", False, False),
            ("modules", "*/**/*.py", False, False),
            ("scripts", "**/*.py", False, True),
        ]

        #
        # get current global contexts
        #
        ctx_all: dict[str, GlobalContext] = {}
        for global_ctx_name, global_ctx in self._contexts.items():
            idx = global_ctx_name.find(".")
            if idx < 0 or global_ctx_name[0:idx] not in {
                "file",
                "apps",
                "modules",
                "scripts",
            }:
                continue
            ctx_all[global_ctx_name] = global_ctx

        #
        # get list and contents of all source files
        #
        apps_config = self.pyscript.config_data.get("apps", None)
        ctx2files = await self.controller.async_add_executor_job(
            _glob_read_files, self.pyscript.pyscript_folder, load_paths, apps_config
        )

        #
        # figure out what to reload based on global_ctx_only and what's changed
        #
        ctx_delete = set()
        if global_ctx_only is not None and global_ctx_only != "*":
            if global_ctx_only not in ctx_all and global_ctx_only not in ctx2files:
                _LOGGER.error(
                    f"pyscript.reload: no global context '{global_ctx_only}' to reload"
                )
                return
            if global_ctx_only not in ctx2files:
                ctx_delete.add(global_ctx_only)
            else:
                ctx2files[global_ctx_only].force = True
        elif global_ctx_only == "*":
            ctx_delete = set(ctx_all.keys())
            for _, src_info in ctx2files.items():
                src_info.force = True
        else:
            # delete all global_ctxs that aren't present in current files
            for global_ctx_name, global_ctx in ctx_all.items():
                if global_ctx_name not in ctx2files:
                    ctx_delete.add(global_ctx_name)
            # delete all global_ctxs that have changeed source or mtime
            for global_ctx_name, src_info in ctx2files.items():
                if global_ctx_name in ctx_all:
                    ctx = ctx_all[global_ctx_name]
                    if (
                        src_info.source != ctx.source
                        or src_info.app_config != ctx.app_config
                        or src_info.mtime != ctx.mtime
                    ):
                        ctx_delete.add(global_ctx_name)
                        src_info.force = True
                else:
                    src_info.force = src_info.autoload

        #
        # force reload if any files uses a module that is bring reloaded by
        # recursively following each import; first find which modules are
        # being reloaded
        #
        will_reload = set()
        for global_ctx_name, src_info in ctx2files.items():
            if global_ctx_name.startswith("modules.") and (
                global_ctx_name in ctx_delete or src_info.force
            ):
                parts = global_ctx_name.split(".")
                root = f"{parts[0]}.{parts[1]}"
                will_reload.add(root)

        if len(will_reload) > 0:
            ctx2imports: dict[str, set[str]] = {}

            def import_recurse(ctx_name, visited: set[str]):
                if ctx_name in visited or ctx_name in ctx2imports:
                    return ctx2imports.get(ctx_name, set())
                visited.add(ctx_name)
                ctx = self.get(ctx_name)
                if not ctx:
                    return set()
                ctx2imports[ctx_name] = set()
                for imp_name in ctx.imports:
                    ctx2imports[ctx_name].add(imp_name)
                    ctx2imports[ctx_name].update(import_recurse(imp_name, visited))
                return ctx2imports[ctx_name]

            for global_ctx_name, global_ctx in ctx_all.items():
                if global_ctx_name not in ctx2imports:
                    visited: set[str] = set()
                    import_recurse(global_ctx_name, visited)
                for mod_name in ctx2imports.get(global_ctx_name, set()):
                    parts = mod_name.split(".")
                    root = f"{parts[0]}.{parts[1]}"
                    if root in will_reload:
                        ctx_delete.add(global_ctx_name)
                        if global_ctx_name in ctx2files:
                            ctx2files[global_ctx_name].force = True

        #
        # if any file in an app or module has changed, then reload just the top-level
        # __init__.py or module/app .py file, and delete everything else
        #
        done = set()
        for global_ctx_name, src_info in ctx2files.items():
            if not src_info.force:
                continue
            if not global_ctx_name.startswith(
                "apps."
            ) and not global_ctx_name.startswith("modules."):
                continue
            parts = global_ctx_name.split(".")
            root = f"{parts[0]}.{parts[1]}"
            if root in done:
                continue
            pkg_path = f"{parts[0]}/{parts[1]}/__init__.py"
            mod_path = f"{parts[0]}/{parts[1]}.py"
            for ctx_name, this_src_info in ctx2files.items():
                if ctx_name == root or ctx_name.startswith(f"{root}."):
                    if this_src_info.rel_path in {pkg_path, mod_path}:
                        this_src_info.force = True
                    else:
                        this_src_info.force = False
                    ctx_delete.add(ctx_name)
            done.add(root)

        #
        # delete contexts that are no longer needed or will be reloaded
        #
        for global_ctx_name in ctx_delete:
            if global_ctx_name in ctx_all:
                global_ctx = ctx_all[global_ctx_name]
                global_ctx.stop()
                if (
                    global_ctx_name not in ctx2files
                    or not ctx2files[global_ctx_name].autoload
                ):
                    _LOGGER.info(f"Unloaded {global_ctx.file_path}")
                self._delete(global_ctx_name)
        await self.pyscript.functions.waiter_sync()

        #
        # now load the requested files, and files that depend on loaded files
        #
        for global_ctx_name, src_info in sorted(ctx2files.items()):
            if not src_info.autoload or not src_info.force:
                continue
            global_ctx = self.create_context(
                src_info.global_ctx_name,
                global_sym_table={"__name__": src_info.fq_mod_name},
                rel_import_path=src_info.rel_import_path,
                app_config=src_info.app_config,
                source=src_info.source,
                mtime=src_info.mtime,
                filepath=src_info.file_path,
            )
            reload = src_info.global_ctx_name in ctx_delete
            # pylint: disable=protected-access
            await global_ctx._load_file(reload=reload)

    async def unload_scripts(
        self, global_ctx_only: str = None, unload_all: bool = False
    ) -> None:
        """Unload all scripts from GlobalContextMgr with given name prefixes."""
        ctx_delete = {}
        for global_ctx_name, global_ctx in self._contexts.items():
            if not unload_all:
                idx = global_ctx_name.find(".")
                if idx < 0 or global_ctx_name[0:idx] not in {
                    "file",
                    "apps",
                    "modules",
                    "scripts",
                }:
                    continue
            if global_ctx_only is not None:
                if (
                    global_ctx_name != global_ctx_only
                    and not global_ctx_name.startswith(global_ctx_only + ".")
                ):
                    continue
            global_ctx.stop()
            ctx_delete[global_ctx_name] = global_ctx

        for global_ctx_name, global_ctx in ctx_delete.items():
            self._delete(global_ctx_name)
        await self.pyscript.functions.waiter_sync()

    def start_global_contexts(self, global_ctx_only: str = None) -> None:
        """Start all the file and apps global contexts."""
        start_list: list[GlobalContext] = []
        for global_ctx in self._contexts.values():
            name = global_ctx.name
            idx = name.find(".")
            if idx < 0 or name[0:idx] not in {"file", "apps", "scripts"}:
                continue
            if global_ctx_only and global_ctx_only != "*":
                if name != global_ctx_only and not name.startswith(
                    global_ctx_only + "."
                ):
                    continue
            global_ctx.set_auto_start(True)
            start_list.append(global_ctx)
        for global_ctx in start_list:
            global_ctx.start()


def _glob_read_files(
    pyscript_dir: str,
    load_paths: list[tuple[str, str, bool, bool]],
    apps_config: dict[str, typing.Any],
) -> dict[str, SourceFile]:
    """Expand globs and read all the source files."""
    ctx2source = {}
    for path, match, check_config, autoload in load_paths:
        for this_path in sorted(
            glob.glob(os.path.join(pyscript_dir, path, match), recursive=True)
        ):
            rel_import_path = None
            rel_path = this_path
            if rel_path.startswith(pyscript_dir):
                rel_path = rel_path[len(pyscript_dir) :]
            if rel_path.startswith("/"):
                rel_path = rel_path[1:]
            if rel_path[0] == "#" or rel_path.find("/#") >= 0:
                # skip "commented" files and directories
                continue
            mod_name = rel_path[0:-3]
            if mod_name.endswith("/__init__"):
                rel_import_path = mod_name
                mod_name = mod_name[: -len("/__init__")]
            mod_name = mod_name.replace("/", ".")
            if path == "":
                global_ctx_name = f"file.{mod_name}"
                fq_mod_name = mod_name
            else:
                fq_mod_name = global_ctx_name = mod_name
                i = fq_mod_name.find(".")
                if i >= 0:
                    fq_mod_name = fq_mod_name[i + 1 :]
            app_config = None

            if global_ctx_name in ctx2source:
                # the globs result in apps/APP/__init__.py matching twice, so skip the 2nd time
                # also skip apps/APP.py if apps/APP/__init__.py is present
                continue

            if check_config:
                app_name = fq_mod_name
                i = app_name.find(".")
                if i >= 0:
                    app_name = app_name[0:i]
                if not isinstance(apps_config, dict) or app_name not in apps_config:
                    _LOGGER.debug(
                        f"load_scripts: skipping {this_path} (app_name={app_name}) because "
                        + "config not present",
                    )
                    continue
                app_config = apps_config[app_name]

            try:
                with open(this_path, encoding="utf-8") as file_desc:
                    source = file_desc.read()
                mtime = os.path.getmtime(this_path)
            except Exception as exc:  # pylint: disable=broad-except
                _LOGGER.error(
                    f"load_scripts: skipping {this_path} due to exception {exc}"
                )
                continue

            ctx2source[global_ctx_name] = SourceFile(
                global_ctx_name=global_ctx_name,
                file_path=this_path,
                rel_path=rel_path,
                rel_import_path=rel_import_path,
                fq_mod_name=fq_mod_name,
                check_config=check_config,
                app_config=app_config,
                source=source,
                mtime=mtime,
                autoload=autoload,
            )

    return ctx2source
