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
import ipaddress
import logging
import typing

from async_upnp_client import aiohttp as ssdp_http
from async_upnp_client import const as ssdp_const
from async_upnp_client import description_cache as ssdp_dc
from async_upnp_client import ssdp
from async_upnp_client import ssdp_listener as ssdp_li
from async_upnp_client import utils as ssdp_util

from ... import core
from .integration_matchers import IntegrationMatchers

_ssdp: typing.TypeAlias = core.SSDP

_LOGGER: typing.Final = logging.getLogger(__name__)
_SSDP_SOURCE_SSDP_CHANGE_MAPPING: typing.Final[
    typing.Mapping[ssdp_li.SsdpSource, _ssdp.Change]
] = {
    ssdp_li.SsdpSource.SEARCH_ALIVE: _ssdp.Change.ALIVE,
    ssdp_li.SsdpSource.SEARCH_CHANGED: _ssdp.Change.ALIVE,
    ssdp_li.SsdpSource.ADVERTISEMENT_ALIVE: _ssdp.Change.ALIVE,
    ssdp_li.SsdpSource.ADVERTISEMENT_BYEBYE: _ssdp.Change.BYEBYE,
    ssdp_li.SsdpSource.ADVERTISEMENT_UPDATE: _ssdp.Change.UPDATE,
}


