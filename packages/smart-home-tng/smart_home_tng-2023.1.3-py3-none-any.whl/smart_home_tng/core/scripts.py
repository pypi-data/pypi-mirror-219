"""
Core components of Smart Home - The Next Generation.

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
"""

import asyncio
import collections.abc
import contextlib
import contextvars
import copy
import datetime as dt
import functools
import itertools
import logging
import types
import typing

import async_timeout
import voluptuous as vol

from . import helpers
from .action_condition_platform import ActionConditionPlatform
from .action_platform import ActionPlatform
from .callback import callback
from .callback_type import CallbackType
from .condition_checker_type import ConditionCheckerType
from .condition_error import ConditionError
from .config_type import ConfigType
from .config_validation import ConfigValidation as cv
from .const import Const
from .context import Context
from .event import Event
from .integration_not_found import IntegrationNotFound
from .invalid_device_automation_config import InvalidDeviceAutomationConfig
from .invalid_entity_format_error import InvalidEntityFormatError
from .no_entity_specified_error import NoEntitySpecifiedError
from .platform import Platform
from .script_condition import ScriptCondition
from .script_variables import ScriptVariables
from .service import Service
from .service_not_found import ServiceNotFound
from .smart_home_controller_component import SmartHomeControllerComponent
from .smart_home_controller_error import SmartHomeControllerError
from .smart_home_controller_job import SmartHomeControllerJob
from .template import Template
from .template_error import TemplateError
from .template_vars_type import TemplateVarsType
from .trace import Trace
from .trigger_data import TriggerData
from .trigger_info import TriggerInfo
from .trigger_platform import TriggerPlatform
from .unauthorized import Unauthorized

_PLATFORM_ALIASES: typing.Final = {
    "device_automation": ("device",),
    "homeassistant": ("event", "numeric_state", "state", "time_pattern", "time"),
}


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_ScriptRunT = typing.TypeVar("_ScriptRunT", bound="_ScriptRun")


class _Const:
    SCRIPT_MODE_PARALLEL: typing.Final = "parallel"
    SCRIPT_MODE_QUEUED: typing.Final = "queued"
    SCRIPT_MODE_RESTART: typing.Final = "restart"
    SCRIPT_MODE_SINGLE: typing.Final = "single"
    SCRIPT_MODE_CHOICES: typing.Final = [
        SCRIPT_MODE_PARALLEL,
        SCRIPT_MODE_QUEUED,
        SCRIPT_MODE_RESTART,
        SCRIPT_MODE_SINGLE,
    ]
    DEFAULT_SCRIPT_MODE: typing.Final = SCRIPT_MODE_SINGLE

    CONF_MAX: typing.Final = "max"
    DEFAULT_MAX: typing.Final = 10

    CONF_MAX_EXCEEDED: typing.Final = "max_exceeded"
    DEFAULT_MAX_EXCEEDED: typing.Final = "WARNING"

    ATTR_CUR: typing.Final = "current"
    ATTR_MAX: typing.Final = "max"

    DATA_SCRIPTS: typing.Final = "helpers.script"
    DATA_SCRIPT_BREAKPOINTS: typing.Final = "helpers.script.breakpoints"
    DATA_NEW_SCRIPT_RUNS_NOT_ALLOWED: typing.Final = "helpers.script.not_allowed"
    RUN_ID_ANY: typing.Final = "*"
    NODE_ANY: typing.Final = "*"
    # Max length of a trace node for repeated actions
    ACTION_TRACE_NODE_MAX_LEN: typing.Final = 20

    SCRIPT_BREAKPOINT_HIT: typing.Final = "script.breakpoint_hit"
    SCRIPT_DEBUG_CONTINUE_STOP: typing.Final = "script.debug_continue_stop_{}_{}"
    SCRIPT_DEBUG_CONTINUE_ALL: typing.Final = "script.debug_continue_all"


_LOGGER: typing.Final = logging.getLogger(__name__)

_MAX_EXCEEDED_CHOICES: typing.Final = list(Const.LOGSEVERITY) + ["SILENT"]
_LOG_EXCEPTION: typing.Final = logging.ERROR + 1
_TIMEOUT_MSG: typing.Final = "Timeout reached, abort script."

_SHUTDOWN_MAX_WAIT: typing.Final = 60

_VarsType: typing.TypeAlias = typing.Union[
    dict[str, typing.Any], types.MappingProxyType
]


_SCRIPT_STACK_CV: typing.Final[
    contextvars.ContextVar[list[int]]
] = contextvars.ContextVar("script_stack", default=None)


def _action_trace_append(variables, path):
    """Append a TraceElement to trace[path]."""
    trace_element = Trace.create_element(variables, path)
    Trace.append_element(trace_element, _Const.ACTION_TRACE_NODE_MAX_LEN)
    return trace_element


@contextlib.asynccontextmanager
async def _trace_action(shc, _script_run, stop, variables):
    """Trace action execution."""
    path = Trace.get_path()
    trace_element = _action_trace_append(variables, path)
    Trace.stack_push(trace_element)

    trace_id = Trace.get_id()
    if trace_id:
        key = trace_id[0]
        run_id = trace_id[1]
        # pylint: disable=protected-access
        breakpoints = _Script._breakpoints
        if key in breakpoints and (
            (
                run_id in breakpoints[key]
                and (
                    path in breakpoints[key][run_id]
                    or _Const.NODE_ANY in breakpoints[key][run_id]
                )
            )
            or (
                _Const.RUN_ID_ANY in breakpoints[key]
                and (
                    path in breakpoints[key][_Const.RUN_ID_ANY]
                    or _Const.NODE_ANY in breakpoints[key][_Const.RUN_ID_ANY]
                )
            )
        ):
            shc.dispatcher.async_send(_Const.SCRIPT_BREAKPOINT_HIT, key, run_id, path)

            done = asyncio.Event()

            @callback
            def async_continue_stop(command=None):
                if command == "stop":
                    stop.set()
                done.set()

            signal = _Const.SCRIPT_DEBUG_CONTINUE_STOP.format(key, run_id)
            remove_signal1 = shc.dispatcher.async_connect(signal, async_continue_stop)
            remove_signal2 = shc.async_dispatcher_connect(
                _Const.SCRIPT_DEBUG_CONTINUE_ALL, async_continue_stop
            )

            tasks = [shc.async_create_task(flag.wait()) for flag in (stop, done)]
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in tasks:
                task.cancel()
            remove_signal1()
            remove_signal2()

    try:
        yield trace_element
    except _AbortScript as ex:
        trace_element.set_error(ex.__cause__ or ex)
        raise ex
    except _ConditionFail as ex:
        # Clear errors which may have been set when evaluating the condition
        trace_element.set_error(None)
        raise ex
    except _StopScript as ex:
        raise ex
    except Exception as ex:
        trace_element.set_error(ex)
        raise ex
    finally:
        Trace.stack_pop()


_STATIC_VALIDATION_ACTION_TYPES: typing.Final = (
    cv.SCRIPT_ACTION_CALL_SERVICE,
    cv.SCRIPT_ACTION_DELAY,
    cv.SCRIPT_ACTION_WAIT_TEMPLATE,
    cv.SCRIPT_ACTION_FIRE_EVENT,
    cv.SCRIPT_ACTION_ACTIVATE_SCENE,
    cv.SCRIPT_ACTION_VARIABLES,
    cv.SCRIPT_ACTION_STOP,
)


class _HaltScript(Exception):
    """Throw if script needs to stop executing."""


class _AbortScript(_HaltScript):
    """Throw if script needs to abort because of an unexpected error."""


class _ConditionFail(_HaltScript):
    """Throw if script needs to stop because a condition evaluated to False."""


class _StopScript(_HaltScript):
    """Throw if script needs to stop."""


