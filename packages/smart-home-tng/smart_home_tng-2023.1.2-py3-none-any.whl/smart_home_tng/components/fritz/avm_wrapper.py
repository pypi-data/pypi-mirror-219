"""
AVM FRITZ!Box Tools Integration for Smart Home - The Next Generation.

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

import functools as ft
import logging
import typing

import fritzconnection.core.exceptions as fritz_exceptions

from .connection_info import ConnectionInfo
from .const import Const
from .fritzbox_tools import FritzboxTools, _is_stopping

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class AvmWrapper(FritzboxTools):
    """Setup AVM wrapper for API calls."""

    def _service_call_action(
        self,
        service_name: str,
        service_suffix: str,
        action_name: str,
        **kwargs: typing.Any,
    ) -> dict:
        """Return service details."""

        if self._shc.is_stopping:
            _is_stopping(f"{service_name}/{action_name}")
            return {}

        if f"{service_name}{service_suffix}" not in self.connection.services:
            return {}

        try:
            result: dict = self.connection.call_action(
                f"{service_name}:{service_suffix}",
                action_name,
                **kwargs,
            )
            return result
        except fritz_exceptions.FritzSecurityError:
            _LOGGER.error(
                "Authorization Error: Please check the provided credentials and "
                + "verify that you can log into the web interface",
                exc_info=True,
            )
        except Const.FRITZ_EXCEPTIONS:
            _LOGGER.error(
                f"Service/Action Error: cannot execute service {service_name} "
                + f"with action {action_name}",
                exc_info=True,
            )
        except fritz_exceptions.FritzConnectionException:
            _LOGGER.error(
                "Connection Error: Please check the device is properly "
                + "configured for remote login",
                exc_info=True,
            )
        return {}

    async def async_get_upnp_configuration(self) -> dict[str, typing.Any]:
        """Call X_AVM-DE_UPnP service."""

        return await self._shc.async_add_executor_job(self.get_upnp_configuration)

    async def async_get_wan_link_properties(self) -> dict[str, typing.Any]:
        """Call WANCommonInterfaceConfig service."""

        return await self._shc.async_add_executor_job(
            ft.partial(self.get_wan_link_properties)
        )

    async def async_get_connection_info(self) -> ConnectionInfo:
        """Return ConnectionInfo data."""

        link_properties = await self.async_get_wan_link_properties()
        connection_info = ConnectionInfo(
            connection=link_properties.get("NewWANAccessType", "").lower(),
            mesh_role=self.mesh_role,
            wan_enabled=self.device_is_router,
        )
        _LOGGER.debug(
            f"ConnectionInfo for FritzBox {self.host}: {connection_info}",
        )
        return connection_info

    async def async_get_port_mapping(
        self, con_type: str, index: int
    ) -> dict[str, typing.Any]:
        """Call GetGenericPortMappingEntry action."""

        return await self._shc.async_add_executor_job(
            ft.partial(self.get_port_mapping, con_type, index)
        )

    async def async_get_wlan_configuration(self, index: int) -> dict[str, typing.Any]:
        """Call WLANConfiguration service."""

        return await self._shc.async_add_executor_job(
            ft.partial(self.get_wlan_configuration, index)
        )

    async def async_get_ontel_deflections(self) -> dict[str, typing.Any]:
        """Call GetDeflections action from X_AVM-DE_OnTel service."""

        return await self._shc.async_add_executor_job(
            ft.partial(self.get_ontel_deflections)
        )

    async def async_set_wlan_configuration(
        self, index: int, turn_on: bool
    ) -> dict[str, typing.Any]:
        """Call SetEnable action from WLANConfiguration service."""

        return await self._shc.async_add_executor_job(
            ft.partial(self.set_wlan_configuration, index, turn_on)
        )

    async def async_set_deflection_enable(
        self, index: int, turn_on: bool
    ) -> dict[str, typing.Any]:
        """Call SetDeflectionEnable service."""

        return await self._shc.async_add_executor_job(
            ft.partial(self.set_deflection_enable, index, turn_on)
        )

    async def async_add_port_mapping(
        self, con_type: str, port_mapping: typing.Any
    ) -> dict[str, typing.Any]:
        """Call AddPortMapping service."""

        return await self._shc.async_add_executor_job(
            ft.partial(
                self.add_port_mapping,
                con_type,
                port_mapping,
            )
        )

    async def async_set_allow_wan_access(
        self, ip_address: str, turn_on: bool
    ) -> dict[str, typing.Any]:
        """Call X_AVM-DE_HostFilter service."""

        return await self._shc.async_add_executor_job(
            ft.partial(self.set_allow_wan_access, ip_address, turn_on)
        )

    def get_upnp_configuration(self) -> dict[str, typing.Any]:
        """Call X_AVM-DE_UPnP service."""

        return self._service_call_action("X_AVM-DE_UPnP", "1", "GetInfo")

    def get_ontel_num_deflections(self) -> dict[str, typing.Any]:
        """Call GetNumberOfDeflections action from X_AVM-DE_OnTel service."""

        return self._service_call_action(
            "X_AVM-DE_OnTel", "1", "GetNumberOfDeflections"
        )

    def get_ontel_deflections(self) -> dict[str, typing.Any]:
        """Call GetDeflections action from X_AVM-DE_OnTel service."""

        return self._service_call_action("X_AVM-DE_OnTel", "1", "GetDeflections")

    def get_default_connection(self) -> dict[str, typing.Any]:
        """Call Layer3Forwarding service."""

        return self._service_call_action(
            "Layer3Forwarding", "1", "GetDefaultConnectionService"
        )

    def get_num_port_mapping(self, con_type: str) -> dict[str, typing.Any]:
        """Call GetPortMappingNumberOfEntries action."""

        return self._service_call_action(con_type, "1", "GetPortMappingNumberOfEntries")

    def get_port_mapping(self, con_type: str, index: int) -> dict[str, typing.Any]:
        """Call GetGenericPortMappingEntry action."""

        return self._service_call_action(
            con_type, "1", "GetGenericPortMappingEntry", NewPortMappingIndex=index
        )

    def get_wlan_configuration(self, index: int) -> dict[str, typing.Any]:
        """Call WLANConfiguration service."""

        return self._service_call_action("WLANConfiguration", str(index), "GetInfo")

    def get_wan_link_properties(self) -> dict[str, typing.Any]:
        """Call WANCommonInterfaceConfig service."""

        return self._service_call_action(
            "WANCommonInterfaceConfig", "1", "GetCommonLinkProperties"
        )

    def set_wlan_configuration(
        self, index: int, turn_on: bool
    ) -> dict[str, typing.Any]:
        """Call SetEnable action from WLANConfiguration service."""

        return self._service_call_action(
            "WLANConfiguration",
            str(index),
            "SetEnable",
            NewEnable="1" if turn_on else "0",
        )

    def set_deflection_enable(self, index: int, turn_on: bool) -> dict[str, typing.Any]:
        """Call SetDeflectionEnable service."""

        return self._service_call_action(
            "X_AVM-DE_OnTel",
            "1",
            "SetDeflectionEnable",
            NewDeflectionId=index,
            NewEnable="1" if turn_on else "0",
        )

    def add_port_mapping(
        self, con_type: str, port_mapping: typing.Any
    ) -> dict[str, typing.Any]:
        """Call AddPortMapping service."""

        return self._service_call_action(
            con_type, "1", "AddPortMapping", **port_mapping
        )

    def set_allow_wan_access(
        self, ip_address: str, turn_on: bool
    ) -> dict[str, typing.Any]:
        """Call X_AVM-DE_HostFilter service."""

        return self._service_call_action(
            "X_AVM-DE_HostFilter",
            "1",
            "DisallowWANAccessByIP",
            NewIPv4Address=ip_address,
            NewDisallow="0" if turn_on else "1",
        )
