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

import ast
import asyncio
import builtins
import functools as ft
import importlib
import inspect
import keyword
import logging
import sys
import typing
import weakref

from ... import core
from .const import Const
from .eval_attr_set import EvalAttrSet
from .eval_break import EvalBreak
from .eval_continue import EvalContinue
from .eval_func import EvalFunc
from .eval_func_var import EvalFuncVar
from .eval_func_var_class_inst import EvalFuncVarClassInst
from .eval_local_var import EvalLocalVar
from .eval_name import EvalName
from .eval_return import EvalReturn
from .eval_stop_flow import EvalStopFlow
from .parse_mode import ParseMode

if not typing.TYPE_CHECKING:

    class GlobalContext:
        pass

    class PyscriptComponent:
        pass


if typing.TYPE_CHECKING:
    from .global_context import GlobalContext
    from .pyscript_component import PyscriptComponent

_LOGGER = logging.getLogger(__package__ + ".eval")


#
# Built-ins to exclude to improve security or avoid i/o
#
_BUILTIN_EXCLUDE: typing.Final = {
    "breakpoint",
    "compile",
    "input",
    "memoryview",
    "open",
    "print",
}

_COMP_DECORATORS: typing.Final = {
    "pyscript_compile",
    "pyscript_executor",
}


@typing.overload
class AstEval:
    pass


def _ast_eval_exec_factory(ast_ctx: AstEval, mode: ParseMode):
    """Generate a function that executes eval() or exec() with given ast_ctx."""

    # pylint: disable=protected-access
    async def eval_func(
        arg_str,
        eval_globals: dict[str, typing.Any] = None,
        eval_locals: dict[str, typing.Any] = None,
    ):
        eval_ast = AstEval(ast_ctx.global_ctx)
        eval_ast.parse(arg_str, f"{mode}()", mode=mode)
        if eval_ast.exception_obj:
            raise eval_ast.exception_obj
        eval_ast.set_local_sym_table(ast_ctx.local_sym_table)
        if eval_globals is not None:
            eval_ast._global_sym_table = eval_globals
            if eval_locals is not None:
                eval_ast._sym_table_stack = [eval_globals]
                eval_ast._sym_table = eval_locals
            else:
                eval_ast._sym_table_stack = []
                eval_ast._sym_table = eval_globals
        else:
            eval_ast._sym_table_stack = ast_ctx.sym_table_stack.copy()
            if ast_ctx._sym_table == ast_ctx.global_sym_table:
                eval_ast._sym_table = ast_ctx._sym_table
            else:
                eval_ast._sym_table = ast_ctx._sym_table.copy()
                eval_ast._sym_table.update(ast_ctx._user_locals)
                to_delete = set()
                for var, value in eval_ast._sym_table.items():
                    if isinstance(value, EvalLocalVar):
                        if value.is_defined():
                            eval_ast._sym_table[var] = value.get()
                        else:
                            to_delete.add(var)
                for var in to_delete:
                    del eval_ast._sym_table[var]

        eval_ast._curr_func = None
        try:
            eval_result = await eval_ast.aeval(eval_ast._ast)
        except Exception as err:
            ast_ctx._exception_obj = err
            ast_ctx._exception = (
                f"Exception in {ast_ctx._filename} line {ast_ctx._lineno} column "
                + f"{ast_ctx._col_offset}: {eval_ast.exception}"
            )
            ast_ctx._exception_long = (
                ast_ctx.format_exc(
                    err, ast_ctx._lineno, ast_ctx._col_offset, short=True
                )
                + "\n"
                + eval_ast.exception_long
            )
            raise
        #
        # save variables only in the locals scope
        #
        if eval_globals is None and eval_ast._sym_table != ast_ctx._sym_table:
            for var, value in eval_ast._sym_table.items():
                if (
                    var in ast_ctx.global_sym_table
                    and value == ast_ctx.global_sym_table[var]
                ):
                    continue
                if var not in ast_ctx._sym_table and (
                    ast_ctx._curr_func is None
                    or var not in ast_ctx._curr_func.local_names
                ):
                    ast_ctx._user_locals[var] = value
        return eval_result

    return eval_func


def _ast_eval_factory(ast_ctx: AstEval):
    """Generate a function that executes eval() with given ast_ctx."""
    return _ast_eval_exec_factory(ast_ctx, ParseMode.EVAL)


def _ast_exec_factory(ast_ctx: AstEval):
    """Generate a function that executes exec() with given ast_ctx."""
    return _ast_eval_exec_factory(ast_ctx, ParseMode.EXEC)


def _ast_globals_factory(ast_ctx: AstEval):
    """Generate a globals() function with given ast_ctx."""

    async def globals_func():
        return ast_ctx.global_sym_table

    return globals_func


def _ast_locals_factory(ast_ctx: AstEval):
    """Generate a locals() function with given ast_ctx."""

    # pylint: disable=protected-access
    async def locals_func():
        if ast_ctx._sym_table == ast_ctx.global_sym_table:
            return ast_ctx._sym_table
        local_sym_table = ast_ctx._sym_table.copy()
        local_sym_table.update(ast_ctx._user_locals)
        to_delete = set()
        for var, value in local_sym_table.items():
            if isinstance(value, EvalLocalVar):
                if value.is_defined():
                    local_sym_table[var] = value.get()
                else:
                    to_delete.add(var)
        for var in to_delete:
            del local_sym_table[var]
        return local_sym_table

    return locals_func


#
# Built-in functions that are also passed the ast context
#
_BUILTIN_AST_FUNCS_FACTORY: typing.Final = {
    "eval": _ast_eval_factory,
    "exec": _ast_exec_factory,
    "globals": _ast_globals_factory,
    "locals": _ast_locals_factory,
}