class _Script:
    """Representation of a script."""

    _all_scripts: dict[str, typing.Any] = None
    _breakpoints: dict = None
    _new_scripts_not_allowed: bool = False

    def __init__(
        self,
        shc: SmartHomeController,
        sequence: collections.abc.Sequence[dict[str, typing.Any]],
        name: str,
        domain: str,
        *,
        # Used in "Running <running_description>" log message
        change_listener: collections.abc.Callable[..., typing.Any] = None,
        copy_variables: bool = False,
        log_exceptions: bool = True,
        logger: logging.Logger = None,
        max_exceeded: str = _Const.DEFAULT_MAX_EXCEEDED,
        max_runs: int = _Const.DEFAULT_MAX,
        running_description: str = None,
        script_mode: str = _Const.DEFAULT_SCRIPT_MODE,
        top_level: bool = True,
        variables: ScriptVariables = None,
    ) -> None:
        """Initialize the script."""
        if _Script._all_scripts is None:
            _Script._all_scripts = []
            shc.bus.async_listen_once(
                Const.EVENT_SHC_STOP,
                self._async_stop_scripts_at_shutdown,
            )
        self._top_level = top_level
        if top_level:
            _Script._all_scripts.append(
                {"instance": self, "started_before_shutdown": not shc.is_stopping}
            )
        if _Script._breakpoints is None:
            _Script._breakpoints = {}

        self._shc = shc
        self._sequence = sequence
        Template.attach(shc, self._sequence)
        self._name = name
        self._domain = domain
        self._running_description = running_description or f"{domain} script"
        self._change_listener = change_listener
        self._change_listener_job = (
            None if change_listener is None else SmartHomeControllerJob(change_listener)
        )

        self._script_mode = script_mode
        self._set_logger(logger)
        self._log_exceptions = log_exceptions

        self._last_action = None
        self._last_triggered: dt.datetime = None

        self._runs: list[_ScriptRun] = []
        self._max_runs = max_runs
        self._max_exceeded = max_exceeded
        if script_mode == _Const.SCRIPT_MODE_QUEUED:
            self._queue_lck = asyncio.Lock()
        self._config_cache: dict[set[tuple], collections.abc.Callable[..., bool]] = {}
        self._repeat_script: dict[int, _Script] = {}
        self._choose_data: dict[int, _ChooseData] = {}
        self._if_data: dict[int, _IfData] = {}
        self._parallel_scripts: dict[int, list[_Script]] = {}
        self._referenced_entities: set[str] = None
        self._referenced_devices: set[str] = None
        self._referenced_areas: set[str] = None
        self._variables = variables
        self._variables_dynamic = Template.is_complex(variables)
        if self._variables_dynamic:
            Template.attach(shc, variables)
        self._copy_variables_on_run = copy_variables

    @property
    def last_triggered(self) -> dt.datetime:
        return self._last_triggered

    @last_triggered.setter
    def last_triggered(self, value: dt.datetime):
        if self._last_triggered is None:
            self._last_triggered = value

    @property
    def script_mode(self) -> str:
        return self._script_mode

    @property
    def max_runs(self) -> int:
        return self._max_runs

    @staticmethod
    def clear_breakpoints():
        _Script._breakpoints = {}

    @staticmethod
    def clear_breakpoint(key, run_id, node):
        breakpoints = _Script._breakpoints
        if key not in breakpoints or run_id not in breakpoints[key]:
            return
        breakpoints[key][run_id].discard(node)

    @staticmethod
    def set_breakpoint(key, run_id, node):
        breakpoints = _Script._breakpoints
        if key not in breakpoints:
            breakpoints[key] = {}
        if run_id not in breakpoints[key]:
            breakpoints[key][run_id] = set()
        breakpoints[key][run_id].add(node)

    @staticmethod
    def list_breakpoints():
        breakpoints = _Script._breakpoints

        return [
            {"key": key, "run_id": run_id, "node": node}
            for key in breakpoints.items()
            for run_id in breakpoints[key]
            for node in breakpoints[key][run_id]
        ]

    @property
    def name(self) -> str:
        return self._name

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def last_action(self):
        return self._last_action

    @property
    def top_level(self) -> bool:
        return self._top_level

    @property
    def sequence(self):
        if self._sequence is None:
            return None
        return iter(self._sequence)

    @property
    def running_description(self) -> str:
        return self._running_description

    @property
    def change_listener(self) -> collections.abc.Callable[..., typing.Any]:
        """Return the change_listener."""
        return self._change_listener

    @change_listener.setter
    def change_listener(
        self, change_listener: collections.abc.Callable[..., typing.Any]
    ) -> None:
        """Update the change_listener."""
        self._change_listener = change_listener
        if (
            self._change_listener_job is None
            or change_listener != self._change_listener_job.target
        ):
            self._change_listener_job = SmartHomeControllerJob(change_listener)

    def _set_logger(self, logger: logging.Logger = None) -> None:
        if logger:
            self._logger = logger
        else:
            self._logger = logging.getLogger(f"{__name__}.{helpers.slugify(self.name)}")

    def update_logger(self, logger: logging.Logger = None) -> None:
        """Update logger."""
        self._set_logger(logger)
        for script in self._repeat_script.values():
            script.update_logger(self._logger)
        for parallel_scripts in self._parallel_scripts.values():
            for parallel_script in parallel_scripts:
                parallel_script.update_logger(self._logger)
        for choose_data in self._choose_data.values():
            for _, script in choose_data["choices"]:
                script.update_logger(self._logger)
            if choose_data["default"] is not None:
                choose_data["default"].update_logger(self._logger)
        for if_data in self._if_data.values():
            if_data["if_then"].update_logger(self._logger)
            if if_data["if_else"] is not None:
                if_data["if_else"].update_logger(self._logger)

    def _changed(self) -> None:
        if self._change_listener_job:
            self._shc.async_run_shc_job(self._change_listener_job)

    @callback
    def _chain_change_listener(self, sub_script) -> None:
        if sub_script.is_running:
            self._last_action = sub_script.last_action
            self._changed()

    @property
    def is_running(self) -> bool:
        """Return true if script is on."""
        return len(self._runs) > 0

    @property
    def runs(self) -> int:
        """Return the number of current runs."""
        return len(self._runs)

    @property
    def supports_max(self) -> bool:
        """Return true if the current mode support max."""
        return self._script_mode in (
            _Const.SCRIPT_MODE_PARALLEL,
            _Const.SCRIPT_MODE_QUEUED,
        )

    @property
    def referenced_areas(self):
        """Return a set of referenced areas."""
        if self._referenced_areas is not None:
            return self._referenced_areas

        self._referenced_areas: set[str] = set()
        _Script._find_referenced_areas(self._referenced_areas, self._sequence)
        return self._referenced_areas

    @staticmethod
    def _find_referenced_areas(referenced, sequence):
        for step in sequence:
            action = cv.determine_script_action(step)

            if action == cv.SCRIPT_ACTION_CALL_SERVICE:
                for data in (
                    step.get(Const.CONF_TARGET),
                    step.get(Const.CONF_SERVICE_DATA),
                    step.get(Const.CONF_SERVICE_DATA_TEMPLATE),
                ):
                    _referenced_extract_ids(data, Const.ATTR_AREA_ID, referenced)

            elif action == cv.SCRIPT_ACTION_CHOOSE:
                for choice in step[Const.CONF_CHOOSE]:
                    _Script._find_referenced_areas(
                        referenced, choice[Const.CONF_SEQUENCE]
                    )
                if Const.CONF_DEFAULT in step:
                    _Script._find_referenced_areas(referenced, step[Const.CONF_DEFAULT])

            elif action == cv.SCRIPT_ACTION_IF:
                _Script._find_referenced_areas(referenced, step[Const.CONF_THEN])
                if Const.CONF_ELSE in step:
                    _Script._find_referenced_areas(referenced, step[Const.CONF_ELSE])

            elif action == cv.SCRIPT_ACTION_PARALLEL:
                for script in step[Const.CONF_PARALLEL]:
                    _Script._find_referenced_areas(
                        referenced, script[Const.CONF_SEQUENCE]
                    )

    @property
    def referenced_devices(self):
        """Return a set of referenced devices."""
        if self._referenced_devices is not None:
            return self._referenced_devices

        self._referenced_devices: set[str] = set()
        _Script._find_referenced_devices(self._referenced_devices, self._sequence)
        return self._referenced_devices

    @staticmethod
    def _find_referenced_devices(referenced, sequence):
        for step in sequence:
            action = cv.determine_script_action(step)

            if action == cv.SCRIPT_ACTION_CALL_SERVICE:
                for data in (
                    step.get(Const.CONF_TARGET),
                    step.get(Const.CONF_SERVICE_DATA),
                    step.get(Const.CONF_SERVICE_DATA_TEMPLATE),
                ):
                    _referenced_extract_ids(data, Const.ATTR_DEVICE_ID, referenced)

            elif action == cv.SCRIPT_ACTION_CHECK_CONDITION:
                referenced |= ScriptCondition.async_extract_devices(step)

            elif action == cv.SCRIPT_ACTION_DEVICE_AUTOMATION:
                referenced.add(step[Const.CONF_DEVICE_ID])

            elif action == cv.SCRIPT_ACTION_CHOOSE:
                for choice in step[Const.CONF_CHOOSE]:
                    for cond in choice[Const.CONF_CONDITIONS]:
                        referenced |= ScriptCondition.async_extract_devices(cond)
                    _Script._find_referenced_devices(
                        referenced, choice[Const.CONF_SEQUENCE]
                    )
                if Const.CONF_DEFAULT in step:
                    _Script._find_referenced_devices(
                        referenced, step[Const.CONF_DEFAULT]
                    )

            elif action == cv.SCRIPT_ACTION_IF:
                for cond in step[Const.CONF_IF]:
                    referenced |= ScriptCondition.async_extract_devices(cond)
                _Script._find_referenced_devices(referenced, step[Const.CONF_THEN])
                if Const.CONF_ELSE in step:
                    _Script._find_referenced_devices(referenced, step[Const.CONF_ELSE])

            elif action == cv.SCRIPT_ACTION_PARALLEL:
                for script in step[Const.CONF_PARALLEL]:
                    _Script._find_referenced_devices(
                        referenced, script[Const.CONF_SEQUENCE]
                    )

    @property
    def referenced_entities(self):
        """Return a set of referenced entities."""
        if self._referenced_entities is not None:
            return self._referenced_entities

        self._referenced_entities: set[str] = set()
        _Script._find_referenced_entities(self._referenced_entities, self._sequence)
        return self._referenced_entities

    @staticmethod
    def _find_referenced_entities(referenced, sequence):
        for step in sequence:
            action = cv.determine_script_action(step)

            if action == cv.SCRIPT_ACTION_CALL_SERVICE:
                for data in (
                    step,
                    step.get(Const.CONF_TARGET),
                    step.get(Const.CONF_SERVICE_DATA),
                    step.get(Const.CONF_SERVICE_DATA_TEMPLATE),
                ):
                    _referenced_extract_ids(data, Const.ATTR_ENTITY_ID, referenced)

            elif action == cv.SCRIPT_ACTION_CHECK_CONDITION:
                referenced |= ScriptCondition.async_extract_entities(step)

            elif action == cv.SCRIPT_ACTION_ACTIVATE_SCENE:
                referenced.add(step[Const.CONF_SCENE])

            elif action == cv.SCRIPT_ACTION_CHOOSE:
                for choice in step[Const.CONF_CHOOSE]:
                    for cond in choice[Const.CONF_CONDITIONS]:
                        referenced |= ScriptCondition.async_extract_entities(cond)
                    _Script._find_referenced_entities(
                        referenced, choice[Const.CONF_SEQUENCE]
                    )
                if Const.CONF_DEFAULT in step:
                    _Script._find_referenced_entities(
                        referenced, step[Const.CONF_DEFAULT]
                    )

            elif action == cv.SCRIPT_ACTION_IF:
                for cond in step[Const.CONF_IF]:
                    referenced |= ScriptCondition.async_extract_entities(cond)
                _Script._find_referenced_entities(referenced, step[Const.CONF_THEN])
                if Const.CONF_ELSE in step:
                    _Script._find_referenced_entities(referenced, step[Const.CONF_ELSE])

            elif action == cv.SCRIPT_ACTION_PARALLEL:
                for script in step[Const.CONF_PARALLEL]:
                    _Script._find_referenced_entities(
                        referenced, script[Const.CONF_SEQUENCE]
                    )

    def run(self, variables: _VarsType = None, context: Context = None) -> None:
        """Run script."""
        self._shc.run_coroutine_threadsafe(self.async_run(variables, context)).result()

    async def async_run(
        self,
        run_variables: _VarsType = None,
        context: Context = None,
        started_action: collections.abc.Callable[..., typing.Any] = None,
    ) -> None:
        """Run script."""
        if context is None:
            self._log(
                "Running script requires passing in a context", level=logging.WARNING
            )
            context = Context()

        # Prevent spawning new script runs when Home Assistant is shutting down
        if _Script._new_scripts_not_allowed:
            self._log("Smart Home Controller is shutting down, starting script blocked")
            return

        # Prevent spawning new script runs if not allowed by script mode
        if self.is_running:
            if self._script_mode == _Const.SCRIPT_MODE_SINGLE:
                if self._max_exceeded != "SILENT":
                    self._log(
                        "Already running", level=Const.LOGSEVERITY[self._max_exceeded]
                    )
                Trace.set_stop_reason("failed_single")
                return
            if (
                self._script_mode != _Const.SCRIPT_MODE_RESTART
                and self.runs == self._max_runs
            ):
                if self._max_exceeded != "SILENT":
                    self._log(
                        "Maximum number of runs exceeded",
                        level=Const.LOGSEVERITY[self._max_exceeded],
                    )
                Trace.set_stop_reason("failed_max_runs")
                return

        # If this is a top level Script then make a copy of the variables in case they
        # are read-only, but more importantly, so as not to leak any variables created
        # during the run back to the caller.
        if self._top_level:
            if self._variables:
                try:
                    variables = self._variables.async_render(
                        self._shc,
                        run_variables,
                    )
                except TemplateError as err:
                    self._log(f"Error rendering variables: {err}", level=logging.ERROR)
                    raise
            elif run_variables:
                variables = dict(run_variables)
            else:
                variables = {}

            variables["context"] = context
        else:
            if self._copy_variables_on_run:
                variables = typing.cast(dict, copy.copy(run_variables))
            else:
                variables = typing.cast(dict, run_variables)

        # Prevent non-allowed recursive calls which will cause deadlocks when we try to
        # stop (restart) or wait for (queued) our own script run.
        script_stack = _SCRIPT_STACK_CV.get()
        if (
            self._script_mode in (_Const.SCRIPT_MODE_RESTART, _Const.SCRIPT_MODE_QUEUED)
            and script_stack is not None
            and id(self) in script_stack
        ):
            Trace.set_stop_reason("disallowed_recursion_detected")
            self._log("Disallowed recursion detected", level=logging.WARNING)
            return

        if self._script_mode != _Const.SCRIPT_MODE_QUEUED:
            cls = _ScriptRun
        else:
            cls = _QueuedScriptRun
        run = cls(
            self._shc, self, typing.cast(dict, variables), context, self._log_exceptions
        )
        self._runs.append(run)
        if self._script_mode == _Const.SCRIPT_MODE_RESTART:
            # When script mode is SCRIPT_MODE_RESTART, first add the new run and then
            # stop any other runs. If we stop other runs first, self.is_running will
            # return false after the other script runs were stopped until our task
            # resumes running.
            self._log("Restarting")
            await self.async_stop(update_state=False, spare=run)

        if started_action:
            self._shc.async_run_job(started_action)
        self._last_triggered = helpers.utcnow()
        self._changed()

        try:
            await asyncio.shield(run.async_run())
        except asyncio.CancelledError:
            await run.async_stop()
            self._changed()
            raise

    async def _async_stop(self, aws: list[asyncio.Task], update_state: bool) -> None:
        await asyncio.wait(aws)
        if update_state:
            self._changed()

    async def async_stop(
        self, update_state: bool = True, spare: _ScriptRunT = None
    ) -> None:
        """Stop running script."""
        # Collect a a list of script runs to stop. This must be done before calling
        # asyncio.shield as asyncio.shield yields to the event loop, which would cause
        # us to wait for script runs added after the call to async_stop.
        aws = [
            asyncio.create_task(run.async_stop()) for run in self._runs if run != spare
        ]
        if not aws:
            return
        await asyncio.shield(self._async_stop(aws, update_state))

    async def _async_get_condition(self, config):
        if isinstance(config, Template):
            config_cache_key = config.template
        else:
            config_cache_key = frozenset((k, str(v)) for k, v in config.items())
        if not (cond := self._config_cache.get(config_cache_key)):
            cond_prot = ScriptCondition.get_action_condition_protocol(self._shc)
            cond = await cond_prot.async_condition_from_config(config)
            self._config_cache[config_cache_key] = cond
        return cond

    def _prep_repeat_script(self, step: int):
        action = self.sequence[step]
        step_name = action.get(Const.CONF_ALIAS, f"Repeat at step {step+1}")
        sub_script = _Script(
            self._shc,
            action[Const.CONF_REPEAT][Const.CONF_SEQUENCE],
            f"{self.name}: {step_name}",
            self.domain,
            running_description=self._running_description,
            script_mode=_Const.SCRIPT_MODE_PARALLEL,
            max_runs=self._max_runs,
            logger=self._logger,
            top_level=False,
        )
        sub_script.change_listener = functools.partial(
            self._chain_change_listener, sub_script
        )
        return sub_script

    def _get_repeat_script(self, step: int):
        if not (sub_script := self._repeat_script.get(step)):
            sub_script = self._prep_repeat_script(step)
            self._repeat_script[step] = sub_script
        return sub_script

    async def _async_prep_choose_data(self, step: int):
        action = self._sequence[step]
        step_name = action.get(Const.CONF_ALIAS, f"Choose at step {step+1}")
        choices = []
        for idx, choice in enumerate(action[Const.CONF_CHOOSE], start=1):
            conditions = [
                await self._async_get_condition(config)
                for config in choice.get(Const.CONF_CONDITIONS, [])
            ]
            choice_name = choice.get(Const.CONF_ALIAS, f"choice {idx}")
            sub_script = _Script(
                self._shc,
                choice[Const.CONF_SEQUENCE],
                f"{self.name}: {step_name}: {choice_name}",
                self.domain,
                running_description=self._running_description,
                script_mode=_Const.SCRIPT_MODE_PARALLEL,
                max_runs=self._max_runs,
                logger=self._logger,
                top_level=False,
            )
            sub_script.change_listener = functools.partial(
                self._chain_change_listener, sub_script
            )
            choices.append((conditions, sub_script))

        default_script: _Script = None
        if Const.CONF_DEFAULT in action:
            default_script = _Script(
                self._shc,
                action[Const.CONF_DEFAULT],
                f"{self.name}: {step_name}: default",
                self.domain,
                running_description=self._running_description,
                script_mode=_Const.SCRIPT_MODE_PARALLEL,
                max_runs=self._max_runs,
                logger=self._logger,
                top_level=False,
            )
            default_script.change_listener = functools.partial(
                self._chain_change_listener, default_script
            )
        else:
            default_script = None

        result: _ChooseData = {"choices": choices, "default": default_script}
        return result

    async def _async_get_choose_data(self, step: int):
        if not (choose_data := self._choose_data.get(step)):
            choose_data = await self._async_prep_choose_data(step)
            self._choose_data[step] = choose_data
        return choose_data

    async def _async_prep_if_data(self, step: int):
        """Prepare data for an if statement."""
        action = self._sequence[step]
        step_name = action.get(Const.CONF_ALIAS, f"If at step {step+1}")

        conditions = [
            await self._async_get_condition(config) for config in action[Const.CONF_IF]
        ]

        then_script = _Script(
            self._shc,
            action[Const.CONF_THEN],
            f"{self.name}: {step_name}",
            self.domain,
            running_description=self._running_description,
            script_mode=_Const.SCRIPT_MODE_PARALLEL,
            max_runs=self._max_runs,
            logger=self._logger,
            top_level=False,
        )
        then_script.change_listener = functools.partial(
            self._chain_change_listener, then_script
        )

        if Const.CONF_ELSE in action:
            else_script = _Script(
                self._shc,
                action[Const.CONF_ELSE],
                f"{self.name}: {step_name}",
                self.domain,
                running_description=self._running_description,
                script_mode=_Const.SCRIPT_MODE_PARALLEL,
                max_runs=self._max_runs,
                logger=self._logger,
                top_level=False,
            )
            else_script.change_listener = functools.partial(
                self._chain_change_listener, else_script
            )
        else:
            else_script = None

        return _IfData(
            if_conditions=conditions,
            if_then=then_script,
            if_else=else_script,
        )

    async def _async_get_if_data(self, step: int):
        if not (if_data := self._if_data.get(step)):
            if_data = await self._async_prep_if_data(step)
            self._if_data[step] = if_data
        return if_data

    async def _async_prep_parallel_scripts(self, step: int):
        action = self._sequence[step]
        step_name = action.get(Const.CONF_ALIAS, f"Parallel action at step {step+1}")
        parallel_scripts: list[_Script] = []
        for idx, parallel_script in enumerate(action[Const.CONF_PARALLEL], start=1):
            parallel_name = parallel_script.get(Const.CONF_ALIAS, f"parallel {idx}")
            parallel_script = _Script(
                self._shc,
                parallel_script[Const.CONF_SEQUENCE],
                f"{self.name}: {step_name}: {parallel_name}",
                self.domain,
                running_description=self._running_description,
                script_mode=_Const.SCRIPT_MODE_PARALLEL,
                max_runs=self._max_runs,
                logger=self._logger,
                top_level=False,
                copy_variables=True,
            )
            parallel_script.change_listener = functools.partial(
                self._chain_change_listener, parallel_script
            )
            parallel_scripts.append(parallel_script)

        return parallel_scripts

    async def _async_get_parallel_scripts(self, step: int):
        if not (parallel_scripts := self._parallel_scripts.get(step)):
            parallel_scripts = await self._async_prep_parallel_scripts(step)
            self._parallel_scripts[step] = parallel_scripts
        return parallel_scripts

    def _log(
        self,
        msg: str,
        *args: typing.Any,
        level: int = logging.INFO,
        **kwargs: typing.Any,
    ) -> None:
        msg = f"%s: {msg}"
        args = (self.name, *args)

        if level == _LOG_EXCEPTION:
            self._logger.exception(msg, *args, **kwargs)
        else:
            self._logger.log(level, msg, *args, **kwargs)

    async def _async_stop_scripts_after_shutdown(self, _now: dt.datetime):
        """Stop running Script objects started after shutdown."""
        _Script._new_scripts_not_allowed = True
        running_scripts = [
            script for script in _Script._all_scripts if script["instance"].is_running
        ]
        if running_scripts:
            names = ", ".join([script["instance"].name for script in running_scripts])
            _LOGGER.warning(
                f"Stopping scripts running too long after shutdown: {names}"
            )
            await asyncio.gather(
                *(
                    script["instance"].async_stop(update_state=False)
                    for script in running_scripts
                )
            )

    async def _async_stop_scripts_at_shutdown(self, _event: Event):
        """Stop running Script objects started before shutdown."""
        shc = self._shc
        shc.tracker.async_call_later(
            _SHUTDOWN_MAX_WAIT,
            self._async_stop_scripts_after_shutdown,
        )

        running_scripts = [
            script
            for script in _Script._all_scripts
            if script["instance"].is_running and script["started_before_shutdown"]
        ]
        if running_scripts:
            names = ", ".join([script["instance"].name for script in running_scripts])
            _LOGGER.debug(f"Stopping scripts running at shutdown: {names}")
            await asyncio.gather(
                *(script["instance"].async_stop() for script in running_scripts)
            )


