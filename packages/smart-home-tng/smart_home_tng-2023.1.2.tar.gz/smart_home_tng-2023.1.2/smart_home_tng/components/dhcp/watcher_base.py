"""
DHCP Component for Smart Home - The Next Generation.

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

import abc
import ipaddress
import fnmatch
import logging
import typing

from ... import core
from .const import Const

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class WatcherBase:
    """Base class for dhcp and device tracker watching."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        address_data: dict[str, dict[str, str]],
        integration_matchers: list[core.DHCPMatcher],
    ) -> None:
        """Initialize class."""
        super().__init__()

        self._shc = shc
        self._integration_matchers = integration_matchers
        self._address_data = address_data

    @abc.abstractmethod
    async def async_stop(self) -> None:
        """Stop the watcher."""

    @abc.abstractmethod
    async def async_start(self) -> None:
        """Start the watcher."""

    def process_client(self, ip_address: str, hostname: str, mac_address: str) -> None:
        """Process a client."""
        return self._shc.run_callback_threadsafe(
            self.async_process_client,
            ip_address,
            hostname,
            mac_address,
        ).result()

    @core.callback
    def async_process_client(
        self, ip_address: str, hostname: str, mac_address: str
    ) -> None:
        """Process a client."""
        made_ip_address = ipaddress.ip_address(ip_address)

        if (
            core.helpers.is_link_local(made_ip_address)
            or core.helpers.is_loopback(made_ip_address)
            or core.helpers.is_invalid(made_ip_address)
        ):
            # Ignore self assigned addresses, loopback, invalid
            return

        data = self._address_data.get(ip_address)
        if (
            data
            and data[Const.MAC_ADDRESS] == mac_address
            and data[Const.HOSTNAME].startswith(hostname)
        ):
            # If the address data is the same no need
            # to process it
            return

        data = {Const.MAC_ADDRESS: mac_address, Const.HOSTNAME: hostname}
        self._address_data[ip_address] = data

        lowercase_hostname = hostname.lower()
        uppercase_mac = mac_address.upper()

        _LOGGER.debug(
            f"Processing updated address data for {ip_address}: mac={uppercase_mac} "
            + f"hostname={lowercase_hostname}",
            ip_address,
            uppercase_mac,
            lowercase_hostname,
        )

        matched_domains = set()
        device_domains = set()

        dev_reg = self._shc.device_registry
        if device := dev_reg.async_get_device(
            identifiers=set(), connections={(dev_reg.ConnectionType.MAC, uppercase_mac)}
        ):
            for entry_id in device.config_entries:
                if entry := self._shc.config_entries.async_get_entry(entry_id):
                    device_domains.add(entry.domain)

        for matcher in self._integration_matchers:
            domain = matcher["domain"]

            if matcher.get(Const.REGISTERED_DEVICES) and domain not in device_domains:
                continue

            if (
                matcher_mac := matcher.get(Const.MAC_ADDRESS)
            ) is not None and not fnmatch.fnmatch(uppercase_mac, matcher_mac):
                continue

            if (
                matcher_hostname := matcher.get(Const.HOSTNAME)
            ) is not None and not fnmatch.fnmatch(lowercase_hostname, matcher_hostname):
                continue

            _LOGGER.debug(f"Matched {data} against {matcher}")
            matched_domains.add(domain)

        for domain in matched_domains:
            self._shc.flow_dispatcher.create_flow(
                domain,
                {"source": core.ConfigEntrySource.DHCP},
                core.DhcpServiceInfo(
                    ip=ip_address,
                    hostname=lowercase_hostname,
                    macaddress=mac_address,
                ),
            )

    @staticmethod
    def _format_mac(mac_address: str) -> str:
        """Format a mac address for matching."""
        return core.helpers.format_mac(mac_address).replace(":", "")
