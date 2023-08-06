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
from .time_pattern import TimePattern

_cv: typing.TypeAlias = core.ConfigValidation


_TRIGGER_SCHEMA: typing.Final = vol.All(
    _cv.TRIGGER_BASE_SCHEMA.extend(
        {
            vol.Required(core.Const.CONF_PLATFORM): "time_pattern",
            core.Trigger.CONF_HOURS: TimePattern(maximum=23),
            core.Trigger.CONF_MINUTES: TimePattern(maximum=59),
            core.Trigger.CONF_SECONDS: TimePattern(maximum=59),
        }
    ),
    _cv.has_at_least_one_key(
        core.Trigger.CONF_HOURS, core.Trigger.CONF_MINUTES, core.Trigger.CONF_SECONDS
    ),
)


# pylint: disable=unused-variable
class TimePatternTrigger(core.TriggerPlatform):
    """Offer time listening automation rules."""

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
        """Listen for state changes based on configuration."""
        trigger_data = trigger_info["trigger_data"]
        hours = config.get(core.Trigger.CONF_HOURS)
        minutes = config.get(core.Trigger.CONF_MINUTES)
        seconds = config.get(core.Trigger.CONF_SECONDS)
        job = core.SmartHomeControllerJob(action)

        # If larger units are specified, default the smaller units to zero
        if minutes is None and hours is not None:
            minutes = 0
        if seconds is None and minutes is not None:
            seconds = 0

        @core.callback
        def time_automation_listener(now):
            """Listen for time changes and calls action."""
            self._shc.async_run_shc_job(
                job,
                {
                    "trigger": {
                        **trigger_data,
                        "platform": "time_pattern",
                        "now": now,
                        "description": "time pattern",
                    }
                },
            )

        return self._shc.tracker.async_track_time_change(
            time_automation_listener, hour=hours, minute=minutes, second=seconds
        )