class Scripts(ActionPlatform):
    """Script helpers."""

    # pylint: disable=invalid-name
    Const: typing.TypeAlias = _Const
    Script: typing.TypeAlias = _Script
    _protocol_helper: typing.Any = None

    def __init__(self, shc: SmartHomeController):
        super().__init__()
        self._shc = shc

    @property
    def action_schema(self) -> vol.Schema:
        return None

    @staticmethod
    def get_action_protocol(shc: SmartHomeController) -> ActionPlatform:
        if Scripts._protocol_helper is None:
            Scripts._protocol_helper = Scripts(shc)
        return Scripts._protocol_helper

    @staticmethod
    def make_script_schema(schema, default_script_mode, extra=vol.PREVENT_EXTRA):
        """Make a schema for a component that uses the script helper."""
        return vol.Schema(
            {
                **schema,
                vol.Optional(Const.CONF_MODE, default=default_script_mode): vol.In(
                    _Const.SCRIPT_MODE_CHOICES
                ),
                vol.Optional(_Const.CONF_MAX, default=_Const.DEFAULT_MAX): vol.All(
                    vol.Coerce(int), vol.Range(min=2)
                ),
                vol.Optional(
                    _Const.CONF_MAX_EXCEEDED, default=_Const.DEFAULT_MAX_EXCEEDED
                ): vol.All(vol.Upper, vol.In(_MAX_EXCEEDED_CHOICES)),
            },
            extra=extra,
        )

    @staticmethod
    def reset_script_stack():
        _SCRIPT_STACK_CV.set([])

    @staticmethod
    async def async_get_device_automation_platform(
        shc: SmartHomeController, domain: str, platform: Platform
    ):
        """
        Get the device automation platform for Action, ActionCondition
        or Trigger.
        """
        if platform not in (Platform.ACTION, Platform.CONDITION, Platform.TRIGGER):
            raise InvalidDeviceAutomationConfig(
                f"Invalid Device Automation Platform: {platform}"
            )
        await shc.setup.async_get_integration_with_requirements(domain)
        comp = SmartHomeControllerComponent.get_component(domain)
        if not isinstance(comp, SmartHomeControllerComponent):
            raise InvalidDeviceAutomationConfig(f"Component '{domain}' not found.")
        result = comp.get_platform(platform)
        if platform == Platform.ACTION and not isinstance(result, ActionPlatform):
            raise InvalidDeviceAutomationConfig(
                f"Action Platform in domain '{domain}' not found."
            )
        if platform == Platform.CONDITION and not isinstance(
            result, ActionConditionPlatform
        ):
            raise InvalidDeviceAutomationConfig(
                f"Action Condition Platform in domain '{domain}' not found."
            )
        if platform == Platform.TRIGGER and not isinstance(result, TriggerPlatform):
            raise InvalidDeviceAutomationConfig(
                f"Trigger Platform in domain '{domain}' not found."
            )
        return result

    @staticmethod
    async def _async_get_trigger_platform(
        shc: SmartHomeController, config: ConfigType
    ) -> TriggerPlatform:
        platform_and_sub_type = config[Const.CONF_PLATFORM].split(".")
        platform = platform_and_sub_type[0]
        for alias, triggers in _PLATFORM_ALIASES.items():
            if platform in triggers:
                platform = alias
                break
        try:
            await shc.setup.async_get_integration(platform)
        except IntegrationNotFound:
            raise vol.Invalid(f"Invalid platform '{platform}' specified") from None

        return await Scripts.async_get_device_automation_platform(
            shc, platform, Platform.TRIGGER
        )

    @staticmethod
    async def async_validate_trigger_config(
        shc: SmartHomeController, trigger_config: list[ConfigType]
    ) -> list[ConfigType]:
        """Validate triggers."""
        config = []
        for conf in trigger_config:
            platform = await Scripts._async_get_trigger_platform(shc, conf)
            schema = platform.trigger_schema
            if schema is not None:
                conf = schema(conf)
            else:
                conf = await platform.async_validate_trigger_config(conf)
            config.append(conf)
        return config

    @staticmethod
    async def async_initialize_triggers(
        shc: SmartHomeController,
        trigger_config: list[ConfigType],
        action: collections.abc.Callable,
        domain: str,
        name: str,
        log_cb: collections.abc.Callable,
        shc_start: bool = False,
        variables: TemplateVarsType = None,
    ) -> CallbackType:
        """Initialize triggers."""

        triggers = []
        for idx, conf in enumerate(trigger_config):
            # Skip triggers that are not enabled
            if not conf.get(Const.CONF_ENABLED, True):
                continue

            platform = await Scripts._async_get_trigger_platform(shc, conf)
            trigger_id = conf.get(Const.CONF_ID, f"{idx}")
            trigger_idx = f"{idx}"
            trigger_data = TriggerData(id=trigger_id, idx=trigger_idx)
            info = TriggerInfo(
                domain=domain,
                name=name,
                shc_start=shc_start,
                variables=variables,
                trigger_data=trigger_data,
            )

            triggers.append(
                platform.async_attach_trigger(
                    conf, _trigger_action_wrapper(shc, action, conf), info
                )
            )

        attach_results = await asyncio.gather(*triggers, return_exceptions=True)
        removes: list[collections.abc.Callable[[], None]] = []

        for result in attach_results:
            if isinstance(result, SmartHomeControllerError):
                log_cb(
                    logging.ERROR, f"Got error '{result}' when setting up triggers for"
                )
            elif isinstance(result, Exception):
                log_cb(logging.ERROR, "Error setting up trigger", exc_info=result)
            elif result is None:
                log_cb(
                    logging.ERROR,
                    "Unknown error while setting up trigger (empty result)",
                )
            else:
                removes.append(result)

        if not removes:
            return None

        log_cb(logging.INFO, "Initialized trigger")

        @callback
        def remove_triggers() -> None:
            """Remove triggers."""
            for remove in removes:
                remove()

        return remove_triggers

    async def async_validate_actions_config(
        self, actions: list[ConfigType]
    ) -> list[ConfigType]:
        """Validate a list of actions."""
        return await asyncio.gather(
            *(self.async_validate_action_config(action) for action in actions)
        )

    async def async_validate_automation_actions_config(
        shc: SmartHomeController, config: ConfigType
    ) -> ConfigType:
        platform = Scripts.get_action_protocol(shc)
        if isinstance(platform, Scripts):
            return await platform.async_validate_actions_config(config)
        raise NotImplementedError()

    async def async_validate_action_config(self, config: ConfigType) -> ConfigType:
        """Validate config."""
        action_type = cv.determine_script_action(config)

        if action_type in _STATIC_VALIDATION_ACTION_TYPES:
            pass

        elif action_type == cv.SCRIPT_ACTION_DEVICE_AUTOMATION:
            config = await self.async_validate_device_action_config(config)

        elif action_type == cv.SCRIPT_ACTION_CHECK_CONDITION:
            cond_prot = ScriptCondition.get_action_condition_protocol(self._shc)
            config = await cond_prot.async_validate_condition_config(config)

        elif action_type == cv.SCRIPT_ACTION_WAIT_FOR_TRIGGER:
            config[
                Const.CONF_WAIT_FOR_TRIGGER
            ] = await self.async_validate_trigger_config(
                self._shc, config[Const.CONF_WAIT_FOR_TRIGGER]
            )

        elif action_type == cv.SCRIPT_ACTION_REPEAT:
            if Const.CONF_UNTIL in config[Const.CONF_REPEAT]:
                cond_prot = ScriptCondition.get_action_condition_protocol(self._shc)
                conditions = await ScriptCondition.async_validate_conditions_config(
                    self._shc, config[Const.CONF_REPEAT][Const.CONF_UNTIL]
                )
                config[Const.CONF_REPEAT][Const.CONF_UNTIL] = conditions
            if Const.CONF_WHILE in config[Const.CONF_REPEAT]:
                conditions = await ScriptCondition.async_validate_conditions_config(
                    self._shc, config[Const.CONF_REPEAT][Const.CONF_WHILE]
                )
                config[Const.CONF_REPEAT][Const.CONF_WHILE] = conditions
            config[Const.CONF_REPEAT][
                Const.CONF_SEQUENCE
            ] = await self.async_validate_actions_config(
                config[Const.CONF_REPEAT][Const.CONF_SEQUENCE]
            )

        elif action_type == cv.SCRIPT_ACTION_CHOOSE:
            if Const.CONF_DEFAULT in config:
                config[Const.CONF_DEFAULT] = await self.async_validate_actions_config(
                    config[Const.CONF_DEFAULT]
                )

            for choose_conf in config[Const.CONF_CHOOSE]:
                conditions = await ScriptCondition.async_validate_conditions_config(
                    self._shc, choose_conf[Const.CONF_CONDITIONS]
                )
                choose_conf[Const.CONF_CONDITIONS] = conditions
                choose_conf[
                    Const.CONF_SEQUENCE
                ] = await self.async_validate_actions_config(
                    choose_conf[Const.CONF_SEQUENCE]
                )

        elif action_type == cv.SCRIPT_ACTION_IF:
            config[
                Const.CONF_IF
            ] = await ScriptCondition.async_validate_conditions_config(
                self._shc, config[Const.CONF_IF]
            )
            config[Const.CONF_THEN] = await self.async_validate_actions_config(
                config[Const.CONF_THEN]
            )
            if Const.CONF_ELSE in config:
                config[Const.CONF_ELSE] = await self.async_validate_actions_config(
                    config[Const.CONF_ELSE]
                )

        elif action_type == cv.SCRIPT_ACTION_PARALLEL:
            for parallel_conf in config[Const.CONF_PARALLEL]:
                parallel_conf[
                    Const.CONF_SEQUENCE
                ] = await self.async_validate_actions_config(
                    parallel_conf[Const.CONF_SEQUENCE]
                )

        else:
            raise ValueError(f"No validation for {action_type}")

        return config

    async def async_validate_device_action_config(
        self, config: ConfigType
    ) -> ConfigType:
        act_prot = await self.async_get_device_automation_platform(
            self._shc, config[Const.CONF_DOMAIN], Platform.ACTION
        )
        schema = act_prot.action_schema
        if schema is not None:
            return schema(config)
        return await act_prot.async_validate_action_config(config)

    @staticmethod
    @callback
    def breakpoint_clear(key, run_id, node):
        """Clear a breakpoint."""
        run_id = run_id or _Const.RUN_ID_ANY
        _Script.clear_breakpoint(key, run_id, node)

    @staticmethod
    @callback
    def breakpoint_clear_all() -> None:
        """Clear all breakpoints."""
        _Script.clear_breakpoints()

    @staticmethod
    @callback
    def breakpoint_set(key, run_id, node):
        """Set a breakpoint."""
        run_id = run_id or _Const.RUN_ID_ANY
        _Script.set_breakpoint(key, run_id, node)

    @staticmethod
    @callback
    def breakpoint_list() -> list[dict[str, typing.Any]]:
        """List breakpoints."""
        return _Script.list_breakpoints()

    @staticmethod
    @callback
    def debug_continue(shc: SmartHomeController, key, run_id):
        """Continue execution of a halted script."""
        # Clear any wildcard breakpoint
        Scripts.breakpoint_clear(key, run_id, _Const.NODE_ANY)

        signal = Const.SCRIPT_DEBUG_CONTINUE_STOP.format(key, run_id)
        shc.dispatcher.async_send(signal, "continue")

    @staticmethod
    @callback
    def debug_step(shc: SmartHomeController, key, run_id):
        """Single step a halted script."""
        # Set a wildcard breakpoint
        Scripts.breakpoint_set(key, run_id, _Const.NODE_ANY)

        signal = _Const.SCRIPT_DEBUG_CONTINUE_STOP.format(key, run_id)
        shc.dispatcher.async_send(signal, "continue")

    @staticmethod
    @callback
    def debug_stop(shc: SmartHomeController, key, run_id):
        """Stop execution of a running or halted script."""
        signal = _Const.SCRIPT_DEBUG_CONTINUE_STOP.format(key, run_id)
        shc.dispatcher.async_send(signal, "stop")

    async def async_call_action_from_config(
        self, config: ConfigType, variables: dict[str, typing.Any], context: Context
    ) -> None:
        """Empty, has to be overridden"""


