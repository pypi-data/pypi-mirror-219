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

Hue V1 API specific platform implementation.
"""

import typing

import voluptuous as vol

from .... import core
from ..const import Const

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from ..hue_bridge import HueBridge

_cv: typing.TypeAlias = core.ConfigValidation

_TRIGGER_SCHEMA: typing.Final = _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {vol.Required(core.Const.CONF_TYPE): str, vol.Required(Const.CONF_SUBTYPE): str}
)


_CONF_SHORT_PRESS: typing.Final = "remote_button_short_press"
_CONF_SHORT_RELEASE: typing.Final = "remote_button_short_release"
_CONF_LONG_RELEASE: typing.Final = "remote_button_long_release"
_CONF_DOUBLE_SHORT_RELEASE: typing.Final = "remote_double_button_short_press"
_CONF_DOUBLE_LONG_RELEASE: typing.Final = "remote_double_button_long_press"

_CONF_TURN_ON: typing.Final = "turn_on"
_CONF_TURN_OFF: typing.Final = "turn_off"
_CONF_DIM_UP: typing.Final = "dim_up"
_CONF_DIM_DOWN: typing.Final = "dim_down"
_CONF_BUTTON_1: typing.Final = "button_1"
_CONF_BUTTON_2: typing.Final = "button_2"
_CONF_BUTTON_3: typing.Final = "button_3"
_CONF_BUTTON_4: typing.Final = "button_4"
_CONF_DOUBLE_BUTTON_1: typing.Final = "double_buttons_1_3"
_CONF_DOUBLE_BUTTON_2: typing.Final = "double_buttons_2_4"

_HUE_DIMMER_REMOTE_MODEL: typing.Final = "Hue dimmer switch"  # RWL020/021
_HUE_DIMMER_REMOTE: typing.Final = {
    (_CONF_SHORT_RELEASE, _CONF_TURN_ON): {core.Const.CONF_EVENT: 1002},
    (_CONF_LONG_RELEASE, _CONF_TURN_ON): {core.Const.CONF_EVENT: 1003},
    (_CONF_SHORT_RELEASE, _CONF_DIM_UP): {core.Const.CONF_EVENT: 2002},
    (_CONF_LONG_RELEASE, _CONF_DIM_UP): {core.Const.CONF_EVENT: 2003},
    (_CONF_SHORT_RELEASE, _CONF_DIM_DOWN): {core.Const.CONF_EVENT: 3002},
    (_CONF_LONG_RELEASE, _CONF_DIM_DOWN): {core.Const.CONF_EVENT: 3003},
    (_CONF_SHORT_RELEASE, _CONF_TURN_OFF): {core.Const.CONF_EVENT: 4002},
    (_CONF_LONG_RELEASE, _CONF_TURN_OFF): {core.Const.CONF_EVENT: 4003},
}

_HUE_BUTTON_REMOTE_MODEL: typing.Final = "Hue Smart button"  # ZLLSWITCH/ROM001
_HUE_BUTTON_REMOTE: typing.Final = {
    (_CONF_SHORT_RELEASE, _CONF_TURN_ON): {core.Const.CONF_EVENT: 1002},
    (_CONF_LONG_RELEASE, _CONF_TURN_ON): {core.Const.CONF_EVENT: 1003},
}

_HUE_WALL_REMOTE_MODEL: typing.Final = "Hue wall switch module"  # ZLLSWITCH/RDM001
_HUE_WALL_REMOTE = {
    (_CONF_SHORT_RELEASE, _CONF_BUTTON_1): {core.Const.CONF_EVENT: 1002},
    (_CONF_SHORT_RELEASE, _CONF_BUTTON_2): {core.Const.CONF_EVENT: 2002},
}

_HUE_TAP_REMOTE_MODEL: typing.Final = "Hue tap switch"  # ZGPSWITCH
_HUE_TAP_REMOTE: typing.Final = {
    (_CONF_SHORT_PRESS, _CONF_BUTTON_1): {core.Const.CONF_EVENT: 34},
    (_CONF_SHORT_PRESS, _CONF_BUTTON_2): {core.Const.CONF_EVENT: 16},
    (_CONF_SHORT_PRESS, _CONF_BUTTON_3): {core.Const.CONF_EVENT: 17},
    (_CONF_SHORT_PRESS, _CONF_BUTTON_4): {core.Const.CONF_EVENT: 18},
}

_HUE_FOHSWITCH_REMOTE_MODEL: typing.Final = "Friends of Hue Switch"  # ZGPSWITCH
_HUE_FOHSWITCH_REMOTE: typing.Final = {
    (_CONF_SHORT_PRESS, _CONF_BUTTON_1): {core.Const.CONF_EVENT: 20},
    (_CONF_LONG_RELEASE, _CONF_BUTTON_1): {core.Const.CONF_EVENT: 16},
    (_CONF_SHORT_PRESS, _CONF_BUTTON_2): {core.Const.CONF_EVENT: 21},
    (_CONF_LONG_RELEASE, _CONF_BUTTON_2): {core.Const.CONF_EVENT: 17},
    (_CONF_SHORT_PRESS, _CONF_BUTTON_3): {core.Const.CONF_EVENT: 23},
    (_CONF_LONG_RELEASE, _CONF_BUTTON_3): {core.Const.CONF_EVENT: 19},
    (_CONF_SHORT_PRESS, _CONF_BUTTON_4): {core.Const.CONF_EVENT: 22},
    (_CONF_LONG_RELEASE, _CONF_BUTTON_4): {core.Const.CONF_EVENT: 18},
    (_CONF_DOUBLE_SHORT_RELEASE, _CONF_DOUBLE_BUTTON_1): {core.Const.CONF_EVENT: 101},
    (_CONF_DOUBLE_LONG_RELEASE, _CONF_DOUBLE_BUTTON_1): {core.Const.CONF_EVENT: 100},
    (_CONF_DOUBLE_SHORT_RELEASE, _CONF_DOUBLE_BUTTON_2): {core.Const.CONF_EVENT: 99},
    (_CONF_DOUBLE_LONG_RELEASE, _CONF_DOUBLE_BUTTON_2): {core.Const.CONF_EVENT: 98},
}


_REMOTES: typing.Final[dict[str, dict[tuple[str, str], dict[str, int]]]] = {
    _HUE_DIMMER_REMOTE_MODEL: _HUE_DIMMER_REMOTE,
    _HUE_TAP_REMOTE_MODEL: _HUE_TAP_REMOTE,
    _HUE_BUTTON_REMOTE_MODEL: _HUE_BUTTON_REMOTE,
    _HUE_WALL_REMOTE_MODEL: _HUE_WALL_REMOTE,
    _HUE_FOHSWITCH_REMOTE_MODEL: _HUE_FOHSWITCH_REMOTE,
}


def _get_hue_event_from_device_id(bridges: dict[str, HueBridge], device_id):
    """Resolve hue event from device id."""
    for bridge in bridges.values():
        for hue_event in bridge.sensor_manager.current_events.values():
            if device_id == hue_event.device_registry_id:
                return hue_event

    return None


# pylint: disable=unused-variable


async def async_validate_trigger_config(
    device_entry: core.Device, config: core.ConfigType
) -> core.ConfigType:
    """Validate config."""
    config = _TRIGGER_SCHEMA(config)
    trigger = (config[core.Const.CONF_TYPE], config[Const.CONF_SUBTYPE])

    if not device_entry:
        raise core.InvalidDeviceAutomationConfig(
            f"Device {config[core.Const.CONF_DEVICE_ID]} not found"
        )

    if device_entry.model not in _REMOTES:
        raise core.InvalidDeviceAutomationConfig(
            f"Device model {device_entry.model} is not a remote"
        )

    if trigger not in _REMOTES[device_entry.model]:
        raise core.InvalidDeviceAutomationConfig(
            f"Device does not support trigger {trigger}"
        )

    return config


async def async_attach_trigger(
    shc: core.SmartHomeController,
    bridges: dict[str, HueBridge],
    device_entry: core.Device,
    config: core.ConfigType,
    action: core.TriggerActionType,
    trigger_info: core.TriggerInfo,
) -> core.CallbackType:
    """Listen for state changes based on configuration."""
    hue_event = _get_hue_event_from_device_id(bridges, device_entry.id)
    if hue_event is None:
        raise core.InvalidDeviceAutomationConfig

    trigger_key: tuple[str, str] = (
        config[core.Const.CONF_TYPE],
        config[Const.CONF_SUBTYPE],
    )

    assert device_entry.model
    trigger = _REMOTES[device_entry.model][trigger_key]

    event_config = {
        core.Const.CONF_PLATFORM: core.Trigger.CONF_EVENT,
        core.Trigger.CONF_EVENT_TYPE: Const.ATTR_HUE_EVENT,
        core.Trigger.CONF_EVENT_DATA: {
            core.Const.CONF_UNIQUE_ID: hue_event.unique_id,
            **trigger,
        },
    }

    event_config = core.Trigger.EVENT_TRIGGER_SCHEMA(event_config)
    return await core.Trigger.async_attach_event_trigger(
        shc, event_config, action, trigger_info, platform_type="device"
    )


@core.callback
def async_get_triggers(bridge: HueBridge, device: core.Device) -> list[dict[str, str]]:
    """Return device triggers for device on `v1` bridge.

    Make sure device is a supported remote model.
    Retrieve the hue event object matching device entry.
    Generate device trigger list.
    """
    if device.model not in _REMOTES:
        return []

    triggers = []
    for trigger, subtype in _REMOTES[device.model]:
        triggers.append(
            {
                core.Const.CONF_DEVICE_ID: device.id,
                core.Const.CONF_DOMAIN: bridge.owner.domain,
                core.Const.CONF_PLATFORM: "device",
                core.Const.CONF_TYPE: trigger,
                Const.CONF_SUBTYPE: subtype,
            }
        )

    return triggers
