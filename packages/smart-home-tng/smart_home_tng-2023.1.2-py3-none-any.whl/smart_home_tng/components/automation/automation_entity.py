"""
Automation Integration for Smart Home - The Next Generation.

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

import collections.abc
import contextlib
import logging
import typing

import voluptuous as vol

from ... import core
from .automation_trace import AutomationTrace
from .const import Const


@contextlib.contextmanager
def _trace_automation(
    domain: str,
    automation_id: str,
    config: core.ConfigType,
    blueprint_inputs: core.ConfigType,
    context: core.Context,
    trace_config: core.ConfigType,
):
    """Trace action execution of automation with automation_id."""
    trace = AutomationTrace(domain, automation_id, config, blueprint_inputs, context)

    comp = core.SmartHomeControllerComponent.get_component("trace")
    if isinstance(comp, core.TraceComponent):
        comp.store_trace(trace, trace_config[core.Const.CONF_STORED_TRACES])

    try:
        yield trace
    except Exception as ex:
        if automation_id:
            trace.set_error(ex)
        raise ex
    finally:
        if automation_id:
            trace.finished()


# pylint: disable=unused-variable
class AutomationEntity(core.Toggle.Entity, core.RestoreEntity):
    """Entity to show status of entity."""

    _attr_should_poll = False

    def __init__(
        self,
        domain: str,
        automation_id: str,
        name: str,
        trigger_config,
        cond_func,
        action_script: core.Scripts.Script,
        initial_state,
        variables: core.TemplateVarsType,
        trigger_variables: core.TemplateVarsType,
        raw_config: core.ConfigType,
        blueprint_inputs,
        trace_config: core.ConfigType,
    ):
        """Initialize an automation entity."""
        self._domain = domain
        self._attr_name = name
        self._trigger_config = trigger_config
        self._async_detach_triggers = None
        self._cond_func = cond_func
        self._action_script = action_script
        self._action_script.change_listener = self.async_write_state
        self._initial_state = initial_state
        self._is_enabled = False
        self._referenced_entities: set[str] = None
        self._referenced_devices: set[str] = None
        self._logger = Const.LOGGER
        self._variables: core.ScriptVariables = variables
        self._trigger_variables: core.ScriptVariables = trigger_variables
        self._raw_config = raw_config
        self._blueprint_inputs = blueprint_inputs
        self._trace_config = trace_config
        self._attr_unique_id = automation_id

    @property
    def extra_state_attributes(self):
        """Return the entity state attributes."""
        attrs = {
            Const.ATTR_LAST_TRIGGERED: self._action_script.last_triggered,
            core.Const.ATTR_MODE: self._action_script.script_mode,
            core.Scripts.Const.ATTR_CUR: self._action_script.runs,
        }
        if self._action_script.supports_max:
            attrs[core.Scripts.Const.ATTR_MAX] = self._action_script.max_runs
        if self.unique_id is not None:
            attrs[core.Const.CONF_ID] = self.unique_id
        return attrs

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        return self._async_detach_triggers is not None or self._is_enabled

    @property
    def referenced_areas(self):
        """Return a set of referenced areas."""
        return self._action_script.referenced_areas

    @property
    def referenced_devices(self):
        """Return a set of referenced devices."""
        if self._referenced_devices is not None:
            return self._referenced_devices

        referenced = self._action_script.referenced_devices

        if self._cond_func is not None:
            for conf in self._cond_func.config:
                referenced |= core.ScriptCondition.async_extract_devices(conf)

        for conf in self._trigger_config:
            referenced |= set(_trigger_extract_device(conf))

        self._referenced_devices = referenced
        return referenced

    @property
    def referenced_entities(self):
        """Return a set of referenced entities."""
        if self._referenced_entities is not None:
            return self._referenced_entities

        referenced = self._action_script.referenced_entities

        if self._cond_func is not None:
            for conf in self._cond_func.config:
                referenced |= core.ScriptCondition.async_extract_entities(conf)

        for conf in self._trigger_config:
            for entity_id in _trigger_extract_entities(conf):
                referenced.add(entity_id)

        self._referenced_entities = referenced
        return referenced

    async def async_added_to_shc(self) -> None:
        """Startup with initial state or previous state."""
        await super().async_added_to_shc()

        self._logger = logging.getLogger(
            f"{__name__}.{core.helpers.split_entity_id(self.entity_id)[1]}"
        )
        self._action_script.update_logger(self._logger)

        if state := await self.async_get_last_state():
            enable_automation = state.state == core.Const.STATE_ON
            last_triggered = state.attributes.get("last_triggered")
            if last_triggered is not None:
                self._action_script.last_triggered = core.helpers.parse_datetime(
                    last_triggered
                )
            self._logger.debug(
                f"Loaded automation {self.entity_id} with state {enable_automation} from state "
                + f"storage last state {state}"
            )
        else:
            enable_automation = Const.DEFAULT_INITIAL_STATE
            self._logger.debug(
                f"Automation {self.entity_id} not in state storage, state "
                + f"{enable_automation} from default is used",
            )

        if self._initial_state is not None:
            enable_automation = self._initial_state
            self._logger.debug(
                f"Automation {self.entity_id} initial state {enable_automation} overridden from "
                + "config initial_state",
            )

        if enable_automation:
            await self.async_enable()

    async def async_turn_on(self, **_kwargs: typing.Any) -> None:
        """Turn the entity on and update the state."""
        await self.async_enable()

    async def async_turn_off(self, **kwargs: typing.Any) -> None:
        """Turn the entity off."""
        if Const.CONF_STOP_ACTIONS in kwargs:
            await self.async_disable(kwargs[Const.CONF_STOP_ACTIONS])
        else:
            await self.async_disable()

    async def async_trigger(self, run_variables, context=None, skip_condition=False):
        """Trigger automation.

        This method is a coroutine.
        """
        reason = ""
        if "trigger" in run_variables and "description" in run_variables["trigger"]:
            reason = f' by {run_variables["trigger"]["description"]}'
        self._logger.debug(f"Automation triggered{reason}")

        # Create a new context referring to the old context.
        parent_id = None if context is None else context.context_id
        trigger_context = core.Context(parent_id=parent_id)

        with _trace_automation(
            self._domain,
            self.unique_id,
            self._raw_config,
            self._blueprint_inputs,
            trigger_context,
            self._trace_config,
        ) as automation_trace:
            this = None
            if state := self._shc.states.get(self.entity_id):
                this = state.as_dict()
            variables = {"this": this, **(run_variables or {})}
            if self._variables:
                try:
                    variables = self._variables.async_render(self._shc, variables)
                except core.TemplateError as err:
                    self._logger.error(f"Error rendering variables: {err}")
                    automation_trace.set_error(err)
                    return

            # Prepare tracing the automation
            automation_trace.set_trace(core.Trace.get())

            # Set trigger reason
            trigger_description = variables.get("trigger", {}).get("description")
            automation_trace.set_trigger_description(trigger_description)

            # Add initial variables as the trigger step
            if "trigger" in variables and "idx" in variables["trigger"]:
                trigger_path = f"trigger/{variables['trigger']['idx']}"
            else:
                trigger_path = "trigger"
            trace_element = core.Trace.create_element(variables, trigger_path)
            core.Trace.append_element(trace_element)

            if (
                not skip_condition
                and self._cond_func is not None
                and not self._cond_func(variables)
            ):
                self._logger.debug(
                    "Conditions not met, aborting automation. Condition summary: "
                    + f"{core.Trace.get(clear=False)}",
                )
                core.Trace.set_stop_reason("failed_conditions")
                return

            self.async_set_context(trigger_context)
            event_data = {
                core.Const.ATTR_NAME: self.name,
                core.Const.ATTR_ENTITY_ID: self.entity_id,
            }
            if "trigger" in variables and "description" in variables["trigger"]:
                event_data[Const.ATTR_SOURCE] = variables["trigger"]["description"]

            @core.callback
            def started_action():
                self._shc.bus.async_fire(
                    core.Const.EVENT_AUTOMATION_TRIGGERED,
                    event_data,
                    context=trigger_context,
                )

            # Make a new empty script stack; automations are allowed
            # to recursively trigger themselves
            core.Scripts.reset_script_stack()

            try:
                with core.Trace.path("action"):
                    await self._action_script.async_run(
                        variables, trigger_context, started_action
                    )
            except (vol.Invalid, core.SmartHomeControllerError) as err:
                self._logger.error(
                    f"Error while executing automation {self.entity_id}: {err}",
                )
                automation_trace.set_error(err)
            except Exception as err:  # pylint: disable=broad-except
                self._logger.exception(f"While executing automation {self.entity_id}")
                automation_trace.set_error(err)

    async def async_will_remove_from_shc(self):
        """Remove listeners when removing automation from Home Assistant."""
        await super().async_will_remove_from_shc()
        await self.async_disable()

    async def async_enable(self):
        """Enable this automation entity.

        This method is a coroutine.
        """
        if self._is_enabled:
            return

        self._is_enabled = True

        # HomeAssistant is starting up
        if self._shc.state != core.CoreState.NOT_RUNNING:
            self._async_detach_triggers = await self._async_attach_triggers(False)
            self.async_write_state()
            return

        async def async_enable_automation(_event):
            """Start automation on startup."""
            # Don't do anything if no longer enabled or already attached
            if not self._is_enabled or self._async_detach_triggers is not None:
                return

            self._async_detach_triggers = await self._async_attach_triggers(True)

        self._shc.bus.async_listen_once(
            core.Const.EVENT_SHC_STARTED, async_enable_automation
        )
        self.async_write_state()

    async def async_disable(self, stop_actions=Const.DEFAULT_STOP_ACTIONS):
        """Disable the automation entity."""
        if not self._is_enabled and not self._action_script.runs:
            return

        self._is_enabled = False

        if self._async_detach_triggers is not None:
            self._async_detach_triggers()
            self._async_detach_triggers = None

        if stop_actions:
            await self._action_script.async_stop()

        self.async_write_state()

    async def _async_attach_triggers(
        self, shc_start: bool
    ) -> collections.abc.Callable[[], None]:
        """Set up the triggers."""

        def log_cb(level, msg, **kwargs):
            self._logger.log(level, f"{msg} {self.name}", **kwargs)

        this = None
        self.async_write_state()
        if state := self._shc.states.get(self.entity_id):
            this = state.as_dict()
        variables = {"this": this}
        if self._trigger_variables:
            try:
                variables = self._trigger_variables.async_render(
                    self._shc,
                    variables,
                    limited=True,
                )
            except core.TemplateError as err:
                self._logger.error(f"Error rendering trigger variables: {err}")
                return None

        return await core.Scripts.async_initialize_triggers(
            self._shc,
            self._trigger_config,
            self.async_trigger,
            self._domain,
            self.name,
            log_cb,
            shc_start,
            variables,
        )


@core.callback
def _trigger_extract_device(trigger_conf: dict) -> list[str]:
    """Extract devices from a trigger config."""
    if trigger_conf[core.Const.CONF_PLATFORM] == "device":
        return [trigger_conf[core.Const.CONF_DEVICE_ID]]

    if (
        trigger_conf[core.Const.CONF_PLATFORM] == "event"
        and core.Const.CONF_EVENT_DATA in trigger_conf
        and core.Const.CONF_DEVICE_ID in trigger_conf[core.Const.CONF_EVENT_DATA]
    ):
        return [trigger_conf[core.Const.CONF_EVENT_DATA][core.Const.CONF_DEVICE_ID]]

    if (
        trigger_conf[core.Const.CONF_PLATFORM] == "tag"
        and core.Const.CONF_DEVICE_ID in trigger_conf
    ):
        return trigger_conf[core.Const.CONF_DEVICE_ID]

    return []


@core.callback
def _trigger_extract_entities(trigger_conf: dict) -> list[str]:
    """Extract entities from a trigger config."""
    if trigger_conf[core.Const.CONF_PLATFORM] in ("state", "numeric_state"):
        return trigger_conf[core.Const.CONF_ENTITY_ID]

    if trigger_conf[core.Const.CONF_PLATFORM] == "calendar":
        return [trigger_conf[core.Const.CONF_ENTITY_ID]]

    if trigger_conf[core.Const.CONF_PLATFORM] == "zone":
        return trigger_conf[core.Const.CONF_ENTITY_ID] + [
            trigger_conf[core.Const.CONF_ZONE]
        ]

    if trigger_conf[core.Const.CONF_PLATFORM] == "geo_location":
        return [trigger_conf[core.Const.CONF_ZONE]]

    if trigger_conf[core.Const.CONF_PLATFORM] == "sun":
        return ["sun.sun"]

    if (
        trigger_conf[core.Const.CONF_PLATFORM] == "event"
        and core.Const.CONF_EVENT_DATA in trigger_conf
        and core.Const.CONF_ENTITY_ID in trigger_conf[core.Const.CONF_EVENT_DATA]
    ):
        return [trigger_conf[core.Const.CONF_EVENT_DATA][core.Const.CONF_ENTITY_ID]]

    return []
