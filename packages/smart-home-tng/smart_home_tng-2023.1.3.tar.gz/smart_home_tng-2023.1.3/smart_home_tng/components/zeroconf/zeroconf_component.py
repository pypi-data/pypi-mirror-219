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
import ipaddress
import logging
import socket
import sys
import typing

import voluptuous as vol
import zeroconf as zc
from zeroconf import asyncio as async_zc

from ... import core
from .const import Const
from .zeroconf_discovery import ZeroconfDiscovery

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class ZeroconfComponent(core.ZeroconfComponent):
    """Support for exposing Home Assistant via Zeroconf."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._discovery: ZeroconfDiscovery = None
        self._aio_zc: core.AsyncZeroConf = None

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        """Validate configuration."""
        schema = vol.Schema(
            {
                self.domain: vol.All(
                    _cv.deprecated(Const.CONF_DEFAULT_INTERFACE),
                    _cv.deprecated(Const.CONF_IPV6),
                    vol.Schema(
                        {
                            vol.Optional(Const.CONF_DEFAULT_INTERFACE): _cv.boolean,
                            vol.Optional(
                                Const.CONF_IPV6, default=Const.DEFAULT_IPV6
                            ): _cv.boolean,
                        }
                    ),
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up Zeroconf and make Home Assistant discoverable."""
        if not await super().async_setup(config):
            return False

        network = self.controller.components.network
        if not isinstance(network, core.NetworkComponent):
            return False

        shc = self._shc
        zc_args: dict = {"ip_version": 1}

        adapters = await network.async_get_adapters()

        ipv6 = False
        if _async_zc_has_functional_dual_stack():
            if any(adapter["enabled"] and adapter["ipv6"] for adapter in adapters):
                ipv6 = True
                zc_args["ip_version"] = 3
        elif not any(adapter["enabled"] and adapter["ipv4"] for adapter in adapters):
            zc_args["ip_version"] = 2
            ipv6 = True

        if not ipv6 and network.async_only_default_interface_enabled(adapters):
            zc_args["interfaces"] = 1
        else:
            zc_args["interfaces"] = [
                str(source_ip)
                for source_ip in await network.async_get_enabled_source_ips()
                if not source_ip.is_loopback
                and not (
                    isinstance(source_ip, ipaddress.IPv6Address) and source_ip.is_global
                )
                and not (
                    isinstance(source_ip, ipaddress.IPv6Address)
                    and zc_args["ip_version"] == 1
                )
                and not (
                    isinstance(source_ip, ipaddress.IPv4Address)
                    and zc_args["ip_version"] == 2
                )
            ]

        logging.getLogger("zeroconf").setLevel(logging.NOTSET)

        aio_zc = await self._async_get_instance(**zc_args)
        zeroconf = typing.cast(core.ZeroConf, aio_zc.zeroconf)
        zeroconf_types, homekit_models = await asyncio.gather(
            shc.setup.async_get_zeroconf(), shc.setup.async_get_homekit()
        )
        discovery = ZeroconfDiscovery(
            self._shc, zeroconf, zeroconf_types, homekit_models, ipv6
        )
        await discovery.async_setup()
        self._discovery = discovery

        shc.bus.async_listen_once(
            core.Const.EVENT_SHC_STOP, self._async_zeroconf_controller_stop
        )
        shc.bus.async_listen_once(
            core.Const.EVENT_SHC_START, self._async_zeroconf_controller_start
        )

        return True

    async def _async_stop_zeroconf(self, _event: core.Event) -> None:
        """Stop Zeroconf."""
        await self._aio_zc.shc_async_close()

    async def _async_zeroconf_controller_start(self, _event: core.Event) -> None:
        """Expose Smart Home - The Next Generation on zeroconf when it starts.

        Wait till started or otherwise HTTP is not up and running.
        """
        uuid = await self._shc.async_get_instance_id()
        await self._async_register_zc_service(uuid)

    async def _async_zeroconf_controller_stop(self, _event: core.Event) -> None:
        await self._discovery.async_stop()

    async def _async_register_zc_service(self, uuid: str) -> None:
        network = self.controller.components.network
        if not isinstance(network, core.NetworkComponent):
            return

        # Get instance UUID
        valid_location_name = _truncate_location_name_to_valid(
            self._shc.config.location_name or "Home"
        )

        params = {
            "location_name": valid_location_name,
            "uuid": uuid,
            "version": core.Const.__version__,
            "external_url": "",
            "internal_url": "",
            # Old base URL, for backward compatibility
            "base_url": "",
            # Always needs authentication
            "requires_api_password": True,
        }

        # Get instance URL's
        with contextlib.suppress(core.NoURLAvailableError):
            params["external_url"] = self._shc.get_url(allow_internal=False)

        with contextlib.suppress(core.NoURLAvailableError):
            params["internal_url"] = self._shc.get_url(allow_external=False)

        # Set old base URL based on external or internal
        params["base_url"] = params["external_url"] or params["internal_url"]

        adapters = await network.async_get_adapters()

        # Puts the default IPv4 address first in the list to preserve compatibility,
        # because some mDNS implementations ignores anything but the first announced address.
        host_ip = await network.async_get_source_ip(target_ip=core.Const.MDNS_TARGET_IP)
        host_ip_pton = None
        if host_ip:
            host_ip_pton = socket.inet_pton(socket.AF_INET, host_ip)
        address_list = _get_announced_addresses(adapters, host_ip_pton)
        _suppress_invalid_properties(params)

        info = async_zc.AsyncServiceInfo(
            Const.ZEROCONF_TYPE,
            name=f"{valid_location_name}.{Const.ZEROCONF_TYPE}",
            server=f"{uuid}.local.",
            addresses=address_list,
            port=self._shc.http.server_port,
            properties=params,
        )

        _LOGGER.info("Starting Zeroconf broadcast")
        await self._aio_zc.async_register_service(info, allow_name_change=True)

    async def async_get_instance(self) -> core.ZeroConf:
        """Zeroconf instance to be shared with other integrations that use it."""
        return typing.cast(core.ZeroConf, (await self._async_get_instance()).zeroconf)

    async def async_get_async_instance(self) -> core.AsyncZeroConf:
        """Zeroconf instance to be shared with other integrations that use it."""
        return await self._async_get_instance()

    async def _async_get_instance(self, **zcargs: typing.Any) -> core.AsyncZeroConf:
        if self._aio_zc is not None:
            return self._aio_zc

        logging.getLogger("zeroconf").setLevel(logging.NOTSET)

        zeroconf = core.ZeroConf(**zcargs)
        aio_zc = core.AsyncZeroConf(zc=zeroconf)

        _install_multiple_zeroconf_catcher(zeroconf)

        self.controller.bus.async_listen_once(
            core.Const.EVENT_SHC_STOP, self._async_stop_zeroconf
        )
        self._aio_zc = aio_zc

        return aio_zc


