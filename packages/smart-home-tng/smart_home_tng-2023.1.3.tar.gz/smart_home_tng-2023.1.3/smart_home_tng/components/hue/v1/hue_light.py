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

import datetime as dt
import functools as ft
import logging
import random
import typing

import aiohue
import async_timeout

from .... import core
from ..const import Const
from .helpers import remove_devices

if not typing.TYPE_CHECKING:

    class HueBridge:
        pass


if typing.TYPE_CHECKING:
    from ..hue_bridge import HueBridge

_SCAN_INTERVAL: typing.Final = dt.timedelta(seconds=5)

_LOGGER: typing.Final = logging.getLogger(__name__)

_COLOR_MODES_HUE_ON_OFF: typing.Final = {core.Light.ColorMode.ONOFF}
_COLOR_MODES_HUE_DIMMABLE: typing.Final = {core.Light.ColorMode.BRIGHTNESS}
_COLOR_MODES_HUE_COLOR_TEMP: typing.Final = {core.Light.ColorMode.COLOR_TEMP}
_COLOR_MODES_HUE_COLOR: typing.Final = {core.Light.ColorMode.HS}
_COLOR_MODES_HUE_EXTENDED: typing.Final = {
    core.Light.ColorMode.COLOR_TEMP,
    core.Light.ColorMode.HS,
}

_COLOR_MODES_HUE: typing.Final = {
    "Extended color light": _COLOR_MODES_HUE_EXTENDED,
    "Color light": _COLOR_MODES_HUE_COLOR,
    "Dimmable light": _COLOR_MODES_HUE_DIMMABLE,
    "On/Off plug-in unit": _COLOR_MODES_HUE_ON_OFF,
    "Color temperature light": _COLOR_MODES_HUE_COLOR_TEMP,
}

_SUPPORT_HUE_ON_OFF: typing.Final = (
    core.Light.EntityFeature.FLASH | core.Light.EntityFeature.TRANSITION
)
_SUPPORT_HUE_DIMMABLE: typing.Final = _SUPPORT_HUE_ON_OFF
_SUPPORT_HUE_COLOR_TEMP: typing.Final = _SUPPORT_HUE_DIMMABLE
_SUPPORT_HUE_COLOR: typing.Final = (
    _SUPPORT_HUE_DIMMABLE | core.Light.EntityFeature.EFFECT
)
_SUPPORT_HUE_EXTENDED: typing.Final = _SUPPORT_HUE_COLOR_TEMP | _SUPPORT_HUE_COLOR

_SUPPORT_HUE: typing.Final = {
    "Extended color light": _SUPPORT_HUE_EXTENDED,
    "Color light": _SUPPORT_HUE_COLOR,
    "Dimmable light": _SUPPORT_HUE_DIMMABLE,
    "On/Off plug-in unit": _SUPPORT_HUE_ON_OFF,
    "Color temperature light": _SUPPORT_HUE_COLOR_TEMP,
}

_ATTR_IS_HUE_GROUP: typing.Final = "is_hue_group"
_GAMUT_TYPE_UNAVAILABLE: typing.Final = "None"
# Minimum Hue Bridge API version to support groups
# 1.4.0 introduced extended group info
# 1.12 introduced the state object for groups
# 1.13 introduced "any_on" to group state objects
_GROUP_MIN_API_VERSION: typing.Final = (1, 13, 0)


