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

# pylint: disable=unused-variable

import dataclasses
import datetime as dt
import logging
import typing

import fritzconnection.lib.fritzstatus as fritz_status
import fritzconnection.core.exceptions as fritz_exceptions

from ... import core
from .avm_wrapper import AvmWrapper
from .connection_info import ConnectionInfo
from .const import Const
from .fritzbox_base_entity import FritzboxBaseEntity

if not typing.TYPE_CHECKING:

    class FritzboxToolsIntegration:
        pass


if typing.TYPE_CHECKING:
    from .fritzbox_tools_integration import FritzboxToolsIntegration


_LOGGER: typing.Final = logging.getLogger(__name__)


@dataclasses.dataclass
class FritzRequireKeysMixin:
    """Fritz sensor data class."""

    value_fn: typing.Callable[[fritz_status.FritzStatus, typing.Any], typing.Any]


@dataclasses.dataclass
class FritzSensorEntityDescription(
    core.Sensor.EntityDescription, FritzRequireKeysMixin
):
    """Describes Fritz sensor entity."""

    is_suitable: typing.Callable[[ConnectionInfo], bool] = lambda info: info.wan_enabled


def _uptime_calculation(seconds_uptime: float, last_value: dt.datetime) -> dt.datetime:
    """Calculate uptime with deviation."""
    delta_uptime = core.helpers.utcnow() - dt.timedelta(seconds=seconds_uptime)

    if (
        not last_value
        or abs((delta_uptime - last_value).total_seconds()) > Const.UPTIME_DEVIATION
    ):
        return delta_uptime

    return last_value


def _retrieve_device_uptime_state(
    status: fritz_status.FritzStatus, last_value: dt.datetime
) -> dt.datetime:
    """Return uptime from device."""
    return _uptime_calculation(status.device_uptime, last_value)


def _retrieve_connection_uptime_state(
    status: fritz_status.FritzStatus, last_value: dt.datetime
) -> dt.datetime:
    """Return uptime from connection."""
    return _uptime_calculation(status.connection_uptime, last_value)


def _retrieve_external_ip_state(
    status: fritz_status.FritzStatus, _last_value: str
) -> str:
    """Return external ip from device."""
    return status.external_ip


def _retrieve_kb_s_sent_state(
    status: fritz_status.FritzStatus, _last_value: str
) -> float:
    """Return upload transmission rate."""
    return round(status.transmission_rate[0] / 1000, 1)


def _retrieve_kb_s_received_state(
    status: fritz_status.FritzStatus, _last_value: str
) -> float:
    """Return download transmission rate."""
    return round(status.transmission_rate[1] / 1000, 1)


def _retrieve_max_kb_s_sent_state(
    status: fritz_status.FritzStatus, _last_value: str
) -> float:
    """Return upload max transmission rate."""
    return round(status.max_bit_rate[0] / 1000, 1)


def _retrieve_max_kb_s_received_state(
    status: fritz_status.FritzStatus, _last_value: str
) -> float:
    """Return download max transmission rate."""
    return round(status.max_bit_rate[1] / 1000, 1)


def _retrieve_gb_sent_state(
    status: fritz_status.FritzStatus, _last_value: str
) -> float:
    """Return upload total data."""
    return round(status.bytes_sent / 1024 / 1024 / 1024, 1)


def _retrieve_gb_received_state(
    status: fritz_status.FritzStatus, _last_value: str
) -> float:
    """Return download total data."""
    return round(status.bytes_received / 1024 / 1024 / 1024, 1)


def _retrieve_link_kb_s_sent_state(
    status: fritz_status.FritzStatus, _last_value: str
) -> float:
    """Return upload link rate."""
    return round(status.max_linked_bit_rate[0] / 1000, 1)


def _retrieve_link_kb_s_received_state(
    status: fritz_status.FritzStatus, _last_value: str
) -> float:
    """Return download link rate."""
    return round(status.max_linked_bit_rate[1] / 1000, 1)


