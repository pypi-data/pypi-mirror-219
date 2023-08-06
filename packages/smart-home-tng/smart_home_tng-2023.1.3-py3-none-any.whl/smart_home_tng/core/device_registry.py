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

import collections
import enum
import logging
import time
import typing

from ..backports import strenum
from . import helpers
from .callback import callback
from .config_entry import ConfigEntry
from .const import Const
from .debouncer import Debouncer
from .deleted_device import DeletedDevice
from .device import Device
from .device_registry_entry_disabler import DeviceRegistryEntryDisabler
from .device_registry_entry_type import DeviceRegistryEntryType
from .device_registry_store import DeviceRegistryStore
from .event import Event
from .required_parameter_missing import RequiredParameterMissing
from .smart_home_controller_error import SmartHomeControllerError

_STORAGE_KEY: typing.Final = "core.device_registry"
_STORAGE_VERSION_MAJOR: typing.Final = 1
_STORAGE_VERSION_MINOR: typing.Final = 3
_SAVE_DELAY: typing.Final = 10
_CLEANUP_DELAY: typing.Final = 10
_UNDEFINED: typing.Final = object()
_LOGGER: typing.Final = logging.getLogger(__name__)


if not typing.TYPE_CHECKING:

    class EntityRegistry:
        ...

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .entity_registry import EntityRegistry
    from .smart_home_controller import SmartHomeController


class _ConnectionType(strenum.LowercaseStrEnum):
    MAC = enum.auto()
    UPNP = enum.auto()
    ZIGBEE = enum.auto()


_ORPHANED_DEVICE_KEEP_SECONDS: typing.Final = 86400 * 30

_RUNTIME_ONLY_ATTRS: typing.Final = {"suggested_area"}


# pylint: disable=unused-variable
class _DeviceIndex(typing.NamedTuple):
    identifiers: dict[tuple[str, str], str]
    connections: dict[tuple[str, str], str]

    def add_device(self, device: Device | DeletedDevice) -> None:
        """Add a device to the index."""
        for identifier in device.identifiers:
            self.identifiers[identifier] = device.id
        for connection in device.connections:
            self.connections[connection] = device.id

    def remove_device(
        self,
        device: Device | DeletedDevice,
    ) -> None:
        """Remove a device from the index."""
        for identifier in device.identifiers:
            if identifier in self.identifiers:
                del self.identifiers[identifier]
        for connection in device.connections:
            if connection in self.connections:
                del self.connections[connection]


