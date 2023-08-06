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

_BASE_SCHEMA: typing.Final = _cv.TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_PLATFORM): "state",
        vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_ids_or_uuids,
        vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_template,
        vol.Optional(core.Const.CONF_ATTRIBUTE): _cv.match_all,
    }
)

_TRIGGER_STATE_SCHEMA: typing.Final = _BASE_SCHEMA.extend(
    {
        # These are str on purpose. Want to catch YAML conversions
        vol.Exclusive(core.Const.CONF_FROM, core.Const.CONF_FROM): vol.Any(
            str, [str], None
        ),
        vol.Exclusive(core.Const.CONF_NOT_FROM, core.Const.CONF_FROM): vol.Any(
            str, [str], None
        ),
        vol.Exclusive(core.Const.CONF_TO, core.Const.CONF_TO): vol.Any(
            str, [str], None
        ),
        vol.Exclusive(core.Const.CONF_NOT_TO, core.Const.CONF_TO): vol.Any(
            str, [str], None
        ),
    }
)

_TRIGGER_ATTRIBUTE_SCHEMA: typing.Final = _BASE_SCHEMA.extend(
    {
        vol.Exclusive(core.Const.CONF_FROM, core.Const.CONF_FROM): _cv.match_all,
        vol.Exclusive(core.Const.CONF_NOT_FROM, core.Const.CONF_FROM): _cv.match_all,
        vol.Exclusive(core.Const.CONF_TO, core.Const.CONF_TO): _cv.match_all,
        vol.Exclusive(core.Const.CONF_NOT_TO, core.Const.CONF_TO): _cv.match_all,
    }
)


# pylint: disable=unused-variable
class StateTrigger(core.TriggerPlatform):
    """Offer state listening automation rules."""

    def __init__(self, shc: core.SmartHomeController) -> None:
        super().__init__()
        self._shc = shc

    async def async_validate_trigger_config(
        self, config: core.ConfigType
    ) -> core.ConfigType:
        """Validate trigger config."""
        if not isinstance(config, dict):
            raise vol.Invalid("Expected a dictionary")

        # We use this approach instead of vol.Any because
        # this gives better error messages.
        if core.Const.CONF_ATTRIBUTE in config:
            config = _TRIGGER_ATTRIBUTE_SCHEMA(config)
        else:
            config = _TRIGGER_STATE_SCHEMA(config)

        registry = self._shc.entity_registry
        config[core.Const.CONF_ENTITY_ID] = registry.async_validate_entity_ids(
            _cv.entity_ids_or_uuids(config[core.Const.CONF_ENTITY_ID])
        )

        return config

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        """Listen for state changes based on configuration."""
        return await core.Trigger.async_attach_state_trigger(
            self._shc, config, action, trigger_info
        )
