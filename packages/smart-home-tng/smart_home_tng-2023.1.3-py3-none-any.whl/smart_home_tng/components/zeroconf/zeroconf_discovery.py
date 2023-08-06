"""
Zeroconf Component for Smart Home - The Next Generation.

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
import contextlib
import fnmatch
import ipaddress
import logging
import typing

import zeroconf as zc
from zeroconf import asyncio as async_zc

from ... import core
from .async_service_browser import AsyncServiceBrowser
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class ZeroconfDiscovery:
    """Discovery via zeroconf."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        zeroconf: core.ZeroConf,
        zeroconf_types: dict[str, list[dict[str, str | dict[str, str]]]],
        homekit_models: dict[str, str],
        ipv6: bool,
    ) -> None:
        """Init discovery."""
        self._shc = shc
        self._zeroconf = zeroconf
        self._zeroconf_types = zeroconf_types
        self._homekit_models = homekit_models
        self._ipv6 = ipv6

        self._async_service_browser: AsyncServiceBrowser = None

    async def async_setup(self) -> None:
        """Start discovery."""
        types = list(self._zeroconf_types)
        # We want to make sure we know about other HomeAssistant
        # instances as soon as possible to avoid name conflicts
        # so we always browse for ZEROCONF_TYPE
        for hk_type in (Const.ZEROCONF_TYPE, *Const.HOMEKIT_TYPES):
            if hk_type not in self._zeroconf_types:
                types.append(hk_type)
        _LOGGER.debug(f"Starting Zeroconf browser for: {types}")
        self._async_service_browser = AsyncServiceBrowser(
            self._ipv6, self._zeroconf, types, handlers=[self._async_service_update]
        )

    async def async_stop(self) -> None:
        """Cancel the service browser and stop processing the queue."""
        if self._async_service_browser:
            await self._async_service_browser.async_cancel()

    @core.callback
    def _async_service_update(
        self,
        zeroconf: core.ZeroConf,
        service_type: str,
        name: str,
        state_change: zc.ServiceStateChange,
    ) -> None:
        """Service state changed."""
        _LOGGER.debug(
            f"service_update: type={service_type} name={name} "
            + f"state_change={state_change}",
        )

        if state_change == zc.ServiceStateChange.Removed:
            return

        asyncio.create_task(self._process_service_update(zeroconf, service_type, name))

    async def _process_service_update(
        self, zeroconf: core.ZeroConf, service_type: str, name: str
    ) -> None:
        """Process a zeroconf update."""
        async_service_info = async_zc.AsyncServiceInfo(service_type, name)
        await async_service_info.async_request(zeroconf, 3000)

        info = _info_from_service(async_service_info)
        if not info:
            # Prevent the browser thread from collapsing
            _LOGGER.debug(f"Failed to get addresses for device {name}")
            return

        _LOGGER.debug(f"Discovered new device {name} {info}")
        props: dict[str, str] = info.properties

        # If we can handle it as a HomeKit discovery, we do that here.
        if service_type in Const.HOMEKIT_TYPES and (
            domain := _async_get_homekit_discovery_domain(self._homekit_models, props)
        ):
            self._shc.flow_dispatcher.create_flow(
                domain, {"source": core.ConfigEntrySource.HOMEKIT}, info
            )
            # Continue on here as homekit_controller
            # still needs to get updates on devices
            # so it can see when the 'c#' field is updated.
            #
            # We only send updates to homekit_controller
            # if the device is already paired in order to avoid
            # offering a second discovery for the same device
            if not _is_homekit_paired(props):
                integration = await self._shc.setup.async_get_integration(domain)
                # Since we prefer local control, if the integration that is being discovered
                # is cloud AND the homekit device is UNPAIRED we still want to discovery it.
                #
                # As soon as the device becomes paired, the config flow will be dismissed
                # in the event the user does not want to pair with Home Assistant.
                #
                if not integration.iot_class or not integration.iot_class.startswith(
                    "cloud"
                ):
                    return

        match_data: dict[str, str] = {}
        for key in Const.LOWER_MATCH_ATTRS:
            attr_value: str = getattr(info, key)
            match_data[key] = attr_value.lower()

        # Not all homekit types are currently used for discovery
        # so not all service type exist in zeroconf_types
        for matcher in self._zeroconf_types.get(service_type, []):
            if len(matcher) > 1:
                if not _match_against_data(matcher, match_data):
                    continue
                if Const.ATTR_PROPERTIES in matcher:
                    matcher_props = matcher[Const.ATTR_PROPERTIES]
                    assert isinstance(matcher_props, dict)
                    if not _match_against_props(matcher_props, props):
                        continue

            matcher_domain = matcher["domain"]
            assert isinstance(matcher_domain, str)
            self._shc.flow_dispatcher.create_flow(
                matcher_domain,
                {"source": core.ConfigEntrySource.ZEROCONF},
                info,
            )


