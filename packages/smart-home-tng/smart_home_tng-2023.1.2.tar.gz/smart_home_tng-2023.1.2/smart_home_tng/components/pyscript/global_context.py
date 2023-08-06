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

import logging
import os
import types
import typing

from ... import core
from .ast_eval import AstEval
from .eval_func import EvalFunc
from .trig_info import TrigInfo

if not typing.TYPE_CHECKING:

    class GlobalContextMgr:
        pass

    class PyscriptComponent:
        pass


if typing.TYPE_CHECKING:
    from .global_context_mgr import GlobalContextMgr
    from .pyscript_component import PyscriptComponent


# pylint: disable=unused-variable
class GlobalContext:
    """Define class for global variables and trigger context."""

    def __init__(
        self,
        name: str,
        manager: GlobalContextMgr,
        global_sym_table: dict[str, typing.Any] = None,
        rel_import_path: str = None,
        app_config: dict[str, typing.Any] = None,
        filepath: str = None,
        source: str = None,
        mtime: float = None,
        module: types.ModuleType = None,
        autostart: bool = False,
        controller_is_global: bool = False,
    ) -> None:
        """Initialize GlobalContext."""
        self._name: str = name
        self._global_sym_table = global_sym_table if global_sym_table else {}
        self._triggers: set[EvalFunc] = set()
        self._triggers_delay_start: set[EvalFunc] = set()
        self._logger: logging.Logger = logging.getLogger(__package__ + "." + name)
        self._manager = manager
        self._auto_start = autostart
        self._module = module
        self._rel_import_path: str = rel_import_path
        self._source: str = source
        self._file_path: str = filepath
        self._mtime: float = mtime
        self._app_config: dict[str, typing.Any] = app_config
        self._imports: set[str] = set()
        if controller_is_global and manager:
            #
            # expose hass as a global variable if configured
            #
            # "hass" is depreacated, use "controller" instead
            self._global_sym_table["controller"] = manager.controller
        if app_config:
            self._global_sym_table["pyscript.app_config"] = app_config.copy()
        self._global_sym_table["tng"] = core
        self._global_sym_table["const"] = core.Const
        self._global_sym_table["helpers"] = core.helpers

    @property
    def controller(self) -> core.SmartHomeController:
        if not self._manager:
            return None
        return self._manager.controller

    @property
    def pyscript(self) -> PyscriptComponent:
        return self._manager.pyscript

    def trigger_register(self, func: EvalFunc) -> bool:
        """Register a trigger function; return True if start now."""
        self._triggers.add(func)
        if self._auto_start:
            return True
        self._triggers_delay_start.add(func)
        return False

    def trigger_unregister(self, func: EvalFunc) -> None:
        """Unregister a trigger function."""
        self._triggers.discard(func)
        self._triggers_delay_start.discard(func)

    def set_auto_start(self, auto_start: bool) -> None:
        """Set the auto-start flag."""
        self._auto_start = auto_start

    def start(self) -> None:
        """Start any unstarted triggers."""
        for func in self._triggers_delay_start:
            func.trigger_start()
        self._triggers_delay_start = set()

    def stop(self) -> None:
        """Stop all triggers and auto_start."""
        for func in self._triggers:
            func.trigger_stop()
        self._triggers = set()
        self._triggers_delay_start = set()
        self.set_auto_start(False)

    @property
    def name(self) -> str:
        """Return the global context name."""
        return self._name

    @property
    def global_sym_table(self) -> dict[str, typing.Any]:
        """Return the global symbol table."""
        return self._global_sym_table

    @property
    def source(self) -> str:
        """Return the source code."""
        return self._source

    @property
    def app_config(self) -> dict[str, typing.Any]:
        """Return the app config."""
        return self._app_config

    @property
    def mtime(self) -> float:
        """Return the mtime."""
        return self._mtime

    @property
    def file_path(self) -> str:
        """Return the file path."""
        return self._file_path

    @property
    def imports(self) -> set[str]:
        """Return the imports."""
        return frozenset(self._imports)

    @property
    def module(self) -> types.ModuleType:
        return self._module

    def get_trig_info(self, name: str, trig_args: dict[str, typing.Any]) -> TrigInfo:
        """Return a new trigger info instance with the given args."""
        return TrigInfo(self.pyscript, name, trig_args, self)

    async def module_import(
        self, module_name: str, import_level: int
    ) -> tuple[types.ModuleType, AstEval]:
        """Import a pyscript module from the pyscript/modules or apps folder."""

        pyscript_dir = self.pyscript.pyscript_folder
        module_path = module_name.replace(".", "/")
        file_paths: list[tuple[str, str, str]] = []

        def find_first_file() -> tuple[str, str, str]:
            for ctx_name, path, rel_path in file_paths:
                abs_path = os.path.join(pyscript_dir, path)
                if os.path.isfile(abs_path):
                    return (ctx_name, abs_path, rel_path)
            return None

        #
        # first build a list of potential import files
        #
        if import_level > 0:
            if self._rel_import_path is None:
                raise ImportError(
                    "attempted relative import with no known parent package"
                )
            path = self._rel_import_path
            if path.endswith("/__init__"):
                path = os.path.dirname(path)
            ctx_name = self._name
            for _ in range(import_level - 1):
                path = os.path.dirname(path)
                idx = ctx_name.rfind(".")
                if path.find("/") < 0 or idx < 0:
                    raise ImportError("attempted relative import above parent package")
                ctx_name = ctx_name[0:idx]
            ctx_name += f".{module_name}"
            module_info = (ctx_name, f"{path}/{module_path}.py", path)
            path += f"/{module_path}"
            file_paths.append((ctx_name, f"{path}/__init__.py", path))
            file_paths.append(module_info)
            module_name = ctx_name[ctx_name.find(".") + 1 :]

        else:
            if self._rel_import_path is not None and self._rel_import_path.startswith(
                "apps/"
            ):
                ctx_name = f"apps.{module_name}"
                file_paths.append(
                    (ctx_name, f"apps/{module_path}/__init__.py", f"apps/{module_path}")
                )
                file_paths.append(
                    (ctx_name, f"apps/{module_path}.py", f"apps/{module_path}")
                )

            ctx_name = f"modules.{module_name}"
            file_paths.append(
                (
                    ctx_name,
                    f"modules/{module_path}/__init__.py",
                    f"modules/{module_path}",
                )
            )
            file_paths.append((ctx_name, f"modules/{module_path}.py", None))

        #
        # now see if we have loaded it already
        #
        for ctx_name, _, _ in file_paths:
            mod_ctx = self._manager.get(ctx_name)
            if mod_ctx and mod_ctx.module:
                self._imports.add(mod_ctx.name)
                return mod_ctx.module, None

        #
        # not loaded already, so try to find and import it
        #
        file_info = await self.controller.async_add_executor_job(find_first_file)
        if not file_info:
            return None, None

        ctx_name, file_path, rel_import_path = file_info

        mod = types.ModuleType(module_name)
        global_ctx = self._manager.create_context(
            ctx_name,
            global_sym_table=mod.__dict__,
            rel_import_path=rel_import_path,
            filepath=file_path,
            autostart=True,
            module=mod,
        )
        # pylint: disable=protected-access
        error_ctx = await global_ctx._load_file()
        if error_ctx:
            self._logger.error(
                f"module_import: failed to load module {module_name}, ctx = {ctx_name}, "
                + f"path = {file_path}",
            )
            return None, error_ctx
        self._imports.add(ctx_name)
        return mod, None

    async def _load_file(self, reload: bool = False) -> AstEval:
        """
        Load, parse and run the given script file; returns error ast_ctx on error,
        or None if ok.
        """

        source = self._source
        mtime = None
        if not source and self._file_path:

            def read_file(path: str) -> tuple[str, float]:
                try:
                    with open(path, encoding="utf-8") as file_desc:
                        source = file_desc.read()
                    return source, os.path.getmtime(path)
                except Exception as exc:  # pylint: disable=broad-except
                    self._logger.error(f"{exc}")
                    return None, 0

            source, mtime = await self.controller.async_add_executor_job(
                read_file, self._file_path
            )

        if source is None:
            # pylint: disable=protected-access
            self._manager._delete(self.name)
            self._module = None
            return None

        #
        # create new ast eval context and parse source file
        #
        ast_ctx = self.create_ast_context()

        filename = self._file_path
        if not filename:
            filename = "<unknown>"

        if not ast_ctx.parse(source, filename=filename):
            exc = ast_ctx.exception_long
            ast_ctx.logger.error(exc)
            self._module = None
            # pylint: disable=protected-access
            self._manager._delete(self.name)
            return ast_ctx
        await ast_ctx.eval()
        exc = ast_ctx.exception_long
        if exc is not None:
            ast_ctx.logger.error(exc)
            self._module = None
            # pylint: disable=protected-access
            self._manager._delete(self.name)
            return ast_ctx
        self._source = source
        if mtime is not None:
            self._mtime = mtime

        self._logger.info(f"{'Reloaded' if reload else 'Loaded'} {self._file_path}")

        return None

    def close(self) -> None:
        """Stop this GlobalContext and remove it from ContextManager."""
        # pylint: disable=protected-access
        self._manager._delete(self.name)

    def create_ast_context(
        self, name: str = None, logger_name: str = None, install_ast_funcs: bool = True
    ):
        """Create a new AstEval context for this GlobalContext"""
        result = AstEval(self, name, logger_name)
        if install_ast_funcs:
            self.pyscript.functions.install_ast_funcs(result)
        return result
