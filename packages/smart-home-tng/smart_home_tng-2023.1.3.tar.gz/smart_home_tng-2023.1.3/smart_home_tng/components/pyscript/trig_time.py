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
import functools as ft
import locale
import logging
import math
import re
import time
import typing

from croniter import croniter

from .eval_func import EvalFunc
from .eval_func_var import EvalFuncVar
from .parse_mode import ParseMode
from .states import _STATE_VIRTUAL_ATTRS

if not typing.TYPE_CHECKING:

    class PyscriptComponent:
        pass

    class AstEval:
        pass


if typing.TYPE_CHECKING:
    from .ast_eval import AstEval
    from .pyscript_component import PyscriptComponent


_LOGGER: typing.Final = logging.getLogger(__package__ + ".trigger")
_STATE_RE: typing.Final = re.compile(r"\w+\.\w+(\.((\w+)|\*))?$")


# pylint: disable=unused-variable
class TrigTime:
    """Class for trigger time functions."""

    def __init__(self, owner: PyscriptComponent):
        """Initialize TrigTime."""
        #
        # Mappings of day of week name to number, using US convention of sunday is 0.
        # Initialized based on locale at startup.
        #
        self._dow2int: dict[str, int] = {}
        self._owner = owner

        def wait_until_factory(ast_ctx: AstEval):
            """Return wapper to call to astFunction with the ast context."""

            async def wait_until_call(*arg, **kw):
                return await self.wait_until(ast_ctx, *arg, **kw)

            return wait_until_call

        def user_task_create_factory(ast_ctx: AstEval):
            """Return wapper to call to astFunction with the ast context."""

            async def user_task_create(func, *args, **kwargs):
                """Implement task.create()."""

                async def func_call(
                    func, func_name: str, new_ast_ctx: AstEval, *args, **kwargs
                ):
                    """Call user function inside task.create()."""
                    ret = await new_ast_ctx.call_func(func, func_name, *args, **kwargs)
                    if new_ast_ctx.get_exception_obj():
                        new_ast_ctx.get_logger().error(new_ast_ctx.get_exception_long())
                    return ret

                try:
                    if isinstance(func, (EvalFunc, EvalFuncVar)):
                        func_name = func.name
                    else:
                        func_name = func.__name__
                except Exception:  # pylint: disable=broad-except
                    func_name = "<function>"

                global_ctx = ast_ctx.global_ctx
                new_ast_ctx = global_ctx.create_ast_context(
                    f"{global_ctx.name()}.{func_name}",
                )
                task = self.pyscript.functions.create_task(
                    func_call(func, func_name, new_ast_ctx, *args, **kwargs),
                    ast_ctx=new_ast_ctx,
                )
                self.pyscript.functions.task_done_callback_ctx(task, new_ast_ctx)
                return task

            return user_task_create

        ast_funcs = {
            "task.wait_until": wait_until_factory,
            "task.create": user_task_create_factory,
        }
        self.pyscript.functions.register_ast(ast_funcs)

        async def user_task_add_done_callback(task, callback, *args, **kwargs):
            """Implement task.add_done_callback()."""
            ast_ctx = None
            if isinstance(callback, EvalFuncVar):
                ast_ctx = callback.ast_ctx
            self.pyscript.functions.task_add_done_callback(
                task, ast_ctx, callback, *args, **kwargs
            )

        funcs = {
            "task.add_done_callback": user_task_add_done_callback,
            "task.executor": self.user_task_executor,
        }
        self.pyscript.functions.register(funcs)
        try:
            for i in range(1, 8):
                self._dow2int[
                    locale.nl_langinfo(getattr(locale, f"ABDAY_{i}")).lower()
                ] = i
                self._dow2int[
                    locale.nl_langinfo(getattr(locale, f"DAY_{i + 1}")).lower()
                ] = i
        except AttributeError:
            # Win10 Python doesn't have locale.nl_langinfo, so default to English days of week
            dow = [
                "sunday",
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
            ]
            for idx, name in enumerate(dow):
                self._dow2int[name] = idx
                self._dow2int[name[0:3]] = idx

    @property
    def controller(self):
        return self._owner.controller

    @property
    def pyscript(self):
        return self._owner

    async def wait_until(  # pylint: disable=too-many-branches, too-many-statements
        self,
        ast_ctx: AstEval,
        state_trigger=None,
        state_check_now=True,
        time_trigger=None,
        event_trigger=None,
        mqtt_trigger=None,
        timeout=None,
        state_hold=None,
        state_hold_false=None,
        __test_handshake__=None,
    ):
        """Wait for zero or more triggers, until an optional timeout."""
        if (
            state_trigger is None
            and time_trigger is None
            and event_trigger is None
            and mqtt_trigger is None
        ):
            if timeout is not None:
                await asyncio.sleep(timeout)
                return {"trigger_type": "timeout"}
            return {"trigger_type": "none"}
        state_trig_ident = set()
        state_trig_ident_any = set()
        state_trig_eval = None
        event_trig_expr = None
        mqtt_trig_expr = None
        exc = None
        notify_q = asyncio.Queue(0)

        last_state_trig_time = None
        state_trig_waiting = False
        state_trig_notify_info = [None, None]
        state_false_time = None
        check_state_expr_on_start = state_check_now or state_hold_false is not None

        if state_trigger is not None:
            state_trig = []
            if isinstance(state_trigger, str):
                state_trigger = [state_trigger]
            elif isinstance(state_trigger, set):
                state_trigger = list(state_trigger)
            #
            # separate out the entries that are just state var names, which mean trigger
            # on any change (no expr)
            #
            for trig in state_trigger:
                if _STATE_RE.match(trig):
                    state_trig_ident_any.add(trig)
                else:
                    state_trig.append(trig)

            if len(state_trig) > 0:
                if len(state_trig) == 1:
                    state_trig_expr = state_trig[0]
                else:
                    state_trig_expr = f"any([{', '.join(state_trig)}])"
                state_trig_eval = AstEval(
                    f"{ast_ctx.name} state_trigger",
                    ast_ctx.get_global_ctx(),
                    logger_name=ast_ctx.get_logger_name(),
                )
                self.pFunction.install_ast_funcs(state_trig_eval)
                state_trig_eval.parse(state_trig_expr, mode="eval")
                state_trig_ident = await state_trig_eval.get_names()
                exc = state_trig_eval.get_exception_obj()
                if exc is not None:
                    raise exc

            state_trig_ident.update(state_trig_ident_any)
            if check_state_expr_on_start and state_trig_eval:
                #
                # check straight away to see if the condition is met
                #
                new_vars = self.pyscript.states.notify_var_get(state_trig_ident, {})
                state_trig_ok = await state_trig_eval.eval(new_vars)
                exc = state_trig_eval.exception_obj
                if exc is not None:
                    raise exc
                if state_hold_false is not None and not state_check_now:
                    #
                    # if state_trig_ok we wait until it is false;
                    # otherwise we consider now to be the start of the false hold time
                    #
                    state_false_time = None if state_trig_ok else time.monotonic()
                elif state_hold is not None and state_trig_ok:
                    state_trig_waiting = True
                    state_trig_notify_info = [None, {"trigger_type": "state"}]
                    last_state_trig_time = time.monotonic()
                    _LOGGER.debug(
                        f"trigger {ast_ctx.name} wait_until: state trigger immediately true; "
                        + f"now waiting for state_hold of {state_hold} seconds",
                    )
                elif state_trig_ok:
                    return {"trigger_type": "state"}

            _LOGGER.debug(
                f"trigger {ast_ctx.name} wait_until: watching vars {state_trig_ident}",
            )
            if len(state_trig_ident) > 0:
                await self.pyscript.states.notify_add(state_trig_ident, notify_q)
        if event_trigger is not None:
            if isinstance(event_trigger, str):
                event_trigger = [event_trigger]
            if len(event_trigger) > 1:
                event_trig_expr = ast_ctx.global_ctx.create_ast_context(
                    f"{ast_ctx.name} event_trigger",
                    logger_name=ast_ctx.logger_name,
                )
                event_trig_expr.parse(event_trigger[1], mode=ParseMode.EVAL)
                exc = event_trig_expr.exception_obj
                if exc is not None:
                    if len(state_trig_ident) > 0:
                        self.pyscript.states.notify_del(state_trig_ident, notify_q)
                    raise exc
            self.pyscript.events.notify_add(event_trigger[0], notify_q)
        if mqtt_trigger is not None:
            if isinstance(mqtt_trigger, str):
                mqtt_trigger = [mqtt_trigger]
            if len(mqtt_trigger) > 1:
                mqtt_trig_expr = ast_ctx.global_ctx.create_ast_context(
                    f"{ast_ctx.name} mqtt_trigger",
                    logger_name=ast_ctx.logger_name,
                )
                mqtt_trig_expr.parse(mqtt_trigger[1], mode=ParseMode.EVAL)
                exc = mqtt_trig_expr.exception_obj
                if exc is not None:
                    if len(state_trig_ident) > 0:
                        self.pyscript.states.notify_del(state_trig_ident, notify_q)
                    raise exc
            await self.pyscript.mqtt.notify_add(mqtt_trigger[0], notify_q)
        time0 = time.monotonic()

        if __test_handshake__:
            #
            # used for testing to avoid race conditions
            # we use this as a handshake that we are about to
            # listen to the queue
            #
            self.pyscript.states.set(__test_handshake__[0], __test_handshake__[1])

        while True:
            ret = None
            this_timeout = None
            state_trig_timeout = False
            time_next = None
            startup_time: dt.datetime = None
            now = dt.datetime.now()
            if startup_time is None:
                startup_time = now
            if time_trigger is not None:
                time_next = self.timer_trigger_next(time_trigger, now, startup_time)
                _LOGGER.debug(
                    f"trigger {ast_ctx.name} wait_until time_next = {time_next}, now = {now}",
                )
                if time_next is not None:
                    this_timeout = (time_next - now).total_seconds()
            if timeout is not None:
                time_left = time0 + timeout - time.monotonic()
                if time_left <= 0:
                    ret = {"trigger_type": "timeout"}
                    break
                if this_timeout is None or this_timeout > time_left:
                    ret = {"trigger_type": "timeout"}
                    this_timeout = time_left
                    time_next = now + dt.timedelta(seconds=this_timeout)
            if state_trig_waiting:
                time_left = last_state_trig_time + state_hold - time.monotonic()
                if this_timeout is None or time_left < this_timeout:
                    this_timeout = time_left
                    state_trig_timeout = True
                    time_next = now + dt.timedelta(seconds=this_timeout)
            if this_timeout is None:
                if (
                    state_trigger is None
                    and event_trigger is None
                    and mqtt_trigger is None
                ):
                    _LOGGER.debug(
                        f"trigger {ast_ctx.name} wait_until no next time - returning with none",
                    )
                    ret = {"trigger_type": "none"}
                    break
                _LOGGER.debug(f"trigger {ast_ctx.name} wait_until no timeout")
                notify_type, notify_info = await notify_q.get()
            else:
                timeout_occurred = False
                while True:
                    try:
                        this_timeout = max(0, this_timeout)
                        _LOGGER.debug(
                            f"trigger {ast_ctx.name} wait_until {this_timeout:.6g} secs",
                        )
                        notify_type, notify_info = await asyncio.wait_for(
                            notify_q.get(), timeout=this_timeout
                        )
                        state_trig_timeout = False
                    except asyncio.TimeoutError:
                        actual_now = dt.datetime.now()
                        if actual_now < time_next:
                            this_timeout = (time_next - actual_now).total_seconds()
                            # tests/tests_function's simple now() requires us to ignore
                            # timeouts that are up to 1us too early; otherwise wait for
                            # longer until we are sure we are at or past time_next
                            if this_timeout > 1e-6:
                                continue
                        if not state_trig_timeout:
                            if not ret:
                                ret = {"trigger_type": "time"}
                                if time_next is not None:
                                    ret["trigger_time"] = time_next
                            timeout_occurred = True
                    break
                if timeout_occurred:
                    break
            if state_trig_timeout:
                ret = state_trig_notify_info[1]
                state_trig_waiting = False
                break
            if notify_type == "state":  # pylint: disable=too-many-nested-blocks
                if notify_info:
                    new_vars, func_args = notify_info
                else:
                    new_vars, func_args = None, {}

                state_trig_ok = True

                if not _ident_any_values_changed(func_args, state_trig_ident_any):
                    # if var_name not in func_args we are state_check_now
                    if "var_name" in func_args and not _ident_values_changed(
                        func_args, state_trig_ident
                    ):
                        continue

                    if state_trig_eval:
                        state_trig_ok = await state_trig_eval.eval(new_vars)
                        exc = state_trig_eval.exception_obj
                        if exc is not None:
                            break

                        if state_hold_false is not None:
                            if state_false_time is None:
                                if state_trig_ok:
                                    #
                                    # wasn't False, so ignore
                                    #
                                    continue
                                #
                                # first False, so remember when it is
                                #
                                state_false_time = time.monotonic()
                            elif state_trig_ok:
                                too_soon = (
                                    time.monotonic() - state_false_time
                                    < state_hold_false
                                )
                                state_false_time = None
                                if too_soon:
                                    #
                                    # was False but not for long enough, so start over
                                    #
                                    continue

                if state_hold is not None:
                    if state_trig_ok:
                        if not state_trig_waiting:
                            state_trig_waiting = True
                            state_trig_notify_info = notify_info
                            last_state_trig_time = time.monotonic()
                            _LOGGER.debug(
                                f"trigger {notify_type} wait_until: got {ast_ctx.name} trigger; "
                                + f"now waiting for state_hold of {state_hold} seconds",
                                notify_type,
                                ast_ctx.name,
                                state_hold,
                            )
                        else:
                            _LOGGER.debug(
                                f"trigger {notify_type} wait_until: got {ast_ctx.name} trigger; "
                                + f"still waiting for state_hold of {state_hold} seconds",
                            )
                        continue
                    if state_trig_waiting:
                        state_trig_waiting = False
                        _LOGGER.debug(
                            f"trigger {notify_type} wait_until: {ast_ctx.name} trigger now false "
                            + "during state_hold; waiting for new trigger",
                        )
                        continue
                if state_trig_ok:
                    ret = notify_info[1] if notify_info else None
                    break
            elif notify_type == "event":
                if event_trig_expr is None:
                    ret = notify_info
                    break
                event_trig_ok = await event_trig_expr.eval(notify_info)
                exc = event_trig_expr.exception_obj
                if exc is not None:
                    break
                if event_trig_ok:
                    ret = notify_info
                    break
            elif notify_type == "mqtt":
                if mqtt_trig_expr is None:
                    ret = notify_info
                    break
                mqtt_trig_ok = await mqtt_trig_expr.eval(notify_info)
                exc = mqtt_trig_expr.exception_obj
                if exc is not None:
                    break
                if mqtt_trig_ok:
                    ret = notify_info
                    break
            else:
                _LOGGER.error(
                    f"trigger {ast_ctx.name} wait_until got unexpected "
                    + f"queue message {notify_type}",
                )

        if len(state_trig_ident) > 0:
            self.pyscript.states.notify_del(state_trig_ident, notify_q)
        if event_trigger is not None:
            self.pyscript.events.notify_del(event_trigger[0], notify_q)
        if mqtt_trigger is not None:
            self.pyscript.mqtt.notify_del(mqtt_trigger[0], notify_q)
        if exc:
            raise exc
        return ret

    async def user_task_executor(self, func, *args, **kwargs):
        """Implement task.executor()."""
        if asyncio.iscoroutinefunction(func) or not callable(func):
            raise TypeError(f"function {func} is not callable by task.executor")
        if isinstance(func, EvalFuncVar):
            raise TypeError(
                "pyscript functions can't be called from task.executor - "
                + "must be a regular python function"
            )
        return await self.controller.async_add_executor_job(
            ft.partial(func, **kwargs), *args
        )

    def parse_date_time(
        self,
        date_time_str: str,
        day_offset: int,
        now: dt.datetime,
        startup_time: dt.datetime,
    ):
        """Parse a date time string, returning datetime."""
        if day_offset > 0:
            now = now + dt.timedelta(days=day_offset)
        year = now.year
        month = now.month
        day = now.day

        dt_str_orig = dt_str = date_time_str.strip().lower()
        #
        # parse the date
        #
        match0 = re.match(r"0*(\d+)[-/]0*(\d+)(?:[-/]0*(\d+))?", dt_str)
        match1 = re.match(r"(\w+)", dt_str)
        if match0:
            if match0[3]:
                year, month, day = int(match0[1]), int(match0[2]), int(match0[3])
            else:
                month, day = int(match0[1]), int(match0[2])
            day_offset = 0  # explicit date means no offset
            dt_str = dt_str[len(match0.group(0)) :]
        elif match1:
            skip = True
            if match1[1] in self._dow2int:
                dow = self._dow2int[match1[1]]
                if dow >= (now.isoweekday() % 7):
                    day_offset = dow - (now.isoweekday() % 7)
                else:
                    day_offset = 7 + dow - (now.isoweekday() % 7)
            elif match1[1] == "today":
                day_offset = 0
            elif match1[1] == "tomorrow":
                day_offset = 1
            else:
                skip = False
            if skip:
                dt_str = dt_str[len(match1.group(0)) :]
        if day_offset != 0:
            now = dt.datetime(year, month, day) + dt.timedelta(days=day_offset)
            year = now.year
            month = now.month
            day = now.day
        else:
            now = dt.datetime(year, month, day)
        dt_str = dt_str.strip()
        if len(dt_str) == 0:
            return now

        #
        # parse the time
        #
        match0 = re.match(
            r"0*(\d+):0*(\d+)(?::0*(\d*\.?\d+(?:[eE][-+]?\d+)?))?", dt_str
        )
        if match0:
            if match0[3]:
                hour, mins, sec = int(match0[1]), int(match0[2]), float(match0[3])
            else:
                hour, mins, sec = int(match0[1]), int(match0[2]), 0
            dt_str = dt_str[len(match0.group(0)) :]
        elif dt_str.startswith("sunrise") or dt_str.startswith("sunset"):
            location = self.controller.sun.get_astral_location()
            if isinstance(location, tuple):
                # HA core-2021.5.0 included this breaking change:
                # https://github.com/home-assistant/core/pull/48573.
                # As part of the upgrade to astral 2.2, sun.get_astral_location()
                # now returns a tuple including the elevation.
                # We just want the astral.location.Location object.
                location = location[0]
            try:
                if dt_str.startswith("sunrise"):
                    time_sun = location.sunrise(dt.date(year, month, day))
                    dt_str = dt_str[7:]
                else:
                    time_sun = location.sunset(dt.date(year, month, day))
                    dt_str = dt_str[6:]
            except Exception:  # pylint: disable=broad-except
                _LOGGER.warning(f"'{dt_str}' not defined at this latitude")
                # return something in the past so it is ignored
                return now - dt.timedelta(days=100)
            now += time_sun.date() - now.date()
            hour, mins, sec = time_sun.hour, time_sun.minute, time_sun.second
        elif dt_str.startswith("noon"):
            hour, mins, sec = 12, 0, 0
            dt_str = dt_str[4:]
        elif dt_str.startswith("midnight"):
            hour, mins, sec = 0, 0, 0
            dt_str = dt_str[8:]
        elif dt_str.startswith("now") and dt_str_orig == dt_str:
            #
            # "now" means the first time, and only matches if there was no date specification
            #
            hour, mins, sec = 0, 0, 0
            now = startup_time
            dt_str = dt_str[3:]
        else:
            hour, mins, sec = 0, 0, 0
        now += dt.timedelta(seconds=sec + 60 * (mins + 60 * hour))
        #
        # parse the offset
        #
        dt_str = dt_str.strip()
        if len(dt_str) > 0:
            now = now + dt.timedelta(seconds=_parse_time_offset(dt_str))
        return now

    def timer_active_check(
        self, time_spec, now: dt.datetime, startup_time: dt.datetime
    ):
        """Check if the given time matches the time specification."""
        results = {"+": [], "-": []}
        for entry in time_spec if isinstance(time_spec, list) else [time_spec]:
            this_match = False
            negate = False
            active_str = entry.strip()
            if active_str.startswith("not"):
                negate = True
                active_str = active_str.replace("not ", "")

            cron_match = re.match(r"cron\((?P<cron_expr>.*)\)", active_str)
            range_expr = re.match(r"range\(([^,]+),\s?([^,]+)\)", active_str)
            if cron_match:
                if not croniter.is_valid(cron_match.group("cron_expr")):
                    _LOGGER.error(f"Invalid cron expression: {cron_match}")
                    return False

                this_match = croniter.match(cron_match.group("cron_expr"), now)

            elif range_expr:
                try:
                    dt_start, dt_end = range_expr.groups()
                except ValueError as exc:
                    _LOGGER.error(f"Invalid range expression: {exc}")
                    return False

                start = self.parse_date_time(dt_start.strip(), 0, now, startup_time)
                end = self.parse_date_time(dt_end.strip(), 0, start, startup_time)

                if start <= end:
                    this_match = start <= now <= end
                else:  # Over midnight
                    this_match = now >= start or now <= end
            else:
                _LOGGER.error(f"Invalid time_active expression: {active_str}")
                return False

            if negate:
                results["-"].append(not this_match)
            else:
                results["+"].append(this_match)

        # An empty spec, or only neg specs, is True
        result = (any(results["+"]) if results["+"] else True) and all(results["-"])

        return result

    def timer_trigger_next(
        self, time_spec, now: dt.datetime, startup_time: dt.datetime
    ):
        """Return the next trigger time based on the given time and time specification."""
        next_time = None
        if not isinstance(time_spec, list):
            time_spec = [time_spec]
        for spec in time_spec:
            cron_match = re.search(r"cron\((?P<cron_expr>.*)\)", spec)
            match1 = re.split(r"once\((.*)\)", spec)
            match2 = re.split(r"period\(([^,]*),([^,]*)(?:,([^,]*))?\)", spec)
            if cron_match:
                if not croniter.is_valid(cron_match.group("cron_expr")):
                    _LOGGER.error(f"Invalid cron expression: {cron_match}")
                    continue

                val = croniter(
                    cron_match.group("cron_expr"), now, dt.datetime
                ).get_next()
                if next_time is None or val < next_time:
                    next_time = val

            elif len(match1) == 3:
                this_t = self.parse_date_time(match1[1].strip(), 0, now, startup_time)
                day_offset = (now - this_t).days + 1
                if day_offset != 0 and this_t != startup_time:
                    #
                    # Try a day offset (won't make a difference if spec has full date)
                    #
                    this_t = self.parse_date_time(
                        match1[1].strip(), day_offset, now, startup_time
                    )
                startup = now == this_t and now == startup_time
                if (now < this_t or startup) and (
                    next_time is None or this_t < next_time
                ):
                    next_time = this_t

            elif len(match2) == 5:
                start_str, period_str = match2[1].strip(), match2[2].strip()
                start = self.parse_date_time(start_str, 0, now, startup_time)
                period = _parse_time_offset(period_str)
                if period <= 0:
                    _LOGGER.error(
                        f"Invalid non-positive period {period} in period(): {time_spec}",
                    )
                    continue

                if match2[3] is None:
                    startup = now == start and now == startup_time
                    if (now < start or startup) and (
                        next_time is None or start < next_time
                    ):
                        next_time = start
                    if now >= start and not startup:
                        secs = period * (
                            1.0 + math.floor((now - start).total_seconds() / period)
                        )
                        this_t = start + dt.timedelta(seconds=secs)
                        if now < this_t and (next_time is None or this_t < next_time):
                            next_time = this_t
                    continue
                end_str = match2[3].strip()
                end = self.parse_date_time(end_str, 0, now, startup_time)
                end_offset = 1 if end < start else 0
                for day in [-1, 0, 1]:
                    start = self.parse_date_time(start_str, day, now, startup_time)
                    end = self.parse_date_time(
                        end_str, day + end_offset, now, startup_time
                    )
                    if now < start or (now == start and now == startup_time):
                        if next_time is None or start < next_time:
                            next_time = start
                        break
                    secs = period * (
                        1.0 + math.floor((now - start).total_seconds() / period)
                    )
                    this_t = start + dt.timedelta(seconds=secs)
                    if start <= this_t <= end:
                        if next_time is None or this_t < next_time:
                            next_time = this_t
                        break

            else:
                test = self.parse_date_time(spec, 0, now, startup_time)
                if test is not None:
                    if test < now:
                        next_time = self.parse_date_time(spec, 1, now, startup_time)
                    else:
                        next_time = test
                else:
                    _LOGGER.warning(f"Can't parse {spec} in time_trigger check")
        return next_time


