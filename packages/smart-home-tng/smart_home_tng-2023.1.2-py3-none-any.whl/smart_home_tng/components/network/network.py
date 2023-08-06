"""
Network Component for Smart Home - The Next Generation.

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

import ipaddress
import logging
import socket
import typing

import ifaddr

from ... import core
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class Network:
    """Network helper class for the network integration."""

    def __init__(self, shc: core.SmartHomeController) -> None:
        """Initialize the Network class."""
        self._store = core.Store[dict[str, list[str]]](
            shc, Const.STORAGE_VERSION, Const.STORAGE_KEY, atomic_writes=True
        )
        self._data: dict[str, list[str]] = {}
        self._adapters: list[core.Adapter] = []

    @property
    def adapters(self) -> list[core.Adapter]:
        return self._adapters

    @property
    def configured_adapters(self) -> list[str]:
        """Return the configured adapters."""
        return self._data.get(
            Const.ATTR_CONFIGURED_ADAPTERS, Const.DEFAULT_CONFIGURED_ADAPTERS
        )

    async def async_setup(self) -> None:
        """Set up the network config."""
        await self.async_load()
        self._adapters = await _async_load_adapters()

    @core.callback
    def async_configure(self) -> None:
        """Configure from storage."""
        if not _enable_adapters(self._adapters, self.configured_adapters):
            _enable_auto_detected_adapters(self.adapters)

    async def async_reconfig(self, config: dict[str, typing.Any]) -> None:
        """Reconfigure network."""
        self._data[Const.ATTR_CONFIGURED_ADAPTERS] = config[
            Const.ATTR_CONFIGURED_ADAPTERS
        ]
        self.async_configure()
        await self._async_save()

    async def async_load(self) -> None:
        """Load config."""
        if stored := await self._store.async_load():
            self._data = stored

    async def _async_save(self) -> None:
        """Save preferences."""
        await self._store.async_save(self._data)

    async def async_get_adapters(self) -> list[core.Adapter]:
        """Get the network adapter configuration."""
        return self.adapters

    # pylint: disable=protected-access
    async def async_get_source_ipv4(
        self, target_ip: str | object = core.NetworkComponent._UNDEFINED
    ) -> str:
        """Get the source ip for a target ip."""
        adapters = self.adapters
        all_ipv4s = []
        for adapter in adapters:
            if adapter["enabled"] and (ipv4s := adapter["ipv4"]):
                all_ipv4s.extend([ipv4["address"] for ipv4 in ipv4s])

        # pylint: disable=protected-access
        if target_ip is core.NetworkComponent._UNDEFINED:
            source_ip = (
                _async_get_source_ip(Const.PUBLIC_TARGET_IP)
                or _async_get_source_ip(core.Const.MDNS_TARGET_IP)
                or _async_get_source_ip(Const.LOOPBACK_TARGET_IP)
            )
        else:
            source_ip = _async_get_source_ip(target_ip)

        if not all_ipv4s:
            _LOGGER.warning(
                "Because the system does not have any enabled IPv4 addresses, "
                + "source address detection may be inaccurate"
            )
            if source_ip is None:
                raise core.SmartHomeControllerError(
                    "Could not determine source ip because the system does not have "
                    + "any enabled IPv4 addresses and creating a socket failed"
                )
            return source_ip

        return source_ip if source_ip in all_ipv4s else all_ipv4s[0]

    async def async_get_enabled_source_ips(
        self,
    ) -> list[ipaddress.IPv4Address | ipaddress.IPv6Address]:
        """Build the list of enabled source ips."""
        adapters = self.adapters
        sources: list[ipaddress.IPv4Address | ipaddress.IPv6Address] = []
        for adapter in adapters:
            if not adapter["enabled"]:
                continue
            if adapter["ipv4"]:
                addrs_ipv4 = [
                    ipaddress.IPv4Address(ipv4["address"]) for ipv4 in adapter["ipv4"]
                ]
                sources.extend(addrs_ipv4)
            if adapter["ipv6"]:
                addrs_ipv6 = [
                    ipaddress.IPv6Address(f"{ipv6['address']}%{ipv6['scope_id']}")
                    for ipv6 in adapter["ipv6"]
                ]
                sources.extend(addrs_ipv6)

        return sources

    @staticmethod
    @core.callback
    def async_only_default_interface_enabled(adapters: list[core.Adapter]) -> bool:
        """Check to see if any non-default adapter is enabled."""
        return not any(
            adapter["enabled"] and not adapter["default"] for adapter in adapters
        )

    async def async_get_ipv4_broadcast_addresses(
        self,
    ) -> set[ipaddress.IPv4Address]:
        """Return a set of broadcast addresses."""
        broadcast_addresses: set[ipaddress.IPv4Address] = {
            ipaddress.IPv4Address(Const.IPV4_BROADCAST_ADDR)
        }
        adapters = self.adapters
        if self.async_only_default_interface_enabled(adapters):
            return broadcast_addresses
        for adapter in adapters:
            if not adapter["enabled"]:
                continue
            for ip_info in adapter["ipv4"]:
                interface = ipaddress.ip_interface(
                    f"{ip_info['address']}/{ip_info['network_prefix']}"
                )
                broadcast_addresses.add(
                    ipaddress.IPv4Address(interface.network.broadcast_address.exploded)
                )
        return broadcast_addresses


async def _async_load_adapters() -> list[core.Adapter]:
    """Load adapters."""
    source_ip = _async_get_source_ip(core.Const.MDNS_TARGET_IP)
    source_ip_address = ipaddress.ip_address(source_ip) if source_ip else None

    shc_adapters: list[core.Adapter] = [
        _ifaddr_adapter_to_shc(adapter, source_ip_address)
        for adapter in ifaddr.get_adapters()
    ]

    if not any(adapter["default"] and adapter["auto"] for adapter in shc_adapters):
        for adapter in shc_adapters:
            if _adapter_has_external_address(adapter):
                adapter["auto"] = True

    return shc_adapters


@core.callback
def _async_get_source_ip(target_ip: str) -> str:
    """Return the source ip that will reach target_ip."""
    test_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    test_sock.setblocking(False)  # must be non-blocking for async
    try:
        test_sock.connect((target_ip, 1))
        return typing.cast(str, test_sock.getsockname()[0])
    except Exception:  # pylint: disable=broad-except
        _LOGGER.debug(
            "The system could not auto detect the source ip for "
            + f"{target_ip} on your operating system"
        )
        return None
    finally:
        test_sock.close()


def _ifaddr_adapter_to_shc(
    adapter: core.Adapter,
    next_hop_address: None | ipaddress.IPv4Address | ipaddress.IPv6Address,
) -> core.Adapter:
    """Convert an ifaddr adapter to ha."""
    ip_v4s: list[core.IPv4ConfiguredAddress] = []
    ip_v6s: list[core.IPv6ConfiguredAddress] = []
    default = False
    auto = False

    for ip_config in adapter.ips:
        if ip_config.is_IPv6:
            ip_addr = ipaddress.ip_address(ip_config.ip[0])
            ip_v6s.append(_ip_v6_from_adapter(ip_config))
        else:
            ip_addr = ipaddress.ip_address(ip_config.ip)
            ip_v4s.append(_ip_v4_from_adapter(ip_config))

        if ip_addr == next_hop_address:
            default = True
            if _ip_address_is_external(ip_addr):
                auto = True

    return {
        "name": adapter.nice_name,
        "index": adapter.index,
        "enabled": False,
        "auto": auto,
        "default": default,
        "ipv4": ip_v4s,
        "ipv6": ip_v6s,
    }


def _adapter_has_external_address(adapter: core.Adapter) -> bool:
    """Adapter has a non-loopback and non-link-local address."""
    return any(
        _has_external_address(v4_config["address"]) for v4_config in adapter["ipv4"]
    ) or any(
        _has_external_address(v6_config["address"]) for v6_config in adapter["ipv6"]
    )


def _has_external_address(ip_str: str) -> bool:
    return _ip_address_is_external(ipaddress.ip_address(ip_str))


def _ip_address_is_external(
    ip_addr: ipaddress.IPv4Address | ipaddress.IPv6Address,
) -> bool:
    return (
        not ip_addr.is_multicast
        and not ip_addr.is_loopback
        and not ip_addr.is_link_local
    )


def _ip_v6_from_adapter(ip_config: ifaddr.IP) -> core.IPv6ConfiguredAddress:
    return {
        "address": ip_config.ip[0],
        "flowinfo": ip_config.ip[1],
        "scope_id": ip_config.ip[2],
        "network_prefix": ip_config.network_prefix,
    }


def _ip_v4_from_adapter(ip_config: ifaddr.IP) -> core.IPv4ConfiguredAddress:
    return {
        "address": ip_config.ip,
        "network_prefix": ip_config.network_prefix,
    }


def _enable_adapters(
    adapters: list[core.Adapter], enabled_interfaces: list[str]
) -> bool:
    """Enable configured adapters."""
    _reset_enabled_adapters(adapters)

    if not enabled_interfaces:
        return False

    found_adapter = False
    for adapter in adapters:
        if adapter["name"] in enabled_interfaces:
            adapter["enabled"] = True
            found_adapter = True

    return found_adapter


def _enable_auto_detected_adapters(adapters: list[core.Adapter]) -> None:
    """Enable auto detected adapters."""
    _enable_adapters(
        adapters, [adapter["name"] for adapter in adapters if adapter["auto"]]
    )


def _reset_enabled_adapters(adapters: list[core.Adapter]) -> None:
    for adapter in adapters:
        adapter["enabled"] = False