class _ChooseData(typing.TypedDict):
    choices: list[tuple[list[ConditionCheckerType], _Script]]
    default: _Script


class _IfData(typing.TypedDict):
    if_conditions: list[ConditionCheckerType]
    if_then: _Script
    if_else: _Script


class _ScriptRun:
    """Manage Script sequence run."""

    def __init__(
        self,
        shc: SmartHomeController,
        script: _Script,
        variables: dict[str, typing.Any],
        context: Context,
        log_exceptions: bool,
    ) -> None:
        self._shc = shc
        self._script = script
        self._variables = variables
        self._context = context
        self._log_exceptions = log_exceptions
        self._step = -1
        self._action: dict[str, typing.Any] = None
        self._stop = asyncio.Event()
        self._stopped = asyncio.Event()

    def _changed(self) -> None:
        if not self._stop.is_set():
            self._script._changed()  # pylint: disable=protected-access

    async def _async_get_condition(self, config):
        # pylint: disable=protected-access
        return await self._script._async_get_condition(config)

    def _log(
        self,
        msg: str,
        *args: typing.Any,
        level: int = logging.INFO,
        **kwargs: typing.Any,
    ) -> None:
        self._script._log(  # pylint: disable=protected-access
            msg, *args, level=level, **kwargs
        )

    def _step_log(self, default_message, timeout=None):
        # pylint: disable=protected-access
        self._script._last_action = self._action.get(Const.CONF_ALIAS, default_message)
        _timeout = (
            "" if timeout is None else f" (timeout: {dt.timedelta(seconds=timeout)})"
        )
        self._log(f"Executing step {self._script.last_action}{_timeout}")

    async def async_run(self) -> None:
        """Run script."""
        # Push the script to the script execution stack
        if (script_stack := _SCRIPT_STACK_CV.get()) is None:
            script_stack = []
            _SCRIPT_STACK_CV.set(script_stack)
        script_stack.append(id(self._script))

        try:
            self._log(f"Running {self._script.running_description}")
            for self._step, self._action in enumerate(self._script.sequence):
                if self._stop.is_set():
                    Trace.set_stop_reason("cancelled")
                    break
                await self._async_step(log_exceptions=False)
            else:
                Trace.set_stop_reason("finished")
        except _AbortScript:
            Trace.set_stop_reason("aborted")
            # Let the _AbortScript bubble up if this is a sub-script
            if not self._script.top_level:
                raise
        except _ConditionFail:
            Trace.set_stop_reason("aborted")
        except _StopScript:
            Trace.set_stop_reason("finished")
            # Let the _StopScript bubble up if this is a sub-script
            if not self._script.top_level:
                raise
        except Exception:
            Trace.set_stop_reason("error")
            raise
        finally:
            # Pop the script from the script execution stack
            script_stack.pop()
            self._finish()

    async def _async_step(self, log_exceptions):
        continue_on_error = self._action.get(Const.CONF_CONTINUE_ON_ERROR, False)

        with Trace.path(str(self._step)):
            async with _trace_action(self._shc, self, self._stop, self._variables):
                if self._stop.is_set():
                    return

                action = cv.determine_script_action(self._action)

                if not self._action.get(Const.CONF_ENABLED, True):
                    self._log(
                        f"Skipped disabled step {self._action.get(Const.CONF_ALIAS, action)}"
                    )
                    Trace.set_result(enabled=False)
                    return

                try:
                    handler = f"_async_{action}_step"
                    await getattr(self, handler)()
                except Exception as ex:  # pylint: disable=broad-except
                    self._handle_exception(
                        ex, continue_on_error, self._log_exceptions or log_exceptions
                    )

    def _finish(self) -> None:
        self._script._runs.remove(self)  # pylint: disable=protected-access
        if not self._script.is_running:
            self._script._last_action = None  # pylint: disable=protected-access
        self._changed()
        self._stopped.set()

    async def async_stop(self) -> None:
        """Stop script run."""
        self._stop.set()
        await self._stopped.wait()

    def _handle_exception(
        self, exception: Exception, continue_on_error: bool, log_exceptions: bool
    ) -> None:
        if not isinstance(exception, _HaltScript) and log_exceptions:
            self._log_exception(exception)

        if not continue_on_error:
            raise exception

        # An explicit request to stop the script has been raised.
        if isinstance(exception, _StopScript):
            raise exception

        # These are incorrect scripts, and not runtime errors that need to
        # be handled and thus cannot be stopped by `continue_on_error`.
        if isinstance(
            exception,
            (
                vol.Invalid,
                TemplateError,
                ServiceNotFound,
                InvalidEntityFormatError,
                NoEntitySpecifiedError,
                ConditionError,
            ),
        ):
            raise exception

        # Only Home Assistant errors can be ignored.
        if not isinstance(exception, SmartHomeControllerError):
            raise exception

    def _log_exception(self, exception):
        action_type = cv.determine_script_action(self._action)

        error = str(exception)
        level = logging.ERROR

        if isinstance(exception, vol.Invalid):
            error_desc = "Invalid data"

        elif isinstance(exception, TemplateError):
            error_desc = "Error rendering template"

        elif isinstance(exception, Unauthorized):
            error_desc = "Unauthorized"

        elif isinstance(exception, ServiceNotFound):
            error_desc = "Service not found"

        elif isinstance(exception, SmartHomeControllerError):
            error_desc = "Error"

        else:
            error_desc = "Unexpected error"
            level = _LOG_EXCEPTION

        self._log(
            f"Error executing script. {error_desc} for {action_type} at pos {self._step+1}: "
            + f"{error}",
            level=level,
        )

    def _get_pos_time_period_template(self, key):
        try:
            return cv.positive_time_period(
                Template.render_complex(self._action[key], self._variables)
            )
        except (TemplateError, vol.Invalid) as ex:
            self._log(
                f"Error rendering {self._script.name} {key} template: {ex}",
                level=logging.ERROR,
            )
            raise _AbortScript from ex

    async def _async_delay_step(self):
        """Handle delay."""
        delay = self._get_pos_time_period_template(Const.CONF_DELAY)

        self._step_log(f"delay {delay}")

        delay = delay.total_seconds()
        self._changed()
        Trace.set_result(delay=delay, done=False)
        try:
            async with async_timeout.timeout(delay):
                await self._stop.wait()
        except asyncio.TimeoutError:
            Trace.set_result(delay=delay, done=True)

    async def _async_wait_template_step(self):
        """Handle a wait template."""
        if Const.CONF_TIMEOUT in self._action:
            timeout = self._get_pos_time_period_template(
                Const.CONF_TIMEOUT
            ).total_seconds()
        else:
            timeout = None

        self._step_log("wait template", timeout)

        self._variables["wait"] = {"remaining": timeout, "completed": False}
        Trace.set_result(wait=self._variables["wait"])

        wait_template = self._action[Const.CONF_WAIT_TEMPLATE]
        wait_template._shc = self._shc  # pylint: disable=protected-access

        # check if condition already okay
        if ScriptCondition.async_template(wait_template, self._variables, False):
            self._variables["wait"]["completed"] = True
            return

        @callback
        def async_script_wait(_entity_id, _from_s, _to_s):
            """Handle script after template condition is true."""
            wait_var = self._variables["wait"]
            if to_context and to_context.deadline:
                curr_loop = asyncio.get_running_loop()
                if curr_loop is not None:
                    time = curr_loop.time()
                else:
                    time = time.time()
                wait_var["remaining"] = to_context.deadline - time
            else:
                wait_var["remaining"] = timeout
            wait_var["completed"] = True
            done.set()

        to_context = None
        unsub = self._shc.tracker.async_track_template(
            wait_template, async_script_wait, self._variables
        )

        self._changed()
        done = asyncio.Event()
        tasks = [
            self._shc.async_create_task(flag.wait()) for flag in (self._stop, done)
        ]
        try:
            async with async_timeout.timeout(timeout) as to_context:
                await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        except asyncio.TimeoutError as ex:
            self._variables["wait"]["remaining"] = 0.0
            if not self._action.get(Const.CONF_CONTINUE_ON_TIMEOUT, True):
                self._log(_TIMEOUT_MSG)
                Trace.set_result(wait=self._variables["wait"], timeout=True)
                raise _AbortScript from ex
        finally:
            for task in tasks:
                task.cancel()
            unsub()

    async def _async_run_long_action(self, long_task: asyncio.Task) -> None:
        """Run a long task while monitoring for stop request."""

        async def async_cancel_long_task() -> None:
            # Stop long task and wait for it to finish.
            long_task.cancel()
            with contextlib.suppress(Exception):
                await long_task

        # Wait for long task while monitoring for a stop request.
        stop_task = self._shc.async_create_task(self._stop.wait())
        try:
            await asyncio.wait(
                {long_task, stop_task}, return_when=asyncio.FIRST_COMPLETED
            )
        # If our task is cancelled, then cancel long task, too. Note that if long task
        # is cancelled otherwise the CancelledError exception will not be raised to
        # here due to the call to asyncio.wait(). Rather we'll check for that below.
        except asyncio.CancelledError:
            await async_cancel_long_task()
            raise
        finally:
            stop_task.cancel()

        if long_task.cancelled():
            raise asyncio.CancelledError
        if long_task.done():
            # Propagate any exceptions that occurred.
            long_task.result()
        else:
            # Stopped before long task completed, so cancel it.
            await async_cancel_long_task()

    async def _async_call_service_step(self):
        """Call the service specified in the action."""
        self._step_log("call service")

        params = Service.async_prepare_call_from_config(
            self._shc, self._action, self._variables
        )

        running_script = (
            params[Const.CONF_DOMAIN] == "automation"
            and params[Const.CONF_SERVICE] == "trigger"
            or params[Const.CONF_DOMAIN] in ("python_script", "script")
        )
        # If this might start a script then disable the call timeout.
        # Otherwise use the normal service call limit.
        if running_script:
            limit = None
        else:
            limit = self._shc.services.SERVICE_CALL_LIMIT

        Trace.set_result(params=params, running_script=running_script, limit=limit)
        service_task = self._shc.async_create_task(
            self._shc.services.async_call(
                **params,
                blocking=True,
                context=self._context,
                limit=limit,
            )
        )
        if limit is not None:
            # There is a call limit, so just wait for it to finish.
            await service_task
            return

        await self._async_run_long_action(service_task)

    async def _async_device_step(self):
        """Perform the device automation specified in the action."""
        self._step_log("device automation")
        act_prot = await Scripts.async_get_device_automation_platform(
            self._shc, self._action[Const.CONF_DOMAIN], Platform.ACTION
        )
        await act_prot.async_call_device_action_from_config(
            self._action, self._variables, self._context
        )

    async def _async_scene_step(self):
        """Activate the scene specified in the action."""
        self._step_log("activate scene")
        Trace.set_result(scene=self._action[Const.CONF_SCENE])
        await self._shc.services.async_call(
            Const.CONF_SCENE,
            Const.SERVICE_TURN_ON,
            {Const.ATTR_ENTITY_ID: self._action[Const.CONF_SCENE]},
            blocking=True,
            context=self._context,
        )

    async def _async_event_step(self):
        """Fire an event."""
        self._step_log(
            self._action.get(Const.CONF_ALIAS, self._action[Const.CONF_EVENT])
        )
        event_data = {}
        for conf in (Const.CONF_EVENT_DATA, Const.CONF_EVENT_DATA_TEMPLATE):
            if conf not in self._action:
                continue

            try:
                event_data.update(
                    Template.render_complex(self._action[conf], self._variables)
                )
            except TemplateError as ex:
                self._log(
                    f"Error rendering event data template: {ex}", level=logging.ERROR
                )

        Trace.set_result(event=self._action[Const.CONF_EVENT], event_data=event_data)
        self._shc.bus.async_fire(
            self._action[Const.CONF_EVENT], event_data, context=self._context
        )

    async def _async_condition_step(self):
        """Test if condition is matching."""
        # pylint: disable=protected-access
        self._script._last_action = self._action.get(
            Const.CONF_ALIAS, self._action[Const.CONF_CONDITION]
        )
        cond = await self._async_get_condition(self._action)
        try:
            trace_element = Trace.stack_top()
            if trace_element:
                trace_element.reuse_by_child = True
            check = cond(self._variables)
        except ConditionError as ex:
            _LOGGER.warning(f"Error in 'condition' evaluation:\n{ex}")
            check = False

        self._log(f"Test condition {self._script.last_action}: {check}")
        Trace.update_result(result=check)
        if not check:
            raise _ConditionFail

    def _test_conditions(self, conditions, name, condition_path=None):
        if condition_path is None:
            condition_path = name

        @Trace.condition_function
        def traced_test_conditions(shc, variables):
            try:
                with Trace.path(condition_path):
                    for idx, cond in enumerate(conditions):
                        with Trace.path(str(idx)):
                            if not cond(shc, variables):
                                return False
            except ConditionError as ex:
                _LOGGER.warning(f"Error in '{name}{idx}]' evaluation: {ex}")
                return None

            return True

        result = traced_test_conditions(self._shc, self._variables)
        return result

    @Trace.async_path("repeat")
    async def _async_repeat_step(self):
        """Repeat a sequence."""
        description = self._action.get(Const.CONF_ALIAS, "sequence")
        repeat = self._action[Const.CONF_REPEAT]

        saved_repeat_vars = self._variables.get("repeat")

        def set_repeat_var(
            iteration: int, count: int = None, item: typing.Any = None
        ) -> None:
            repeat_vars = {"first": iteration == 1, "index": iteration}
            if count:
                repeat_vars["last"] = iteration == count
            if item is not None:
                repeat_vars["item"] = item
            self._variables["repeat"] = repeat_vars

        # pylint: disable=protected-access
        script = self._script._get_repeat_script(self._step)

        async def async_run_sequence(iteration, extra_msg=""):
            self._log(f"Repeating {description}: Iteration {iteration}{extra_msg}")
            with Trace.path("sequence"):
                await self._async_run_script(script)

        if Const.CONF_COUNT in repeat:
            count = repeat[Const.CONF_COUNT]
            if isinstance(count, Template):
                try:
                    count = int(count.async_render(self._variables))
                except (TemplateError, ValueError) as ex:
                    self._log(
                        f"Error rendering {self._script.name} repeat count template: "
                        + f"{ex}",
                        level=logging.ERROR,
                    )
                    raise _AbortScript from ex
            extra_msg = f" of {count}"
            for iteration in range(1, count + 1):
                set_repeat_var(iteration, count)
                await async_run_sequence(iteration, extra_msg)
                if self._stop.is_set():
                    break

        elif Const.CONF_FOR_EACH in repeat:
            try:
                items = Template.render_complex(
                    repeat[Const.CONF_FOR_EACH], self._variables
                )
            except (TemplateError, ValueError) as ex:
                self._log(
                    f"Error rendering {self._script.name} repeat for each items "
                    + f"template: {ex}",
                    level=logging.ERROR,
                )
                raise _AbortScript from ex

            if not isinstance(items, list):
                self._log(
                    f"Repeat 'for_each' must be a list of items in {self._script.name}, "
                    + f"got: {items}",
                    level=logging.ERROR,
                )
                raise _AbortScript("Repeat 'for_each' must be a list of items")

            count = len(items)
            for iteration, item in enumerate(items, 1):
                set_repeat_var(iteration, count, item)
                extra_msg = f" of {count} with item: {repr(item)}"
                if self._stop.is_set():
                    break
                await async_run_sequence(iteration, extra_msg)

        elif Const.CONF_WHILE in repeat:
            conditions = [
                await self._async_get_condition(config)
                for config in repeat[Const.CONF_WHILE]
            ]
            for iteration in itertools.count(1):
                set_repeat_var(iteration)
                try:
                    if self._stop.is_set():
                        break
                    if not self._test_conditions(conditions, "while"):
                        break
                except ConditionError as ex:
                    _LOGGER.warning(f"Error in 'while' evaluation:\n{ex}")
                    break

                await async_run_sequence(iteration)

        elif Const.CONF_UNTIL in repeat:
            conditions = [
                await self._async_get_condition(config)
                for config in repeat[Const.CONF_UNTIL]
            ]
            for iteration in itertools.count(1):
                set_repeat_var(iteration)
                await async_run_sequence(iteration)
                try:
                    if self._stop.is_set():
                        break
                    if self._test_conditions(conditions, "until") in [True, None]:
                        break
                except ConditionError as ex:
                    _LOGGER.warning(f"Error in 'until' evaluation:\n{ex}")
                    break

        if saved_repeat_vars:
            self._variables["repeat"] = saved_repeat_vars
        else:
            self._variables.pop("repeat", None)  # Not set if count = 0

    async def _async_choose_step(self) -> None:
        """Choose a sequence."""
        # pylint: disable=protected-access
        choose_data = await self._script._async_get_choose_data(self._step)

        with Trace.path("choose"):
            for idx, (conditions, script) in enumerate(choose_data["choices"]):
                with Trace.path(str(idx)):
                    try:
                        if self._test_conditions(conditions, "choose", "conditions"):
                            Trace.set_result(choice=idx)
                            with Trace.path("sequence"):
                                await self._async_run_script(script)
                                return
                    except ConditionError as ex:
                        _LOGGER.warning(f"Error in 'choose' evaluation:\n{ex}")

        if choose_data["default"] is not None:
            Trace.set_result(choice="default")
            with Trace.path(["default"]):
                await self._async_run_script(choose_data["default"])

    async def _async_if_step(self) -> None:
        """If sequence."""
        # pylint: disable=protected-access
        if_data = await self._script._async_get_if_data(self._step)

        test_conditions = False
        try:
            with Trace.path("if"):
                test_conditions = self._test_conditions(
                    if_data["if_conditions"], "if", "condition"
                )
        except ConditionError as ex:
            _LOGGER.warning(f"Error in 'if' evaluation:\n{ex}")

        if test_conditions:
            Trace.set_result(choice="then")
            with Trace.path("then"):
                await self._async_run_script(if_data["if_then"])
                return

        if if_data["if_else"] is not None:
            Trace.set_result(choice="else")
            with Trace.path("else"):
                await self._async_run_script(if_data["if_else"])

    async def _async_wait_for_trigger_step(self):
        """Wait for a trigger event."""
        if Const.CONF_TIMEOUT in self._action:
            timeout = self._get_pos_time_period_template(
                Const.CONF_TIMEOUT
            ).total_seconds()
        else:
            timeout = None

        self._step_log("wait for trigger", timeout)

        variables = {**self._variables}
        self._variables["wait"] = {"remaining": timeout, "trigger": None}
        Trace.set_result(wait=self._variables["wait"])

        done = asyncio.Event()

        async def async_done(variables, _context=None):
            wait_var = self._variables["wait"]
            if to_context and to_context.deadline:
                curr_loop = asyncio.get_running_loop()
                if curr_loop is not None:
                    time = curr_loop.time()
                else:
                    time = time.time()
                wait_var["remaining"] = to_context.deadline - time
            else:
                wait_var["remaining"] = timeout
            wait_var["trigger"] = variables["trigger"]
            done.set()

        def log_cb(level, msg, **kwargs):
            self._log(msg, level=level, **kwargs)

        to_context = None
        remove_triggers = await Scripts.async_initialize_triggers(
            self._shc,
            self._action[Const.CONF_WAIT_FOR_TRIGGER],
            async_done,
            self._script.domain,
            self._script.name,
            log_cb,
            variables=variables,
        )
        if not remove_triggers:
            return

        self._changed()
        tasks = [
            self._shc.async_create_task(flag.wait()) for flag in (self._stop, done)
        ]
        try:
            async with async_timeout.timeout(timeout) as to_context:
                await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        except asyncio.TimeoutError as ex:
            self._variables["wait"]["remaining"] = 0.0
            if not self._action.get(Const.CONF_CONTINUE_ON_TIMEOUT, True):
                self._log(_TIMEOUT_MSG)
                Trace.set_result(wait=self._variables["wait"], timeout=True)
                raise _AbortScript from ex
        finally:
            for task in tasks:
                task.cancel()
            remove_triggers()

    async def _async_variables_step(self):
        """Set a variable value."""
        self._step_log("setting variables")
        self._variables = self._action[Const.CONF_VARIABLES].async_render(
            self._shc, self._variables, render_as_defaults=False
        )

    async def _async_stop_step(self):
        """Stop script execution."""
        stop = self._action[Const.CONF_STOP]
        error = self._action[Const.CONF_ERROR]
        Trace.set_result(stop=stop, error=error)
        if error:
            self._log("Error script sequence: %s", stop)
            raise _AbortScript(stop)
        self._log("Stop script sequence: %s", stop)
        raise _StopScript(stop)

    @Trace.path("parallel")
    async def _async_parallel_step(self) -> None:
        """Run a sequence in parallel."""
        # pylint: disable=protected-access
        scripts = await self._script._async_get_parallel_scripts(self._step)

        async def async_run_with_trace(idx: int, script: _Script) -> None:
            """Run a script with a trace path."""
            Trace.start_parallel_run()
            with Trace.path([str(idx), "sequence"]):
                await self._async_run_script(script)

        results = await asyncio.gather(
            *(async_run_with_trace(idx, script) for idx, script in enumerate(scripts)),
            return_exceptions=True,
        )
        for result in results:
            if isinstance(result, Exception):
                raise result

    async def _async_run_script(self, script: _Script) -> None:
        """Execute a script."""
        await self._async_run_long_action(
            self._shc.async_create_task(
                script.async_run(self._variables, self._context)
            )
        )


