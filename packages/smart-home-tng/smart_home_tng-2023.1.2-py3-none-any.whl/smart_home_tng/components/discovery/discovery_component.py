"""
Discovery Component for Smart Home - The Next Generation.

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
import json
import logging
import typing

import voluptuous as vol
from netdisco import discovery

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)

_SERVICE_APPLE_TV: typing.Final = "apple_tv"
_SERVICE_DAIKIN: typing.Final = "daikin"
_SERVICE_DLNA_DMR: typing.Final = "dlna_dmr"
_SERVICE_ENIGMA2: typing.Final = "enigma2"
_SERVICE_HASS_IOS_APP: typing.Final = "hass_ios"
_SERVICE_HEOS: typing.Final = "heos"
_SERVICE_KONNECTED: typing.Final = "konnected"
_SERVICE_MOBILE_APP: typing.Final = "hass_mobile_app"
_SERVICE_NETGEAR: typing.Final = "netgear_router"
_SERVICE_OCTOPRINT: typing.Final = "octoprint"
_SERVICE_SABNZBD: typing.Final = "sabnzbd"
_SERVICE_SAMSUNG_PRINTER: typing.Final = "samsung_printer"
_SERVICE_TELLDUSLIVE: typing.Final = "tellstick"
_SERVICE_YEELIGHT: typing.Final = "yeelight"
_SERVICE_WEMO: typing.Final = "belkin_wemo"
_SERVICE_XIAOMI_GW: typing.Final = "xiaomi_gw"

# These have custom protocols
_CONFIG_ENTRY_HANDLERS: typing.Final = {
    _SERVICE_TELLDUSLIVE: "tellduslive",
    "logitech_mediaserver": "squeezebox",
}


class ServiceDetails(typing.NamedTuple):
    """Store service details."""

    component: str
    platform: str


# These have no config flows
_SERVICE_HANDLERS: typing.Final = {
    _SERVICE_ENIGMA2: ServiceDetails("media_player", "enigma2"),
    "yamaha": ServiceDetails("media_player", "yamaha"),
    "frontier_silicon": ServiceDetails("media_player", "frontier_silicon"),
    "openhome": ServiceDetails("media_player", "openhome"),
    "bluesound": ServiceDetails("media_player", "bluesound"),
}

_OPTIONAL_SERVICE_HANDLERS: typing.Final = dict[str, tuple[str, str]]()

_MIGRATED_SERVICE_HANDLERS: typing.Final = [
    _SERVICE_APPLE_TV,
    "axis",
    "bose_soundtouch",
    "deconz",
    _SERVICE_DAIKIN,
    "denonavr",
    _SERVICE_DLNA_DMR,
    "esphome",
    "google_cast",
    _SERVICE_HASS_IOS_APP,
    _SERVICE_HEOS,
    "harmony",
    "homekit",
    "ikea_tradfri",
    "kodi",
    _SERVICE_KONNECTED,
    _SERVICE_MOBILE_APP,
    _SERVICE_NETGEAR,
    _SERVICE_OCTOPRINT,
    "philips_hue",
    _SERVICE_SAMSUNG_PRINTER,
    "sonos",
    "songpal",
    _SERVICE_WEMO,
    _SERVICE_XIAOMI_GW,
    "volumio",
    _SERVICE_YEELIGHT,
    _SERVICE_SABNZBD,
    "nanoleaf_aurora",
    "lg_smart_device",
]

_DEFAULT_ENABLED: typing.Final = (
    list(_CONFIG_ENTRY_HANDLERS) + list(_SERVICE_HANDLERS) + _MIGRATED_SERVICE_HANDLERS
)
_DEFAULT_DISABLED = list(_OPTIONAL_SERVICE_HANDLERS) + _MIGRATED_SERVICE_HANDLERS

_CONF_IGNORE: typing.Final = "ignore"
_CONF_ENABLE: typing.Final = "enable"


# pylint: disable=unused-variable
class DiscoveryComponent(core.SmartHomeControllerComponent):
    """Starts a service to scan in intervals for new devices."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._ignored_platforms = list[str]()
        self._enabled_platforms = list[str]()
        self._already_discovered = set[str]()
        self._netdisco: discovery.NetworkDiscovery = None
        self._full_config: core.ConfigType = None
        self._zeroconf_instance: core.ZeroConf = None
        self._zeroconf_types: list[str] = None

    @property
    def scan_interval(self) -> dt.timedelta:
        """Default Scan Interval for Discovery Platforms."""
        return dt.timedelta(seconds=300)

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        """Validate configuration."""
        schema = vol.Schema(
            {
                vol.Optional(self.domain): vol.Schema(
                    {
                        vol.Optional(_CONF_IGNORE, default=[]): vol.All(
                            _cv.ensure_list, [vol.In(_DEFAULT_ENABLED)]
                        ),
                        vol.Optional(_CONF_ENABLE, default=[]): vol.All(
                            _cv.ensure_list,
                            [vol.In(_DEFAULT_DISABLED + _DEFAULT_ENABLED)],
                        ),
                    }
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Start a discovery service."""

        # pylint: disable=no-member
        if not await super().async_setup(config):
            return False

        self._full_config = config
        zeroconf = self.get_component(core.Const.ZEROCONF_COMPONENT_NAME)
        if not isinstance(zeroconf, core.ZeroconfComponent):
            return False

        self._netdisco = discovery.NetworkDiscovery()

        if self._config is not None:
            # Platforms ignore by config
            self._ignored_platforms: list[str] = self._config[_CONF_IGNORE]

            # Optional platforms enabled by config
            self._enabled_platforms: list[str] = self._config[_CONF_ENABLE]

        for platform in self._enabled_platforms:
            if platform in _DEFAULT_ENABLED:
                _LOGGER.warning(
                    f"Please remove {platform} from your discovery.enable "
                    + "configuration as it is now enabled by default",
                )

        self._zeroconf_instance = await zeroconf.async_get_instance()
        # Do not scan for types that have already been converted
        # as it will generate excess network traffic for questions
        # the zeroconf instance already knows the answers
        self._zeroconf_types = list(await self.controller.setup.async_get_zeroconf())

        self.controller.bus.async_listen_once(
            core.Const.EVENT_SHC_STARTED, self._schedule_first
        )

        return True

    async def _new_service_found(self, service: str, info: core.DiscoveryInfoType):
        """Handle a new service if one is found."""
        if service in _MIGRATED_SERVICE_HANDLERS:
            return

        if service in self._ignored_platforms:
            _LOGGER.info(f"Ignoring service: {service} {info}")
            return

        discovery_hash = json.dumps([service, info], sort_keys=True)
        if discovery_hash in self._already_discovered:
            _LOGGER.debug(f"Already discovered service {service} {info}.")
            return

        self._already_discovered.add(discovery_hash)

        if service in _CONFIG_ENTRY_HANDLERS:
            await self.controller.config_entries.flow.async_init(
                _CONFIG_ENTRY_HANDLERS[service],
                context={"source": core.ConfigEntrySource.DISCOVERY},
                data=info,
            )
            return

        service_details = _SERVICE_HANDLERS.get(service)

        if not service_details and service in self._enabled_platforms:
            service_details = _OPTIONAL_SERVICE_HANDLERS[service]

        # We do not know how to handle this service.
        if not service_details:
            _LOGGER.debug(f"Unknown service discovered: {service} {info}")
            return

        _LOGGER.info(f"Found new service: {service} {info}")

        if service_details.platform is None:
            await self.controller.setup.async_discover(
                service, info, service_details.component, self._full_config
            )
        else:
            await self.controller.setup.async_load_platform(
                service_details.component,
                service_details.platform,
                info,
                self._full_config,
            )

    async def _scan_devices(self, _now: dt.datetime):
        """Scan for devices."""
        try:
            results = await self.controller.async_add_executor_job(
                _discover, self._netdisco, self._zeroconf_instance, self._zeroconf_types
            )

            for result in results:
                self.controller.async_create_task(self._new_service_found(*result))
        except OSError:
            _LOGGER.error("Network is unreachable")

        self.controller.tracker.async_track_point_in_utc_time(
            self._scan_devices, core.helpers.utcnow() + self.scan_interval
        )

    @core.callback
    def _schedule_first(self, _event: core.Event):
        """Schedule the first discovery when Home Assistant starts up."""
        self.controller.tracker.async_track_point_in_utc_time(
            self._scan_devices, core.helpers.utcnow()
        )


def _discover(
    netdisco: discovery.NetworkDiscovery,
    zeroconf_instance: core.ZeroConf,
    zeroconf_types: list[str],
):
    """Discover devices."""
    results = []
    try:
        netdisco.scan(
            zeroconf_instance=zeroconf_instance, suppress_mdns_types=zeroconf_types
        )

        for disc in netdisco.discover():
            for service in netdisco.get_info(disc):
                results.append((disc, service))

    finally:
        netdisco.stop()

    return results
