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

import asyncio
import datetime as dt
import time
import typing

from ... import core
from .const import Const
from .eval_func import EvalFunc
from .parse_mode import ParseMode
from .trig_time import (
    _LOGGER,
    _STATE_RE,
    _ident_any_values_changed,
    _ident_values_changed,
)
from .ast_eval import AstEval

if not typing.TYPE_CHECKING:

    class GlobalContext:
        pass

    class PyscriptComponent:
        pass


if typing.TYPE_CHECKING:
    from .global_context import GlobalContext
    from .pyscript_component import PyscriptComponent

_mode: typing.TypeAlias = ParseMode


# pylint: disable=unused-variable
class TrigInfo:
    """Class for all trigger-decorated functions."""

    def __init__(
        self,
        owner: PyscriptComponent,
        name: str,
        trig_cfg,
        global_ctx: GlobalContext = None,
    ):
        """Create a new TrigInfo."""
        self._owner = owner
        self._name = name
        self._task = None
        self._global_ctx = global_ctx
        self._trig_cfg = trig_cfg
        self._state_trigger = trig_cfg.get("state_trigger", {}).get("args", None)
        self._state_trigger_kwargs = trig_cfg.get("state_trigger", {}).get("kwargs", {})
        self._state_hold = self._state_trigger_kwargs.get("state_hold", None)
        self._state_hold_false = self._state_trigger_kwargs.get(
            "state_hold_false", None
        )
        self._state_check_now = self._state_trigger_kwargs.get("state_check_now", False)
        self._state_user_watch = self._state_trigger_kwargs.get("watch", None)
        self._time_trigger = trig_cfg.get("time_trigger", {}).get("args", None)
        self._time_trigger_kwargs = trig_cfg.get("time_trigger", {}).get("kwargs", {})
        self._event_trigger = trig_cfg.get("event_trigger", {}).get("args", None)
        self._event_trigger_kwargs = trig_cfg.get("event_trigger", {}).get("kwargs", {})
        self._mqtt_trigger = trig_cfg.get("mqtt_trigger", {}).get("args", None)
        self._mqtt_trigger_kwargs = trig_cfg.get("mqtt_trigger", {}).get("kwargs", {})
        self._state_active = trig_cfg.get("state_active", {}).get("args", None)
        self._time_active = trig_cfg.get("time_active", {}).get("args", None)
        self._time_active_hold_off = (
            trig_cfg.get("time_active", {}).get("kwargs", {}).get("hold_off", None)
        )
        self._task_unique: str = trig_cfg.get("task_unique", {}).get("args", None)
        self._task_unique_kwargs: dict[str, typing.Any] = trig_cfg.get(
            "task_unique", {}
        ).get("kwargs", None)
        self._action: EvalFunc = trig_cfg.get("action")
        self._global_sym_table = trig_cfg.get("global_sym_table", {})
        self._notify_q = asyncio.Queue(0)
        self._active_expr: AstEval = None
        self._state_active_ident = None
        self._state_trig_expr = None
        self._state_trig_eval = None
        self._state_trig_ident = None
        self._state_trig_ident_any = set()
        self._event_trig_expr = None
        self._mqtt_trig_expr = None
        self._have_trigger = False
        self._setup_ok = False
        self._run_on_startup = False
        self._run_on_shutdown = False

        if self._state_active is not None:
            self._active_expr = self._global_ctx.create_ast_context(
                name=f"{self.name} @state_active()",
                logger_name=self.name,
            )
            self._active_expr.parse(self._state_active, mode=_mode.EVAL)
            exc = self._active_expr.exception_long
            if exc is not None:
                self._active_expr.logger.error(exc)
                return

        if "time_trigger" in trig_cfg and self._time_trigger is None:
            self._run_on_startup = True
        if self._time_trigger is not None:
            while "startup" in self._time_trigger:
                self._run_on_startup = True
                self._time_trigger.remove("startup")
            while "shutdown" in self._time_trigger:
                self._run_on_shutdown = True
                self._time_trigger.remove("shutdown")
            if len(self._time_trigger) == 0:
                self._time_trigger = None

        if self._state_trigger is not None:
            state_trig = []
            for triggers in self._state_trigger:
                if isinstance(triggers, str):
                    triggers = [triggers]
                elif isinstance(triggers, set):
                    triggers = list(triggers)
                #
                # separate out the entries that are just state var names, which mean trigger
                # on any change (no expr)
                #
                for trig in triggers:
                    if _STATE_RE.match(trig):
                        self._state_trig_ident_any.add(trig)
                    else:
                        state_trig.append(trig)

            if len(state_trig) > 0:
                if len(state_trig) == 1:
                    self._state_trig_expr = state_trig[0]
                else:
                    self._state_trig_expr = f"any([{', '.join(state_trig)}])"
                self._state_trig_eval = self.global_ctx.create_ast_context(
                    name=f"{self.name} @state_trigger()",
                    logger_name=self.name,
                )
                self._state_trig_eval.parse(self._state_trig_expr, mode=_mode.EVAL)
                exc = self._state_trig_eval.exception_long
                if exc is not None:
                    self._state_trig_eval.logger.error(exc)
                    return
            self._have_trigger = True

        if self._event_trigger is not None:
            if len(self._event_trigger) == 2:
                self._event_trig_expr = self.global_ctx.create_ast_context(
                    name=f"{self.name} @event_trigger()",
                    logger_name=self.name,
                )
                self._event_trig_expr.parse(self._event_trigger[1], mode=_mode.EVAL)
                exc = self._event_trig_expr.exception_long
                if exc is not None:
                    self._event_trig_expr.logger.error(exc)
                    return
            self._have_trigger = True

        if self._mqtt_trigger is not None:
            if len(self._mqtt_trigger) == 2:
                self._mqtt_trig_expr = self.global_ctx.create_ast_context(
                    name=f"{self.name} @mqtt_trigger()",
                    logger_name=self.name,
                )
                self._mqtt_trig_expr.parse(self._mqtt_trigger[1], mode=_mode.EVAL)
                exc = self._mqtt_trig_expr.exception_long
                if exc is not None:
                    self._mqtt_trig_expr.logger.error(exc)
                    return
            self._have_trigger = True

        self._setup_ok = True

    @property
    def name(self):
        return self._name

    @property
    def controller(self):
        return self._owner.controller

    @property
    def global_ctx(self):
        return self._global_ctx

    @property
    def pyscript(self):
        return self._owner

    def stop(self):
        """Stop this trigger task."""

        if self._task:
            if self._state_trig_ident:
                self.pyscript.states.notify_del(self._state_trig_ident, self._notify_q)
            if self._event_trigger is not None:
                self.pyscript.events.notify_del(self._event_trigger[0], self._notify_q)
            if self._mqtt_trigger is not None:
                self.pyscript.mqtt.notify_del(self._mqtt_trigger[0], self._notify_q)
            self.pyscript.functions.reaper_cancel(self._task)
            self._task = None
        if self._run_on_shutdown:
            notify_type = "shutdown"
            notify_info = {"trigger_type": "time", "trigger_time": "shutdown"}
            notify_info.update(self._time_trigger_kwargs.get("kwargs", {}))
            action_future = self.call_action(notify_type, notify_info, run_task=False)
            self.pyscript.functions.waiter_await(action_future)

    def start(self):
        """Start this trigger task."""
        if not self._task and self._setup_ok:
            self._task = self.pyscript.functions.create_task(self._trigger_watch())
            _LOGGER.debug(f"trigger {self.name} is active")

    async def _trigger_watch(self):  # pylint: disable=too-many-statements
        """
        Task that runs for each trigger,
        waiting for the next trigger and calling the function."""

        try:  # pylint: disable=too-many-nested-blocks
            if self._state_trigger is not None:
                self._state_trig_ident = set()
                if self._state_user_watch:
                    if isinstance(self._state_user_watch, list):
                        self._state_trig_ident = set(self._state_user_watch)
                    else:
                        self._state_trig_ident = self._state_user_watch
                else:
                    if self._state_trig_eval:
                        self._state_trig_ident = await self._state_trig_eval.get_names()
                    self._state_trig_ident.update(self._state_trig_ident_any)
                _LOGGER.debug(
                    f"trigger {self.name}: watching vars {self._state_trig_ident}"
                )
                if len(
                    self._state_trig_ident
                ) == 0 or not await self.pyscript.states.notify_add(
                    self._state_trig_ident, self._notify_q
                ):
                    _LOGGER.error(
                        f"trigger {self.name}: @state_trigger is not watching any variables; "
                        + "will never trigger",
                    )

            if self._active_expr:
                self._state_active_ident = await self._active_expr.get_names()

            if self._event_trigger is not None:
                _LOGGER.debug(
                    f"trigger {self.name} adding event_trigger {self._event_trigger[0]}",
                )
                self.pyscript.events.notify_add(self._event_trigger[0], self._notify_q)
            if self._mqtt_trigger is not None:
                _LOGGER.debug(
                    f"trigger {self.name} adding mqtt_trigger {self._mqtt_trigger[0]}"
                )
                await self.pyscript.mqtt.notify_add(
                    self._mqtt_trigger[0], self._notify_q
                )

            last_trig_time = None
            last_state_trig_time = None
            state_trig_waiting = False
            state_trig_notify_info = [None, None]
            state_false_time = None
            now = startup_time = None
            check_state_expr_on_start = (
                self._state_check_now or self._state_hold_false is not None
            )

            while True:
                timeout = None
                state_trig_timeout = False
                notify_info = None
                notify_type = None
                now = dt.datetime.now()
                if startup_time is None:
                    startup_time = now
                if self._run_on_startup:
                    #
                    # first time only - skip waiting for other triggers
                    #
                    notify_type = "startup"
                    notify_info = {"trigger_type": "time", "trigger_time": "startup"}
                    self._run_on_startup = False
                elif check_state_expr_on_start:
                    #
                    # first time only - skip wait and check state trigger
                    #
                    notify_type = "state"
                    if self._state_trig_ident:
                        notify_vars = self.pyscript.states.notify_var_get(
                            self._state_trig_ident, {}
                        )
                    else:
                        notify_vars = {}
                    notify_info = [notify_vars, {"trigger_type": notify_type}]
                    check_state_expr_on_start = False
                else:
                    if self._time_trigger:
                        time_next = self.pyscript.time_triggers.timer_trigger_next(
                            self._time_trigger, now, startup_time
                        )
                        _LOGGER.debug(
                            f"trigger {self.name} time_next = {time_next}, now = {now}",
                        )
                        if time_next is not None:
                            timeout = (time_next - now).total_seconds()
                    if state_trig_waiting:
                        time_left = (
                            last_state_trig_time + self.state_hold - time.monotonic()
                        )
                        if timeout is None or time_left < timeout:
                            timeout = time_left
                            time_next = now + dt.timedelta(seconds=timeout)
                            state_trig_timeout = True
                    if timeout is not None:
                        while True:
                            try:
                                timeout = max(0, timeout)
                                _LOGGER.debug(
                                    f"trigger {self.name} waiting for {timeout:.6g} secs",
                                )
                                notify_type, notify_info = await asyncio.wait_for(
                                    self._notify_q.get(), timeout=timeout
                                )
                                state_trig_timeout = False
                                now = dt.datetime.now()
                            except asyncio.TimeoutError:
                                actual_now = dt.datetime.now()
                                if actual_now < time_next:
                                    timeout = (time_next - actual_now).total_seconds()
                                    continue
                                now = time_next
                                if not state_trig_timeout:
                                    notify_type = "time"
                                    notify_info = {
                                        "trigger_type": "time",
                                        "trigger_time": time_next,
                                    }
                            break
                    elif self._have_trigger:
                        _LOGGER.debug(
                            f"trigger {self.name} waiting for state change or event"
                        )
                        notify_type, notify_info = await self._notify_q.get()
                        now = dt.datetime.now()
                    else:
                        _LOGGER.debug(f"trigger {self.name} finished")
                        return

                #
                # check the trigger-specific expressions
                #
                trig_ok = True
                new_vars = {}
                user_kwargs = {}
                if state_trig_timeout:
                    new_vars, func_args = state_trig_notify_info
                    state_trig_waiting = False
                elif notify_type == "state":  # pylint: disable=too-many-nested-blocks
                    new_vars, func_args = notify_info
                    user_kwargs = self._state_trigger_kwargs.get("kwargs", {})

                    if not _ident_any_values_changed(
                        func_args, self._state_trig_ident_any
                    ):
                        #
                        # if var_name not in func_args we are check_state_expr_on_start
                        #
                        if "var_name" in func_args and not _ident_values_changed(
                            func_args, self._state_trig_ident
                        ):
                            continue

                        if self._state_trig_eval:
                            trig_ok = await self._state_trig_eval.eval(new_vars)
                            exc = self._state_trig_eval.exception_long
                            if exc is not None:
                                self._state_trig_eval.logger.error(exc)
                                trig_ok = False

                            if self._state_hold_false is not None:
                                if "var_name" not in func_args:
                                    #
                                    # this is check_state_expr_on_start check
                                    # if immediately true, force wait until False
                                    # otherwise start False wait now
                                    #
                                    state_false_time = (
                                        None if trig_ok else time.monotonic()
                                    )
                                    if not self._state_check_now:
                                        continue
                                if state_false_time is None:
                                    if trig_ok:
                                        #
                                        # wasn't False, so ignore after initial check
                                        #
                                        if "var_name" in func_args:
                                            continue
                                    else:
                                        #
                                        # first False, so remember when it is
                                        #
                                        state_false_time = time.monotonic()
                                elif trig_ok and "var_name" in func_args:
                                    too_soon = (
                                        time.monotonic() - state_false_time
                                        < self._state_hold_false
                                    )
                                    state_false_time = None
                                    if too_soon:
                                        #
                                        # was False but not for long enough, so start over
                                        #
                                        continue
                        else:
                            trig_ok = False

                    if self._state_hold is not None:
                        if trig_ok:
                            if not state_trig_waiting:
                                state_trig_waiting = True
                                state_trig_notify_info = notify_info
                                last_state_trig_time = time.monotonic()
                                _LOGGER.debug(
                                    f"trigger {notify_type} got {self.name} trigger; "
                                    + f"now waiting for state_hold of {self._state_hold} "
                                    + "seconds",
                                )
                            else:
                                _LOGGER.debug(
                                    f"trigger {notify_type} got {self.name} trigger; "
                                    + f"still waiting for state_hold of {self._state_hold} "
                                    + "seconds",
                                )
                            func_args.update(user_kwargs)
                            continue
                        if state_trig_waiting:
                            state_trig_waiting = False
                            _LOGGER.debug(
                                f"trigger {notify_type} {self.name} trigger now false during "
                                + "state_hold; waiting for new trigger",
                                notify_type,
                                self.name,
                            )
                            continue

                elif notify_type == "event":
                    func_args = notify_info
                    user_kwargs = self._event_trigger_kwargs.get("kwargs", {})
                    if self._event_trig_expr:
                        trig_ok = await self._event_trig_expr.eval(notify_info)
                elif notify_type == "mqtt":
                    func_args = notify_info
                    user_kwargs = self._mqtt_trigger_kwargs.get("kwargs", {})
                    if self._mqtt_trig_expr:
                        trig_ok = await self._mqtt_trig_expr.eval(notify_info)

                else:
                    user_kwargs = self._time_trigger_kwargs.get("kwargs", {})
                    func_args = notify_info

                #
                # now check the state and time active expressions
                #
                if trig_ok and self._active_expr:
                    active_vars = self.pyscript.states.notify_var_get(
                        self._state_active_ident, new_vars
                    )
                    trig_ok = await self._active_expr.eval(active_vars)
                    exc = self._active_expr.exception_long
                    if exc is not None:
                        self._active_expr.logger.error(exc)
                        trig_ok = False
                if trig_ok and self._time_active:
                    trig_ok = self.pyscript.time_triggers.timer_active_check(
                        self._time_active, now, startup_time
                    )

                if not trig_ok:
                    _LOGGER.debug(
                        f"trigger {self.name} got {notify_type} trigger, but not active",
                    )
                    continue

                if (
                    self._time_active_hold_off is not None
                    and last_trig_time is not None
                    and time.monotonic() < last_trig_time + self._time_active_hold_off
                ):
                    _LOGGER.debug(
                        f"trigger {notify_type} got {self.name} trigger, but less than "
                        + f"{self._time_active_hold_off} seconds since last trigger, "
                        + "so skipping",
                    )
                    continue

                func_args.update(user_kwargs)
                if self.call_action(notify_type, func_args):
                    last_trig_time = time.monotonic()

        except asyncio.CancelledError:  # pylint: disable=try-except-raise
            raise

        except Exception as exc:  # pylint: disable=broad-except
            _LOGGER.error(f"{self.name}: {exc}")
            if self._state_trig_ident:
                self.pyscript.states.notify_del(self._state_trig_ident, self._notify_q)
            if self._event_trigger is not None:
                self.pyscript.events.notify_del(self._event_trigger[0], self._notify_q)
            if self._mqtt_trigger is not None:
                self.pyscript.mqtt.notify_del(self._mqtt_trigger[0], self._notify_q)
            return

    def call_action(self, notify_type, func_args, run_task=True):
        """Call the trigger action function."""
        action_ast_ctx = self.global_ctx.create_ast_context(
            name=f"{self.global_ctx.name}.{self._action.name}",
        )
        task_unique_func = None
        if self._task_unique is not None:
            task_unique_func = self.pyscript.functions.task_unique_factory(
                action_ast_ctx
            )

        #
        # check for @task_unique with kill_me=True
        #
        if (
            self._task_unique is not None
            and self._task_unique_kwargs
            and self._task_unique_kwargs["kill_me"]
            and self.pyscript.functions.unique_name_used(
                action_ast_ctx, self._task_unique
            )
        ):
            _LOGGER.debug(
                f"trigger {notify_type} got {self.name} trigger, "
                + "@task_unique kill_me=True prevented new action",
            )
            return False

        # Create new HASS Context with incoming as parent
        context = func_args.get("context")
        if isinstance(context, core.Context):
            context = core.Context(parent_id=context.id)
        else:
            context = core.Context()

        # Fire an event indicating that pyscript is running
        # Note: the event must have an entity_id for logbook to work correctly.
        ev_name = self.name.replace(".", "_")
        ev_entity_id = f"pyscript.{ev_name}"

        event_data = {
            "name": ev_name,
            "entity_id": ev_entity_id,
            "func_args": func_args,
        }
        self.controller.bus.async_fire(
            Const.EVENT_PYSCRIPT_RUNNING, event_data, context=context
        )

        _LOGGER.debug(
            f"trigger {self.name} got {notify_type} trigger, "
            + f"running action (kwargs = {func_args})",
        )

        async def do_func_call(**kwargs):
            # Store HASS Context for this Task
            self.pyscript.functions.store_context(context)

            if self._task_unique and task_unique_func:
                await task_unique_func(self._task_unique)
            await action_ast_ctx.call_func(self._action, None, **kwargs)
            if action_ast_ctx.exception_obj:
                action_ast_ctx.logger.error(action_ast_ctx.exception_long)

        func = do_func_call(
            **func_args,
        )
        if run_task:
            task = self.pyscript.functions.create_task(func, ast_ctx=action_ast_ctx)
            self.pyscript.functions.task_done_callback_ctx(task, action_ast_ctx)
            return True
        return func
