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

import logging
import typing

import voluptuous as vol

from ... import core
from .const import Const

if not typing.TYPE_CHECKING:

    class FritzboxToolsIntegration:
        pass


if typing.TYPE_CHECKING:
    from .fritzbox_tools_integration import FritzboxToolsIntegration


_LOGGER: typing.Final = logging.getLogger(__name__)
_SERVICE_SCHEMA_SET_GUEST_WIFI_PW: typing.Final = vol.Schema(
    {
        vol.Required("device_id"): str,
        vol.Optional("password"): vol.Length(min=8, max=63),
        vol.Optional("length"): vol.Range(min=8, max=63),
    }
)

_SERVICE_LIST: typing.Final[list[tuple[str, vol.Schema]]] = [
    (Const.SERVICE_CLEANUP, None),
    (Const.SERVICE_REBOOT, None),
    (Const.SERVICE_RECONNECT, None),
    (Const.SERVICE_SET_GUEST_WIFI_PW, _SERVICE_SCHEMA_SET_GUEST_WIFI_PW),
]


# pylint: disable=unused-variable
async def async_setup_services(tools: FritzboxToolsIntegration) -> bool:
    """Set up services for Fritz integration."""

    shc = tools.controller

    for service, _ in _SERVICE_LIST:
        if shc.services.has_service(tools.domain, service):
            return False

    async def async_call_fritz_service(service_call: core.ServiceCall) -> None:
        """Call correct Fritz service."""

        if not (
            fritzbox_entry_ids := await _async_get_configured_avm_device(
                tools, service_call
            )
        ):
            raise core.SmartHomeControllerError(
                f"Failed to call service '{service_call.service}'. "
                + "Config entry for target not found"
            )

        for entry_id in fritzbox_entry_ids:
            _LOGGER.debug(f"Executing service {service_call.service}")
            avm_wrapper = tools.wrappers[entry_id]
            if config_entry := shc.config_entries.async_get_entry(entry_id):
                await avm_wrapper.service_fritzbox(service_call, config_entry)
            else:
                _LOGGER.error(
                    f"Executing service {service_call.service} failed, "
                    + "no config entry found",
                )

    for service, schema in _SERVICE_LIST:
        shc.services.async_register(
            tools.domain, service, async_call_fritz_service, schema
        )
    return True


async def _async_get_configured_avm_device(
    tools: FritzboxToolsIntegration, service_call: core.ServiceCall
) -> list:
    """Get FritzBoxTools class from config entry."""

    shc = tools.controller
    list_entry_id: list = []
    for entry_id in await core.Service.async_extract_config_entry_ids(
        shc, service_call
    ):
        config_entry = shc.config_entries.async_get_entry(entry_id)
        if (
            config_entry
            and config_entry.domain == tools.domain
            and config_entry.state == core.ConfigEntryState.LOADED
        ):
            list_entry_id.append(entry_id)
    return list_entry_id


async def async_unload_services(tools: FritzboxToolsIntegration) -> None:
    """Unload services for Fritz integration."""

    if not tools.services_registered:
        return

    for service, _ in _SERVICE_LIST:
        tools.controller.services.async_remove(tools.domain, service)
