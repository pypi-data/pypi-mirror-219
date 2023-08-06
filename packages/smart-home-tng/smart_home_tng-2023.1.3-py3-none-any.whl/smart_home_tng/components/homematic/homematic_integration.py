"""
Homematic Integration for Smart Home - The Next Generation.

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
import functools as ft
import logging
import typing

import pyhomematic
import voluptuous as vol

from ... import core
from .binary_sensors import async_setup_binary_sensors
from .const import Const
from .covers import async_setup_covers
from .hm_hub import HMHub
from .hm_light import async_setup_lights
from .hm_lock import async_setup_locks
from .hm_thermostat import async_setup_climates
from .hm_sensor import async_setup_sensors
from .hm_switch import async_setup_switches
from .homematic_notification_service import HomematicNotificationService

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)
_DEFAULT_LOCAL_IP: typing.Final = "0.0.0.0"  # nosec
_DEFAULT_LOCAL_PORT: typing.Final = 0
_DEFAULT_RESOLVENAMES: typing.Final = False
_DEFAULT_JSONPORT: typing.Final = 80
_DEFAULT_PORT: typing.Final = 2001
_DEFAULT_PATH: typing.Final = ""
_DEFAULT_USERNAME: typing.Final = "Admin"
_DEFAULT_PASSWORD: typing.Final = ""
_DEFAULT_SSL: typing.Final = False
_DEFAULT_VERIFY_SSL: typing.Final = False
_DEFAULT_CHANNEL: typing.Final = 1


_DEVICE_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Required(core.Const.CONF_PLATFORM): "homematic",
        vol.Required(core.Const.ATTR_NAME): _cv.string,
        vol.Required(Const.ATTR_ADDRESS): _cv.string,
        vol.Required(Const.ATTR_INTERFACE): _cv.string,
        vol.Optional(Const.ATTR_DEVICE_TYPE): _cv.string,
        vol.Optional(Const.ATTR_CHANNEL, default=_DEFAULT_CHANNEL): vol.Coerce(int),
        vol.Optional(Const.ATTR_PARAM): _cv.string,
        vol.Optional(Const.ATTR_UNIQUE_ID): _cv.string,
    }
)

_SCHEMA_SERVICE_VIRTUALKEY: typing.Final = vol.Schema(
    {
        vol.Required(Const.ATTR_ADDRESS): vol.All(_cv.string, vol.Upper),
        vol.Required(Const.ATTR_CHANNEL): vol.Coerce(int),
        vol.Required(Const.ATTR_PARAM): _cv.string,
        vol.Optional(Const.ATTR_INTERFACE): _cv.string,
    }
)

_SCHEMA_SERVICE_SET_VARIABLE_VALUE: typing.Final = vol.Schema(
    {
        vol.Required(core.Const.ATTR_NAME): _cv.string,
        vol.Required(Const.ATTR_VALUE): _cv.match_all,
        vol.Optional(core.Const.ATTR_ENTITY_ID): _cv.entity_ids,
    }
)

_SCHEMA_SERVICE_SET_DEVICE_VALUE: typing.Final = vol.Schema(
    {
        vol.Required(Const.ATTR_ADDRESS): vol.All(_cv.string, vol.Upper),
        vol.Required(Const.ATTR_CHANNEL): vol.Coerce(int),
        vol.Required(Const.ATTR_PARAM): vol.All(_cv.string, vol.Upper),
        vol.Required(Const.ATTR_VALUE): _cv.match_all,
        vol.Optional(Const.ATTR_VALUE_TYPE): vol.In(
            ["boolean", "dateTime.iso8601", "double", "int", "string"]
        ),
        vol.Optional(Const.ATTR_INTERFACE): _cv.string,
    }
)

_SCHEMA_SERVICE_RECONNECT: typing.Final = vol.Schema({})

_SCHEMA_SERVICE_SET_INSTALL_MODE: typing.Final = vol.Schema(
    {
        vol.Required(Const.ATTR_INTERFACE): _cv.string,
        vol.Optional(core.Const.ATTR_TIME, default=60): _cv.positive_int,
        vol.Optional(core.Const.ATTR_MODE, default=1): vol.All(
            vol.Coerce(int), vol.In([1, 2])
        ),
        vol.Optional(Const.ATTR_ADDRESS): vol.All(_cv.string, vol.Upper),
    }
)

_SCHEMA_SERVICE_PUT_PARAMSET: typing.Final = vol.Schema(
    {
        vol.Required(Const.ATTR_INTERFACE): _cv.string,
        vol.Required(Const.ATTR_ADDRESS): vol.All(_cv.string, vol.Upper),
        vol.Required(Const.ATTR_PARAMSET_KEY): vol.All(_cv.string, vol.Upper),
        vol.Required(Const.ATTR_PARAMSET): dict,
        vol.Optional(Const.ATTR_RX_MODE): vol.All(_cv.string, vol.Upper),
    }
)

_NOTIFY_PLATFORM_SCHEMA = core.Notify.PLATFORM_SCHEMA.extend(
    {
        vol.Required(Const.ATTR_ADDRESS): vol.All(_cv.string, vol.Upper),
        vol.Required(Const.ATTR_CHANNEL): vol.Coerce(int),
        vol.Required(Const.ATTR_PARAM): vol.All(_cv.string, vol.Upper),
        vol.Required(Const.ATTR_VALUE): _cv.match_all,
        vol.Optional(Const.ATTR_INTERFACE): _cv.string,
    }
)


# pyint: disable=unused-variable
class HomematicIntegration(core.SmartHomeControllerComponent, core.NotifyPlatform):
    """Support for HomeMatic devices."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._remotes: dict[str, dict[str, typing.Any]] = None
        self._stores: set = None
        self._homematic: pyhomematic.HMConnection = None
        if _NOTIFY_PLATFORM_SCHEMA is not None:
            pass
        self._entity_hubs: list[HMHub] = None
        self._supported_platforms = frozenset(
            [
                core.Platform.BINARY_SENSOR,
                core.Platform.CLIMATE,
                core.Platform.COVER,
                core.Platform.LIGHT,
                core.Platform.LOCK,
                core.Platform.NOTIFY,
                core.Platform.SENSOR,
                core.Platform.SWITCH,
            ]
        )

    @property
    def homematic(self) -> pyhomematic.HMConnection:
        """Return current HomeMatic connection."""
        return self._homematic

    @property
    def remotes(self):
        return self._remotes

    @property
    def stores(self):
        return self._stores

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        """Validate configuration"""
        _CONFIG_SCHEMA: typing.Final = vol.Schema(
            {
                self.domain: vol.Schema(
                    {
                        vol.Optional(Const.CONF_INTERFACES, default={}): {
                            _cv.match_all: {
                                vol.Required(core.Const.CONF_HOST): _cv.string,
                                vol.Optional(
                                    core.Const.CONF_PORT, default=_DEFAULT_PORT
                                ): _cv.port,
                                vol.Optional(
                                    core.Const.CONF_PATH, default=_DEFAULT_PATH
                                ): _cv.string,
                                vol.Optional(
                                    Const.CONF_RESOLVENAMES,
                                    default=_DEFAULT_RESOLVENAMES,
                                ): vol.In(Const.CONF_RESOLVENAMES_OPTIONS),
                                vol.Optional(
                                    Const.CONF_JSONPORT, default=_DEFAULT_JSONPORT
                                ): _cv.port,
                                vol.Optional(
                                    core.Const.CONF_USERNAME, default=_DEFAULT_USERNAME
                                ): _cv.string,
                                vol.Optional(
                                    core.Const.CONF_PASSWORD, default=_DEFAULT_PASSWORD
                                ): _cv.string,
                                vol.Optional(Const.CONF_CALLBACK_IP): _cv.string,
                                vol.Optional(Const.CONF_CALLBACK_PORT): _cv.port,
                                vol.Optional(
                                    core.Const.CONF_SSL, default=_DEFAULT_SSL
                                ): _cv.boolean,
                                vol.Optional(
                                    core.Const.CONF_VERIFY_SSL,
                                    default=_DEFAULT_VERIFY_SSL,
                                ): _cv.boolean,
                            }
                        },
                        vol.Optional(core.Const.CONF_HOSTS, default={}): {
                            _cv.match_all: {
                                vol.Required(core.Const.CONF_HOST): _cv.string,
                                vol.Optional(
                                    core.Const.CONF_PORT, default=_DEFAULT_PORT
                                ): _cv.port,
                                vol.Optional(
                                    core.Const.CONF_USERNAME, default=_DEFAULT_USERNAME
                                ): _cv.string,
                                vol.Optional(
                                    core.Const.CONF_PASSWORD, default=_DEFAULT_PASSWORD
                                ): _cv.string,
                            }
                        },
                        vol.Optional(
                            Const.CONF_LOCAL_IP, default=_DEFAULT_LOCAL_IP
                        ): _cv.string,
                        vol.Optional(Const.CONF_LOCAL_PORT): _cv.port,
                    }
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return _CONFIG_SCHEMA(config)

    def setup(self, config: core.ConfigType) -> bool:
        """Set up the Homematic component."""
        if not super().setup(config):
            return False

        self._remotes = remotes = {}
        self._stores = set()

        # Create hosts-dictionary for pyhomematic
        for rname, rconfig in self._config[Const.CONF_INTERFACES].items():
            remotes[rname] = {
                "ip": rconfig.get(core.Const.CONF_HOST),
                "port": rconfig.get(core.Const.CONF_PORT),
                "path": rconfig.get(core.Const.CONF_PATH),
                "resolvenames": rconfig.get(Const.CONF_RESOLVENAMES),
                "jsonport": rconfig.get(Const.CONF_JSONPORT),
                "username": rconfig.get(core.Const.CONF_USERNAME),
                "password": rconfig.get(core.Const.CONF_PASSWORD),
                "callbackip": rconfig.get(Const.CONF_CALLBACK_IP),
                "callbackport": rconfig.get(Const.CONF_CALLBACK_PORT),
                "ssl": rconfig[core.Const.CONF_SSL],
                "verify_ssl": rconfig.get(core.Const.CONF_VERIFY_SSL),
                "connect": True,
            }

        for sname, sconfig in self._config[core.Const.CONF_HOSTS].items():
            remotes[sname] = {
                "ip": sconfig.get(core.Const.CONF_HOST),
                "port": sconfig[core.Const.CONF_PORT],
                "username": sconfig.get(core.Const.CONF_USERNAME),
                "password": sconfig.get(core.Const.CONF_PASSWORD),
                "connect": False,
            }

        # Create server thread
        bound_system_callback = ft.partial(_system_callback_handler, self, config)
        self._homematic = homematic = pyhomematic.HMConnection(
            local=self._config.get(Const.CONF_LOCAL_IP),
            localport=self._config.get(Const.CONF_LOCAL_PORT, _DEFAULT_LOCAL_PORT),
            remotes=remotes,
            systemcallback=bound_system_callback,
            interface_id="homeassistant",
        )

        # Start server thread, connect to hosts, initialize to receive events
        homematic.start()

        # Stops server when Home Assistant is shutting down
        self.controller.bus.listen_once(core.Const.EVENT_SHC_STOP, self._homematic.stop)

        # Init homematic hubs
        self._entity_hubs = entity_hubs = []
        for hub_name in self._config[core.Const.CONF_HOSTS]:
            entity_hubs.append(HMHub(self, hub_name))

        self.controller.services.register(
            self.domain,
            Const.SERVICE_VIRTUALKEY,
            self._hm_service_virtualkey,
            schema=_SCHEMA_SERVICE_VIRTUALKEY,
        )

        self.controller.services.register(
            self.domain,
            Const.SERVICE_SET_VARIABLE_VALUE,
            self._service_handle_value,
            schema=_SCHEMA_SERVICE_SET_VARIABLE_VALUE,
        )

        self.controller.services.register(
            self.domain,
            Const.SERVICE_RECONNECT,
            self._service_handle_reconnect,
            schema=_SCHEMA_SERVICE_RECONNECT,
        )

        self.controller.services.register(
            self.domain,
            Const.SERVICE_SET_DEVICE_VALUE,
            self._service_handle_device,
            schema=_SCHEMA_SERVICE_SET_DEVICE_VALUE,
        )

        self.controller.services.register(
            self.domain,
            Const.SERVICE_SET_INSTALL_MODE,
            self._service_handle_install_mode,
            schema=_SCHEMA_SERVICE_SET_INSTALL_MODE,
        )

        self.controller.services.register(
            self.domain,
            Const.SERVICE_PUT_PARAMSET,
            self._service_put_paramset,
            schema=_SCHEMA_SERVICE_PUT_PARAMSET,
        )

        return True

    def _hm_service_virtualkey(self, service: core.ServiceCall) -> None:
        """Service to handle virtualkey servicecalls."""
        address = service.data.get(Const.ATTR_ADDRESS)
        channel = service.data.get(Const.ATTR_CHANNEL)
        param = service.data.get(Const.ATTR_PARAM)

        # Device not found
        hmdevice = _device_from_servicecall(self, service)
        if hmdevice is None:
            _LOGGER.error(f"{address} not found for service virtualkey!")
            return

        # Parameter doesn't exist for device
        if param not in hmdevice.ACTIONNODE:
            _LOGGER.error(f"{param} not datapoint in hm device {address}")
            return

        # Channel doesn't exist for device
        if channel not in hmdevice.ACTIONNODE[param]:
            _LOGGER.error(f"{channel:i} is not a channel in hm device {address}")
            return

        # Call parameter
        hmdevice.actionNodeData(param, True, channel)

    def _service_handle_value(self, service: core.ServiceCall) -> None:
        """Service to call setValue method for HomeMatic system variable."""
        entity_ids = service.data.get(core.Const.ATTR_ENTITY_ID)
        name = service.data[core.Const.ATTR_NAME]
        value = service.data[core.Const.ATTR_VALUE]

        if entity_ids:
            entities = [
                entity for entity in self._entity_hubs if entity.entity_id in entity_ids
            ]
        else:
            entities = self._entity_hubs

        if not entities:
            _LOGGER.error("No HomeMatic hubs available")
            return

        for hub in entities:
            hub.hm_set_variable(name, value)

    def _service_handle_reconnect(self, _service: core.ServiceCall) -> None:
        """Service to reconnect all HomeMatic hubs."""
        self._homematic.reconnect()

    def _service_handle_device(self, service: core.ServiceCall) -> None:
        """Service to call setValue method for HomeMatic devices."""
        address = service.data[Const.ATTR_ADDRESS]
        channel = service.data[Const.ATTR_CHANNEL]
        param = service.data[Const.ATTR_PARAM]
        value = service.data[Const.ATTR_VALUE]
        value_type = service.data.get(Const.ATTR_VALUE_TYPE)

        # Convert value into correct XML-RPC Type.
        # https://docs.python.org/3/library/xmlrpc.client.html#xmlrpc.client.ServerProxy
        if value_type:
            if value_type == "int":
                value = int(value)
            elif value_type == "double":
                value = float(value)
            elif value_type == "boolean":
                value = bool(value)
            elif value_type == "dateTime.iso8601":
                value = dt.datetime.strptime(value, "%Y%m%dT%H:%M:%S")
            else:
                # Default is 'string'
                value = str(value)

        # Device not found
        hmdevice = _device_from_servicecall(self, service)
        if hmdevice is None:
            _LOGGER.error(f"{address} not found!")
            return

        hmdevice.setValue(param, value, channel)

    def _service_handle_install_mode(self, service: core.ServiceCall) -> None:
        """Service to set interface into install mode."""
        interface = service.data.get(Const.ATTR_INTERFACE)
        mode = service.data.get(core.Const.ATTR_MODE)
        time = service.data.get(core.Const.ATTR_TIME)
        address = service.data.get(Const.ATTR_ADDRESS)

        self._homematic.setInstallMode(interface, t=time, mode=mode, address=address)

    def _service_put_paramset(self, service: core.ServiceCall) -> None:
        """Service to call the putParamset method on a HomeMatic connection."""
        interface = service.data[Const.ATTR_INTERFACE]
        address = service.data[Const.ATTR_ADDRESS]
        paramset_key = service.data[Const.ATTR_PARAMSET_KEY]
        # When passing in the paramset from a YAML file we get an OrderedDict
        # here instead of a dict, so add this explicit cast.
        # The service schema makes sure that this cast works.
        paramset = dict(service.data[Const.ATTR_PARAMSET])
        rx_mode = service.data.get(Const.ATTR_RX_MODE)

        _LOGGER.debug(
            f"Calling putParamset: {interface}, {address}, {paramset_key}, "
            + f"{paramset}, {rx_mode}",
        )
        self._homematic.putParamset(interface, address, paramset_key, paramset, rx_mode)

    async def async_setup_platform(
        self,
        _platform_config: core.ConfigType,
        add_entities: core.AddEntitiesCallback,
        discovery_info: core.DiscoveryInfoType,
    ):
        """Setup platform implementations"""
        current_entity_platform = core.EntityPlatform.async_get_current_platform()
        platform = current_entity_platform.domain
        if platform == core.Platform.BINARY_SENSOR:
            await async_setup_binary_sensors(self, add_entities, discovery_info)
        elif platform == core.Platform.CLIMATE:
            await async_setup_climates(self, add_entities, discovery_info)
        elif platform == core.Platform.COVER:
            await async_setup_covers(self, add_entities, discovery_info)
        elif platform == core.Platform.LIGHT:
            await async_setup_lights(self, add_entities, discovery_info)
        elif platform == core.Platform.LOCK:
            await async_setup_locks(self, add_entities, discovery_info)
        elif platform == core.Platform.SENSOR:
            await async_setup_sensors(self, add_entities, discovery_info)
        elif platform == core.Platform.SWITCH:
            await async_setup_switches(self, add_entities, discovery_info)

    # --------------- Notify Platform --------------------------------

    async def async_get_service(
        self, config: core.ConfigType, discovery_info: core.DiscoveryInfoType = None
    ) -> core.BaseNotificationService:
        """Get the Homematic notification service."""
        data = {
            Const.ATTR_ADDRESS: config[Const.ATTR_ADDRESS],
            Const.ATTR_CHANNEL: config[Const.ATTR_CHANNEL],
            Const.ATTR_PARAM: config[Const.ATTR_PARAM],
            Const.ATTR_VALUE: config[Const.ATTR_VALUE],
        }
        if Const.ATTR_INTERFACE in config:
            data[Const.ATTR_INTERFACE] = config[Const.ATTR_INTERFACE]

        return HomematicNotificationService(self, data)


def _system_callback_handler(comp: HomematicIntegration, config, src, *args):
    """System callback handler."""
    # New devices available at hub
    if src == "newDevices":
        (interface_id, dev_descriptions) = args
        interface: str = interface_id.split("-")[-1]

        # Device support active?
        if not comp.remotes[interface]["connect"]:
            return

        addresses = []
        for dev in dev_descriptions:
            address = dev["ADDRESS"].split(":")[0]
            if address not in comp.stores:
                comp.stores.add(address)
                addresses.append(address)

        # Register EVENTS
        # Search all devices with an EVENTNODE that includes data
        bound_event_callback = ft.partial(_hm_event_handler, comp, interface)
        for dev in addresses:
            hmdevice = comp.homematic.devices[interface].get(dev)

            if hmdevice.EVENTNODE:
                hmdevice.setEventCallback(callback=bound_event_callback, bequeath=True)

        # Create Home Assistant entities
        if addresses:
            for component_name, discovery_type in (
                (core.Platform.SWITCH, Const.DISCOVER_SWITCHES),
                (core.Platform.LIGHT, Const.DISCOVER_LIGHTS),
                (core.Platform.COVER, Const.DISCOVER_COVER),
                (core.Platform.BINARY_SENSOR, Const.DISCOVER_BINARY_SENSORS),
                (core.Platform.SENSOR, Const.DISCOVER_SENSORS),
                (core.Platform.CLIMATE, Const.DISCOVER_CLIMATE),
                (core.Platform.LOCK, Const.DISCOVER_LOCKS),
                (core.Platform.BINARY_SENSOR, Const.DISCOVER_BATTERY),
            ):
                # Get all devices of a specific type
                found_devices = _get_devices(comp, discovery_type, addresses, interface)

                # When devices of this type are found
                # they are setup in Home Assistant and a discovery event is fired
                if found_devices:
                    comp.controller.setup.load_platform(
                        component_name,
                        comp.domain,
                        {
                            Const.ATTR_DISCOVER_DEVICES: found_devices,
                            Const.ATTR_DISCOVERY_TYPE: discovery_type,
                        },
                        config,
                    )

    # Homegear error message
    elif src == "error":
        _LOGGER.error(f"Error: {args}")
        (interface_id, errorcode, message) = args
        comp.controller.bus.fire(
            Const.EVENT_ERROR,
            {Const.ATTR_ERRORCODE: errorcode, Const.ATTR_MESSAGE: message},
        )


def _get_devices(comp: HomematicIntegration, discovery_type, keys, interface):
    """Get the HomeMatic devices for given discovery_type."""
    device_arr = []

    for key in keys:
        device = comp.homematic.devices[interface][key]
        class_name = device.__class__.__name__
        metadata = {}

        # Class not supported by discovery type
        is_simulated_binary_sensor = False
        if (
            discovery_type != Const.DISCOVER_BATTERY
            and class_name not in Const.HM_DEVICE_TYPES[discovery_type]
        ):
            if discovery_type == Const.DISCOVER_BINARY_SENSORS and class_name in [
                "RotaryHandleSensor",
                "RotaryHandleSensorIP",
            ]:
                is_simulated_binary_sensor = True
            if not is_simulated_binary_sensor:
                continue

        # Load metadata needed to generate a parameter list
        if discovery_type == Const.DISCOVER_SENSORS or is_simulated_binary_sensor:
            metadata.update(device.SENSORNODE)
        elif discovery_type == Const.DISCOVER_BINARY_SENSORS:
            metadata.update(device.BINARYNODE)
        elif discovery_type == Const.DISCOVER_BATTERY:
            if Const.ATTR_LOWBAT in device.ATTRIBUTENODE:
                metadata.update(
                    {Const.ATTR_LOWBAT: device.ATTRIBUTENODE[Const.ATTR_LOWBAT]}
                )
            elif Const.ATTR_LOW_BAT in device.ATTRIBUTENODE:
                metadata.update(
                    {Const.ATTR_LOW_BAT: device.ATTRIBUTENODE[Const.ATTR_LOW_BAT]}
                )
            else:
                continue
        else:
            metadata.update({None: device.ELEMENT})

        # Generate options for 1...n elements with 1...n parameters
        for param, channels in metadata.items():
            if (
                param in Const.HM_IGNORE_DISCOVERY_NODE
                and class_name
                not in Const.HM_IGNORE_DISCOVERY_NODE_EXCEPTIONS.get(param, [])
            ):
                continue
            if (
                discovery_type == Const.DISCOVER_SWITCHES
                and class_name == "IPKeySwitchLevel"
            ):
                channels.remove(8)
                channels.remove(12)
            if (
                discovery_type == Const.DISCOVER_LIGHTS
                and class_name == "IPKeySwitchLevel"
            ):
                channels.remove(4)

            # Add devices
            _LOGGER.debug(f"{discovery_type}: Handling {key}: {param}: {channels}")
            for channel in channels:
                name = _create_shc_id(
                    name=device.NAME, channel=channel, param=param, count=len(channels)
                )
                unique_id = _create_shc_id(
                    name=key, channel=channel, param=param, count=len(channels)
                )
                device_dict = {
                    core.Const.CONF_PLATFORM: "homematic",
                    Const.ATTR_ADDRESS: key,
                    Const.ATTR_INTERFACE: interface,
                    core.Const.ATTR_NAME: name,
                    Const.ATTR_DEVICE_TYPE: class_name,
                    Const.ATTR_CHANNEL: channel,
                    Const.ATTR_UNIQUE_ID: unique_id,
                }
                if param is not None:
                    device_dict[Const.ATTR_PARAM] = param

                # Add new device
                try:
                    _DEVICE_SCHEMA(device_dict)
                    device_arr.append(device_dict)
                except vol.MultipleInvalid as err:
                    _LOGGER.error(f"Invalid device config: {str(err)}")
    return device_arr


def _create_shc_id(name, channel, param, count) -> str:
    """Generate a unique entity id."""
    # HMDevice is a simple device
    if count == 1 and param is None:
        return name

    # Has multiple elements/channels
    if count > 1 and param is None:
        return f"{name} {channel}"

    # With multiple parameters on first channel
    if count == 1 and param is not None:
        return f"{name} {param}"

    # Multiple parameters with multiple channels
    if count > 1 and param is not None:
        return f"{name} {channel} {param}"

    return None


def _hm_event_handler(
    comp: HomematicIntegration, interface, device, _caller, attribute, _value
):
    """Handle all pyhomematic device events."""
    try:
        channel = int(device.split(":")[1])
        address = device.split(":")[0]
        hmdevice = comp.homematic.devices[interface].get(address)
    except (TypeError, ValueError):
        _LOGGER.error("Event handling channel convert error!")
        return

    # Return if not an event supported by device
    if attribute not in hmdevice.EVENTNODE:
        return

    _LOGGER.debug(f"Event {attribute} for {hmdevice.NAME} channel {channel:i}")

    # Keypress event
    if attribute in Const.HM_PRESS_EVENTS:
        comp.controller.bus.fire(
            Const.EVENT_KEYPRESS,
            {
                core.Const.ATTR_NAME: hmdevice.NAME,
                Const.ATTR_PARAM: attribute,
                Const.ATTR_CHANNEL: channel,
            },
        )
        return

    # Impulse event
    if attribute in Const.HM_IMPULSE_EVENTS:
        comp.controller.bus.fire(
            Const.EVENT_IMPULSE,
            {core.Const.ATTR_NAME: hmdevice.NAME, Const.ATTR_CHANNEL: channel},
        )
        return

    _LOGGER.warning("Event is unknown and not forwarded")


def _device_from_servicecall(comp: HomematicIntegration, service):
    """Extract HomeMatic device from service call."""
    address = service.data.get(Const.ATTR_ADDRESS)
    interface = service.data.get(Const.ATTR_INTERFACE)
    if address == "BIDCOS-RF":
        address = "BidCoS-RF"
    if address == "HMIP-RCV-1":
        address = "HmIP-RCV-1"

    if interface:
        return comp.homematic.devices[interface].get(address)

    for devices in comp.homematic.devices.values():
        if address in devices:
            return devices[address]
    return None