def _trigger_action_wrapper(
    shc: SmartHomeController, action: collections.abc.Callable, conf: ConfigType
) -> collections.abc.Callable:
    """Wrap trigger action with extra vars if configured."""
    if Const.CONF_VARIABLES not in conf:
        return action

    @functools.wraps(action)
    async def with_vars(
        run_variables: dict[str, typing.Any], context: Context = None
    ) -> None:
        """Wrap action with extra vars."""
        trigger_variables = conf[Const.CONF_VARIABLES]
        run_variables.update(trigger_variables.async_render(shc, run_variables))
        await action(run_variables, context)

    return with_vars


class _QueuedScriptRun(_ScriptRun):
    """Manage queued Script sequence run."""

    lock_acquired = False

    async def async_run(self) -> None:
        """Run script."""
        # Wait for previous run, if any, to finish by attempting to acquire the script's
        # shared lock. At the same time monitor if we've been told to stop.
        lock_task = self._shc.async_create_task(
            self._script._queue_lck.acquire()  # pylint: disable=protected-access
        )
        stop_task = self._shc.async_create_task(self._stop.wait())
        try:
            await asyncio.wait(
                {lock_task, stop_task}, return_when=asyncio.FIRST_COMPLETED
            )
        except asyncio.CancelledError:
            self._finish()
            raise
        else:
            self.lock_acquired = lock_task.done() and not lock_task.cancelled()
        finally:
            lock_task.cancel()
            stop_task.cancel()

        # If we've been told to stop, then just finish up. Otherwise, we've acquired the
        # lock so we can go ahead and start the run.
        if self._stop.is_set():
            self._finish()
        else:
            await super().async_run()

    def _finish(self) -> None:
        # pylint: disable=protected-access
        if self.lock_acquired:
            self._script._queue_lck.release()
            self.lock_acquired = False
        super()._finish()


def _referenced_extract_ids(
    data: dict[str, typing.Any], key: str, found: set[str]
) -> None:
    """Extract referenced IDs."""
    if not data:
        return

    item_ids = data.get(key)

    if item_ids is None or isinstance(item_ids, Template):
        return

    if isinstance(item_ids, str):
        found.add(item_ids)
    else:
        for item_id in item_ids:
            found.add(item_id)