@core.callback
def _async_zc_has_functional_dual_stack() -> bool:
    """Return true for platforms that not support IP_ADD_MEMBERSHIP on an AF_INET6 socket.

    Zeroconf only supports a single listen socket at this time.
    """
    return not sys.platform.startswith("freebsd") and not sys.platform.startswith(
        "darwin"
    )


def _get_announced_addresses(
    adapters: list[core.Adapter],
    first_ip: bytes = None,
) -> list[bytes]:
    """Return a list of IP addresses to announce via zeroconf.

    If first_ip is not None, it will be the first address in the list.
    """
    addresses = {
        addr.packed
        for addr in [
            ipaddress.ip_address(ip["address"])
            for adapter in adapters
            if adapter["enabled"]
            for ip in typing.cast(list, adapter["ipv6"])
            + typing.cast(list, adapter["ipv4"])
        ]
        if not (addr.is_unspecified or addr.is_loopback)
    }
    if first_ip:
        address_list = [first_ip]
        address_list.extend(addresses - set({first_ip}))
    else:
        address_list = list(addresses)
    return address_list


def _suppress_invalid_properties(properties: dict) -> None:
    """Suppress any properties that will cause zeroconf to fail to startup."""

    for prop, prop_value in properties.items():
        if not isinstance(prop_value, str):
            continue

        if len(prop_value.encode("utf-8")) > Const.MAX_PROPERTY_VALUE_LEN:
            _LOGGER.error(
                f"The property '{prop}' was suppressed because it is longer than the maximum "
                + f"length of {Const.MAX_PROPERTY_VALUE_LEN:d} bytes: {prop_value}",
            )
            properties[prop] = ""


def _truncate_location_name_to_valid(location_name: str) -> str:
    """Truncate or return the location name usable for zeroconf."""
    if len(location_name.encode("utf-8")) < Const.MAX_NAME_LEN:
        return location_name

    _LOGGER.warning(
        "The location name was truncated because it is longer than the maximum length "
        + f"of {Const.MAX_NAME_LEN:d} bytes: {location_name}",
    )
    return location_name.encode("utf-8")[: Const.MAX_NAME_LEN].decode("utf-8", "ignore")


def _install_multiple_zeroconf_catcher(shc_zc: core.ZeroConf) -> None:
    """Wrap the Zeroconf class to return the shared instance if multiple instances are detected."""

    # pylint: disable=unused-argument
    def new_zeroconf_new(
        self: zc.Zeroconf, *k: typing.Any, **kw: typing.Any
    ) -> core.ZeroConf:
        core.helpers.report(
            "attempted to create another Zeroconf instance. Please use the shared "
            + "Zeroconf via await "
            + "homeassistant.components.zeroconf.async_get_instance(hass)",
            exclude_integrations={"zeroconf"},
            error_if_core=False,
        )
        return shc_zc

    def new_zeroconf_init(self: zc.Zeroconf, *k: typing.Any, **kw: typing.Any) -> None:
        return

    zc.Zeroconf.__new__ = new_zeroconf_new
    zc.Zeroconf.__init__ = new_zeroconf_init
