"""
Simple Service Discovery Protocol (SSDP) for Smart Home - The Next Generation.

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
import typing

from async_upnp_client import utils as ssdp_util

from ... import core
from .integration_matchers import IntegrationMatchers
from .scanner import Scanner

_ssdp: typing.TypeAlias = core.SSDP


# pylint: disable=unused-variable
class SsdpComponent(_ssdp.Component):
    """The SSDP integration."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._scanner: Scanner = None

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the SSDP integration."""
        if not await super().async_setup(config):
            return False

        integration_matchers = IntegrationMatchers()
        integration_matchers.async_setup(await self._shc.setup.async_get_ssdp())

        self._scanner = scanner = Scanner(self, integration_matchers)

        asyncio.create_task(scanner.async_start())

        return True

    async def async_register_callback(
        self, callback: _ssdp.Callback, match_dict: dict[str, str] = None
    ) -> typing.Callable[[], None]:
        """Register to receive a callback on ssdp broadcast.

        Returns a callback that can be used to cancel the registration.
        """
        scanner: Scanner = self._scanner
        return await scanner.async_register_callback(callback, match_dict)

    # pylint: disable=invalid-name
    async def async_get_discovery_info_by_udn_st(
        self, udn: str, st: str
    ) -> _ssdp.ServiceInfo:
        """Fetch the discovery info cache."""
        scanner: Scanner = self._scanner
        return await scanner.async_get_discovery_info_by_udn_st(udn, st)

    async def async_get_discovery_info_by_st(self, st: str) -> list[_ssdp.ServiceInfo]:
        """Fetch all the entries matching the st."""
        scanner: Scanner = self._scanner
        return await scanner.async_get_discovery_info_by_st(st)

    async def async_get_discovery_info_by_udn(
        self, udn: str
    ) -> list[_ssdp.ServiceInfo]:
        """Fetch all the entries matching the udn."""
        scanner: Scanner = self._scanner
        return await scanner.async_get_discovery_info_by_udn(udn)

    def discovery_info_from_headers_and_description(
        self,
        combined_headers: ssdp_util.CaseInsensitiveDict,
        info_desc: typing.Mapping[str, typing.Any],
    ) -> _ssdp.ServiceInfo:
        """Convert headers and description to discovery_info."""
        ssdp_usn = combined_headers["usn"]
        ssdp_st = combined_headers.get("st")
        if isinstance(info_desc, ssdp_util.CaseInsensitiveDict):
            upnp_info = {**info_desc.as_dict()}
        else:
            upnp_info = {**info_desc}

        # Increase compatibility: depending on the message type,
        # either the ST (Search Target, from M-SEARCH messages)
        # or NT (Notification Type, from NOTIFY messages) header is mandatory
        if not ssdp_st:
            ssdp_st = combined_headers["nt"]

        # Ensure UPnP "udn" is set
        if _ssdp.ATTR_UPNP_UDN not in upnp_info:
            if udn := _udn_from_usn(ssdp_usn):
                upnp_info[_ssdp.ATTR_UPNP_UDN] = udn

        return _ssdp.ServiceInfo(
            ssdp_usn=ssdp_usn,
            ssdp_st=ssdp_st,
            ssdp_ext=combined_headers.get("ext"),
            ssdp_server=combined_headers.get("server"),
            ssdp_location=combined_headers.get("location"),
            ssdp_udn=combined_headers.get("_udn"),
            ssdp_nt=combined_headers.get("nt"),
            ssdp_headers=combined_headers,
            upnp=upnp_info,
        )


def _udn_from_usn(usn: str) -> str:
    """Get the UDN from the USN."""
    if usn is None:
        return None
    if usn.startswith("uuid:"):
        return usn.split("::")[0]
    return None