def _ident_any_values_changed(func_args, ident: set):
    """Check for any changes to state or attributes on ident vars."""
    var_name = func_args.get("var_name", None)

    if var_name is None:
        return False
    value = func_args["value"]
    old_value = func_args["old_value"]

    for check_var in ident:  # pylint: disable=too-many-nested-blocks
        if check_var == var_name and old_value != value:
            return True

        if check_var.startswith(f"{var_name}."):
            var_pieces = check_var.split(".")
            if len(var_pieces) == 3 and f"{var_pieces[0]}.{var_pieces[1]}" == var_name:
                if var_pieces[2] == "*":
                    # catch all has been requested, check all attributes for change
                    all_attrs = set()
                    if value is not None:
                        all_attrs |= set(value.__dict__.keys())
                    if old_value is not None:
                        all_attrs |= set(old_value.__dict__.keys())
                    for attr in all_attrs - _STATE_VIRTUAL_ATTRS:
                        if getattr(value, attr, None) != getattr(old_value, attr, None):
                            return True
                elif getattr(value, var_pieces[2], None) != getattr(
                    old_value, var_pieces[2], None
                ):
                    return True

    return False


def _ident_values_changed(func_args, ident: set):
    """Check for changes to state or attributes on ident vars."""
    var_name = func_args.get("var_name", None)

    if var_name is None:
        return False
    value = func_args["value"]
    old_value = func_args["old_value"]

    for check_var in ident:
        var_pieces = check_var.split(".")
        if len(var_pieces) < 2 or len(var_pieces) > 3:
            continue
        var_root = f"{var_pieces[0]}.{var_pieces[1]}"
        if var_root == var_name and (len(var_pieces) == 2 or var_pieces[2] == "old"):
            if value != old_value:
                return True
        elif len(var_pieces) == 3 and var_root == var_name:
            if getattr(value, var_pieces[2], None) != getattr(
                old_value, var_pieces[2], None
            ):
                return True

    return False


def _parse_time_offset(offset_str):
    """Parse a time offset."""
    match = re.split(r"([-+]?\s*\d*\.?\d+(?:[eE][-+]?\d+)?)\s*(\w*)", offset_str)
    scale = 1
    value = 0
    if len(match) == 4:
        value = float(match[1].replace(" ", ""))
        if match[2] in {"m", "min", "mins", "minute", "minutes"}:
            scale = 60
        elif match[2] in {"h", "hr", "hour", "hours"}:
            scale = 60 * 60
        elif match[2] in {"d", "day", "days"}:
            scale = 60 * 60 * 24
        elif match[2] in {"w", "week", "weeks"}:
            scale = 60 * 60 * 24 * 7
        elif match[2] not in {"", "s", "sec", "second", "seconds"}:
            _LOGGER.error(f"can't parse time offset {offset_str}")
    else:
        _LOGGER.error(f"can't parse time offset {offset_str}")
    return value * scale