def _retrieve_link_noise_margin_sent_state(
    status: fritz_status.FritzStatus, _last_value: str
) -> float:
    """Return upload noise margin."""
    return status.noise_margin[0] / 10


def _retrieve_link_noise_margin_received_state(
    status: fritz_status.FritzStatus, _last_value: str
) -> float:
    """Return download noise margin."""
    return status.noise_margin[1] / 10


def _retrieve_link_attenuation_sent_state(
    status: fritz_status.FritzStatus, _last_value: str
) -> float:
    """Return upload line attenuation."""
    return status.attenuation[0] / 10


def _retrieve_link_attenuation_received_state(
    status: fritz_status.FritzStatus, _last_value: str
) -> float:
    """Return download line attenuation."""
    return status.attenuation[1] / 10


_SENSOR_TYPES: typing.Final[tuple[FritzSensorEntityDescription, ...]] = (
    FritzSensorEntityDescription(
        key="external_ip",
        name="External IP",
        icon="mdi:earth",
        value_fn=_retrieve_external_ip_state,
    ),
    FritzSensorEntityDescription(
        key="device_uptime",
        name="Device Uptime",
        device_class=core.Sensor.DeviceClass.TIMESTAMP,
        entity_category=core.EntityCategory.DIAGNOSTIC,
        value_fn=_retrieve_device_uptime_state,
        is_suitable=lambda info: True,
    ),
    FritzSensorEntityDescription(
        key="connection_uptime",
        name="Connection Uptime",
        device_class=core.Sensor.DeviceClass.TIMESTAMP,
        entity_category=core.EntityCategory.DIAGNOSTIC,
        value_fn=_retrieve_connection_uptime_state,
    ),
    FritzSensorEntityDescription(
        key="kb_s_sent",
        name="Upload Throughput",
        state_class=core.Sensor.StateClass.MEASUREMENT,
        native_unit_of_measurement=core.Const.UnitOfDataRate.KILOBYTES_PER_SECOND,
        icon="mdi:upload",
        value_fn=_retrieve_kb_s_sent_state,
    ),
    FritzSensorEntityDescription(
        key="kb_s_received",
        name="Download Throughput",
        state_class=core.Sensor.StateClass.MEASUREMENT,
        native_unit_of_measurement=core.Const.UnitOfDataRate.KILOBYTES_PER_SECOND,
        icon="mdi:download",
        value_fn=_retrieve_kb_s_received_state,
    ),
    FritzSensorEntityDescription(
        key="max_kb_s_sent",
        name="Max Connection Upload Throughput",
        native_unit_of_measurement=core.Const.UnitOfDataRate.KILOBITS_PER_SECOND,
        icon="mdi:upload",
        entity_category=core.EntityCategory.DIAGNOSTIC,
        value_fn=_retrieve_max_kb_s_sent_state,
    ),
    FritzSensorEntityDescription(
        key="max_kb_s_received",
        name="Max Connection Download Throughput",
        native_unit_of_measurement=core.Const.UnitOfDataRate.KILOBITS_PER_SECOND,
        icon="mdi:download",
        entity_category=core.EntityCategory.DIAGNOSTIC,
        value_fn=_retrieve_max_kb_s_received_state,
    ),
    FritzSensorEntityDescription(
        key="gb_sent",
        name="GB sent",
        state_class=core.Sensor.StateClass.TOTAL_INCREASING,
        native_unit_of_measurement=core.Const.UnitOfInformation.GIGABYTES,
        icon="mdi:upload",
        value_fn=_retrieve_gb_sent_state,
    ),
    FritzSensorEntityDescription(
        key="gb_received",
        name="GB received",
        state_class=core.Sensor.StateClass.TOTAL_INCREASING,
        native_unit_of_measurement=core.Const.UnitOfInformation.GIGABYTES,
        icon="mdi:download",
        value_fn=_retrieve_gb_received_state,
    ),
    FritzSensorEntityDescription(
        key="link_kb_s_sent",
        name="Link Upload Throughput",
        native_unit_of_measurement=core.Const.UnitOfDataRate.KILOBITS_PER_SECOND,
        icon="mdi:upload",
        value_fn=_retrieve_link_kb_s_sent_state,
    ),
    FritzSensorEntityDescription(
        key="link_kb_s_received",
        name="Link Download Throughput",
        native_unit_of_measurement=core.Const.UnitOfDataRate.KILOBITS_PER_SECOND,
        icon="mdi:download",
        value_fn=_retrieve_link_kb_s_received_state,
    ),
    FritzSensorEntityDescription(
        key="link_noise_margin_sent",
        name="Link Upload Noise Margin",
        native_unit_of_measurement=core.Const.SIGNAL_STRENGTH_DECIBELS,
        icon="mdi:upload",
        value_fn=_retrieve_link_noise_margin_sent_state,
        is_suitable=lambda info: info.wan_enabled
        and info.connection == Const.DSL_CONNECTION,
    ),
    FritzSensorEntityDescription(
        key="link_noise_margin_received",
        name="Link Download Noise Margin",
        native_unit_of_measurement=core.Const.SIGNAL_STRENGTH_DECIBELS,
        icon="mdi:download",
        value_fn=_retrieve_link_noise_margin_received_state,
        is_suitable=lambda info: info.wan_enabled
        and info.connection == Const.DSL_CONNECTION,
    ),
    FritzSensorEntityDescription(
        key="link_attenuation_sent",
        name="Link Upload Power Attenuation",
        native_unit_of_measurement=core.Const.SIGNAL_STRENGTH_DECIBELS,
        icon="mdi:upload",
        value_fn=_retrieve_link_attenuation_sent_state,
        is_suitable=lambda info: info.wan_enabled
        and info.connection == Const.DSL_CONNECTION,
    ),
    FritzSensorEntityDescription(
        key="link_attenuation_received",
        name="Link Download Power Attenuation",
        native_unit_of_measurement=core.Const.SIGNAL_STRENGTH_DECIBELS,
        icon="mdi:download",
        value_fn=_retrieve_link_attenuation_received_state,
        is_suitable=lambda info: info.wan_enabled
        and info.connection == Const.DSL_CONNECTION,
    ),
)