# pylint: disable=unused-variable, invalid-name
class AstEval:
    """Python interpreter 'Abstract Syntax Tree' (AST) object evaluator."""

    def __init__(
        self, global_ctx: GlobalContext, name: str = None, logger_name: str = None
    ):
        """Initialize an interpreter execution context."""
        self._str = None
        self._ast = None
        self._name = name or global_ctx.name
        self._global_ctx = global_ctx
        self._global_sym_table = global_ctx.global_sym_table if global_ctx else {}
        self._sym_table_stack: list[dict[str, typing.Any]] = []
        self._sym_table: dict[str, typing.Any] = self._global_sym_table
        self._local_sym_table = {}
        self._user_locals = {}
        self._curr_func: EvalFunc = None
        self._filename = global_ctx.name
        self._code_str = None
        self._code_list = None
        self._exception = None
        self._exception_obj = None
        self._exception_long = None
        self._exception_curr = None
        self._lineno = 1
        self._col_offset = 0
        self._logger_handlers = set()
        self._logger = None
        self.set_logger_name(logger_name)
        self._dec_eval_depth = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def global_sym_table(self) -> dict[str, typing.Any]:
        return self._global_sym_table

    @property
    def local_sym_table(self) -> dict[str, typing.Any]:
        return self._local_sym_table

    @property
    def controller(self) -> core.SmartHomeController:
        return self._global_ctx.controller

    @property
    def pyscript(self) -> PyscriptComponent:
        return self._global_ctx.pyscript

    # pylint: disable=unused-argument
    async def ast_not_implemented(self, arg: ast.AST, *args):
        """Raise NotImplementedError exception for unimplemented AST types."""
        name = "ast_" + arg.__class__.__name__.lower()
        raise NotImplementedError(f"{self.name}: not implemented ast " + name)

    async def aeval(self, arg: ast.AST, undefined_check=True):
        """Vector to specific function based on ast class type."""
        name: str = "ast_" + arg.__class__.__name__.lower()
        try:
            if hasattr(arg, "lineno"):
                self._lineno = arg.lineno
                self._col_offset = arg.col_offset
            val = await getattr(self, name, self.ast_not_implemented)(arg)
            if undefined_check and isinstance(val, EvalName):
                raise NameError(f"name '{val.name}' is not defined")
            return val
        except Exception as err:
            if not self._exception_obj:
                func_name = self._curr_func.name + "(), " if self._curr_func else ""
                self._exception_obj = err
                self._exception = (
                    f"Exception in {func_name}{self._filename} line {self._lineno} "
                    + f"column {self._col_offset}: {err}"
                )
                self._exception_long = self.format_exc(
                    err, self._lineno, self._col_offset
                )
            raise

    # Statements return NONE, EvalBreak, EvalContinue, EvalReturn
    async def ast_module(self, arg: ast.Module):
        """Execute ast_module - a list of statements."""
        val = None
        for stmt in arg.body:
            val = await self.aeval(stmt)
            if isinstance(val, EvalReturn):
                raise SyntaxError(f"{val.name} statement outside function")
            if isinstance(val, EvalStopFlow):
                raise SyntaxError(f"{val.name} statement outside loop")
        return val

    async def ast_import(self, arg: ast.Import):
        """Execute import."""
        for imp in arg.names:
            mod, error_ctx = await self.global_ctx.module_import(imp.name, 0)
            if error_ctx:
                self._exception_obj = error_ctx.exception_obj
                self._exception = error_ctx.exception
                self._exception_long = error_ctx.exception_long
                raise self._exception_obj
            if not mod:
                if (
                    not self.pyscript.config_data.get(
                        Const.CONF_ALLOW_ALL_IMPORTS, False
                    )
                    and imp.name not in Const.ALLOWED_IMPORTS
                ):
                    raise ModuleNotFoundError(f"import of {imp.name} not allowed")
                mod = sys.modules.get(imp.name)
                if not mod:
                    mod = await self.controller.async_add_executor_job(
                        importlib.import_module, imp.name
                    )
            self._sym_table[imp.asname if imp.asname else imp.name] = mod

    async def ast_importfrom(self, arg: ast.ImportFrom):
        """Execute from X import Y."""
        if arg.module is None:
            # handle: "from . import xyz"
            for imp in arg.names:
                mod, error_ctx = await self.global_ctx.module_import(
                    imp.name, arg.level
                )
                if error_ctx:
                    self._exception_obj = error_ctx.exception_obj
                    self._exception = error_ctx.exception
                    self._exception_long = error_ctx.exception_long
                    raise self._exception_obj
                if not mod:
                    raise ModuleNotFoundError(f"module '{imp.name}' not found")
                self._sym_table[imp.asname if imp.asname else imp.name] = mod
            return
        mod, error_ctx = await self.global_ctx.module_import(arg.module, arg.level)
        if error_ctx:
            self._exception_obj = error_ctx.exception_obj
            self._exception = error_ctx.exception
            self._exception_long = error_ctx.exception_long
            raise self._exception_obj
        if not mod:
            if (
                not self.pyscript.config_data.get(Const.CONF_ALLOW_ALL_IMPORTS, False)
                and arg.module not in Const.ALLOWED_IMPORTS
            ):
                raise ModuleNotFoundError(f"import from {arg.module} not allowed")
            mod = sys.modules.get(arg.module)
            if not mod:
                mod = await self.controller.async_add_executor_job(
                    importlib.import_module, arg.module
                )
        for imp in arg.names:
            if imp.name == "*":
                for name, value in mod.__dict__.items():
                    if name[0] != "_":
                        self._sym_table[name] = value
            else:
                self._sym_table[imp.asname if imp.asname else imp.name] = getattr(
                    mod, imp.name
                )

    async def ast_if(self, arg: ast.If):
        """Execute if statement."""
        val = None
        if await self.aeval(arg.test):
            for stmt in arg.body:
                val = await self.aeval(stmt)
                if isinstance(val, EvalStopFlow):
                    return val
        else:
            for stmt in arg.orelse:
                val = await self.aeval(stmt)
                if isinstance(val, EvalStopFlow):
                    return val
        return val

    async def ast_for(self, arg: ast.For | ast.AsyncFor):
        """Execute for statement."""
        for loop_var in await self.aeval(arg.iter):
            await self.recurse_assign(arg.target, loop_var)
            for stmt in arg.body:
                val = await self.aeval(stmt)
                if isinstance(val, EvalStopFlow):
                    break
            if isinstance(val, EvalBreak):
                break
            if isinstance(val, EvalReturn):
                return val
        else:
            for stmt in arg.orelse:
                val = await self.aeval(stmt)
                if isinstance(val, EvalReturn):
                    return val
        return None

    async def ast_asyncfor(self, arg: ast.AsyncFor):
        """Execute async for statement."""
        return await self.ast_for(arg)

    async def ast_while(self, arg: ast.While):
        """Execute while statement."""
        while await self.aeval(arg.test):
            for stmt in arg.body:
                val = await self.aeval(stmt)
                if isinstance(val, EvalStopFlow):
                    break
            if isinstance(val, EvalBreak):
                break
            if isinstance(val, EvalReturn):
                return val
        else:
            for stmt in arg.orelse:
                val = await self.aeval(stmt)
                if isinstance(val, EvalReturn):
                    return val
        return None

    async def ast_classdef(self, arg: ast.ClassDef):
        """Evaluate class definition."""
        bases = [(await self.aeval(base)) for base in arg.bases]
        if self._curr_func and arg.name in self._curr_func.global_names:
            sym_table_assign = self._global_sym_table
        else:
            sym_table_assign = self._sym_table
        sym_table_assign[arg.name] = EvalLocalVar(arg.name)
        sym_table = {}
        self._sym_table_stack.append(self._sym_table)
        self._sym_table = sym_table
        for stmt in arg.body:
            val = await self.aeval(stmt)
            if isinstance(val, EvalReturn):
                raise SyntaxError(f"{val.name} statement outside function")
            if isinstance(val, EvalStopFlow):
                raise SyntaxError(f"{val.name} statement outside loop")
        self._sym_table = self._sym_table_stack.pop()

        if "__init__" in sym_table:
            sym_table["__init__evalfunc_wrap__"] = sym_table["__init__"]
            del sym_table["__init__"]
        sym_table_assign[arg.name].set((arg.name, tuple(bases), sym_table))

    async def ast_functiondef(self, arg: ast.FunctionDef | ast.AsyncFunctionDef):
        """Evaluate function definition."""
        other_dec = []
        dec_name = None
        pyscript_compile = None
        for dec in arg.decorator_list:
            if isinstance(dec, ast.Name) and dec.id in _COMP_DECORATORS:
                dec_name = dec.id
            elif (
                isinstance(dec, ast.Call)
                and isinstance(dec.func, ast.Name)
                and dec.func.id in _COMP_DECORATORS
            ):
                dec_name = dec.func.id
            else:
                other_dec.append(dec)
                continue
            if pyscript_compile:
                raise SyntaxError(
                    f"can only specify single decorator of {', '.join(sorted(_COMP_DECORATORS))}"
                )
            pyscript_compile = dec

        if pyscript_compile:
            if isinstance(pyscript_compile, ast.Call):
                if len(pyscript_compile.args) > 0:
                    raise TypeError(f"@{dec_name}() takes 0 positional arguments")
                if len(pyscript_compile.keywords) > 0:
                    raise TypeError(f"@{dec_name}() takes no keyword arguments")
            arg.decorator_list = other_dec
            local_var = None
            if arg.name in self._sym_table and isinstance(
                self._sym_table[arg.name], EvalLocalVar
            ):
                local_var = self._sym_table[arg.name]
            code = compile(
                ast.Module(body=[arg], type_ignores=[]),
                filename=self._filename,
                mode="exec",
            )
            # pylint: disable=exec-used
            exec(code, self._global_sym_table, self._sym_table)  # nosec

            func = self._sym_table[arg.name]
            if dec_name == "pyscript_executor":
                if not asyncio.iscoroutinefunction(func):

                    def executor_wrap_factory(func):
                        async def executor_wrap(*args, **kwargs):
                            return await self.controller.async_add_executor_job(
                                ft.partial(func, **kwargs), *args
                            )

                        return executor_wrap

                    self._sym_table[arg.name] = executor_wrap_factory(func)
                else:
                    raise TypeError(
                        "@pyscript_executor() needs a regular, not async, function"
                    )
            if local_var:
                self._sym_table[arg.name] = local_var
                self._sym_table[arg.name].set(func)
            return

        func = EvalFunc(arg, self._code_list, self._code_str, self._global_ctx)
        await func.eval_defaults(self)
        await func.resolve_nonlocals(self)
        name = func.name
        dec_trig, dec_other = await func.eval_decorators(self)
        self._dec_eval_depth += 1
        for dec_func in dec_other:
            func = await self.call_func(dec_func, None, func)
            if isinstance(func, EvalFuncVar):
                func = func.remove_func()
                dec_trig += func.decorators
        self._dec_eval_depth -= 1
        if isinstance(func, EvalFunc):
            # pylint: disable=protected-access
            func._decorators = dec_trig
            if self._dec_eval_depth == 0:
                func.trigger_stop()
                await func.trigger_init()
                func_var = EvalFuncVar(func)
            else:
                func_var = EvalFuncVar(func)
            func_var.set_ast_ctx(self)
        else:
            func_var = func

        if self._curr_func and name in self._curr_func.global_names:
            sym_table = self._global_sym_table
        else:
            sym_table = self._sym_table
        if name in sym_table and isinstance(sym_table[name], EvalLocalVar):
            sym_table[name].set(func_var)
        else:
            sym_table[name] = func_var

    async def ast_lambda(self, arg: ast.Lambda):
        """Evaluate lambda definition by compiling a regular function."""
        name = "__lambda_defn_temp__"
        await self.aeval(
            ast.FunctionDef(
                args=arg.args,
                body=[
                    ast.Return(
                        value=arg.body,
                        lineno=arg.body.lineno,
                        col_offset=arg.body.col_offset,
                    )
                ],
                name=name,
                decorator_list=[ast.Name(id="pyscript_compile", ctx=ast.Load())],
                lineno=arg.col_offset,
                col_offset=arg.col_offset,
            )
        )
        func = self._sym_table[name]
        del self._sym_table[name]
        return func

    async def ast_asyncfunctiondef(self, arg: ast.AsyncFunctionDef):
        """Evaluate async function definition."""
        return await self.ast_functiondef(arg)

    async def ast_try(self, arg: ast.Try):
        """Execute try...except statement."""
        try:
            for arg1 in arg.body:
                val = await self.aeval(arg1)
                if isinstance(val, EvalStopFlow):
                    return val
                if self._exception_obj is not None:
                    raise self._exception_obj
        except Exception as err:  # pylint: disable=broad-except
            # pylint: disable=too-many-nested-blocks
            curr_exc = self._exception_curr
            self._exception_curr = err
            for handler in arg.handlers:
                match = False
                if handler.type:
                    exc_list = await self.aeval(handler.type)
                    if not isinstance(exc_list, tuple):
                        exc_list = [exc_list]
                    for exc in exc_list:
                        if isinstance(err, exc):
                            match = True
                            break
                else:
                    match = True
                if match:
                    save_obj = self._exception_obj
                    save_exc_long = self._exception_long
                    save_exc = self._exception
                    self._exception_obj = None
                    self._exception = None
                    self._exception_long = None
                    if handler.name is not None:
                        if handler.name in self._sym_table and isinstance(
                            self._sym_table[handler.name], EvalLocalVar
                        ):
                            self._sym_table[handler.name].set(err)
                        else:
                            self._sym_table[handler.name] = err
                    for stmt in handler.body:
                        try:
                            val = await self.aeval(stmt)
                            if isinstance(val, EvalStopFlow):
                                if handler.name is not None:
                                    del self._sym_table[handler.name]
                                self._exception_curr = curr_exc
                                return val
                        except Exception:  # pylint: disable=broad-except
                            if self._exception_obj is not None:
                                if handler.name is not None:
                                    del self._sym_table[handler.name]
                                self._exception_curr = curr_exc
                                if self._exception_obj == save_obj:
                                    self._exception_long = save_exc_long
                                    self._exception = save_exc
                                else:
                                    self._exception_long = (
                                        save_exc_long
                                        + "\n\nDuring handling of the above exception, "
                                        + "another exception occurred:\n\n"
                                        + self._exception_long
                                    )
                                raise self._exception_obj  # pylint: disable=raise-missing-from
                    if handler.name is not None:
                        del self._sym_table[handler.name]
                    break
            else:
                self._exception_curr = curr_exc
                raise err
        else:
            for stmt in arg.orelse:
                val = await self.aeval(stmt)
                if isinstance(val, EvalStopFlow):
                    return val
        finally:
            for stmt in arg.finalbody:
                val = await self.aeval(stmt)
                if isinstance(val, EvalStopFlow):
                    return val  # pylint: disable=lost-exception
        return None

    async def ast_raise(self, arg: ast.Raise):
        """Execute raise statement."""
        if not arg.exc:
            if not self._exception_curr:
                raise RuntimeError("No active exception to reraise")
            exc = self._exception_curr
        else:
            exc = await self.aeval(arg.exc)
        if self._exception_curr:
            exc.__cause__ = self._exception_curr
        if arg.cause:
            cause = await self.aeval(arg.cause)
            raise exc from cause
        raise exc

    async def ast_with(self, arg: ast.With | ast.AsyncWith, async_attr=""):
        """Execute with statement."""
        hit_except = False
        ctx_list = []
        val = None
        enter_attr = f"__{async_attr}enter__"
        exit_attr = f"__{async_attr}exit__"
        try:
            for item in arg.items:
                manager = await self.aeval(item.context_expr)
                ctx_list.append(
                    {
                        "manager": manager,
                        "enter": getattr(type(manager), enter_attr),
                        "exit": getattr(type(manager), exit_attr),
                        "target": item.optional_vars,
                    }
                )
            for ctx in ctx_list:
                if ctx["target"]:
                    value = await self.call_func(
                        ctx["enter"], enter_attr, ctx["manager"]
                    )
                    await self.recurse_assign(ctx["target"], value)
            for stmt in arg.body:
                val = await self.aeval(stmt)
                if isinstance(val, EvalStopFlow):
                    break
        except Exception:  # pylint: disable=broad-except
            hit_except = True
            exit_ok = True
            for ctx in reversed(ctx_list):
                ret = await self.call_func(
                    ctx["exit"], exit_attr, ctx["manager"], *sys.exc_info()
                )
                exit_ok = exit_ok and ret
            if not exit_ok:
                raise
        finally:
            if not hit_except:
                for ctx in reversed(ctx_list):
                    await self.call_func(
                        ctx["exit"], exit_attr, ctx["manager"], None, None, None
                    )
        return val

    async def ast_asyncwith(self, arg: ast.AsyncWith):
        """Execute async with statement."""
        return await self.ast_with(arg, async_attr="a")

    async def ast_pass(self, arg: ast.Pass):
        """Execute pass statement."""

    async def ast_expression(self, arg: ast.Expression):
        """Execute expression statement."""
        return await self.aeval(arg.body)

    async def ast_expr(self, arg: ast.Expr):
        """Execute expression statement."""
        return await self.aeval(arg.value)

    async def ast_break(self, _arg: ast.Break):
        """Execute break statement - return special class."""
        return EvalBreak()

    async def ast_continue(self, _arg: ast.Continue):
        """Execute continue statement - return special class."""
        return EvalContinue()

    async def ast_return(self, arg: ast.Return):
        """Execute return statement - return special class."""
        return EvalReturn(await self.aeval(arg.value) if arg.value else None)

    async def ast_global(self, arg: ast.Global):
        """Execute global statement."""
        # pylint: disable=protected-access
        if not self._curr_func:
            raise SyntaxError("global statement outside function")
        for var_name in arg.names:
            self._curr_func._global_names.add(var_name)

    async def ast_nonlocal(self, arg: ast.Nonlocal):
        """Execute nonlocal statement."""
        # pylint: disable=protected-access
        if not self._curr_func:
            raise SyntaxError("nonlocal statement outside function")
        for var_name in arg.names:
            self._curr_func._nonlocal_names.add(var_name)

    async def recurse_assign(self, lhs, val):
        """Recursive assignment."""
        if isinstance(lhs, ast.Tuple):
            try:
                vals = [*iter(val)]
            except Exception:  # pylint: disable=broad-except
                raise TypeError(  # pylint: disable=raise-missing-from
                    "cannot unpack non-iterable object"
                )
            got_star = 0
            for lhs_elt in lhs.elts:
                if isinstance(lhs_elt, ast.Starred):
                    got_star = 1
                    break
            if len(lhs.elts) > len(vals) + got_star:
                if got_star:
                    err_msg = f"at least {len(lhs.elts) - got_star}"
                else:
                    err_msg = f"{len(lhs.elts)}"
                raise ValueError(f"too few values to unpack (expected {err_msg})")
            if len(lhs.elts) < len(vals) and got_star == 0:
                raise ValueError(
                    f"too many values to unpack (expected {len(lhs.elts)})"
                )
            val_idx = 0
            for lhs_elt in lhs.elts:
                if isinstance(lhs_elt, ast.Starred):
                    star_len = len(vals) - len(lhs.elts) + 1
                    star_name = lhs_elt.value.id
                    await self.recurse_assign(
                        ast.Name(id=star_name, ctx=ast.Store()),
                        vals[val_idx : val_idx + star_len],
                    )
                    val_idx += star_len
                else:
                    await self.recurse_assign(lhs_elt, vals[val_idx])
                    val_idx += 1
        elif isinstance(lhs, ast.Subscript):
            var = await self.aeval(lhs.value)
            if isinstance(lhs.slice, ast.Index):
                ind = await self.aeval(lhs.slice.value)
                var[ind] = val
            elif isinstance(lhs.slice, ast.Slice):
                lower = await self.aeval(lhs.slice.lower) if lhs.slice.lower else None
                upper = await self.aeval(lhs.slice.upper) if lhs.slice.upper else None
                step = await self.aeval(lhs.slice.step) if lhs.slice.step else None
                var[slice(lower, upper, step)] = val
            else:
                var[await self.aeval(lhs.slice)] = val
        else:
            var_name = await self.aeval(lhs)
            if isinstance(var_name, EvalAttrSet):
                var_name.setattr(val)
                return
            if not isinstance(var_name, str):
                raise NotImplementedError(
                    f"unknown lhs type {lhs} (got {var_name}) in assign"
                )
            dot_count = var_name.count(".")
            if dot_count == 1:
                self.pyscript.states.set(var_name, val)
                return
            if dot_count == 2:
                self.pyscript.states.setattr(var_name, val)
                return
            if dot_count > 0:
                raise NameError(
                    f"invalid name '{var_name}' (should be 'domain.entity' or 'domain.entity.attr')"
                )
            if self._curr_func and var_name in self._curr_func.global_names:
                self._global_sym_table[var_name] = val
                return
            if var_name in self._sym_table and isinstance(
                self._sym_table[var_name], EvalLocalVar
            ):
                self._sym_table[var_name].set(val)
            else:
                self._sym_table[var_name] = val

    async def ast_assign(self, arg: ast.Assign):
        """Execute assignment statement."""
        rhs = await self.aeval(arg.value)
        for target in arg.targets:
            await self.recurse_assign(target, rhs)

    async def ast_augassign(self, arg: ast.AugAssign):
        """Execute augmented assignment statement (lhs <BinOp>= value)."""
        arg.target.ctx = ast.Load()
        new_val = await self.aeval(
            ast.BinOp(left=arg.target, op=arg.op, right=arg.value)
        )
        arg.target.ctx = ast.Store()
        await self.recurse_assign(arg.target, new_val)

    async def ast_namedexpr(self, arg: ast.NamedExpr):
        """Execute named expression."""
        val = await self.aeval(arg.value)
        await self.recurse_assign(arg.target, val)
        return val

    async def ast_delete(self, arg: ast.Delete):
        """Execute del statement."""
        for arg1 in arg.targets:
            if isinstance(arg1, ast.Subscript):
                var = await self.aeval(arg1.value)
                if isinstance(arg1.slice, ast.Index):
                    ind = await self.aeval(arg1.slice.value)
                    for elt in ind if isinstance(ind, list) else [ind]:
                        del var[elt]
                elif isinstance(arg1.slice, ast.Slice):
                    lower, upper, step = None, None, None
                    if arg1.slice.lower:
                        lower = await self.aeval(arg1.slice.lower)
                    if arg1.slice.upper:
                        upper = await self.aeval(arg1.slice.upper)
                    if arg1.slice.step:
                        step = await self.aeval(arg1.slice.step)
                    del var[slice(lower, upper, step)]
                else:
                    del var[await self.aeval(arg1.slice)]
            elif isinstance(arg1, ast.Name):
                if self._curr_func and arg1.id in self._curr_func.global_names:
                    if arg1.id in self._global_sym_table:
                        del self._global_sym_table[arg1.id]
                elif arg1.id in self._sym_table:
                    if isinstance(self._sym_table[arg1.id], EvalLocalVar):
                        if self._sym_table[arg1.id].is_defined():
                            self._sym_table[arg1.id].set_undefined()
                        else:
                            raise NameError(f"name '{arg1.id}' is not defined")
                    else:
                        del self._sym_table[arg1.id]
                else:
                    raise NameError(f"name '{arg1.id}' is not defined")
            elif isinstance(arg1, ast.Attribute):
                var_name = await self.ast_attribute_collapse(arg1, check_undef=False)
                if not isinstance(var_name, str):
                    raise NameError(
                        "state name should be 'domain.entity' or 'domain.entity.attr'"
                    )
                self.pyscript.states.delete(var_name)
            else:
                raise NotImplementedError(f"unknown target type {arg1} in del")

    async def ast_assert(self, arg: ast.Assert):
        """Execute assert statement."""
        if not await self.aeval(arg.test):
            if arg.msg:
                raise AssertionError(await self.aeval(arg.msg))
            raise AssertionError

    async def ast_attribute_collapse(self, arg: ast.Attribute, check_undef=True):
        """Combine dotted attributes to allow variable names to have dots."""
        # collapse dotted names, eg:
        #   Attribute(
        #       value=Attribute(
        #           value=Name(
        #               id='i',
        #               ctx=Load()
        #           ),
        #           attr='j',
        #           ctx=Load()
        #       ),
        #       attr='k',
        #       ctx=Store()
        #   )
        name = arg.attr
        val = arg.value
        while isinstance(val, ast.Attribute):
            name = val.attr + "." + name
            val = val.value
        if isinstance(val, ast.Name):
            name = val.id + "." + name
            # ensure the first portion of name is undefined
            if check_undef and not isinstance(
                await self.ast_name(ast.Name(id=val.id, ctx=ast.Load())), EvalName
            ):
                return None
            return name
        return None

    async def ast_attribute(self, arg: ast.Attribute):
        """Apply attributes."""
        full_name = await self.ast_attribute_collapse(arg)
        if full_name is not None:
            if isinstance(arg.ctx, ast.Store):
                return full_name
            val = await self.ast_name(ast.Name(id=full_name, ctx=arg.ctx))
            if not isinstance(val, EvalName):
                return val
        val = await self.aeval(arg.value)
        if isinstance(arg.ctx, ast.Store):
            return EvalAttrSet(val, arg.attr)
        return getattr(val, arg.attr)

    async def ast_name(self, arg: ast.Name):
        """Look up value of identifier on load, or returns name on set."""
        if isinstance(arg.ctx, ast.Load):
            #
            # check other scopes if required by global declarations
            #
            if self._curr_func and arg.id in self._curr_func.global_names:
                if arg.id in self._global_sym_table:
                    return self._global_sym_table[arg.id]
                raise NameError(f"global name '{arg.id}' is not defined")
            #
            # now check in our current symbol table, and then some other places
            #
            if arg.id in self._sym_table:
                if isinstance(self._sym_table[arg.id], EvalLocalVar):
                    return self._sym_table[arg.id].get()
                return self._sym_table[arg.id]
            if arg.id in self._local_sym_table:
                return self._local_sym_table[arg.id]
            if arg.id in self._global_sym_table:
                if self._curr_func and arg.id in self._curr_func.local_names:
                    raise UnboundLocalError(
                        f"local variable '{arg.id}' referenced before assignment"
                    )
                return self._global_sym_table[arg.id]
            if arg.id in _BUILTIN_AST_FUNCS_FACTORY:
                return _BUILTIN_AST_FUNCS_FACTORY[arg.id](self)
            if (
                hasattr(builtins, arg.id)
                and arg.id not in _BUILTIN_EXCLUDE
                and arg.id[0] != "_"
            ):
                return getattr(builtins, arg.id)
            ret_val = self.pyscript.functions.get(arg.id)
            if ret_val:
                return ret_val
            num_dots = arg.id.count(".")
            #
            # any single-dot name could be a state variable
            # a two-dot name for state.attr needs to exist
            #
            if num_dots == 1 or (num_dots == 2 and self.pyscript.states.exist(arg.id)):
                return self.pyscript.states.get(arg.id)
            #
            # Couldn't find it, so return just the name wrapped in EvalName to
            # distinguish from a string variable value.  This is to support
            # names with ".", which are joined by ast_attribute
            #
            return EvalName(arg.id)
        return arg.id

    async def _lookup_name(self, name: str):
        """look for "name" in all possible scopes."""
        #
        # check other scopes if required by global declarations
        #
        if self._curr_func and name in self._curr_func.global_names:
            if name in self._global_sym_table:
                return self._global_sym_table[name]
            raise NameError(f"global name '{name}' is not defined")

        #
        # now check in our current symbol table, and then some other places
        #
        if name in self._sym_table:
            result = self._sym_table[name]
            if isinstance(result, EvalLocalVar):
                return result.get()
            return result

        if name in self._local_sym_table:
            return self._local_sym_table[name]

        if name in self._global_sym_table:
            if self._curr_func and name in self._curr_func.local_names:
                raise UnboundLocalError(
                    f"local variable '{name}' referenced before assignment"
                )
            return self._global_sym_table[name]

        if name in _BUILTIN_AST_FUNCS_FACTORY:
            return _BUILTIN_AST_FUNCS_FACTORY[name](self)
        if hasattr(builtins, name) and name not in _BUILTIN_EXCLUDE and name[0] != "_":
            return getattr(builtins, name)

        ret_val = self.pyscript.functions.get(name)
        if ret_val:
            return ret_val
        num_dots = name.count(".")
        #
        # any single-dot name could be a state variable
        # a two-dot name for state.attr needs to exist
        #
        if num_dots == 1 or (num_dots == 2 and self.pyscript.states.exist(name)):
            return self.pyscript.states.get(name)
        #
        # Couldn't find it, so return just the name wrapped in EvalName to
        # distinguish from a string variable value.  This is to support
        # names with ".", which are joined by ast_attribute
        #
        return EvalName(name)

    async def ast_binop(self, arg: ast.BinOp):
        """Evaluate binary operators by calling function based on class."""
        name = "ast_binop_" + arg.op.__class__.__name__.lower()
        return await getattr(self, name, self.ast_not_implemented)(arg.left, arg.right)

    async def ast_binop_add(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate binary operator: +."""
        return (await self.aeval(arg0)) + (await self.aeval(arg1))

    async def ast_binop_sub(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate binary operator: -."""
        return (await self.aeval(arg0)) - (await self.aeval(arg1))

    async def ast_binop_mult(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate binary operator: *."""
        return (await self.aeval(arg0)) * (await self.aeval(arg1))

    async def ast_binop_div(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate binary operator: /."""
        return (await self.aeval(arg0)) / (await self.aeval(arg1))

    async def ast_binop_mod(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate binary operator: %."""
        return (await self.aeval(arg0)) % (await self.aeval(arg1))

    async def ast_binop_pow(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate binary operator: **."""
        return (await self.aeval(arg0)) ** (await self.aeval(arg1))

    async def ast_binop_lshift(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate binary operator: <<."""
        return (await self.aeval(arg0)) << (await self.aeval(arg1))

    async def ast_binop_rshift(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate binary operator: >>."""
        return (await self.aeval(arg0)) >> (await self.aeval(arg1))

    async def ast_binop_bitor(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate binary operator: |."""
        return (await self.aeval(arg0)) | (await self.aeval(arg1))

    async def ast_binop_bitxor(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate binary operator: ^."""
        return (await self.aeval(arg0)) ^ (await self.aeval(arg1))

    async def ast_binop_bitand(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate binary operator: &."""
        return (await self.aeval(arg0)) & (await self.aeval(arg1))

    async def ast_binop_floordiv(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate binary operator: //."""
        return (await self.aeval(arg0)) // (await self.aeval(arg1))

    async def ast_unaryop(self, arg: ast.UnaryOp):
        """Evaluate unary operators by calling function based on class."""
        name = "ast_unaryop_" + arg.op.__class__.__name__.lower()
        return await getattr(self, name, self.ast_not_implemented)(arg.operand)

    async def ast_unaryop_not(self, arg: ast.expr):
        """Evaluate unary operator: not."""
        return not await self.aeval(arg)

    async def ast_unaryop_invert(self, arg: ast.expr):
        """Evaluate unary operator: ~."""
        return ~await self.aeval(arg)

    async def ast_unaryop_uadd(self, arg: ast.expr):
        """Evaluate unary operator: +."""
        return await self.aeval(arg)

    async def ast_unaryop_usub(self, arg: ast.expr):
        """Evaluate unary operator: -."""
        return -await self.aeval(arg)

    async def ast_compare(self, arg: ast.Compare):
        """Evaluate comparison operators by calling function based on class."""
        left = arg.left
        for cmp_op, right in zip(arg.ops, arg.comparators):
            name = "ast_cmpop_" + cmp_op.__class__.__name__.lower()
            val = await getattr(self, name, self.ast_not_implemented)(left, right)
            if not val:
                return False
            left = right
        return True

    async def ast_cmpop_eq(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate comparison operator: ==."""
        return (await self.aeval(arg0)) == (await self.aeval(arg1))

    async def ast_cmpop_noteq(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate comparison operator: !=."""
        return (await self.aeval(arg0)) != (await self.aeval(arg1))

    async def ast_cmpop_lt(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate comparison operator: <."""
        return (await self.aeval(arg0)) < (await self.aeval(arg1))

    async def ast_cmpop_lte(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate comparison operator: <=."""
        return (await self.aeval(arg0)) <= (await self.aeval(arg1))

    async def ast_cmpop_gt(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate comparison operator: >."""
        return (await self.aeval(arg0)) > (await self.aeval(arg1))

    async def ast_cmpop_gte(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate comparison operator: >=."""
        return (await self.aeval(arg0)) >= (await self.aeval(arg1))

    async def ast_cmpop_is(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate comparison operator: is."""
        return (await self.aeval(arg0)) is (await self.aeval(arg1))

    async def ast_cmpop_isnot(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate comparison operator: is not."""
        return (await self.aeval(arg0)) is not (await self.aeval(arg1))

    async def ast_cmpop_in(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate comparison operator: in."""
        return await self.aeval(arg0) in await self.aeval(arg1)

    async def ast_cmpop_notin(self, arg0: ast.expr, arg1: ast.expr):
        """Evaluate comparison operator: not in."""
        return await self.aeval(arg0) not in await self.aeval(arg1)

    async def ast_boolop(self, arg: ast.BoolOp):
        """Evaluate boolean operators and and or."""
        if isinstance(arg.op, ast.And):
            for expr in arg.values:
                this_val = await self.aeval(expr)
                if not this_val:
                    return False
            return True
        for expr in arg.values:
            val = await self.aeval(expr)
            if bool(val):
                return True
        return False

    async def eval_elt_list(self, elts):
        """Evaluate and star list elements."""
        val = []
        for arg in elts:
            if isinstance(arg, ast.Starred):
                val += await self.aeval(arg.value)
            else:
                val.append(await self.aeval(arg))
        return val

    async def ast_list(self, arg: ast.List):
        """Evaluate list."""
        if isinstance(arg.ctx, ast.Load):
            return await self.eval_elt_list(arg.elts)

    async def loopvar_scope_save(self, generators):
        """Return current scope variables that match looping target vars."""
        #
        # looping variables are in their own implicit nested scope, so save/restore
        # variables in the current scope with the same names
        #
        lvars = set()
        for gen in generators:
            await self.get_names(
                ast.Assign(targets=[gen.target], value=ast.Constant(value=None)),
                local_names=lvars,
            )
        return lvars, {
            var: self._sym_table[var] for var in lvars if var in self._sym_table
        }

    async def loopvar_scope_restore(self, var_names, save_vars):
        """Restore current scope variables that match looping target vars."""
        for var_name in var_names:
            if var_name in save_vars:
                self._sym_table[var_name] = save_vars[var_name]
            else:
                del self._sym_table[var_name]

    async def listcomp_loop(self, generators, elt):
        """Recursive list comprehension."""
        out = []
        gen = generators[0]
        for loop_var in await self.aeval(gen.iter):
            await self.recurse_assign(gen.target, loop_var)
            for cond in gen.ifs:
                if not await self.aeval(cond):
                    break
            else:
                if len(generators) == 1:
                    out.append(await self.aeval(elt))
                else:
                    out += await self.listcomp_loop(generators[1:], elt)
        return out

    async def ast_listcomp(self, arg: ast.ListComp):
        """Evaluate list comprehension."""
        target_vars, save_values = await self.loopvar_scope_save(arg.generators)
        result = await self.listcomp_loop(arg.generators, arg.elt)
        await self.loopvar_scope_restore(target_vars, save_values)
        return result

    async def ast_tuple(self, arg: ast.Tuple):
        """Evaluate Tuple."""
        return tuple(await self.eval_elt_list(arg.elts))

    async def ast_dict(self, arg: ast.Dict):
        """Evaluate dict."""
        val = {}
        for key_ast, val_ast in zip(arg.keys, arg.values):
            this_val = await self.aeval(val_ast)
            if key_ast is None:
                val.update(this_val)
            else:
                val[await self.aeval(key_ast)] = this_val
        return val

    async def dictcomp_loop(self, generators, key, value):
        """Recursive dict comprehension."""
        out = {}
        gen = generators[0]
        for loop_var in await self.aeval(gen.iter):
            await self.recurse_assign(gen.target, loop_var)
            for cond in gen.ifs:
                if not await self.aeval(cond):
                    break
            else:
                if len(generators) == 1:
                    #
                    # key is evaluated before value starting in 3.8
                    #
                    key_val = await self.aeval(key)
                    out[key_val] = await self.aeval(value)
                else:
                    out.update(await self.dictcomp_loop(generators[1:], key, value))
        return out

    async def ast_dictcomp(self, arg: ast.DictComp):
        """Evaluate dict comprehension."""
        target_vars, save_values = await self.loopvar_scope_save(arg.generators)
        result = await self.dictcomp_loop(arg.generators, arg.key, arg.value)
        await self.loopvar_scope_restore(target_vars, save_values)
        return result

    async def ast_set(self, arg: ast.Set):
        """Evaluate set."""
        ret = set()
        for elt in await self.eval_elt_list(arg.elts):
            ret.add(elt)
        return ret

    async def setcomp_loop(self, generators, elt):
        """Recursive list comprehension."""
        out = set()
        gen = generators[0]
        for loop_var in await self.aeval(gen.iter):
            await self.recurse_assign(gen.target, loop_var)
            for cond in gen.ifs:
                if not await self.aeval(cond):
                    break
            else:
                if len(generators) == 1:
                    out.add(await self.aeval(elt))
                else:
                    out.update(await self.setcomp_loop(generators[1:], elt))
        return out

    async def ast_setcomp(self, arg: ast.SetComp):
        """Evaluate set comprehension."""
        target_vars, save_values = await self.loopvar_scope_save(arg.generators)
        result = await self.setcomp_loop(arg.generators, arg.elt)
        await self.loopvar_scope_restore(target_vars, save_values)
        return result

    async def ast_subscript(self, arg: ast.Subscript):
        """Evaluate subscript."""
        var = await self.aeval(arg.value)
        if isinstance(arg.ctx, ast.Load):
            if isinstance(arg.slice, ast.Index):
                return var[await self.aeval(arg.slice)]
            if isinstance(arg.slice, ast.Slice):
                lower = (await self.aeval(arg.slice.lower)) if arg.slice.lower else None
                upper = (await self.aeval(arg.slice.upper)) if arg.slice.upper else None
                step = (await self.aeval(arg.slice.step)) if arg.slice.step else None
                return var[slice(lower, upper, step)]
            return var[await self.aeval(arg.slice)]
        return None

    async def ast_index(self, arg: ast.Index):
        """Evaluate index."""
        return await self.aeval(arg.value)

    async def ast_slice(self, arg: ast.Slice):
        """Evaluate slice."""
        return await self.aeval(arg.value)

    async def ast_call(self, arg: ast.Call):
        """Evaluate function call."""
        func = await self.aeval(arg.func)
        kwargs = {}
        for kw_arg in arg.keywords:
            if kw_arg.arg is None:
                kwargs.update(await self.aeval(kw_arg.value))
            else:
                kwargs[kw_arg.arg] = await self.aeval(kw_arg.value)
        args = await self.eval_elt_list(arg.args)
        #
        # try to deduce function name, although this only works in simple cases
        #
        func_name = None
        if isinstance(arg.func, ast.Name):
            func_name = arg.func.id
        elif isinstance(arg.func, ast.Attribute):
            func_name = arg.func.attr
        if isinstance(func, EvalLocalVar):
            func_name = func.name
            func = func.get()
        return await self.call_func(func, func_name, *args, **kwargs)

    async def _process_classdef(self, inst, inst_weak, class_def: tuple):
        """process class and base_class definitions"""
        class_name, bases, sym_table = class_def
        for name in bases:
            # Basisklassen der Basisklasse verarbeiten.
            await self._process_classdef(inst, inst_weak, name)

        for name, value in sym_table.items():
            if isinstance(value, EvalFuncVar):
                setattr(
                    inst,
                    name,
                    EvalFuncVarClassInst(value.func, value.ast_ctx, inst_weak),
                )
            else:
                setattr(inst, name, value)

    async def call_func(self, func, func_name: str, *args, **kwargs):
        """Call a function with the given arguments."""
        if func_name is None:
            try:
                if isinstance(func, (EvalFunc, EvalFuncVar)):
                    func_name = func.name
                else:
                    func_name = func.__name__
            except Exception:  # pylint: disable=broad-except
                func_name = "<function>"
        arg_str = ", ".join(
            ['"' + elt + '"' if isinstance(elt, str) else str(elt) for elt in args]
        )
        _LOGGER.debug(f"{self.name}: calling {func_name}({arg_str}, {kwargs})")
        if isinstance(func, (EvalFunc, EvalFuncVar)):
            return await func.call(self, *args, **kwargs)
        if inspect.isclass(func) and hasattr(func, "__init__evalfunc_wrap__"):
            inst = func()
            #
            # we use weak references when we bind the method calls to the instance inst;
            # otherwise these self references cause the object to not be deleted until
            # it is later garbage collected
            #
            inst_weak = weakref.ref(inst)
            for name in dir(inst):
                value = getattr(inst, name)
                if not isinstance(value, EvalFuncVar):
                    continue
                setattr(
                    inst,
                    name,
                    EvalFuncVarClassInst(value.func, value.ast_ctx, inst_weak),
                )
            if getattr(func, "__init__evalfunc_wrap__") is not None:
                #
                # since our __init__ function is async, call the renamed one
                #
                await inst.__init__evalfunc_wrap__.call(self, *args, **kwargs)
            return inst
        if isinstance(func, tuple):

            class Wrapper:
                def __init__(self):
                    class_name, bases, sym_table = func
                    self.class_name = class_name
                    self.bases = bases
                    self.sym_table = sym_table

            inst = Wrapper()
            #
            # we use weak references when we bind the method calls to the instance inst;
            # otherwise these self references cause the object to not be deleted until
            # it is later garbage collected
            #
            inst_weak = weakref.ref(inst)
            await self._process_classdef(inst, inst_weak, func)

            if getattr(inst, "__init__evalfunc_wrap__") is not None:
                #
                # since our __init__ function is async, call the renamed one
                #
                await inst.__init__evalfunc_wrap__.call(self, *args, **kwargs)
            return inst

        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        if callable(func):
            return func(*args, **kwargs)
        raise TypeError(f"'{func_name}' is not callable (got {func})")

    async def ast_ifexp(self, arg: ast.IfExp):
        """Evaluate if expression."""
        return (
            await self.aeval(arg.body)
            if (await self.aeval(arg.test))
            else await self.aeval(arg.orelse)
        )

    async def ast_num(self, arg: ast.Num):
        """Evaluate number."""
        return arg.n

    async def ast_str(self, arg: ast.Str):
        """Evaluate string."""
        return arg.s

    async def ast_nameconstant(self, arg: ast.NameConstant):
        """Evaluate name constant."""
        return arg.value

    async def ast_constant(self, arg: ast.Constant):
        """Evaluate constant."""
        return arg.value

    async def ast_joinedstr(self, arg: ast.JoinedStr):
        """Evaluate joined string."""
        val = ""
        for arg1 in arg.values:
            this_val = await self.aeval(arg1)
            val = val + str(this_val)
        return val

    async def ast_formattedvalue(self, arg: ast.FormattedValue):
        """Evaluate formatted value."""
        val = await self.aeval(arg.value)
        if arg.format_spec is not None:
            fmt = await self.aeval(arg.format_spec)
            return f"{val:{fmt}}"
        return f"{val}"

    async def ast_await(self, arg: ast.Await):
        """Evaluate await expr."""
        coro = await self.aeval(arg.value)
        if coro:
            return await coro
        return None

    async def get_target_names(self, lhs):
        """Recursively find all the target names mentioned in the AST tree."""
        names = set()
        if isinstance(lhs, ast.Tuple):
            for lhs_elt in lhs.elts:
                if isinstance(lhs_elt, ast.Starred):
                    names.add(lhs_elt.value.id)
                else:
                    names = names.union(await self.get_target_names(lhs_elt))
        elif isinstance(lhs, ast.Attribute):
            var_name = await self.ast_attribute_collapse(lhs, check_undef=False)
            if isinstance(var_name, str):
                names.add(var_name)
        elif isinstance(lhs, ast.Name):
            names.add(lhs.id)
        return names

    async def get_names_set(
        self, arg, names, nonlocal_names, global_names, local_names
    ):
        """Recursively find all the names mentioned in the AST tree."""

        cls_name = arg.__class__.__name__
        if cls_name == "Attribute":
            full_name = await self.ast_attribute_collapse(arg)
            if full_name is not None:
                names.add(full_name)
                return
        if cls_name == "Name":
            names.add(arg.id)
            return
        if cls_name == "Nonlocal" and nonlocal_names is not None:
            for var_name in arg.names:
                nonlocal_names.add(var_name)
                names.add(var_name)
            return
        if cls_name == "Global" and global_names is not None:
            for var_name in arg.names:
                global_names.add(var_name)
                names.add(var_name)
            return
        if local_names is not None:
            #
            # find all the local variables by looking for assignments;
            # also, don't recurse into function definitions
            #
            if cls_name == "Assign":
                for target in arg.targets:
                    for name in await self.get_target_names(target):
                        local_names.add(name)
                        names.add(name)
            elif cls_name in {"AugAssign", "For", "AsyncFor", "NamedExpr"}:
                for name in await self.get_target_names(arg.target):
                    local_names.add(name)
                    names.add(name)
            elif cls_name in {"With", "AsyncWith"}:
                for item in arg.items:
                    if item.optional_vars:
                        for name in await self.get_target_names(item.optional_vars):
                            local_names.add(name)
                            names.add(name)
            elif cls_name in {"ListComp", "DictComp", "SetComp"}:
                target_vars, _ = await self.loopvar_scope_save(arg.generators)
                for name in target_vars:
                    local_names.add(name)
            elif cls_name == "Try":
                for handler in arg.handlers:
                    if handler.name is not None:
                        local_names.add(handler.name)
                        names.add(handler.name)
            elif cls_name == "Call":
                await self.get_names_set(
                    arg.func, names, nonlocal_names, global_names, local_names
                )
                for this_arg in arg.args:
                    await self.get_names_set(
                        this_arg, names, nonlocal_names, global_names, local_names
                    )
                for this_arg in arg.keywords or []:
                    await self.get_names_set(
                        this_arg, names, nonlocal_names, global_names, local_names
                    )
                return
            elif cls_name in {"FunctionDef", "ClassDef", "AsyncFunctionDef"}:
                local_names.add(arg.name)
                names.add(arg.name)
                for dec in arg.decorator_list:
                    await self.get_names_set(
                        dec, names, nonlocal_names, global_names, local_names
                    )
                #
                # find unbound names from the body of the function or class
                #
                inner_global, inner_names, inner_local = set(), set(), set()
                for child in arg.body:
                    await self.get_names_set(
                        child, inner_names, None, inner_global, inner_local
                    )
                for name in inner_names:
                    if name not in inner_local and name not in inner_global:
                        names.add(name)
                return
            elif cls_name == "Delete":
                for arg1 in arg.targets:
                    if isinstance(arg1, ast.Name):
                        local_names.add(arg1.id)
        for child in ast.iter_child_nodes(arg):
            await self.get_names_set(
                child, names, nonlocal_names, global_names, local_names
            )

    async def get_names(
        self,
        this_ast: ast.AST = None,
        nonlocal_names=None,
        global_names=None,
        local_names=None,
    ):
        """Return set of all the names mentioned in our AST tree."""
        names = set()
        this_ast = this_ast or self._ast
        if this_ast:
            await self.get_names_set(
                this_ast, names, nonlocal_names, global_names, local_names
            )
        return names

    def parse(
        self,
        code_str: str | list[str],
        filename: str = None,
        mode: ParseMode = ParseMode.EXEC,
    ):
        """Parse the code_str source code into an AST tree."""
        self._exception = None
        self._exception_obj = None
        self._exception_long = None
        self._ast: ast.AST = None
        if filename is not None:
            self._filename = filename
        else:
            self._filename = "<unknown>"
        try:
            if isinstance(code_str, list):
                self._code_list = code_str
                self._code_str = "\n".join(code_str)
            elif isinstance(code_str, str):
                self._code_str = code_str
                self._code_list = code_str.split("\n")
            else:
                self._code_str = code_str
                self._code_list = []
            self._ast = ast.parse(
                self._code_str, filename=self._filename, mode=str(mode)
            )
            return True
        except SyntaxError as err:
            self._exception_obj = err
            self._lineno = err.lineno
            self._col_offset = err.offset - 1
            self._exception = f"syntax error {err}"
            if err.filename == self._filename:
                self._exception_long = self.format_exc(
                    err, self._lineno, self._col_offset
                )
            else:
                self._exception_long = self.format_exc(
                    err, 1, self._col_offset, code_list=[err.text]
                )
            return False
        except asyncio.CancelledError:  # pylint: disable=try-except-raise
            raise
        except Exception as err:  # pylint: disable=broad-except
            self._exception_obj = err
            self._lineno = 1
            self._col_offset = 0
            self._exception = f"parsing error {err}"
            self._exception_long = self.format_exc(err)
            return False

    def format_exc(
        self, exc, lineno=None, col_offset=None, short=False, code_list=None
    ):
        """Format an multi-line exception message using lineno if available."""
        if code_list is None:
            code_list = self._code_list
        if lineno is not None and lineno <= len(code_list):
            if short:
                mesg = f"In {self._filename}, line {lineno}:\n"
                mesg += "    " + code_list[lineno - 1]
            else:
                mesg = f'Exception in "{self._filename}:{lineno}:'
                if col_offset is not None:
                    mesg += f"{col_offset}"
                mesg += '"\n'
                mesg += "    " + code_list[lineno - 1] + "\n"
                if col_offset is not None:
                    mesg += "    " + " " * col_offset + "^\n"
                mesg += f"{type(exc).__name__}: {exc}"
        else:
            mesg = f"Exception in {self._filename}:\n"
            mesg += f"{type(exc).__name__}: {exc}"
        #
        # to get a more detailed traceback on exception (eg, when chasing an internal
        # error), add an "import traceback" above, and uncomment this next line
        #
        # return mesg + "\n" + traceback.format_exc(-1)
        return mesg

    @property
    def exception(self):
        """Return the last exception str."""
        return self._exception

    @property
    def exception_obj(self):
        """Return the last exception object."""
        return self._exception_obj

    @property
    def exception_long(self) -> str:
        """Return the last exception in a longer str form."""
        return self._exception_long

    def set_local_sym_table(self, sym_table: dict[str, typing.Any]):
        """Set the local symbol table."""
        self._local_sym_table = sym_table

    @property
    def global_ctx(self):
        """Return the global context."""
        return self._global_ctx

    @global_ctx.setter
    def global_ctx(self, global_ctx: GlobalContext):
        """Set the global context."""
        if global_ctx is None:
            return

        self._global_ctx = global_ctx
        if self._sym_table == self._global_sym_table:
            self._sym_table = global_ctx.global_sym_table
        self._global_sym_table = global_ctx.global_sym_table
        if len(self._sym_table_stack) > 0:
            self._sym_table_stack[0] = self._global_sym_table

    def set_logger_name(self, name: str):
        """Set the context's logger name."""
        if name is None:
            name = self.name
        if self.logger:
            for handler in self._logger_handlers:
                self.logger.removeHandler(handler)
        self._logger_name = name
        self._logger = logging.getLogger(__package__ + "." + name)
        for handler in self._logger_handlers:
            self._logger.addHandler(handler)

    @property
    def logger_name(self):
        """Get the context's logger name."""
        return self._logger_name

    @property
    def logger(self):
        """Get the context's logger."""
        return self._logger

    def add_logger_handler(self, handler):
        """Add logger handler to this context."""
        self._logger.addHandler(handler)
        self._logger_handlers.add(handler)

    def remove_logger_handler(self, handler):
        """Remove logger handler to this context."""
        self._logger.removeHandler(handler)
        self._logger_handlers.discard(handler)

    def completions(self, root):
        """Return potential variable, function or attribute matches."""
        words = set()
        num_period = root.count(".")
        if num_period >= 1:
            last_period = root.rfind(".")
            name = root[0:last_period]
            attr_root = root[last_period + 1 :]
            if name in self.global_sym_table:
                var = self.global_sym_table[name]
                try:
                    for attr in var.__dict__:
                        if attr.lower().startswith(attr_root) and (
                            attr_root != "" or attr[0:1] != "_"
                        ):
                            words.add(f"{name}.{attr}")
                # pylint: disable=broad-except
                except Exception:  # nosec
                    pass
        for keyw in set(keyword.kwlist) - {"yield"}:
            if keyw.lower().startswith(root):
                words.add(keyw)
        sym_table = _BUILTIN_AST_FUNCS_FACTORY.copy()
        for name, value in builtins.__dict__.items():
            if name[0] != "_" and name not in _BUILTIN_EXCLUDE:
                sym_table[name] = value
        sym_table.update(self.global_sym_table.items())
        for name, value in sym_table.items():
            if name.lower().startswith(root):
                words.add(name)
        return words

    async def eval(self, new_state_vars=None):
        """Execute parsed code, with the optional state variables added to the scope."""
        self._exception = None
        self._exception_obj = None
        self._exception_long = None
        if new_state_vars:
            self._local_sym_table.update(new_state_vars)
        if self._ast:
            try:
                val = await self.aeval(self._ast)
                if isinstance(val, EvalStopFlow):
                    return None
                return val
            except asyncio.CancelledError:  # pylint: disable=try-except-raise
                raise
            except Exception as err:  # pylint: disable=broad-except
                if self._exception_long is None:
                    self._exception_long = self.format_exc(
                        err, self._lineno, self._col_offset
                    )
        return None

    def dump(self, this_ast=None):
        """Dump the AST tree for debugging."""
        return ast.dump(this_ast if this_ast else self._ast)
