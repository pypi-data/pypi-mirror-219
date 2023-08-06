"""
Sun Component for Smart Home - The Next Generation.

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

import datetime as dt
import logging
import typing
import voluptuous as vol

from ... import core
from .const import Const
from .sun_config_flow import SunConfigFlow
from .sun_entity import SunEntity

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)
_TRIGGER_SCHEMA: typing.Final = _cv.TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_PLATFORM): "sun",
        vol.Required(core.Const.CONF_EVENT): _cv.sun_event,
        vol.Required(core.Const.CONF_OFFSET, default=dt.timedelta(0)): _cv.time_period,
    }
)


# pylint: disable=unused-variable
class SunComponent(
    core.SmartHomeControllerComponent,
    core.ConfigFlowPlatform,
    core.RecorderPlatform,
    core.TriggerPlatform,
):
    """Support for functionality to keep track of the sun."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._register_flow()
        self._supported_platforms = frozenset(
            [core.Platform.CONFIG_FLOW, core.Platform.RECORDER, core.Platform.TRIGGER]
        )
        self._sun: SunEntity = None

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Track the state of the sun."""
        if not await super().async_setup(config):
            return False

        if config.get(core.Const.CONF_ELEVATION) is not None:
            _LOGGER.warning(
                "Elevation is now configured in Home Assistant core. "
                + "See https://www.home-assistant.io/docs/configuration/basic/"
            )
        self._shc.async_create_task(
            self._shc.config_entries.flow.async_init(
                self.domain,
                context={"source": core.ConfigEntrySource.IMPORT},
                data=config,
            )
        )
        return True

    async def async_setup_entry(self, _entry: core.ConfigEntry) -> bool:
        """Set up from a config entry."""
        # Process integration platforms right away since
        # we will create entities before firing EVENT_COMPONENT_LOADED
        await self._shc.setup.async_process_integration_platform_for_component(
            self.domain
        )
        self._sun = SunEntity(self._shc)
        return True

    async def async_unload_entry(self, _entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        # pylint: disable=protected-access
        self._sun._remove_listeners()
        self._shc.states.async_remove(self._sun.entity_id)
        return True

    def create_config_flow(
        self, context: dict, init_data: typing.Any
    ) -> core.ConfigFlow:
        return SunConfigFlow(self, context, init_data)

    def exclude_attributes(self) -> set[str]:
        """Exclude sun attributes from being recorded in the database."""
        return {
            Const.STATE_ATTR_AZIMUTH,
            Const.STATE_ATTR_ELEVATION,
            Const.STATE_ATTR_RISING,
            Const.STATE_ATTR_NEXT_DAWN,
            Const.STATE_ATTR_NEXT_DUSK,
            Const.STATE_ATTR_NEXT_MIDNIGHT,
            Const.STATE_ATTR_NEXT_NOON,
            Const.STATE_ATTR_NEXT_RISING,
            Const.STATE_ATTR_NEXT_SETTING,
        }

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
        offset = config.get(core.Const.CONF_OFFSET)
        description = event
        if offset:
            description = f"{description} with offset"
        job = core.SmartHomeControllerJob(action)

        @core.callback
        def call_action():
            """Call action with right context."""
            self._shc.async_run_shc_job(
                job,
                {
                    "trigger": {
                        **trigger_data,
                        "platform": "sun",
                        "event": event,
                        "offset": offset,
                        "description": description,
                    }
                },
            )

        if event == core.Const.SUN_EVENT_SUNRISE:
            return self._shc.tracker.async_track_sunrise(call_action, offset)
        return self._shc.tracker.async_track_sunset(call_action, offset)
