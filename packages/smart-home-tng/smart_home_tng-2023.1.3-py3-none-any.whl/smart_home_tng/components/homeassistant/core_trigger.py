"""
Core pieces for Smart Home - The Next Generation.

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

import typing

import voluptuous as vol

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation

_EVENT_START: typing.Final = "start"
_EVENT_SHUTDOWN: typing.Final = "shutdown"

_TRIGGER_SCHEMA = _cv.TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_PLATFORM): core.Const.CORE_COMPONENT_NAME,
        vol.Required(core.Const.CONF_EVENT): vol.Any(_EVENT_START, _EVENT_SHUTDOWN),
    }
)


# pylint: disable=unused-variable
class CoreTrigger(core.TriggerPlatform):
    """Offer Smart Home - The Next Generation core automation rules."""

    def __init__(self, shc: core.SmartHomeController) -> None:
        super().__init__()
        self._shc = shc

    async def async_validate_trigger_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        return _TRIGGER_SCHEMA(config)

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Listen for events based on configuration."""
        trigger_data = trigger_info["trigger_data"]
        event = config.get(core.Const.CONF_EVENT)
        job = core.SmartHomeControllerJob(action)

        if event == _EVENT_SHUTDOWN:

            @core.callback
            def _shutdown(event):
                """Execute when Smart Home - The Next Generation is shutting down."""
                self._shc.async_run_shc_job(
                    job,
                    {
                        "trigger": {
                            **trigger_data,
                            "platform": core.Const.CORE_COMPONENT_NAME,
                            "event": event,
                            "description": "Smart Home - The Next Generation stopping",
                        }
                    },
                    event.context,
                )

            return self._shc.bus.async_listen_once(core.Const.EVENT_SHC_STOP, _shutdown)

        # Automation are enabled while hass is starting up, fire right away
        # Check state because a config reload shouldn't trigger it.
        if trigger_info["shc_start"]:
            self._shc.async_run_shc_job(
                job,
                {
                    "trigger": {
                        **trigger_data,
                        "platform": core.Const.CORE_COMPONENT_NAME,
                        "event": event,
                        "description": "Smart Home - The Next Generation starting",
                    }
                },
            )

        return lambda: None
