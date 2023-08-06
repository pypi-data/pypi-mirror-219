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
import io
import logging
import typing

import yaml

from ... import core
from .const import Const
from .eval_local_var import EvalLocalVar
from .eval_name import EvalName
from .eval_return import EvalReturn


if not typing.TYPE_CHECKING:

    class AstEval:
        pass

    class GlobalContext:
        pass


if typing.TYPE_CHECKING:
    from .ast_eval import AstEval
    from .global_context import GlobalContext

_TRIG_DECORATORS: typing.Final = {
    "time_trigger",
    "state_trigger",
    "event_trigger",
    "mqtt_trigger",
    "state_active",
    "time_active",
    "task_unique",
}

_TRIG_SERV_DECORATORS: typing.Final = _TRIG_DECORATORS.union({"service"})

_TRIGGER_KWARGS: typing.Final = {
    "context",
    "event_type",
    "old_value",
    "payload",
    "payload_obj",
    "qos",
    "topic",
    "trigger_type",
    "trigger_time",
    "var_name",
    "value",
}


# pylint: disable=unused-variable
class EvalFunc:
    """Class for a callable pyscript function."""

    def __init__(
        self,
        func_def: ast.FunctionDef,
        code_list: list[str],
        code_str: str,
        global_ctx: GlobalContext,
    ):
        """Initialize a function calling context."""
        self._func_def = func_def
        self._name: str = func_def.name
        self._global_ctx = global_ctx
        self._logger = logging.getLogger(__package__ + "." + global_ctx.name)
        self._defaults = []
        self._kw_defaults = []
        self._decorators = []
        self._global_names: set[str] = set()
        self._nonlocal_names: set[str] = set()
        self._local_names: set[str] = set()
        self._local_sym_table = {}
        self._doc_string = ast.get_docstring(func_def)
        self._num_posn_arg = len(self._func_def.args.args)
        self._code_list = code_list
        self._code_str = code_str
        self._exception = None
        self._exception_obj = None
        self._exception_long = None
        self._trigger = []
        self._trigger_service = set()
        self._has_closure = False

    @property
    def controller(self) -> core.SmartHomeController:
        return self._global_ctx.controller

    @property
    def name(self):
        """Return the function name."""
        return self._name

    @property
    def pyscript(self):
        return self._global_ctx.pyscript

    @property
    def global_names(self):
        return frozenset(self._global_names)

    @property
    def local_names(self):
        return frozenset(self._local_names)

    @property
    def nonlocal_names(self):
        return frozenset(self._nonlocal_names)

    async def eval_defaults(self, ast_ctx: AstEval):
        """Evaluate the default function arguments."""
        self._defaults = []
        for val in self._func_def.args.defaults:
            self._defaults.append(await ast_ctx.aeval(val))
        self._num_posn_arg = len(self._func_def.args.args) - len(self._defaults)
        self._kw_defaults = []
        for val in self._func_def.args.kw_defaults:
            self._kw_defaults.append(
                {"ok": bool(val), "val": None if not val else await ast_ctx.aeval(val)}
            )

    async def trigger_init(self):
        """Initialize decorator triggers for this function."""
        trig_args = {}
        trig_decs = {}
        got_reqd_dec = False
        exc_mesg = f"function '{self.name}' defined in {self._global_ctx.name}"
        trig_decorators_reqd = {
            "event_trigger",
            "mqtt_trigger",
            "state_trigger",
            "time_trigger",
        }
        arg_check = {
            "event_trigger": {"arg_cnt": [1, 2], "rep_ok": True},
            "mqtt_trigger": {"arg_cnt": [1, 2], "rep_ok": True},
            "state_active": {"arg_cnt": [1]},
            "state_trigger": {"arg_cnt": ["*"], "type": [list, set], "rep_ok": True},
            "service": {"arg_cnt": [0, "*"]},
            "task_unique": {"arg_cnt": [1]},
            "time_active": {"arg_cnt": ["*"]},
            "time_trigger": {"arg_cnt": [0, "*"], "rep_ok": True},
        }
        kwarg_check = {
            "event_trigger": {"kwargs": {dict}},
            "mqtt_trigger": {"kwargs": {dict}},
            "time_trigger": {"kwargs": {dict}},
            "task_unique": {"kill_me": {bool, int}},
            "time_active": {"hold_off": {int, float}},
            "state_trigger": {
                "kwargs": {dict},
                "state_hold": {int, float},
                "state_check_now": {bool, int},
                "state_hold_false": {int, float},
                "watch": {set, list},
            },
        }

        for dec in self._decorators:  # pylint: disable=too-many-nested-blocks
            dec_name, dec_args, dec_kwargs = dec[0], dec[1], dec[2]
            if dec_name not in _TRIG_SERV_DECORATORS:
                raise SyntaxError(f"{exc_mesg}: unknown decorator @{dec_name}")
            if dec_name in trig_decorators_reqd:
                got_reqd_dec = True
            arg_info = arg_check.get(dec_name, {})
            #
            # check that we have the right number of arguments, and that they are
            # strings
            #
            arg_cnt = arg_info["arg_cnt"]
            if dec_args is None and 0 not in arg_cnt:
                raise TypeError(
                    f"{exc_mesg}: decorator @{dec_name} needs at least one argument"
                )
            if dec_args:
                if "*" not in arg_cnt and len(dec_args) not in arg_cnt:
                    raise TypeError(
                        f"{exc_mesg}: decorator @{dec_name} got {len(dec_args)}"
                        f" argument{'s' if len(dec_args) > 1 else ''}, expected"
                        f" {' or '.join([str(cnt) for cnt in sorted(arg_cnt)])}"
                    )
                for arg_num, arg in enumerate(dec_args):
                    if isinstance(arg, str):
                        continue
                    mesg = "string"
                    if "type" in arg_info:
                        if type(arg) in arg_info["type"]:
                            for val in arg:
                                if not isinstance(val, str):
                                    break
                            else:
                                continue
                            mesg += ", or " + ", or ".join(
                                sorted(ok_type.__name__ for ok_type in arg_info["type"])
                            )
                    raise TypeError(
                        f"{exc_mesg}: decorator @{dec_name} argument {arg_num + 1} "
                        + f"should be a {mesg}"
                    )
            if arg_cnt == [1]:
                dec_args = dec_args[0]

            if dec_name not in kwarg_check and dec_kwargs is not None:
                raise TypeError(
                    f"{exc_mesg}: decorator @{dec_name} doesn't take keyword arguments"
                )
            if dec_kwargs is None:
                dec_kwargs = {}
            if dec_name in kwarg_check:
                allowed = kwarg_check[dec_name]
                for arg, value in dec_kwargs.items():
                    if arg not in allowed:
                        raise TypeError(
                            f"{exc_mesg}: decorator @{dec_name} invalid keyword argument '{arg}'"
                        )
                    if value is None or type(value) in allowed[arg]:
                        continue
                    ok_types = " or ".join(sorted(t.__name__ for t in allowed[arg]))
                    raise TypeError(
                        f"{exc_mesg}: decorator @{dec_name} keyword '{arg}' "
                        + f"should be type {ok_types}"
                    )
            if dec_name == "service":
                desc = self._doc_string
                if not desc:
                    desc = f"pyscript function {self.name}()"
                desc = desc.lstrip(" \n\r")
                if desc.startswith("yaml"):
                    try:
                        desc = desc[4:].lstrip(" \n\r")
                        file_desc = io.StringIO(desc)
                        service_desc = (
                            yaml.load(file_desc, Loader=yaml.BaseLoader)  # nosec
                            or typing.OrderedDict()
                        )
                        file_desc.close()
                    except Exception as exc:
                        self._logger.error(
                            f"Unable to decode yaml doc_string for {self.name}(): {str(exc)}",
                        )
                        raise exc
                else:
                    fields = typing.OrderedDict()
                    for arg in self.positional_args:
                        fields[arg] = typing.OrderedDict(description=f"argument {arg}")
                    service_desc = {"description": desc, "fields": fields}

                def pyscript_service_factory(func_name: str, func: EvalFunc):
                    async def pyscript_service_handler(call: core.ServiceCall):
                        """Handle python script service calls."""
                        # self.logger.debug("service call to %s", func_name)
                        #
                        # use a new AstEval context so it can run fully independently
                        # of other instances (except for global_ctx which is common)
                        #
                        ast_ctx = self._global_ctx.create_ast_context(
                            f"{self._global_ctx.name}.{func_name}"
                        )
                        func_args = {
                            "trigger_type": "service",
                            "context": call.context,
                        }
                        func_args.update(call.data)

                        async def do_service_call():
                            await func.call(ast_ctx, **func_args)
                            if ast_ctx.exception_obj:
                                ast_ctx.logger.error(ast_ctx.exception_long)

                        self.pyscript.functions.create_task(do_service_call())

                    return pyscript_service_handler

                for srv_name in (
                    dec_args if dec_args else [f"{self.pyscript.domain}.{self.name}"]
                ):
                    if not isinstance(srv_name, str) or srv_name.count(".") != 1:
                        raise ValueError(
                            f"{exc_mesg}: @service argument must be a string with one period"
                        )
                    domain, name = srv_name.split(".", 1)
                    domain = domain.lower()
                    name = name.lower()
                    if name in (
                        core.Const.SERVICE_RELOAD,
                        Const.SERVICE_JUPYTER_KERNEL_START,
                    ):
                        raise SyntaxError(
                            f"{exc_mesg}: @service conflicts with builtin service"
                        )
                    self.pyscript.functions.service_register(
                        self._global_ctx.name,
                        domain,
                        name,
                        pyscript_service_factory(self.name, self),
                    )
                    core.Service.async_set_service_schema(
                        self.controller, domain, name, service_desc
                    )
                    self._trigger_service.add(srv_name)
                continue

            if dec_name not in trig_decs:
                trig_decs[dec_name] = []
            if len(trig_decs[dec_name]) > 0 and "rep_ok" not in arg_info:
                raise SyntaxError(
                    f"{exc_mesg}: decorator @{dec_name} can only be used once"
                )
            trig_decs[dec_name].append({"args": dec_args, "kwargs": dec_kwargs})

        if not got_reqd_dec and len(trig_decs) > 0:
            self._logger.error(
                f"{self.name} defined in {self._global_ctx.name}: needs at least "
                + f"one trigger decorator (ie: {', '.join(sorted(trig_decorators_reqd))})",
            )
            return

        if len(trig_decs) == 0:
            if len(self._trigger_service) > 0:
                self._global_ctx.trigger_register(self)
            return

        #
        # start one or more triggers until they are all consumed
        # each trigger task can handle at most one of each type of
        # trigger; all get the same state_active, time_active and
        # task_unique decorators
        #
        while True:
            trig_args = {
                "action": self,
                "global_sym_table": self._global_ctx.global_sym_table,
            }
            got_trig = False
            for trig in trig_decorators_reqd:
                if trig not in trig_decs or len(trig_decs[trig]) == 0:
                    continue
                trig_args[trig] = trig_decs[trig].pop(0)
                got_trig = True
            if not got_trig:
                break
            for dec_name in ["state_active", "time_active", "task_unique"]:
                if dec_name in trig_decs:
                    trig_args[dec_name] = trig_decs[dec_name][0]

            self._trigger.append(
                self._global_ctx.get_trig_info(
                    f"{self._global_ctx.name}.{self.name}", trig_args
                )
            )

        if self._global_ctx.trigger_register(self):
            self.trigger_start()

    def trigger_start(self):
        """Start any triggers for this function."""
        for trigger in self._trigger:
            trigger.start()

    def trigger_stop(self):
        """Stop any triggers for this function."""
        for trigger in self._trigger:
            trigger.stop()
        self._trigger = []
        for srv_name in self._trigger_service:
            domain, name = srv_name.split(".", 1)
            self.pyscript.functions.service_remove(self._global_ctx.name, domain, name)
        self._trigger_service = set()

    async def eval_decorators(self, ast_ctx: AstEval):
        """Evaluate the function decorators arguments."""
        # pylint: disable=protected-access
        code_str, code_list = ast_ctx._code_str, ast_ctx._code_list
        ast_ctx._code_str, ast_ctx._code_list = self._code_str, self._code_list

        dec_other = []
        dec_trig = []
        for dec in self._func_def.decorator_list:
            if (
                isinstance(dec, ast.Call)
                and isinstance(dec.func, ast.Name)
                and dec.func.id in _TRIG_SERV_DECORATORS
            ):
                args = [await ast_ctx.aeval(arg) for arg in dec.args]
                kwargs = {
                    keyw.arg: await ast_ctx.aeval(keyw.value) for keyw in dec.keywords
                }
                dec_trig.append(
                    [dec.func.id, args, kwargs if len(kwargs) > 0 else None]
                )
            elif isinstance(dec, ast.Name) and dec.id in _TRIG_SERV_DECORATORS:
                dec_trig.append([dec.id, None, None])
            else:
                dec_other.append(await ast_ctx.aeval(dec))

        ast_ctx._code_str, ast_ctx._code_list = code_str, code_list
        return dec_trig, reversed(dec_other)

    async def resolve_nonlocals(self, ast_ctx: AstEval):
        """Tag local variables and resolve nonlocals."""

        # pylint: disable=protected-access

        #
        # determine the list of local variables, nonlocal and global
        # arguments are local variables too
        #
        args = self.positional_args
        if self._func_def.args.vararg:
            args.append(self._func_def.args.vararg.arg)
        if self._func_def.args.kwarg:
            args.append(self._func_def.args.kwarg.arg)
        for arg in self._func_def.args.kwonlyargs:
            args.append(arg.arg)
        nonlocal_names = set()
        global_names = set()
        var_names = set(args)
        self._local_names = set(args)
        for stmt in self._func_def.body:
            self._has_closure = self._has_closure or await self.check_for_closure(stmt)
            var_names = var_names.union(
                await ast_ctx.get_names(
                    stmt,
                    nonlocal_names=nonlocal_names,
                    global_names=global_names,
                    local_names=self._local_names,
                )
            )
        for var_name in var_names:
            got_dot = var_name.find(".")
            if got_dot >= 0:
                var_name = var_name[0:got_dot]

            if var_name in global_names:
                continue

            if var_name in self._local_names and var_name not in nonlocal_names:
                if self._has_closure:
                    self._local_sym_table[var_name] = EvalLocalVar(var_name)
                continue

            if var_name in nonlocal_names:
                sym_table_idx = 1
            else:
                sym_table_idx = 0
            for sym_table in reversed(
                ast_ctx._sym_table_stack[sym_table_idx:] + [ast_ctx._sym_table]
            ):
                if var_name in sym_table and isinstance(
                    sym_table[var_name], EvalLocalVar
                ):
                    self._local_sym_table[var_name] = sym_table[var_name]
                    break
            else:
                if var_name in nonlocal_names:
                    val = await ast_ctx.ast_name(ast.Name(id=var_name, ctx=ast.Load()))
                    if isinstance(val, EvalName) and got_dot < 0:
                        raise SyntaxError(f"no binding for nonlocal '{var_name}' found")

    @property
    def decorators(self):
        """Return the function decorators."""
        return self._decorators

    @property
    def doc_string(self):
        """Return the function doc_string."""
        return self._doc_string

    @property
    def positional_args(self):
        """Return the function positional arguments."""
        args: list[str] = []
        for arg in self._func_def.args.args:
            args.append(arg.arg)
        return args

    async def try_aeval(self, ast_ctx: AstEval, arg):
        """Call self.aeval and capture exceptions."""
        try:
            return await ast_ctx.aeval(arg)
        except asyncio.CancelledError:  # pylint: disable=try-except-raise
            raise
        except Exception as err:  # pylint: disable=broad-except
            if ast_ctx.exception_long is None:
                # pylint: disable=protected-access
                ast_ctx._exception_long = ast_ctx.format_exc(
                    err, arg.lineno, arg.col_offset
                )

    async def call(self, ast_ctx: AstEval, *args, **kwargs):
        """Call the function with the given context and arguments."""
        # pylint: disable=protected-access
        sym_table = {}
        if args is None:
            args = []
        kwargs = kwargs.copy() if kwargs else {}
        i = 0
        for arg in self._func_def.args.args:
            var_name = arg.arg
            val = None
            if i < len(args):
                val = args[i]
                if var_name in kwargs:
                    raise TypeError(
                        f"{self.name}() got multiple values for argument '{var_name}'"
                    )
            elif var_name in kwargs:
                val = kwargs[var_name]
                del kwargs[var_name]
            elif self._num_posn_arg <= i < len(self._defaults) + self._num_posn_arg:
                val = self._defaults[i - self._num_posn_arg]
            else:
                raise TypeError(
                    f"{self.name}() missing {self._num_posn_arg - i} required positional arguments"
                )
            sym_table[var_name] = val
            i += 1
        i = 0
        for arg in self._func_def.args.kwonlyargs:
            var_name = arg.arg
            if var_name in kwargs:
                val = kwargs[var_name]
                del kwargs[var_name]
            elif i < len(self._kw_defaults) and self._kw_defaults[i]["ok"]:
                val = self._kw_defaults[i]["val"]
            else:
                raise TypeError(
                    f"{self.name}() missing required keyword-only arguments"
                )
            sym_table[var_name] = val
            i += 1
        if self._func_def.args.kwarg:
            sym_table[self._func_def.args.kwarg.arg] = kwargs
        elif not set(kwargs.keys()).issubset(_TRIGGER_KWARGS):
            # don't raise an exception for extra trigger keyword parameters;
            # it's difficult to apply this exception to just trigger functions
            # since they could have non-trigger decorators too
            unexpected = ", ".join(sorted(set(kwargs.keys()) - _TRIGGER_KWARGS))
            raise TypeError(
                f"{self.name}() called with unexpected keyword arguments: {unexpected}"
            )
        if self._func_def.args.vararg:
            if len(args) > len(self._func_def.args.args):
                sym_table[self._func_def.args.vararg.arg] = tuple(
                    args[len(self._func_def.args.args) :]
                )
            else:
                sym_table[self._func_def.args.vararg.arg] = ()
        elif len(args) > len(self._func_def.args.args):
            raise TypeError(f"{self.name}() called with too many positional arguments")
        for name, value in self._local_sym_table.items():
            if name in sym_table:
                sym_table[name] = EvalLocalVar(name, value=sym_table[name])
            elif value.is_defined():
                sym_table[name] = value
            else:
                sym_table[name] = EvalLocalVar(name)
        if ast_ctx.global_ctx != self._global_ctx:
            #
            # switch to the global symbol table in the global context
            # where the function was defined
            #
            prev_sym_table = (
                ast_ctx._global_sym_table,
                ast_ctx._sym_table,
                ast_ctx._sym_table_stack,
                ast_ctx._global_ctx,
            )
            ast_ctx._global_sym_table = self._global_ctx.global_sym_table
            ast_ctx._sym_table_stack = [ast_ctx.global_sym_table]
            ast_ctx._global_ctx = self._global_ctx
        else:
            ast_ctx._sym_table_stack.append(ast_ctx._sym_table)
            prev_sym_table = None
        ast_ctx._sym_table = sym_table
        code_str, code_list = ast_ctx._code_str, ast_ctx._code_list
        ast_ctx._code_str, ast_ctx._code_list = self._code_str, self._code_list
        self._exception = None
        self._exception_obj = None
        self._exception_long = None
        prev_func = ast_ctx._curr_func
        save_user_locals = ast_ctx._user_locals
        ast_ctx._user_locals = {}
        ast_ctx._curr_func = self
        del args, kwargs
        for arg1 in self._func_def.body:
            val = await self.try_aeval(ast_ctx, arg1)
            if isinstance(val, EvalReturn):
                val = val.value
                break
            # return None at end if there isn't a return
            val = None
            if ast_ctx.exception_obj:
                break
        ast_ctx._curr_func = prev_func
        ast_ctx._user_locals = save_user_locals
        ast_ctx._code_str, ast_ctx._code_list = code_str, code_list
        if prev_sym_table is not None:
            (
                ast_ctx._global_sym_table,
                ast_ctx._sym_table,
                ast_ctx._sym_table_stack,
                ast_ctx._global_ctx,
            ) = prev_sym_table
        else:
            ast_ctx._sym_table = ast_ctx._sym_table_stack.pop()
        return val

    async def check_for_closure(self, arg: ast.stmt):
        """Recursively check ast tree arg and return True if there is an inner function or class."""
        if isinstance(arg, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            return True
        for child in ast.iter_child_nodes(arg):
            if await self.check_for_closure(child):
                return True
        return False