class FritzboxSensor(FritzboxBaseEntity, core.Sensor.Entity):
    """Define FRITZ!Box connectivity class."""

    _entity_description: FritzSensorEntityDescription

    def __init__(
        self,
        owner: FritzboxToolsIntegration,
        avm_wrapper: AvmWrapper,
        device_friendly_name: str,
        description: FritzSensorEntityDescription,
    ) -> None:
        """Init FRITZ!Box connectivity class."""
        self._entity_description = description
        self._last_device_value: str = None
        self._attr_available = True
        self._attr_name = f"{device_friendly_name} {description.name}"
        self._attr_unique_id = f"{avm_wrapper.unique_id}-{description.key}"
        super().__init__(owner, avm_wrapper, device_friendly_name)

    @property
    def entity_description(self) -> FritzSensorEntityDescription:
        return super().entity_description

    def update(self) -> None:
        """Update data."""
        _LOGGER.debug("Updating FRITZ!Box sensors")

        status = self._avm_wrapper.fritz_status
        try:
            self._attr_native_value = (
                self._last_device_value
            ) = self.entity_description.value_fn(status, self._last_device_value)
        except fritz_exceptions.FritzConnectionException:
            _LOGGER.error("Error getting the state from the FRITZ!Box", exc_info=True)
            self._attr_available = False
            return
        self._attr_available = True


async def async_setup_sensors(
    owner: FritzboxToolsIntegration,
    entry: core.ConfigEntry,
    async_add_entities: core.AddEntitiesCallback,
) -> None:
    """Set up entry."""
    _LOGGER.debug("Setting up FRITZ!Box sensors")
    avm_wrapper = owner.wrappers[entry.entry_id]

    connection_info = await avm_wrapper.async_get_connection_info()

    entities = [
        FritzboxSensor(owner, avm_wrapper, entry.title, description)
        for description in _SENSOR_TYPES
        if description.is_suitable(connection_info)
    ]

    async_add_entities(entities, True)
