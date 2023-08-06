"""
Script Component for Smart Home - The Next Generation.

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
import logging

from ... import core
from .const import Const
from .script_trace import ScriptTrace


# pylint: disable=unused-variable
class ScriptEntity(core.Toggle.Entity, core.RestoreEntity):
    """Representation of a script entity."""

    def __init__(
        self, owner: core.ScriptComponent, object_id, cfg, raw_config, blueprint_inputs
    ):
        """Initialize the script."""
        self._shc = owner.controller
        self._owner = owner
        self._object_id = object_id
        self._attr_icon = cfg.get(core.Const.CONF_ICON)
        self._description = cfg[core.Const.CONF_DESCRIPTION]
        self._fields: core.ConfigType = cfg[Const.CONF_FIELDS]

        # The object ID of scripts need / are unique already
        # they cannot be changed from the UI after creating
        self._attr_unique_id = object_id

        self._entity_id = f"{self._owner.domain}.{object_id}"
        self._script = core.Scripts.Script(
            self._owner.controller,
            cfg[core.Const.CONF_SEQUENCE],
            cfg.get(core.Const.CONF_ALIAS, object_id),
            self._owner.domain,
            running_description="script sequence",
            change_listener=self.async_change_listener,
            script_mode=cfg[core.Const.CONF_MODE],
            max_runs=cfg[core.Scripts.Const.CONF_MAX],
            max_exceeded=cfg[core.Scripts.Const.CONF_MAX_EXCEEDED],
            logger=logging.getLogger(f"{__name__}.{object_id}"),
            variables=cfg.get(core.Const.CONF_VARIABLES),
        )
        self._changed = asyncio.Event()
        self._raw_config = raw_config
        self._trace_config = cfg[Const.CONF_TRACE]
        self._blueprint_inputs = blueprint_inputs

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def name(self):
        """Return the name of the entity."""
        return self._script.name

    @property
    def description(self) -> str:
        return self._description

    @property
    def fields(self) -> core.ConfigType:
        return self._fields

    @property
    def object_id(self) -> str:
        return self._object_id

    @property
    def script(self) -> core.Scripts.Script:
        return self._script

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {
            Const.ATTR_LAST_TRIGGERED: self._script.last_triggered,
            core.Const.ATTR_MODE: self._script.script_mode,
            core.Scripts.Const.ATTR_CUR: self._script.runs,
        }
        if self._script.supports_max:
            attrs[core.Scripts.Const.ATTR_MAX] = self._script.max_runs
        if self._script.last_action:
            attrs[Const.ATTR_LAST_ACTION] = self._script.last_action
        return attrs

    @property
    def is_on(self):
        """Return true if script is on."""
        return self._script.is_running

    @core.callback
    def async_change_listener(self):
        """Update state."""
        self.async_write_state()
        self._changed.set()

    async def async_turn_on(self, **kwargs):
        """Run the script.

        Depending on the script's run mode, this may do nothing, restart the script or
        fire an additional parallel run.
        """
        variables = kwargs.get("variables")
        context = kwargs.get("context")
        wait = kwargs.get("wait", True)
        self.async_set_context(context)
        self._shc.bus.async_fire(
            core.Const.EVENT_SCRIPT_STARTED,
            {
                core.Const.ATTR_NAME: self._script.name,
                core.Const.ATTR_ENTITY_ID: self.entity_id,
            },
            context=context,
        )
        coro = self._async_run(variables, context)
        if wait:
            await coro
            return

        # Caller does not want to wait for called script to finish so let script run in
        # separate Task. Make a new empty script stack; scripts are allowed to
        # recursively turn themselves on when not waiting.
        core.Scripts.reset_script_stack()

        self._changed.clear()
        self._shc.async_create_task(coro)
        # Wait for first state change so we can guarantee that
        # it is written to the State Machine before we return.
        await self._changed.wait()

    async def _async_run(self, variables, context):
        with ScriptTrace.trace_script(
            self._owner,
            self._object_id,
            self._raw_config,
            self._blueprint_inputs,
            context,
            self._trace_config,
        ) as script_trace:
            # Prepare tracing the execution of the script's sequence
            script_trace.set_trace(core.Trace.get())
            with core.Trace.path("sequence"):
                this = None
                if state := self._shc.states.get(self.entity_id):
                    this = state.as_dict()
                script_vars = {"this": this, **(variables or {})}
                return await self._script.async_run(script_vars, context)

    async def async_turn_off(self, **kwargs):
        """Stop running the script.

        If multiple runs are in progress, all will be stopped.
        """
        await self._script.async_stop()

    async def async_added_to_shc(self) -> None:
        """Restore last triggered on startup."""
        if state := await self.async_get_last_state():
            if last_triggered := state.attributes.get("last_triggered"):
                self._script.last_triggered = core.helpers.parse_datetime(
                    last_triggered
                )

    async def async_will_remove_from_shc(self):
        """Stop script and remove service when it will be removed from Home Assistant."""
        await self.script.async_stop()

        # remove service
        self._shc.services.async_remove(self._owner.domain, self.object_id)