class DeviceRegistry:
    """Class to hold a registry of devices."""

    _devices: dict[str, Device]
    _deleted_devices: dict[str, DeletedDevice]
    _registered_index: _DeviceIndex
    _deleted_index: _DeviceIndex

    def __init__(self, shc: SmartHomeController) -> None:
        """Initialize the device registry."""
        self._shc = shc
        self._loaded = False
        self._store = DeviceRegistryStore(
            shc,
            _STORAGE_VERSION_MAJOR,
            _STORAGE_KEY,
            atomic_writes=True,
            minor_version=_STORAGE_VERSION_MINOR,
        )
        self._clear_index()

    # pylint: disable=invalid-name
    ConnectionType: typing.TypeAlias = _ConnectionType

    @property
    def devices(self) -> dict[str, Device]:
        return self._devices

    @property
    def deleted_devices(self) -> dict[str, DeletedDevice]:
        return self._deleted_devices

    @callback
    def async_get(self, device_id: str) -> Device:
        """Get device."""
        return self._devices.get(device_id)

    @callback
    def async_get_device(
        self,
        identifiers: set[tuple[str, str]],
        connections: set[tuple[str, str]] = None,
    ) -> Device:
        """Check if device is registered."""
        device_id = self._async_get_device_id_from_index(
            self._registered_index, identifiers, connections
        )
        if device_id is None:
            return None
        return self._devices[device_id]

    def _async_get_deleted_device(
        self,
        identifiers: set[tuple[str, str]],
        connections: set[tuple[str, str]],
    ) -> DeletedDevice:
        """Check if device is deleted."""
        device_id = self._async_get_device_id_from_index(
            self._deleted_index, identifiers, connections
        )
        if device_id is None:
            return None
        return self._deleted_devices[device_id]

    def _add_device(self, device: Device | DeletedDevice) -> None:
        """Add a device and index it."""
        if isinstance(device, DeletedDevice):
            devices_index = self._deleted_index
            self._deleted_devices[device.id] = device
        else:
            devices_index = self._registered_index
            self._devices[device.id] = device
        devices_index.add_device(device)

    def _remove_device(self, device: Device | DeletedDevice) -> None:
        """Remove a device and remove it from the index."""
        if isinstance(device, DeletedDevice):
            devices_index = self._deleted_index
            self._deleted_devices.pop(device.id)
        else:
            devices_index = self._registered_index
            self._devices.pop(device.id)
        devices_index.remove_device(device)

    def _update_device(self, old_device: Device, new_device: Device) -> None:
        """Update a device and the index."""
        self._devices[new_device.id] = new_device

        devices_index = self._registered_index
        devices_index.remove_device(old_device)
        devices_index.add_device(new_device)

    def _clear_index(self) -> None:
        """Clear the index."""
        self._registered_index = _DeviceIndex(identifiers={}, connections={})
        self._deleted_index = _DeviceIndex(identifiers={}, connections={})

    def _rebuild_index(self) -> None:
        """Create the index after loading devices."""
        self._clear_index()
        index = self._registered_index
        for device in self._devices.values():
            index.add_device(device)

        index = self._deleted_index
        for deleted_device in self._deleted_devices.values():
            index.add_device(deleted_device)

    @callback
    def async_get_or_create(
        self,
        *,
        config_entry_id: str | object = _UNDEFINED,
        configuration_url: str | object = _UNDEFINED,
        connections: set[tuple[str, str]] = None,
        default_manufacturer: str | object = _UNDEFINED,
        default_model: str | object = _UNDEFINED,
        default_name: str | object = _UNDEFINED,
        # To disable a device if it gets created
        disabled_by: DeviceRegistryEntryDisabler | object = _UNDEFINED,
        entry_type: DeviceRegistryEntryType | object = _UNDEFINED,
        identifiers: set[tuple[str, str]] = None,
        manufacturer: str | object = _UNDEFINED,
        model: str | object = _UNDEFINED,
        name: str | object = _UNDEFINED,
        suggested_area: str | object = _UNDEFINED,
        sw_version: str | object = _UNDEFINED,
        hw_version: str | object = _UNDEFINED,
        via_device: tuple[str, str] = None,
    ) -> Device:
        """Get device. Create if it doesn't exist."""
        if not identifiers and not connections:
            raise RequiredParameterMissing(["identifiers", "connections"])

        if identifiers is None:
            identifiers = set()

        if connections is None:
            connections = set()
        else:
            connections = self._normalize_connections(connections)

        device = self.async_get_device(identifiers, connections)

        if device is None:
            deleted_device = self._async_get_deleted_device(identifiers, connections)
            if deleted_device is None:
                device = Device(is_new=True)
            else:
                self._remove_device(deleted_device)
                device = deleted_device.to_device_entry(
                    config_entry_id, connections, identifiers
                )
            self._add_device(device)

        if default_manufacturer is not _UNDEFINED and device.manufacturer is None:
            manufacturer = default_manufacturer

        if default_model is not _UNDEFINED and device.model is None:
            model = default_model

        if default_name is not _UNDEFINED and device.name is None:
            name = default_name

        if via_device is not None:
            via = self.async_get_device({via_device})
            via_device_id: str = via.id if via else None
        else:
            via_device_id = None

        if isinstance(entry_type, str) and not isinstance(
            entry_type, DeviceRegistryEntryType
        ):
            self._shc.report(
                "uses str for device registry entry_type. This is deprecated and will "
                + "stop working in Home Assistant 2022.3, it should be updated to use "
                + "DeviceRegistryEntryType instead",
                error_if_core=False,
            )
            entry_type = DeviceRegistryEntryType(entry_type)

        device = self.async_update_device(
            device.id,
            add_config_entry_id=config_entry_id,
            configuration_url=configuration_url,
            disabled_by=disabled_by,
            entry_type=entry_type,
            manufacturer=manufacturer,
            merge_connections=connections or _UNDEFINED,
            merge_identifiers=identifiers or _UNDEFINED,
            model=model,
            name=name,
            suggested_area=suggested_area,
            sw_version=sw_version,
            hw_version=hw_version,
            via_device_id=via_device_id,
        )

        # This is safe because _async_update_device will always return a device
        # in this use case.
        assert device
        return device

    @callback
    def async_update_device(
        self,
        device_id: str,
        *,
        add_config_entry_id: str | object = _UNDEFINED,
        area_id: str | object = _UNDEFINED,
        configuration_url: str | object = _UNDEFINED,
        disabled_by: DeviceRegistryEntryDisabler | object = _UNDEFINED,
        entry_type: DeviceRegistryEntryType | object = _UNDEFINED,
        manufacturer: str | object = _UNDEFINED,
        merge_connections: set[tuple[str, str]] | object = _UNDEFINED,
        merge_identifiers: set[tuple[str, str]] | object = _UNDEFINED,
        model: str | object = _UNDEFINED,
        name_by_user: str | object = _UNDEFINED,
        name: str | object = _UNDEFINED,
        new_identifiers: set[tuple[str, str]] | object = _UNDEFINED,
        remove_config_entry_id: str | object = _UNDEFINED,
        suggested_area: str | object = _UNDEFINED,
        sw_version: str | object = _UNDEFINED,
        hw_version: str | object = _UNDEFINED,
        via_device_id: str | object = _UNDEFINED,
    ) -> Device:
        """Update device attributes."""

        old = self._devices[device_id]

        # Dict with new key/value pairs
        new_values: dict[str, typing.Any] = {}
        # Dict with old key/value pairs
        old_values: dict[str, typing.Any] = {}

        config_entries = old.config_entries

        if merge_identifiers is not _UNDEFINED and new_identifiers is not _UNDEFINED:
            raise SmartHomeControllerError()

        if isinstance(disabled_by, str) and not isinstance(
            disabled_by, DeviceRegistryEntryDisabler
        ):
            self._shc.report(
                "uses str for device registry disabled_by. This is deprecated and will "
                + "stop working in Home Assistant 2022.3, it should be updated to use "
                + "DeviceRegistryEntryDisabler instead",
                error_if_core=False,
            )
            disabled_by = DeviceRegistryEntryDisabler(disabled_by)

        if (
            suggested_area is not None
            and suggested_area is not _UNDEFINED
            and suggested_area != ""
            and area_id is _UNDEFINED
            and old.area_id is None
        ):
            area = self._shc.area_registry.async_get_or_create(suggested_area)
            area_id = area.id
            new_values["area_id"] = area_id
        else:
            new_values["area_id"] = old.area_id

        if (
            add_config_entry_id is not _UNDEFINED
            and add_config_entry_id not in old.config_entries
        ):
            config_entries = old.config_entries | {add_config_entry_id}

        if (
            remove_config_entry_id is not _UNDEFINED
            and remove_config_entry_id in config_entries
        ):
            if config_entries == {remove_config_entry_id}:
                self.async_remove_device(device_id)
                return None

            config_entries = config_entries - {remove_config_entry_id}

        new_values["config_entries"] = config_entries
        if config_entries != old.config_entries:
            old_values["config_entries"] = old.config_entries

        for attr_name, setvalue in (
            ("connections", merge_connections),
            ("identifiers", merge_identifiers),
        ):
            old_value = getattr(old, attr_name)
            # If not undefined, check if `value` contains new items.
            if setvalue is not _UNDEFINED and not setvalue.issubset(old_value):
                new_values[attr_name] = old_value | setvalue
                old_values[attr_name] = old_value
            else:
                new_values[attr_name] = old_value

        if new_identifiers is not _UNDEFINED:
            new_values["identifiers"] = new_identifiers
            old_values["identifiers"] = old.identifiers

        for attr_name, value in (
            ("configuration_url", configuration_url),
            ("disabled_by", disabled_by),
            ("entry_type", entry_type),
            ("manufacturer", manufacturer),
            ("model", model),
            ("name", name),
            ("name_by_user", name_by_user),
            ("area_id", area_id),
            ("suggested_area", suggested_area),
            ("sw_version", sw_version),
            ("hw_version", hw_version),
            ("via_device_id", via_device_id),
        ):
            if value is not _UNDEFINED and value != getattr(old, attr_name):
                new_values[attr_name] = value
                old_values[attr_name] = getattr(old, attr_name)
            else:
                new_values[attr_name] = getattr(old, attr_name)

        if old.is_new:
            new_values["is_new"] = False

        if not new_values:
            return old

        new_values["device_id"] = old.id

        new = Device(**new_values)
        self._update_device(old, new)

        # If its only run time attributes (suggested_area)
        # that do not get saved we do not want to write
        # to disk or fire an event as we would end up
        # firing events for data we have nothing to compare
        # against since its never saved on disk
        if _RUNTIME_ONLY_ATTRS.issuperset(new_values):
            return new

        self.async_schedule_save()

        data: dict[str, typing.Any] = {
            "action": "create" if old.is_new else "update",
            "device_id": new.id,
        }
        if not old.is_new:
            data["changes"] = old_values

        self._shc.bus.async_fire(Const.EVENT_DEVICE_REGISTRY_UPDATED, data)

        return new

    @callback
    def async_remove_device(self, device_id: str) -> None:
        """Remove a device from the device registry."""
        device = self.devices[device_id]
        self._remove_device(device)
        self._add_device(
            DeletedDevice(
                config_entries=device.config_entries,
                connections=device.connections,
                identifiers=device.identifiers,
                device_id=device.id,
                orphaned_timestamp=None,
            )
        )
        for other_device in list(self.devices.values()):
            if other_device.via_device_id == device_id:
                self.async_update_device(other_device.id, via_device_id=None)
        self._shc.bus.async_fire(
            Const.EVENT_DEVICE_REGISTRY_UPDATED,
            {"action": "remove", "device_id": device_id},
        )
        self.async_schedule_save()

    async def async_load(self) -> None:
        """Load the device registry."""
        if self._loaded:
            return None
        self._loaded = True
        self.async_setup_cleanup()

        data = await self._store.async_load()

        devices = collections.OrderedDict()
        deleted_devices = collections.OrderedDict()

        if data is not None:
            data = typing.cast("dict[str, typing.Any]", data)
            for device in data["devices"]:
                devices[device["id"]] = Device(
                    area_id=device["area_id"],
                    config_entries=set(device["config_entries"]),
                    configuration_url=device["configuration_url"],
                    connections={tuple(conn) for conn in device["connections"]},
                    disabled_by=DeviceRegistryEntryDisabler(device["disabled_by"])
                    if device["disabled_by"]
                    else None,
                    entry_type=DeviceRegistryEntryType(device["entry_type"])
                    if device["entry_type"]
                    else None,
                    device_id=device["id"],
                    identifiers={tuple(iden) for iden in device["identifiers"]},
                    manufacturer=device["manufacturer"],
                    model=device["model"],
                    name_by_user=device["name_by_user"],
                    name=device["name"],
                    sw_version=device["sw_version"],
                    hw_version=device["hw_version"],
                    via_device_id=device["via_device_id"],
                )
            # Introduced in 0.111
            for device in data["deleted_devices"]:
                deleted_devices[device["id"]] = DeletedDevice(
                    config_entries=set(device["config_entries"]),
                    connections={tuple(conn) for conn in device["connections"]},
                    identifiers={tuple(iden) for iden in device["identifiers"]},
                    device_id=device["id"],
                    orphaned_timestamp=device["orphaned_timestamp"],
                )

        self._devices = devices
        self._deleted_devices = deleted_devices
        self._rebuild_index()

    @callback
    def async_schedule_save(self) -> None:
        """Schedule saving the device registry."""
        self._store.async_delay_save(self._data_to_save, _SAVE_DELAY)

    @callback
    def _data_to_save(self) -> dict[str, list[dict[str, typing.Any]]]:
        """Return data of device registry to store in a file."""
        data = {}

        data["devices"] = [
            {
                "config_entries": list(entry.config_entries),
                "connections": list(entry.connections),
                "identifiers": list(entry.identifiers),
                "manufacturer": entry.manufacturer,
                "model": entry.model,
                "name": entry.name,
                "sw_version": entry.sw_version,
                "hw_version": entry.hw_version,
                "entry_type": entry.entry_type,
                "id": entry.id,
                "via_device_id": entry.via_device_id,
                "area_id": entry.area_id,
                "name_by_user": entry.name_by_user,
                "disabled_by": entry.disabled_by,
                "configuration_url": entry.configuration_url,
            }
            for entry in self.devices.values()
        ]
        data["deleted_devices"] = [
            {
                "config_entries": list(entry.config_entries),
                "connections": list(entry.connections),
                "identifiers": list(entry.identifiers),
                "id": entry.id,
                "orphaned_timestamp": entry.orphaned_timestamp,
            }
            for entry in self.deleted_devices.values()
        ]

        return data

    @callback
    def async_clear_config_entry(self, config_entry_id: str) -> None:
        """Clear config entry from registry entries."""
        now_time = time.time()
        for device in list(self.devices.values()):
            self.async_update_device(device.id, remove_config_entry_id=config_entry_id)
        for deleted_device in list(self.deleted_devices.values()):
            config_entries = deleted_device.config_entries
            if config_entry_id not in config_entries:
                continue
            if config_entries == {config_entry_id}:
                # Add a time stamp when the deleted device became orphaned
                self.deleted_devices[deleted_device.id] = DeletedDevice(
                    device_id=deleted_device.id,
                    config_entries=set(),
                    connections=deleted_device.connections,
                    identifiers=deleted_device.identifiers,
                    orphaned_timestamp=now_time,
                )
            else:
                config_entries = config_entries - {config_entry_id}
                # No need to reindex here since we currently
                # do not have a lookup by config entry
                self.deleted_devices[deleted_device.id] = DeletedDevice(
                    device_id=deleted_device.id,
                    config_entries=config_entries,
                    connections=deleted_device.connections,
                    identifiers=deleted_device.identifiers,
                    orphaned_timestamp=deleted_device.orphaned_timestamp,
                )
            self.async_schedule_save()

    @callback
    def async_purge_expired_orphaned_devices(self) -> None:
        """Purge expired orphaned devices from the registry.

        We need to purge these periodically to avoid the database
        growing without bound.
        """
        now_time = time.time()
        for deleted_device in list(self.deleted_devices.values()):
            if deleted_device.orphaned_timestamp is None:
                continue

            if (
                deleted_device.orphaned_timestamp + _ORPHANED_DEVICE_KEEP_SECONDS
                < now_time
            ):
                self._remove_device(deleted_device)

    @callback
    def async_clear_area_id(self, area_id: str) -> None:
        """Clear area id from registry entries."""
        for dev_id, device in self._devices.items():
            if area_id == device.area_id:
                self.async_update_device(dev_id, area_id=None)

    @callback
    def async_config_entry_disabled_by_changed(self, config_entry: ConfigEntry) -> None:
        """Handle a config entry being disabled or enabled.

        Disable devices in the registry that are associated with a config entry when
        the config entry is disabled, enable devices in the registry that are associated
        with a config entry when the config entry is enabled and the devices are marked
        DeviceEntryDisabler.CONFIG_ENTRY.
        Only disable a device if all associated config entries are disabled.
        """

        devices = self.async_entries_for_config_entry(config_entry.entry_id)

        if not config_entry.disabled_by:
            for device in devices:
                if device.disabled_by is not DeviceRegistryEntryDisabler.CONFIG_ENTRY:
                    continue
                self.async_update_device(device.id, disabled_by=None)
            return

        enabled_config_entries = {
            entry.entry_id
            for entry in self._shc.config_entries.async_entries()
            if not entry.disabled_by
        }

        for device in devices:
            if device.disabled:
                # Device already disabled, do not overwrite
                continue
            if len(device.config_entries) > 1 and device.config_entries.intersection(
                enabled_config_entries
            ):
                continue
            self.async_update_device(
                device.id, disabled_by=DeviceRegistryEntryDisabler.CONFIG_ENTRY
            )

    @staticmethod
    def _async_get_device_id_from_index(
        devices_index: _DeviceIndex,
        identifiers: set[tuple[str, str]],
        connections: set[tuple[str, str]],
    ) -> str:
        """Check if device has previously been registered."""
        for identifier in identifiers:
            if identifier in devices_index.identifiers:
                return devices_index.identifiers[identifier]
        if not connections:
            return None
        for connection in DeviceRegistry._normalize_connections(connections):
            if connection in devices_index.connections:
                return devices_index.connections[connection]
        return None

    @staticmethod
    def _normalize_connections(
        connections: set[tuple[str, str]]
    ) -> set[tuple[str, str]]:
        """Normalize connections to ensure we can match mac addresses."""
        return {
            (key, helpers.format_mac(value))
            if key == _ConnectionType.MAC
            else (key, value)
            for key, value in connections
        }

    @callback
    def async_setup_cleanup(self) -> None:
        """Clean up device registry when entities removed."""

        async def cleanup() -> None:
            """Cleanup."""
            ent_reg = self._shc.entity_registry
            self.async_cleanup(ent_reg)

        debounced_cleanup = Debouncer(
            self._shc,
            _LOGGER,
            cooldown=_CLEANUP_DELAY,
            immediate=False,
            function=cleanup,
        )

        async def entity_registry_changed(_event: Event) -> None:
            """Handle entity updated or removed dispatch."""
            await debounced_cleanup.async_call()

        @callback
        def entity_registry_changed_filter(event: Event) -> bool:
            """Handle entity updated or removed filter."""
            if (
                event.data["action"] == "update"
                and "device_id" not in event.data["changes"]
            ) or event.data["action"] == "create":
                return False

            return True

        if self._shc.is_running:
            self._shc.bus.async_listen(
                Const.EVENT_ENTITY_REGISTRY_UPDATED,
                entity_registry_changed,
                event_filter=entity_registry_changed_filter,
            )
            return

        async def startup_clean(_event: Event) -> None:
            """Clean up on startup."""
            self._shc.bus.async_listen(
                Const.EVENT_ENTITY_REGISTRY_UPDATED,
                entity_registry_changed,
                event_filter=entity_registry_changed_filter,
            )
            await debounced_cleanup.async_call()

        self._shc.bus.async_listen_once(Const.EVENT_SHC_STARTED, startup_clean)

    @callback
    def async_cleanup(
        self,
        ent_reg: EntityRegistry,
    ) -> None:
        """Clean up device registry."""
        # Find all devices that are referenced by a config_entry.
        config_entry_ids = {
            entry.entry_id for entry in self._shc.config_entries.async_entries()
        }
        references_config_entries = {
            device.id
            for device in self._devices.values()
            for config_entry_id in device.config_entries
            if config_entry_id in config_entry_ids
        }

        # Find all devices that are referenced in the entity registry.
        references_entities = {entry.device_id for entry in ent_reg.entities.values()}

        orphan = set(self._devices) - references_entities - references_config_entries

        for dev_id in orphan:
            self.async_remove_device(dev_id)

        # Find all referenced config entries that no longer exist
        # This shouldn't happen but have not been able to track down the bug :(
        for device in list(self._devices.values()):
            for config_entry_id in device.config_entries:
                if config_entry_id not in config_entry_ids:
                    self.async_update_device(
                        device.id, remove_config_entry_id=config_entry_id
                    )

        # Periodic purge of orphaned devices to avoid the registry
        # growing without bounds when there are lots of deleted devices
        self.async_purge_expired_orphaned_devices()

    @callback
    def async_entries_for_area(self, area_id: str) -> list[Device]:
        """Return entries that match an area."""
        return [device for device in self.devices.values() if device.area_id == area_id]

    @callback
    def async_entries_for_config_entry(self, config_entry_id: str) -> list[Device]:
        """Return entries that match a config entry."""
        return [
            device
            for device in self.devices.values()
            if config_entry_id in device.config_entries
        ]