# pylint: disable=unused-variable
class HueLight(core.CoordinatorEntity, core.Light.Entity):
    """Representation of a Hue light."""

    def __init__(
        self,
        coordinator: core.DataUpdateCoordinator,
        bridge: HueBridge,
        is_group: bool,
        light,
        supported_color_modes,
        supported_features,
        rooms,
    ):
        """Initialize the light."""
        super().__init__(coordinator)
        self._attr_supported_color_modes = supported_color_modes
        self._attr_supported_features = supported_features
        self._light = light
        self._bridge = bridge
        self._is_group = is_group
        self._rooms = rooms
        self._allow_unreachable = self._bridge.config_entry.options.get(
            Const.CONF_ALLOW_UNREACHABLE, Const.DEFAULT_ALLOW_UNREACHABLE
        )

        self._fixed_color_mode = None
        if len(supported_color_modes) == 1:
            self._fixed_color_mode = next(iter(supported_color_modes))
        else:
            assert supported_color_modes == {
                core.Light.ColorMode.COLOR_TEMP,
                core.Light.ColorMode.HS,
            }

        if is_group:
            self._is_osram = False
            self._is_philips = False
            self._is_innr = False
            self._is_ewelink = False
            self._is_livarno = False
            self._is_s31litezb = False
            self._gamut_typ = _GAMUT_TYPE_UNAVAILABLE
            self._gamut = None
        else:
            self._is_osram = light.manufacturername == "OSRAM"
            self._is_philips = light.manufacturername == "Philips"
            self._is_innr = light.manufacturername == "innr"
            self._is_ewelink = light.manufacturername == "eWeLink"
            self._is_livarno = light.manufacturername.startswith("_TZ3000_")
            self._is_s31litezb = light.modelid == "S31 Lite zb"
            self._gamut_typ = light.colorgamuttype
            self._gamut = light.colorgamut
            _LOGGER.debug(f"Color gamut of {self.name}: {str(self._gamut)}")
            if light.swupdatestate == "readytoinstall":
                err = (
                    f"Please check for software updates of the {self.name} "
                    + "bulb in the Philips Hue App."
                )
                _LOGGER.warning(err)
            if self._gamut and not core.helpers.Color.check_valid_gamut(self._gamut):
                err = (
                    f"Color gamut of {self.name}: {str(self._gamut)}, "
                    + "not valid, setting gamut to None."
                )
                _LOGGER.debug(err)
                self._gamut_typ = _GAMUT_TYPE_UNAVAILABLE
                self._gamut = None

    @property
    def unique_id(self):
        """Return the unique ID of this Hue light."""
        unique_id = self._light.uniqueid
        if not unique_id and self._is_group:
            unique_id = self._light.id

        return unique_id

    @property
    def device_id(self):
        """Return the ID of this Hue light."""
        return self.unique_id

    @property
    def name(self):
        """Return the name of the Hue light."""
        return self._light.name

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        if self._is_group:
            bri = self._light.action.get("bri")
        else:
            bri = self._light.state.get("bri")

        if bri is None:
            return bri

        return _hue_brightness_to_shc(bri)

    @property
    def color_mode(self) -> str:
        """Return the color mode of the light."""
        if self._fixed_color_mode:
            return self._fixed_color_mode

        # The light supports both hs/xy and white with adjustable color_temperature
        mode = self._color_mode
        if mode in ("xy", "hs"):
            return core.Light.ColorMode.HS

        return core.Light.ColorMode.COLOR_TEMP

    @property
    def _color_mode(self):
        """Return the hue color mode."""
        if self._is_group:
            return self._light.action.get("colormode")
        return self._light.state.get("colormode")

    @property
    def hs_color(self):
        """Return the hs color value."""
        mode = self._color_mode
        source = self._light.action if self._is_group else self._light.state

        if mode in ("xy", "hs") and "xy" in source:
            return core.helpers.Color.xy_to_hs(*source["xy"], self._gamut)

        return None

    @property
    def color_temp(self):
        """Return the CT color value."""
        # Don't return color temperature unless in color temperature mode
        if self._color_mode != "ct":
            return None

        if self._is_group:
            return self._light.action.get("ct")
        return self._light.state.get("ct")

    @property
    def min_mireds(self):
        """Return the coldest color_temp that this light supports."""
        if self._is_group:
            return super().min_mireds

        min_mireds = self._light.controlcapabilities.get("ct", {}).get("min")

        # We filter out '0' too, which can be incorrectly reported by 3rd party buls
        if not min_mireds:
            return super().min_mireds

        return min_mireds

    @property
    def max_mireds(self):
        """Return the warmest color_temp that this light supports."""
        if self._is_group:
            return super().max_mireds
        if self._is_livarno:
            return 500

        max_mireds = self._light.controlcapabilities.get("ct", {}).get("max")

        if not max_mireds:
            return super().max_mireds

        return max_mireds

    @property
    def is_on(self):
        """Return true if device is on."""
        if self._is_group:
            return self._light.state["any_on"]
        return self._light.state["on"]

    @property
    def available(self):
        """Return if light is available."""
        return self.coordinator.last_update_success and (
            self._is_group or self._allow_unreachable or self._light.state["reachable"]
        )

    @property
    def effect(self):
        """Return the current effect."""
        return self._light.state.get("effect", None)

    @property
    def effect_list(self):
        """Return the list of supported effects."""
        if self._is_osram:
            return [core.Light.EFFECT_RANDOM]
        return [core.Light.EFFECT_COLORLOOP, core.Light.EFFECT_RANDOM]

    @property
    def device_info(self) -> core.DeviceInfo:
        """Return the device info."""
        if self._light.type in (
            Const.GROUP_TYPE_ENTERTAINMENT,
            Const.GROUP_TYPE_LIGHT_GROUP,
            Const.GROUP_TYPE_ROOM,
            Const.GROUP_TYPE_LUMINAIRE,
            Const.GROUP_TYPE_LIGHT_SOURCE,
            Const.GROUP_TYPE_ZONE,
        ):
            return None

        suggested_area = None
        if self._rooms and self._light.id in self._rooms:
            suggested_area = self._rooms[self._light.id]

        return core.DeviceInfo(
            identifiers={(self._bridge.owner.domain, self.device_id)},
            manufacturer=self._light.manufacturername,
            # productname added in Hue Bridge API 1.24
            # (published 03/05/2018)
            model=self._light.productname or self._light.modelid,
            name=self.name,
            sw_version=self._light.swversion,
            suggested_area=suggested_area,
            via_device=(self._bridge.owner.domain, self._bridge.api.config.bridgeid),
        )

    async def async_turn_on(self, **kwargs):
        """Turn the specified or all lights on."""
        command = {"on": True}

        if core.Light.ATTR_TRANSITION in kwargs:
            command["transitiontime"] = int(kwargs[core.Light.ATTR_TRANSITION] * 10)

        if core.Light.ATTR_HS_COLOR in kwargs:
            if self._is_osram:
                command["hue"] = int(kwargs[core.Light.ATTR_HS_COLOR][0] / 360 * 65535)
                command["sat"] = int(kwargs[core.Light.ATTR_HS_COLOR][1] / 100 * 255)
            else:
                # Philips hue bulb models respond differently to hue/sat
                # requests, so we convert to XY first to ensure a consistent
                # color.
                xy_color = core.helpers.Color.hs_to_xy(
                    *kwargs[core.Light.ATTR_HS_COLOR], self._gamut
                )
                command["xy"] = xy_color
        elif core.Light.ATTR_COLOR_TEMP in kwargs:
            temp = kwargs[core.Light.ATTR_COLOR_TEMP]
            command["ct"] = max(self.min_mireds, min(temp, self.max_mireds))

        if core.Light.ATTR_BRIGHTNESS in kwargs:
            command["bri"] = _shc_to_hue_brightness(kwargs[core.Light.ATTR_BRIGHTNESS])

        flash = kwargs.get(core.Light.ATTR_FLASH)

        if flash == core.Light.FLASH_LONG:
            command["alert"] = "lselect"
            del command["on"]
        elif flash == core.Light.FLASH_SHORT:
            command["alert"] = "select"
            del command["on"]
        elif (
            not self._is_innr
            and not self._is_ewelink
            and not self._is_livarno
            and not self._is_s31litezb
        ):
            command["alert"] = "none"

        if core.Light.ATTR_EFFECT in kwargs:
            effect = kwargs[core.Light.ATTR_EFFECT]
            if effect == core.Light.EFFECT_COLORLOOP:
                command["effect"] = "colorloop"
            elif effect == core.Light.EFFECT_RANDOM:
                command["hue"] = random.randrange(0, 65535)  # nosec
                command["sat"] = random.randrange(150, 254)  # nosec
            else:
                command["effect"] = "none"

        if self._is_group:
            await self._bridge.async_request_call(self._light.set_action, **command)
        else:
            await self._bridge.async_request_call(self._light.set_state, **command)

        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn the specified or all lights off."""
        command = {"on": False}

        if core.Light.ATTR_TRANSITION in kwargs:
            command["transitiontime"] = int(kwargs[core.Light.ATTR_TRANSITION] * 10)

        flash = kwargs.get(core.Light.ATTR_FLASH)

        if flash == core.Light.FLASH_LONG:
            command["alert"] = "lselect"
            del command["on"]
        elif flash == core.Light.FLASH_SHORT:
            command["alert"] = "select"
            del command["on"]
        elif not self._is_innr and not self._is_livarno:
            command["alert"] = "none"

        if self._is_group:
            await self._bridge.async_request_call(self._light.set_action, **command)
        else:
            await self._bridge.async_request_call(self._light.set_state, **command)

        await self.coordinator.async_request_refresh()

    @property
    def extra_state_attributes(self):
        """Return the device state attributes."""
        if not self._is_group:
            return {}
        return {_ATTR_IS_HUE_GROUP: self._is_group}


def _hue_brightness_to_shc(value):
    """Convert hue brightness 1..254 to hass format 0..255."""
    return min(255, round((value / 254) * 255))


def _shc_to_hue_brightness(value):
    """Convert hass brightness 0..255 to hue 1..254 scale."""
    return max(1, round((value / 255) * 254))


async def async_setup_lights(
    bridge: HueBridge,
    config_entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
):
    """Set up the Hue lights from a config entry."""
    api_version = tuple(int(v) for v in bridge.api.config.apiversion.split("."))
    rooms = {}

    allow_groups = config_entry.options.get(
        Const.CONF_ALLOW_HUE_GROUPS, Const.DEFAULT_ALLOW_HUE_GROUPS
    )
    supports_groups = api_version >= _GROUP_MIN_API_VERSION
    if allow_groups and not supports_groups:
        _LOGGER.warning("Please update your Hue bridge to support groups")

    light_coordinator = core.DataUpdateCoordinator(
        bridge.controller,
        _LOGGER,
        name="light",
        update_method=ft.partial(async_safe_fetch, bridge, bridge.api.lights.update),
        update_interval=_SCAN_INTERVAL,
        request_refresh_debouncer=core.Debouncer(
            bridge.controller,
            _LOGGER,
            cooldown=Const.REQUEST_REFRESH_DELAY,
            immediate=True,
        ),
    )

    # First do a refresh to see if we can reach the hub.
    # Otherwise we will declare not ready.
    await light_coordinator.async_refresh()

    if not light_coordinator.last_update_success:
        raise core.PlatformNotReady

    if not supports_groups:
        update_lights_without_group_support = ft.partial(
            async_update_items,
            bridge,
            bridge.api.lights,
            {},
            async_add_entities,
            ft.partial(create_light, HueLight, light_coordinator, bridge, False, rooms),
            None,
        )
        # We add a listener after fetching the data, so manually trigger listener
        bridge.reset_jobs.append(
            light_coordinator.async_add_listener(update_lights_without_group_support)
        )
        return

    group_coordinator = core.DataUpdateCoordinator(
        bridge.controller,
        _LOGGER,
        name="group",
        update_method=ft.partial(async_safe_fetch, bridge, bridge.api.groups.update),
        update_interval=_SCAN_INTERVAL,
        request_refresh_debouncer=core.Debouncer(
            bridge.controller,
            _LOGGER,
            cooldown=Const.REQUEST_REFRESH_DELAY,
            immediate=True,
        ),
    )

    if allow_groups:
        update_groups = ft.partial(
            async_update_items,
            bridge,
            bridge.api.groups,
            {},
            async_add_entities,
            ft.partial(create_light, HueLight, group_coordinator, bridge, True, None),
            None,
        )

        bridge.reset_jobs.append(group_coordinator.async_add_listener(update_groups))

    cancel_update_rooms_listener = None

    @core.callback
    def _async_update_rooms():
        """Update rooms."""
        nonlocal cancel_update_rooms_listener
        rooms.clear()
        for item_id in bridge.api.groups:
            group = bridge.api.groups[item_id]
            if group.type not in [Const.GROUP_TYPE_ROOM, Const.GROUP_TYPE_ZONE]:
                continue
            for light_id in group.lights:
                rooms[light_id] = group.name

        # Once we do a rooms update, we cancel the listener
        # until the next time lights are added
        bridge.reset_jobs.remove(cancel_update_rooms_listener)
        cancel_update_rooms_listener()  # pylint: disable=not-callable
        cancel_update_rooms_listener = None

    @core.callback
    def _setup_rooms_listener():
        nonlocal cancel_update_rooms_listener
        if cancel_update_rooms_listener is not None:
            # If there are new lights added before _async_update_rooms
            # is called we should not add another listener
            return

        cancel_update_rooms_listener = group_coordinator.async_add_listener(
            _async_update_rooms
        )
        bridge.reset_jobs.append(cancel_update_rooms_listener)

    _setup_rooms_listener()
    await group_coordinator.async_refresh()

    update_lights_with_group_support = ft.partial(
        async_update_items,
        bridge,
        bridge.api.lights,
        {},
        async_add_entities,
        ft.partial(create_light, HueLight, light_coordinator, bridge, False, rooms),
        _setup_rooms_listener,
    )
    # We add a listener after fetching the data, so manually trigger listener
    bridge.reset_jobs.append(
        light_coordinator.async_add_listener(update_lights_with_group_support)
    )
    update_lights_with_group_support()


def create_light(item_class, coordinator, bridge, is_group, rooms, api, item_id):
    """Create the light."""
    api_item = api[item_id]

    if is_group:
        supported_color_modes = set()
        supported_features = 0
        for light_id in api_item.lights:
            if light_id not in bridge.api.lights:
                continue
            light = bridge.api.lights[light_id]
            supported_features |= _SUPPORT_HUE.get(light.type, _SUPPORT_HUE_EXTENDED)
            supported_color_modes.update(
                _COLOR_MODES_HUE.get(light.type, _COLOR_MODES_HUE_EXTENDED)
            )
        supported_features = supported_features or _SUPPORT_HUE_EXTENDED
        supported_color_modes = supported_color_modes or _COLOR_MODES_HUE_EXTENDED
        supported_color_modes = core.Light.filter_supported_color_modes(
            supported_color_modes
        )
    else:
        supported_color_modes = _COLOR_MODES_HUE.get(
            api_item.type, _COLOR_MODES_HUE_EXTENDED
        )
        supported_features = _SUPPORT_HUE.get(api_item.type, _SUPPORT_HUE_EXTENDED)
    return item_class(
        coordinator,
        bridge,
        is_group,
        api_item,
        supported_color_modes,
        supported_features,
        rooms,
    )


@core.callback
def async_update_items(
    bridge, api, current, async_add_entities, create_item, new_items_callback
):
    """Update items."""
    new_items = []

    for item_id in api:
        if item_id in current:
            continue

        current[item_id] = create_item(api, item_id)
        new_items.append(current[item_id])

    bridge.hass.async_create_task(remove_devices(bridge, api, current))

    if new_items:
        # This is currently used to setup the listener to update rooms
        if new_items_callback:
            new_items_callback()
        async_add_entities(new_items)


async def async_safe_fetch(bridge, fetch_method):
    """Safely fetch data."""
    try:
        with async_timeout.timeout(4):
            return await bridge.async_request_call(fetch_method)
    except aiohue.Unauthorized as err:
        await bridge.handle_unauthorized_error()
        raise core.UpdateFailed("Unauthorized") from err
    except aiohue.AiohueException as err:
        raise core.UpdateFailed(f"Hue error: {err}") from err