def _info_from_service(service: async_zc.AsyncServiceInfo) -> core.ZeroconfServiceInfo:
    """Return prepared info from mDNS entries."""
    properties: dict[str, typing.Any] = {"_raw": {}}

    for key, value in service.properties.items():
        # See https://ietf.org/rfc/rfc6763.html#section-6.4 and
        # https://ietf.org/rfc/rfc6763.html#section-6.5 for expected encodings
        # for property keys and values
        try:
            key = key.decode("ascii")
        except UnicodeDecodeError:
            _LOGGER.debug(f"Ignoring invalid key provided by [{service.name}]: {key}")
            continue

        properties["_raw"][key] = value

        with contextlib.suppress(UnicodeDecodeError):
            if isinstance(value, bytes):
                properties[key] = value.decode("utf-8")

    if not (addresses := service.addresses or service.parsed_addresses()):
        return None
    if (host := _first_non_link_local_address(addresses)) is None:
        return None

    return core.ZeroconfServiceInfo(
        host=str(host),
        addresses=service.parsed_addresses(),
        port=service.port,
        hostname=service.server,
        type=service.type,
        name=service.name,
        properties=properties,
    )


def _first_non_link_local_address(
    addresses: list[bytes] | list[str],
) -> str | None:
    """Return the first ipv6 or non-link local ipv4 address, preferring IPv4."""
    for address in addresses:
        ip_addr = ipaddress.ip_address(address)
        if not ip_addr.is_link_local and ip_addr.version == 4:
            return str(ip_addr)
    # If we didn't find a good IPv4 address, check for IPv6 addresses.
    for address in addresses:
        ip_addr = ipaddress.ip_address(address)
        if not ip_addr.is_link_local and ip_addr.version == 6:
            return str(ip_addr)
    return None


def _async_get_homekit_discovery_domain(
    homekit_models: dict[str, str], props: dict[str, typing.Any]
) -> str | None:
    """Handle a HomeKit discovery.

    Return the domain to forward the discovery data to
    """
    model = None
    for key in props:
        if key.lower() == Const.HOMEKIT_MODEL:
            model = props[key]
            break

    if model is None:
        return None

    for test_model in homekit_models:
        if (
            model != test_model
            and not model.startswith((f"{test_model} ", f"{test_model}-"))
            and not fnmatch.fnmatch(model, test_model)
        ):
            continue

        return homekit_models[test_model]

    return None


def _is_homekit_paired(props: dict[str, typing.Any]) -> bool:
    """Check properties to see if a device is homekit paired."""
    if Const.HOMEKIT_PAIRED_STATUS_FLAG not in props:
        return False
    with contextlib.suppress(ValueError):
        # 0 means paired and not discoverable by iOS clients)
        return int(props[Const.HOMEKIT_PAIRED_STATUS_FLAG]) == 0
    # If we cannot tell, we assume its not paired
    return False


def _match_against_data(
    matcher: dict[str, str | dict[str, str]], match_data: dict[str, str]
) -> bool:
    """Check a matcher to ensure all values in match_data match."""
    for key in Const.LOWER_MATCH_ATTRS:
        if key not in matcher:
            continue
        if key not in match_data:
            return False
        match_val = matcher[key]
        assert isinstance(match_val, str)
        if not fnmatch.fnmatch(match_data[key], match_val):
            return False
    return True


def _match_against_props(matcher: dict[str, str], props: dict[str, str]) -> bool:
    """Check a matcher to ensure all values in props."""
    return not any(
        key
        for key in matcher
        if key not in props or not fnmatch.fnmatch(props[key].lower(), matcher[key])
    )
