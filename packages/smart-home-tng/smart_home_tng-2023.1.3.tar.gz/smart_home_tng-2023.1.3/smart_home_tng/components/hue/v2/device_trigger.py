"""
Philips Hue Integration for Smart Home - The Next Generation.

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

Hue V2 API specific platform implementation.
"""

import typing

import voluptuous as vol
import aiohue
from aiohue.v2.models.button import ButtonEvent
from aiohue.v2.models.relative_rotary import (
    RelativeRotaryAction,
    RelativeRotaryDirection,
)
from aiohue.v2.models.resource import ResourceTypes

from .... import core
from ..const import Const

_cv: typing.TypeAlias = core.ConfigValidation

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from ..hue_bridge import HueBridge

_TRIGGER_SCHEMA: typing.Final = _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(core.Const.CONF_TYPE): str,
        vol.Required(Const.CONF_SUBTYPE): vol.Union(int, str),
        vol.Optional(core.Const.CONF_UNIQUE_ID): str,
    }
)

_DEFAULT_BUTTON_EVENT_TYPES: typing.Final = (
    # all except `DOUBLE_SHORT_RELEASE`
    ButtonEvent.INITIAL_PRESS,
    ButtonEvent.REPEAT,
    ButtonEvent.SHORT_RELEASE,
    ButtonEvent.LONG_RELEASE,
)

_DEFAULT_ROTARY_EVENT_TYPES: typing.Final = (
    RelativeRotaryAction.START,
    RelativeRotaryAction.REPEAT,
)
_DEFAULT_ROTARY_EVENT_SUBTYPES: typing.Final = (
    RelativeRotaryDirection.CLOCK_WISE,
    RelativeRotaryDirection.COUNTER_CLOCK_WISE,
)

_DEVICE_SPECIFIC_EVENT_TYPES: typing.Final = {
    # device specific overrides of specific supported button events
    "Hue tap switch": (ButtonEvent.INITIAL_PRESS,),
}

# pylint: disable=unused-variable


async def async_validate_trigger_config(
    config: core.ConfigType,
) -> core.ConfigType:
    """Validate config."""
    return _TRIGGER_SCHEMA(config)


async def async_attach_trigger(
    bridge: HueBridge,
    config: core.ConfigType,
    action: core.TriggerActionType,
    trigger_info: core.TriggerInfo,
) -> core.CallbackType:
    """Listen for state changes based on configuration."""
    shc = bridge.controller
    event_config = core.Trigger.EVENT_TRIGGER_SCHEMA(
        {
            core.Trigger.CONF_PLATFORM: core.Trigger.CONF_EVENT,
            core.Trigger.CONF_EVENT_TYPE: Const.ATTR_HUE_EVENT,
            core.Trigger.CONF_EVENT_DATA: {
                core.Const.CONF_DEVICE_ID: config[core.Const.CONF_DEVICE_ID],
                core.Const.CONF_TYPE: config[core.Const.CONF_TYPE],
                Const.CONF_SUBTYPE: config[Const.CONF_SUBTYPE],
            },
        }
    )
    return await core.Trigger.async_attach_event_trigger(
        shc, event_config, action, trigger_info, platform_type="device"
    )


@core.callback
def async_get_triggers(
    bridge: HueBridge, device_entry: core.Device
) -> list[dict[str, typing.Any]]:
    """Return device triggers for device on `v2` bridge."""
    api: aiohue.HueBridgeV2 = bridge.api
    domain = bridge.owner.domain

    # Get Hue device id from device identifier
    hue_dev_id = get_hue_device_id(device_entry, domain)
    # extract triggers from all button resources of this Hue device
    triggers = []
    model_id = api.devices[hue_dev_id].product_data.product_name

    for resource in api.devices.get_sensors(hue_dev_id):
        # button triggers
        if resource.type == ResourceTypes.BUTTON:
            for event_type in _DEVICE_SPECIFIC_EVENT_TYPES.get(
                model_id, _DEFAULT_BUTTON_EVENT_TYPES
            ):
                triggers.append(
                    {
                        core.Const.CONF_DEVICE_ID: device_entry.id,
                        core.Const.CONF_DOMAIN: domain,
                        core.Const.CONF_PLATFORM: "device",
                        core.Const.CONF_TYPE: event_type.value,
                        Const.CONF_SUBTYPE: resource.metadata.control_id,
                        core.Const.CONF_UNIQUE_ID: resource.id,
                    }
                )
        # relative_rotary triggers
        elif resource.type == ResourceTypes.RELATIVE_ROTARY:
            for event_type in _DEFAULT_ROTARY_EVENT_TYPES:
                for sub_type in _DEFAULT_ROTARY_EVENT_SUBTYPES:
                    triggers.append(
                        {
                            core.Const.CONF_DEVICE_ID: device_entry.id,
                            core.Const.CONF_DOMAIN: domain,
                            core.Const.CONF_PLATFORM: "device",
                            core.Const.CONF_TYPE: event_type.value,
                            Const.CONF_SUBTYPE: sub_type.value,
                            core.Const.CONF_UNIQUE_ID: resource.id,
                        }
                    )
    return triggers


@core.callback
def get_hue_device_id(device_entry: core.Device, domain: str) -> str:
    """Get Hue device id from device entry."""
    return next(
        (
            identifier[1]
            for identifier in device_entry.identifiers
            if identifier[0] == domain
            and ":" not in identifier[1]  # filter out v1 mac id
        ),
        None,
    )
