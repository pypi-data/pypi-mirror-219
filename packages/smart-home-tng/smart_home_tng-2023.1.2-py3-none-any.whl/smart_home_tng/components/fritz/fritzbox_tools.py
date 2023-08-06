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

import datetime as dt
import logging
import types
import typing

import fritzconnection as fritz
import fritzconnection.lib.fritzwlan as fritz_wlan
import fritzconnection.lib.fritzhosts as fritz_hosts
import fritzconnection.lib.fritzstatus as fritz_status
import fritzconnection.core.exceptions as fritz_exceptions

from ... import core
from .class_setup_missing import ClassSetupMissing
from .const import Const
from .device import Device
from .fritz_device import FritzDevice
from .host_info import HostInfo
from .interface import Interface

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class FritzboxTools(core.DataUpdateCoordinator):
    """FritzBoxTools class."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        password: str,
        username: str = Const.DEFAULT_USERNAME,
        host: str = Const.DEFAULT_HOST,
        port: int = Const.DEFAULT_PORT,
    ) -> None:
        """Initialize FritzboxTools class."""
        super().__init__(
            shc=owner.controller,
            logger=_LOGGER,
            name=f"{owner.domain}-{host}-coordinator",
            update_interval=dt.timedelta(seconds=30),
        )

        self._devices: dict[str, FritzDevice] = {}
        self._options: types.MappingProxyType[str, typing.Any] = None
        self._unique_id: str = None
        self._connection: fritz.FritzConnection = None
        self._fritz_guest_wifi: fritz_wlan.FritzGuestWLAN = None
        self._fritz_hosts: fritz_hosts.FritzHosts = None
        self._fritz_status: fritz_status.FritzStatus = None
        self._owner = owner
        self._host = host
        self._mesh_role = Const.MeshRole.NONE
        self._device_conn_type: str = None
        self._device_is_router: bool = False
        self._password = password
        self._port = port
        self._username = username
        self._model: str = None
        self._current_firmware: str = None
        self._latest_firmware: str = None
        self._update_available: bool = False
        self._release_url: str = None

    @property
    def connection(self) -> fritz.FritzConnection:
        return self._connection

    @property
    def device_conn_type(self):
        return self._device_conn_type

    @property
    def device_is_router(self):
        return self._device_is_router

    @property
    def fritz_guest_wifi(self):
        return self._fritz_guest_wifi

    @property
    def fritz_hosts(self):
        return self._fritz_hosts

    @property
    def fritz_status(self):
        return self._fritz_status

    @property
    def host(self):
        return self._host

    @property
    def mesh_role(self):
        return self._mesh_role

    @property
    def password(self):
        return self._password

    @property
    def port(self):
        return self._port

    @property
    def username(self):
        return self._username

    async def async_setup(
        self, options: types.MappingProxyType[str, typing.Any] = None
    ) -> None:
        """Wrap up FritzboxTools class setup."""
        self._options = options
        await self._shc.async_add_executor_job(self.setup)

    def setup(self) -> None:
        """Set up FritzboxTools class."""
        self._connection = fritz.FritzConnection(
            address=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            timeout=60.0,
            pool_maxsize=30,
        )

        if not self.connection:
            _LOGGER.error(f"Unable to establish a connection with {self.host}")
            return

        _LOGGER.debug(
            f"detected services on {self.host} "
            + f"{list(self.connection.services.keys())}",
        )

        self._fritz_hosts = fritz_hosts.FritzHosts(fc=self.connection)
        self._fritz_guest_wifi = fritz_wlan.FritzGuestWLAN(fc=self.connection)
        self._fritz_status = fritz_status.FritzStatus(fc=self.connection)
        info = self.connection.call_action("DeviceInfo:1", "GetInfo")

        info_dict = {
            **info,
            "NewDeviceLog": "***omitted***",
            "NewSerialNumber": "***omitted***",
        }
        _LOGGER.debug(
            f"gathered device info of {self.host} {info_dict}",
            self.host,
        )

        if not self._unique_id:
            self._unique_id = info["NewSerialNumber"]

        self._model = info.get("NewModelName")
        self._current_firmware = info.get("NewSoftwareVersion")

        (
            self._update_available,
            self._latest_firmware,
            self._release_url,
        ) = self._update_device_info()
        if "Layer3Forwarding1" in self.connection.services:
            if connection_type := self.connection.call_action(
                "Layer3Forwarding1", "GetDefaultConnectionService"
            ).get("NewDefaultConnectionService"):
                # Return NewDefaultConnectionService sample: "1.WANPPPConnection.1"
                self._device_conn_type = connection_type[2:][:-2]
                self._device_is_router = self.connection.call_action(
                    self.device_conn_type, "GetInfo"
                ).get("NewEnable")

    async def _async_update_data(self) -> None:
        """Update FritzboxTools data."""
        try:
            await self.async_scan_devices()
        except Const.FRITZ_EXCEPTIONS as ex:
            raise core.UpdateFailed(ex) from ex

    @property
    def unique_id(self) -> str:
        """Return unique id."""
        if not self._unique_id:
            raise ClassSetupMissing()
        return self._unique_id

    @property
    def model(self) -> str:
        """Return device model."""
        if not self._model:
            raise ClassSetupMissing()
        return self._model

    @property
    def current_firmware(self) -> str:
        """Return current SW version."""
        if not self._current_firmware:
            raise ClassSetupMissing()
        return self._current_firmware

    @property
    def latest_firmware(self) -> str:
        """Return latest SW version."""
        return self._latest_firmware

    @property
    def update_available(self) -> bool:
        """Return if new SW version is available."""
        return self._update_available

    @property
    def release_url(self) -> str:
        """Return the info URL for latest firmware."""
        return self._release_url

    @property
    def mac(self) -> str:
        """Return device Mac address."""
        if not self._unique_id:
            raise ClassSetupMissing()
        return core.helpers.format_mac(self._unique_id)

    @property
    def devices(self) -> dict[str, FritzDevice]:
        """Return devices."""
        return self._devices

    @property
    def signal_device_new(self) -> str:
        """Event specific per FRITZ!Box entry to signal new device."""
        return f"{self._owner.domain}-device-new-{self._unique_id}"

    @property
    def signal_device_update(self) -> str:
        """Event specific per FRITZ!Box entry to signal updates in devices."""
        return f"{self._owner.domain}-device-update-{self._unique_id}"

    def _update_hosts_info(self) -> list[HostInfo]:
        """Retrieve latest hosts information from the FRITZ!Box."""
        try:
            return self.fritz_hosts.get_hosts_info()
        except Exception as ex:  # pylint: disable=[broad-except]
            if not self._shc.is_stopping:
                raise core.SmartHomeControllerError(
                    "Error refreshing hosts info"
                ) from ex
        return []

    def _update_device_info(self) -> tuple[bool, str, str]:
        """Retrieve latest device information from the FRITZ!Box."""
        info = self.connection.call_action("UserInterface1", "GetInfo")
        version = info.get("NewX_AVM-DE_Version")
        release_url = info.get("NewX_AVM-DE_InfoURL")
        return bool(version), version, release_url

    def _get_wan_access(self, ip_address: str) -> bool:
        """Get WAN access rule for given IP address."""
        try:
            return not self.connection.call_action(
                "X_AVM-DE_HostFilter:1",
                "GetWANAccessByIP",
                NewIPv4Address=ip_address,
            ).get("NewDisallow")
        except Const.FRITZ_EXCEPTIONS as ex:
            _LOGGER.debug(
                f"could not get WAN access rule for client device with IP '{ip_address}', "
                + f"error: {ex}",
            )
            return None

    async def async_scan_devices(self, now: dt.datetime = None) -> None:
        """Wrap up FritzboxTools class scan."""
        await self._shc.async_add_executor_job(self.scan_devices, now)

    def manage_device_info(
        self, dev_info: Device, dev_mac: str, consider_home: bool
    ) -> bool:
        """Update device lists."""
        _LOGGER.debug(f"Client dev_info: {dev_info}")

        if dev_mac in self._devices:
            self._devices[dev_mac].update(dev_info, consider_home)
            return False

        device = FritzDevice(dev_mac, dev_info.name)
        device.update(dev_info, consider_home)
        self._devices[dev_mac] = device
        return True

    def send_signal_device_update(self, new_device: bool) -> None:
        """Signal device data updated."""
        self._shc.dispatcher.send(self.signal_device_update)
        if new_device:
            self._shc.dispatcher.send(self.signal_device_new)

    def scan_devices(self, _now: dt.datetime = None) -> None:
        """Scan for new devices and return a list of found device ids."""

        if self._shc.is_stopping:
            _is_stopping("scan devices")
            return

        _LOGGER.debug(f"Checking host info for FRITZ!Box device {self.host}")
        (
            self._update_available,
            self._latest_firmware,
            self._release_url,
        ) = self._update_device_info()

        _LOGGER.debug(f"Checking devices for FRITZ!Box device {self.host}")
        _default_consider_home = (
            core.DeviceTracker.DEFAULT_CONSIDER_HOME.total_seconds()
        )
        if self._options:
            consider_home = self._options.get(
                core.DeviceTracker.CONF_CONSIDER_HOME, _default_consider_home
            )
        else:
            consider_home = _default_consider_home

        new_device = False
        hosts = {}
        for host in self._update_hosts_info():
            if not host.get("mac"):
                continue

            hosts[host["mac"]] = Device(
                name=host["name"],
                connected=host["status"],
                connected_to="",
                connection_type="",
                ip_address=host["ip"],
                ssid=None,
                wan_access=None,
            )

        if (
            "Hosts1" not in self.connection.services
            or "X_AVM-DE_GetMeshListPath"
            not in self.connection.services["Hosts1"].actions
        ) or (
            self._options
            and self._options.get(
                Const.CONF_OLD_DISCOVERY, Const.DEFAULT_CONF_OLD_DISCOVERY
            )
        ):
            _LOGGER.debug(
                "Using old hosts discovery method. (Mesh not supported or user option)"
            )
            self._mesh_role = Const.MeshRole.NONE
            for mac, info in hosts.items():
                if info.ip_address:
                    info.wan_access = self._get_wan_access(info.ip_address)
                if self.manage_device_info(info, mac, consider_home):
                    new_device = True
            self.send_signal_device_update(new_device)
            return

        try:
            if not (topology := self.fritz_hosts.get_mesh_topology()):
                # pylint: disable=broad-exception-raised
                raise Exception("Mesh supported but empty topology reported")
        except fritz_exceptions.FritzActionError:
            self._mesh_role = Const.MeshRole.SLAVE
            # Avoid duplicating device trackers
            return

        mesh_intf = {}
        # first get all meshed devices
        for node in topology.get("nodes", []):
            if not node["is_meshed"]:
                continue

            for interf in node["node_interfaces"]:
                int_mac = interf["mac_address"]
                mesh_intf[interf["uid"]] = Interface(
                    device=node["device_name"],
                    mac=int_mac,
                    op_mode=interf.get("op_mode", ""),
                    ssid=interf.get("ssid", ""),
                    type=interf["type"],
                )
                if core.helpers.format_mac(int_mac) == self.mac:
                    self._mesh_role = Const.MeshRole(node["mesh_role"])

        # second get all client devices
        for node in topology.get("nodes", []):
            if node["is_meshed"]:
                continue

            for interf in node["node_interfaces"]:
                dev_mac = interf["mac_address"]

                if dev_mac not in hosts:
                    continue

                dev_info: Device = hosts[dev_mac]

                if dev_info.ip_address:
                    dev_info.wan_access = self._get_wan_access(dev_info.ip_address)

                for link in interf["node_links"]:
                    intf = mesh_intf.get(link["node_interface_1_uid"])
                    if intf is not None:
                        if intf["op_mode"] == "AP_GUEST":
                            dev_info.wan_access = None

                        dev_info.connected_to = intf["device"]
                        dev_info.connection_type = intf["type"]
                        dev_info.ssid = intf.get("ssid")

                if self.manage_device_info(dev_info, dev_mac, consider_home):
                    new_device = True

        self.send_signal_device_update(new_device)

    async def async_trigger_firmware_update(self) -> bool:
        """Trigger firmware update."""
        results = await self._shc.async_add_executor_job(
            self.connection.call_action, "UserInterface:1", "X_AVM-DE_DoUpdate"
        )
        return typing.cast(bool, results["NewX_AVM-DE_UpdateState"])

    async def async_trigger_reboot(self) -> None:
        """Trigger device reboot."""
        await self._shc.async_add_executor_job(self.connection.reboot)

    async def async_trigger_reconnect(self) -> None:
        """Trigger device reconnect."""
        await self._shc.async_add_executor_job(self.connection.reconnect)

    async def async_trigger_set_guest_password(
        self, password: str, length: int
    ) -> None:
        """Trigger service to set a new guest wifi password."""
        await self._shc.async_add_executor_job(
            self.fritz_guest_wifi.set_password, password, length
        )

    async def async_trigger_cleanup(
        self, config_entry: core.ConfigEntry = None
    ) -> None:
        """Trigger device trackers cleanup."""
        device_hosts_list = await self._shc.async_add_executor_job(
            self.fritz_hosts.get_hosts_info
        )
        entity_reg = self._shc.entity_registry

        if config_entry is None:
            if self._config_entry is None:
                return
            config_entry = self._config_entry

        shc_entity_reg_list: list[
            core.EntityRegistryEntry
        ] = entity_reg.async_entries_for_config_entry(config_entry.entry_id)
        entities_removed: bool = False

        device_hosts_macs = set()
        device_hosts_names = set()
        for device in device_hosts_list:
            device_hosts_macs.add(device["mac"])
            device_hosts_names.add(device["name"])

        for entry in shc_entity_reg_list:
            if entry.original_name is None:
                continue
            entry_name = entry.name or entry.original_name
            entry_host = entry_name.split(" ")[0]
            entry_mac = entry.unique_id.split("_")[0]

            if not _cleanup_entity_filter(self._shc, entry) or (
                entry_mac in device_hosts_macs and entry_host in device_hosts_names
            ):
                _LOGGER.debug(
                    f"Skipping entity {entry_name} [mac={entry_mac}, host={entry_host}]",
                )
                continue
            _LOGGER.info(f"Removing entity: {entry_name}")
            entity_reg.async_remove(entry.entity_id)
            entities_removed = True

        if entities_removed:
            self._async_remove_empty_devices(entity_reg, config_entry)

    @core.callback
    def _async_remove_empty_devices(
        self, entity_reg: core.EntityRegistry, config_entry: core.ConfigEntry
    ) -> None:
        """Remove devices with no entities."""

        device_reg = self._shc.device_registry
        device_list = device_reg.async_entries_for_config_entry(config_entry.entry_id)
        for device_entry in device_list:
            if not entity_reg.async_entries_for_device(
                device_entry.id,
                include_disabled_entities=True,
            ):
                _LOGGER.info(f"Removing device: {device_entry.name}")
                device_reg.async_remove_device(device_entry.id)

    async def service_fritzbox(
        self, service_call: core.ServiceCall, config_entry: core.ConfigEntry
    ) -> None:
        """Define FRITZ!Box services."""
        _LOGGER.debug(f"FRITZ!Box service: {service_call.service}")

        if not self.connection:
            raise core.SmartHomeControllerError("Unable to establish a connection")

        try:
            if service_call.service == Const.SERVICE_REBOOT:
                _LOGGER.warning(
                    'Service "fritz.reboot" is deprecated, '
                    + "please use the corresponding button entity instead"
                )
                await self.async_trigger_reboot()
                return

            if service_call.service == Const.SERVICE_RECONNECT:
                _LOGGER.warning(
                    'Service "fritz.reconnect" is deprecated, '
                    + "please use the corresponding button entity instead"
                )
                await self.async_trigger_reconnect()
                return

            if service_call.service == Const.SERVICE_CLEANUP:
                _LOGGER.warning(
                    'Service "fritz.cleanup" is deprecated, '
                    + "please use the corresponding button entity instead"
                )
                await self.async_trigger_cleanup(config_entry)
                return

            if service_call.service == Const.SERVICE_SET_GUEST_WIFI_PW:
                await self.async_trigger_set_guest_password(
                    service_call.data.get("password"),
                    service_call.data.get("length", fritz_wlan.DEFAULT_PASSWORD_LENGTH),
                )
                return

        except (
            fritz_exceptions.FritzServiceError,
            fritz_exceptions.FritzActionError,
        ) as ex:
            raise core.SmartHomeControllerError("Service or parameter unknown") from ex
        except fritz_exceptions.FritzConnectionException as ex:
            raise core.SmartHomeControllerError("Service not supported") from ex


def _is_stopping(activity: str) -> None:
    """Inform that Smart Home - The Next Generation is stopping."""
    _LOGGER.info(
        f"Cannot execute {activity}: Smart Home - The Next Generation is shutting down"
    )


def _cleanup_entity_filter(
    shc: core.SmartHomeController, device: core.EntityRegistryEntry
) -> bool:
    """Filter only relevant entities."""
    return device.domain == shc.components.device_tracker.domain or (
        device.domain == shc.components.switch.domain
        and "_internet_access" in device.entity_id
    )