# pylint: disable=unused-variable
class Scanner:
    """Class to manage SSDP searching and SSDP advertisements."""

    def __init__(
        self, owner: _ssdp.Component, integration_matchers: IntegrationMatchers
    ) -> None:
        """Initialize class."""
        self._owner = owner
        self._cancel_scan: typing.Callable[[], None] = None
        self._ssdp_listeners: list[ssdp_li.SsdpListener] = []
        self._callbacks: list[tuple[_ssdp.Callback, dict[str, str]]] = []
        self._description_cache: ssdp_dc.DescriptionCache = None
        self._integration_matchers = integration_matchers

    @property
    def _ssdp_devices(self) -> list[ssdp_li.SsdpDevice]:
        """Get all seen devices."""
        return [
            ssdp_device
            for ssdp_listener in self._ssdp_listeners
            for ssdp_device in ssdp_listener.devices.values()
        ]

    @property
    def _all_headers_from_ssdp_devices(
        self,
    ) -> dict[tuple[str, str], ssdp_util.CaseInsensitiveDict]:
        return {
            (ssdp_device.udn, dst): headers
            for ssdp_device in self._ssdp_devices
            for dst, headers in ssdp_device.all_combined_headers.items()
        }

    async def async_register_callback(
        self, callback: _ssdp.Callback, match_dict: dict[str, str] = None
    ) -> typing.Callable[[], None]:
        """Register a callback."""
        if match_dict is None:
            lower_match_dict = {}
        else:
            lower_match_dict = {k.lower(): v for k, v in match_dict.items()}

        # Make sure any entries that happened
        # before the callback was registered are fired
        for headers in self._all_headers_from_ssdp_devices.values():
            if _async_headers_match(headers, lower_match_dict):
                await _async_process_callbacks(
                    [callback],
                    await self._async_headers_to_discovery_info(headers),
                    _ssdp.Change.ALIVE,
                )

        callback_entry = (callback, lower_match_dict)
        self._callbacks.append(callback_entry)

        @core.callback
        def _async_remove_callback() -> None:
            self._callbacks.remove(callback_entry)

        return _async_remove_callback

    async def async_stop(self, *_: typing.Any) -> None:
        """Stop the scanner."""
        assert self._cancel_scan is not None
        self._cancel_scan()

        await self._async_stop_ssdp_listeners()

    async def _async_stop_ssdp_listeners(self) -> None:
        """Stop the SSDP listeners."""
        await asyncio.gather(
            *(listener.async_stop() for listener in self._ssdp_listeners),
            return_exceptions=True,
        )

    async def _async_build_source_set(
        self,
    ) -> set[ipaddress.IPv4Address | ipaddress.IPv6Address]:
        """Build the list of ssdp sources."""
        network = self._owner.controller.components.network
        if not isinstance(network, core.NetworkComponent):
            return []

        return {
            source_ip
            for source_ip in await network.async_get_enabled_source_ips()
            if not source_ip.is_loopback and not source_ip.is_global
        }

    async def async_scan(self, *_: typing.Any) -> None:
        """Scan for new entries using ssdp listeners."""
        await self.async_scan_multicast()
        await self.async_scan_broadcast()

    async def async_scan_multicast(self, *_: typing.Any) -> None:
        """Scan for new entries using multicase target."""
        for ssdp_listener in self._ssdp_listeners:
            await ssdp_listener.async_search()

    async def async_scan_broadcast(self, *_: typing.Any) -> None:
        """Scan for new entries using broadcast target."""
        # Some sonos devices only seem to respond if we send to the broadcast
        # address. This matches pysonos' behavior
        # https://github.com/amelchio/pysonos/blob/d4329b4abb657d106394ae69357805269708c996/pysonos/discovery.py#L120
        for listener in self._ssdp_listeners:
            if ssdp.is_ipv4_address(listener.source):
                await listener.async_search((str(_ssdp.IPV4_BROADCAST), ssdp.SSDP_PORT))

    async def async_start(self) -> None:
        """Start the scanners."""
        shc = self._owner.controller
        session = core.HttpClient.async_get_clientsession(shc)
        requester = ssdp_http.AiohttpSessionRequester(session, True, 10)
        self._description_cache = ssdp_dc.DescriptionCache(requester)

        await self._async_start_ssdp_listeners()

        shc.bus.async_listen_once(core.Const.EVENT_SHC_STOP, self.async_stop)
        self._cancel_scan = shc.tracker.async_track_time_interval(
            self.async_scan, _ssdp.SCAN_INTERVAL
        )

        # Trigger the initial-scan.
        await self.async_scan()

    async def _async_start_ssdp_listeners(self) -> None:
        """Start the SSDP Listeners."""
        # Devices are shared between all sources.
        device_tracker = ssdp_li.SsdpDeviceTracker()
        for source_ip in await self._async_build_source_set():
            source_ip_str = str(source_ip)
            if source_ip.version == 6:
                source_tuple: ssdp_const.AddressTupleVXType = (
                    source_ip_str,
                    0,
                    0,
                    int(getattr(source_ip, "scope_id")),
                )
            else:
                source_tuple = (source_ip_str, 0)
            source, target = ssdp.determine_source_target(source_tuple)
            self._ssdp_listeners.append(
                ssdp_li.SsdpListener(
                    async_callback=self._ssdp_listener_callback,
                    source=source,
                    target=target,
                    device_tracker=device_tracker,
                )
            )
        results = await asyncio.gather(
            *(listener.async_start() for listener in self._ssdp_listeners),
            return_exceptions=True,
        )
        failed_listeners = []
        for idx, result in enumerate(results):
            if isinstance(result, Exception):
                _LOGGER.debug(
                    f"Failed to setup listener for {self._ssdp_listeners[idx].source}: "
                    + f"{result}",
                )
                failed_listeners.append(self._ssdp_listeners[idx])
        for listener in failed_listeners:
            self._ssdp_listeners.remove(listener)

    @core.callback
    def _async_get_matching_callbacks(
        self,
        combined_headers: ssdp_util.CaseInsensitiveDict,
    ) -> list[_ssdp.Callback]:
        """Return a list of callbacks that match."""
        return [
            callback
            for callback, lower_match_dict in self._callbacks
            if _async_headers_match(combined_headers, lower_match_dict)
        ]

    async def _ssdp_listener_callback(
        self,
        ssdp_device: ssdp_li.SsdpDevice,
        dst: ssdp_li.DeviceOrServiceType,
        source: ssdp_li.SsdpSource,
    ) -> None:
        """Handle a device/service change."""
        _LOGGER.debug(f"SSDP: ssdp_device: {ssdp_device}, dst: {dst}, source: {source}")

        location = ssdp_device.location
        info_desc = None
        combined_headers = ssdp_device.combined_headers(dst)
        callbacks = self._async_get_matching_callbacks(combined_headers)
        matching_domains: set[str] = set()

        # If there are no changes from a search, do not trigger a config flow
        if source != ssdp_li.SsdpSource.SEARCH_ALIVE:
            info_desc = await self._async_get_description_dict(location) or {}
            matching_domains = self._integration_matchers.async_matching_domains(
                ssdp_util.CaseInsensitiveDict(combined_headers.as_dict(), **info_desc)
            )

        if not callbacks and not matching_domains:
            return

        if info_desc is None:
            info_desc = await self._async_get_description_dict(location) or {}
        discovery_info = self._owner.discovery_info_from_headers_and_description(
            combined_headers, info_desc
        )
        discovery_info.x_smart_home_tng_matching_domains = matching_domains
        ssdp_change = _SSDP_SOURCE_SSDP_CHANGE_MAPPING[source]
        await _async_process_callbacks(callbacks, discovery_info, ssdp_change)

        # Config flows should only be created for alive/update messages from alive devices
        if ssdp_change == core.SSDP.Change.BYEBYE:
            return

        _LOGGER.debug(f"Discovery info: {discovery_info}")

        flow = self._owner.controller.flow_dispatcher
        for domain in matching_domains:
            _LOGGER.debug(f"Discovered {domain} at {location}")
            flow.create_flow(
                domain,
                {"source": core.ConfigEntrySource.SSDP},
                discovery_info,
            )

    async def _async_get_description_dict(
        self, location: str
    ) -> typing.Mapping[str, str]:
        """Get description dict."""
        assert self._description_cache is not None
        return await self._description_cache.async_get_description_dict(location) or {}

    async def _async_headers_to_discovery_info(
        self, headers: ssdp_util.CaseInsensitiveDict
    ) -> _ssdp.ServiceInfo:
        """Combine the headers and description into discovery_info.

        Building this is a bit expensive so we only do it on demand.
        """
        assert self._description_cache is not None
        location = headers["location"]
        info_desc = (
            await self._description_cache.async_get_description_dict(location) or {}
        )
        return self._owner.discovery_info_from_headers_and_description(
            headers, info_desc
        )

    async def async_get_discovery_info_by_udn_st(  # pylint: disable=invalid-name
        self, udn: str, st: str
    ) -> _ssdp.ServiceInfo:
        """Return discovery_info for a udn and st."""
        if headers := self._all_headers_from_ssdp_devices.get((udn, st)):
            return await self._async_headers_to_discovery_info(headers)
        return None

    async def async_get_discovery_info_by_st(  # pylint: disable=invalid-name
        self, st: str
    ) -> list[_ssdp.ServiceInfo]:
        """Return matching discovery_infos for a st."""
        return [
            await self._async_headers_to_discovery_info(headers)
            for udn_st, headers in self._all_headers_from_ssdp_devices.items()
            if udn_st[1] == st
        ]

    async def async_get_discovery_info_by_udn(
        self, udn: str
    ) -> list[_ssdp.ServiceInfo]:
        """Return matching discovery_infos for a udn."""
        return [
            await self._async_headers_to_discovery_info(headers)
            for udn_st, headers in self._all_headers_from_ssdp_devices.items()
            if udn_st[0] == udn
        ]


@core.callback
def _async_headers_match(
    headers: ssdp_util.CaseInsensitiveDict, lower_match_dict: dict[str, str]
) -> bool:
    for header, val in lower_match_dict.items():
        if val == core.Const.MATCH_ALL:
            if header not in headers:
                return False
        elif headers.get_lower(header) != val:
            return False
    return True


async def _async_process_callbacks(
    callbacks: list[_ssdp.Callback],
    discovery_info: _ssdp.ServiceInfo,
    ssdp_change: _ssdp.Change,
) -> None:
    for callback in callbacks:
        try:
            await callback(discovery_info, ssdp_change)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception(f"Failed to callback info: {discovery_info}")
