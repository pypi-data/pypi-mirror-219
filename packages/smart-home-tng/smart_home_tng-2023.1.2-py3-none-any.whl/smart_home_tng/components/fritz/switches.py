"""
AVM FRITZ!SmartHome Integration for Smart Home - The Next Generation.

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

import xmltodict

from ... import core
from .avm_wrapper import AvmWrapper
from .const import Const
from .fritz_data import FritzData
from .fritzbox_defection_switch import FritzboxDeflectionSwitch
from .fritzbox_port_switch import FritzboxPortSwitch
from .fritzbox_profile_switch import FritzboxProfileSwitch
from .fritzbox_tracker import _device_filter_out_from_trackers
from .fritzbox_wifi_switch import FritzboxWifiSwitch

if not typing.TYPE_CHECKING:

    class FritzboxToolsIntegration:
        pass


if typing.TYPE_CHECKING:
    from .fritzbox_tools_integration import FritzboxToolsIntegration


_LOGGER: typing.Final = logging.getLogger(__name__)


def _deflection_entities_list(
    owner: core.SmartHomeControllerComponent,
    avm_wrapper: AvmWrapper,
    device_friendly_name: str,
) -> list[FritzboxDeflectionSwitch]:
    """Get list of deflection entities."""

    _LOGGER.debug(f"Setting up {Const.SWITCH_TYPE_DEFLECTION} switches")

    deflections_response = avm_wrapper.get_ontel_num_deflections()
    if not deflections_response:
        _LOGGER.debug(f"The FRITZ!Box has no {Const.SWITCH_TYPE_DEFLECTION} options")
        return []

    _LOGGER.debug(
        f"Specific {Const.SWITCH_TYPE_DEFLECTION} response: "
        + f"GetNumberOfDeflections={deflections_response}",
    )

    if deflections_response["NewNumberOfDeflections"] == 0:
        _LOGGER.debug(f"The FRITZ!Box has no {Const.SWITCH_TYPE_DEFLECTION} options")
        return []

    if not (deflection_list := avm_wrapper.get_ontel_deflections()):
        return []

    items = xmltodict.parse(deflection_list["NewDeflectionList"])["List"]["Item"]
    if not isinstance(items, list):
        items = [items]

    return [
        FritzboxDeflectionSwitch(
            owner, avm_wrapper, device_friendly_name, dict_of_deflection
        )
        for dict_of_deflection in items
    ]


def _port_entities_list(
    owner: core.SmartHomeControllerComponent,
    avm_wrapper: AvmWrapper,
    device_friendly_name: str,
    local_ip: str,
) -> list[FritzboxPortSwitch]:
    """Get list of port forwarding entities."""

    _LOGGER.debug(f"Setting up {Const.SWITCH_TYPE_PORTFORWARD} switches")
    entities_list: list[FritzboxPortSwitch] = []
    if not avm_wrapper.device_conn_type:
        _LOGGER.debug(f"The FRITZ!Box has no {Const.SWITCH_TYPE_PORTFORWARD} options")
        return []

    # Query port forwardings and setup a switch for each forward for the current device
    resp = avm_wrapper.get_num_port_mapping(avm_wrapper.device_conn_type)
    if not resp:
        _LOGGER.debug(f"The FRITZ!Box has no {Const.SWITCH_TYPE_PORTFORWARD} options")
        return []

    port_forwards_count: int = resp["NewPortMappingNumberOfEntries"]

    _LOGGER.debug(
        f"Specific {Const.SWITCH_TYPE_PORTFORWARD} response: "
        + f"GetPortMappingNumberOfEntries={port_forwards_count}",
    )

    _LOGGER.debug(f"IP source for {avm_wrapper.host} is {local_ip}")

    for i in range(port_forwards_count):
        portmap = avm_wrapper.get_port_mapping(avm_wrapper.device_conn_type, i)
        if not portmap:
            _LOGGER.debug(
                f"The FRITZ!Box has no {Const.SWITCH_TYPE_PORTFORWARD} options"
            )
            continue

        _LOGGER.debug(
            f"Specific {Const.SWITCH_TYPE_PORTFORWARD} response: "
            + f"GetGenericPortMappingEntry={portmap}",
        )

        # We can only handle port forwards of the given device
        if portmap["NewInternalClient"] == local_ip:
            port_name = portmap["NewPortMappingDescription"]
            for entity in entities_list:
                if entity.port_mapping and (
                    port_name in entity.port_mapping["NewPortMappingDescription"]
                ):
                    port_name = f"{port_name} {portmap['NewExternalPort']}"
            entities_list.append(
                FritzboxPortSwitch(
                    owner,
                    avm_wrapper,
                    device_friendly_name,
                    portmap,
                    port_name,
                    i,
                    avm_wrapper.device_conn_type,
                )
            )

    return entities_list


def _wifi_entities_list(
    owner: core.SmartHomeControllerComponent,
    avm_wrapper: AvmWrapper,
    device_friendly_name: str,
) -> list[FritzboxWifiSwitch]:
    """Get list of wifi entities."""
    _LOGGER.debug(f"Setting up {Const.SWITCH_TYPE_WIFINETWORK} switches")

    #
    # https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/wlanconfigSCPD.pdf
    #
    wifi_count = len(
        [
            s
            for s in avm_wrapper.connection.services
            if s.startswith("WLANConfiguration")
        ]
    )
    _LOGGER.debug(f"WiFi networks count: {wifi_count}")
    networks: dict = {}
    for i in range(1, wifi_count + 1):
        network_info = avm_wrapper.connection.call_action(
            f"WLANConfiguration{i}", "GetInfo"
        )
        # Devices with 4 WLAN services, use the 2nd for internal communications
        if not (wifi_count == 4 and i == 2):
            networks[i] = {
                "ssid": network_info["NewSSID"],
                "bssid": network_info["NewBSSID"],
                "standard": network_info["NewStandard"],
                "enabled": network_info["NewEnable"],
                "status": network_info["NewStatus"],
            }
    for i, network in networks.copy().items():
        networks[i]["switch_name"] = network["ssid"]
        if (
            len(
                [
                    j
                    for j, n in networks.items()
                    if core.helpers.slugify(n["ssid"])
                    == core.helpers.slugify(network["ssid"])
                ]
            )
            > 1
        ):
            networks[i]["switch_name"] += f" ({Const.WIFI_STANDARD[i]})"

    _LOGGER.debug(f"WiFi networks list: {networks}")
    return [
        FritzboxWifiSwitch(
            owner, avm_wrapper, device_friendly_name, index, data["switch_name"]
        )
        for index, data in networks.items()
    ]


def _profile_entities_list(
    owner: core.SmartHomeControllerComponent,
    avm_wrapper: AvmWrapper,
    data_fritz: FritzData,
) -> list[FritzboxProfileSwitch]:
    """Add new tracker entities from the AVM device."""
    _LOGGER.debug(f"Setting up {Const.SWITCH_TYPE_PROFILE} switches")

    new_profiles: list[FritzboxProfileSwitch] = []

    if "X_AVM-DE_HostFilter1" not in avm_wrapper.connection.services:
        return new_profiles

    if avm_wrapper.unique_id not in data_fritz.profile_switches:
        data_fritz.profile_switches[avm_wrapper.unique_id] = set()

    for mac, device in avm_wrapper.devices.items():
        if _device_filter_out_from_trackers(
            mac, device, data_fritz.profile_switches.values()
        ):
            _LOGGER.debug(
                f"Skipping profile switch creation for device {device.hostname}"
            )
            continue

        new_profiles.append(FritzboxProfileSwitch(owner, avm_wrapper, device))
        data_fritz.profile_switches[avm_wrapper.unique_id].add(mac)

    _LOGGER.debug(f"Creating {len(new_profiles)} profile switches")
    return new_profiles


def _all_entities_list(
    owner: core.SmartHomeControllerComponent,
    avm_wrapper: AvmWrapper,
    device_friendly_name: str,
    data_fritz: FritzData,
    local_ip: str,
) -> list[core.Entity]:
    """Get a list of all entities."""

    if avm_wrapper.mesh_role == Const.MeshRole.SLAVE:
        return []

    return [
        *_deflection_entities_list(owner, avm_wrapper, device_friendly_name),
        *_port_entities_list(owner, avm_wrapper, device_friendly_name, local_ip),
        *_wifi_entities_list(owner, avm_wrapper, device_friendly_name),
        *_profile_entities_list(owner, avm_wrapper, data_fritz),
    ]


# pylint: disable=unused-variable
async def async_setup_switches(
    owner: FritzboxToolsIntegration,
    entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up entry."""
    _LOGGER.debug("Setting up switches")
    avm_wrapper = owner.wrappers[entry.entry_id]
    data_fritz = owner.data

    _LOGGER.debug(f"Fritzbox services: {avm_wrapper.connection.services}")

    network: core.NetworkComponent = owner.controller.components.network
    local_ip = await network.async_get_source_ip(target_ip=avm_wrapper.host)

    entities_list = await owner.controller.async_add_executor_job(
        _all_entities_list,
        owner,
        avm_wrapper,
        entry.title,
        data_fritz,
        local_ip,
    )

    async_add_entities(entities_list)

    @core.callback
    def update_avm_device() -> None:
        """Update the values of the AVM device."""
        async_add_entities(_profile_entities_list(owner, avm_wrapper, data_fritz))

    entry.async_on_unload(
        owner.controller.dispatcher.async_connect(
            avm_wrapper.signal_device_new, update_avm_device
        )
    )
