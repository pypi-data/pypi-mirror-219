"""
Core components of Smart Home - The Next Generation.

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

# pylint: disable=unused-variable

import abc
import dataclasses
import datetime as dt
import enum
import ipaddress
import typing

from async_upnp_client import utils as ssdp_util

from .base_service_info import BaseServiceInfo
from .smart_home_controller_component import SmartHomeControllerComponent


@dataclasses.dataclass()
class _ShcServiceDescription:
    """Keys added by HA."""

    x_shc_matching_domains: set[str] = dataclasses.field(default_factory=set)


@dataclasses.dataclass()
class _SsdpServiceDescription:
    """SSDP info with optional keys."""

    ssdp_usn: str
    ssdp_st: str
    ssdp_location: str = None
    ssdp_nt: str = None
    ssdp_udn: str = None
    ssdp_ext: str = None
    ssdp_server: str = None
    ssdp_headers: typing.Mapping[str, typing.Any] = dataclasses.field(
        default_factory=dict
    )


@dataclasses.dataclass()
class _UpnpServiceDescription:
    """UPnP info."""

    upnp: typing.Mapping[str, typing.Any]


@dataclasses.dataclass()
class _ServiceInfo(
    _ShcServiceDescription,
    _SsdpServiceDescription,
    _UpnpServiceDescription,
    BaseServiceInfo,
):
    """Prepared info from ssdp/upnp entries."""


class _Change(enum.Enum):
    ALIVE = enum.auto()
    BYEBYE = enum.auto()
    UPDATE = enum.auto()


_Callback: typing.TypeAlias = typing.Callable[[_ServiceInfo, _Change], typing.Awaitable]


class _Component(SmartHomeControllerComponent):
    """Required base class for the Simple Service Discovery Protocol component."""

    @abc.abstractmethod
    async def async_register_callback(
        self,
        callback: _Callback,
        match_dict: dict[str, str] = None,
    ) -> typing.Callable[[], None]:
        """Register to receive a callback on ssdp broadcast.

        Returns a callback that can be used to cancel the registration.
        """

    # pylint: disable=invalid-name
    @abc.abstractmethod
    async def async_get_discovery_info_by_udn_st(
        self, udn: str, st: str
    ) -> _ServiceInfo:
        """Fetch the discovery info cache."""

    @abc.abstractmethod
    async def async_get_discovery_info_by_st(self, st: str) -> list[_ServiceInfo]:
        """Fetch all the entries matching the st."""

    @abc.abstractmethod
    async def async_get_discovery_info_by_udn(self, udn: str) -> list[_ServiceInfo]:
        """Fetch all the entries matching the udn."""

    @abc.abstractmethod
    def discovery_info_from_headers_and_description(
        self,
        combined_headers: ssdp_util.CaseInsensitiveDict,
        info_desc: typing.Mapping[str, typing.Any],
    ) -> _ServiceInfo:
        """Convert headers and description to discovery_info."""


# pylint: disable=invalid-name
class SSDP:
    """Simple Service Discovery Protocol (SSDP) namespace."""

    Callback: typing.TypeAlias = _Callback
    Change: typing.TypeAlias = _Change
    Component: typing.TypeAlias = _Component
    ServiceInfo: typing.TypeAlias = _ServiceInfo

    # Constants for the Simple Service Discovery Protocol.

    SCAN_INTERVAL: typing.Final = dt.timedelta(minutes=2)

    IPV4_BROADCAST: typing.Final = ipaddress.IPv4Address("255.255.255.255")

    # Attributes for accessing info from SSDP response
    ATTR_SSDP_LOCATION: typing.Final = "ssdp_location"
    ATTR_SSDP_ST: typing.Final = "ssdp_st"
    ATTR_SSDP_NT: typing.Final = "ssdp_nt"
    ATTR_SSDP_UDN: typing.Final = "ssdp_udn"
    ATTR_SSDP_USN: typing.Final = "ssdp_usn"
    ATTR_SSDP_EXT: typing.Final = "ssdp_ext"
    ATTR_SSDP_SERVER: typing.Final = "ssdp_server"
    ATTR_SSDP_BOOTID: typing.Final = "BOOTID.UPNP.ORG"
    ATTR_SSDP_NEXTBOOTID: typing.Final = "NEXTBOOTID.UPNP.ORG"
    # Attributes for accessing info from retrieved UPnP device description
    ATTR_ST: typing.Final = "st"
    ATTR_NT: typing.Final = "nt"
    ATTR_UPNP_DEVICE_TYPE: typing.Final = "deviceType"
    ATTR_UPNP_FRIENDLY_NAME: typing.Final = "friendlyName"
    ATTR_UPNP_MANUFACTURER: typing.Final = "manufacturer"
    ATTR_UPNP_MANUFACTURER_URL: typing.Final = "manufacturerURL"
    ATTR_UPNP_MODEL_DESCRIPTION: typing.Final = "modelDescription"
    ATTR_UPNP_MODEL_NAME: typing.Final = "modelName"
    ATTR_UPNP_MODEL_NUMBER: typing.Final = "modelNumber"
    ATTR_UPNP_MODEL_URL: typing.Final = "modelURL"
    ATTR_UPNP_SERIAL: typing.Final = "serialNumber"
    ATTR_UPNP_SERVICE_LIST: typing.Final = "serviceList"
    ATTR_UPNP_UDN: typing.Final = "UDN"
    ATTR_UPNP_UPC: typing.Final = "UPC"
    ATTR_UPNP_PRESENTATION_URL: typing.Final = "presentationURL"
    # Attributes for accessing info added by Home Assistant
    ATTR_SHC_MATCHING_DOMAINS: typing.Final = "x_smart_home_tng_matching_domains"

    PRIMARY_MATCH_KEYS: typing.Final = [
        ATTR_UPNP_MANUFACTURER,
        ATTR_ST,
        ATTR_UPNP_DEVICE_TYPE,
        ATTR_NT,
        ATTR_UPNP_MANUFACTURER_URL,
    ]
