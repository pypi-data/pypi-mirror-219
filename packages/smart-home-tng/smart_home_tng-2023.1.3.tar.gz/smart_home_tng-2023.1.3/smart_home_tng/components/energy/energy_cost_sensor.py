"""
Energy Component for Smart Home - The Next Generation.

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
import copy
import logging
import typing
from ... import core

from .const import Const
from .source_adapter import SourceAdapter

_LOGGER: typing.Final = logging.getLogger(__name__)
_COST_SENSORS: typing.Final = dict[str, str]()


# pylint: disable=unused-variable
class EnergyCostSensor(core.Sensor.Entity):
    """Calculate costs incurred by consuming energy.

    This is intended as a fallback for when no specific cost sensor is available for the
    utility.
    """

    _attr_entity_registry_visible_default = False
    _wrong_state_class_reported = False
    _wrong_unit_reported = False

    def __init__(
        self,
        adapter: SourceAdapter,
        config: dict,
    ) -> None:
        """Initialize the sensor."""
        super().__init__()

        self._adapter = adapter
        self.entity_id = (
            f"{config[adapter.entity_energy_key]}_{adapter.entity_id_suffix}"
        )
        self._attr_device_class = core.Sensor.DeviceClass.MONETARY
        self._attr_state_class = core.Sensor.StateClass.TOTAL
        self._config = config
        self._last_energy_sensor_state: core.State = None
        # add_finished is set when either of async_added_to_hass or add_to_platform_abort
        # is called
        self.add_finished = asyncio.Event()

    def _reset(self, energy_state: core.State) -> None:
        """Reset the cost sensor."""
        self._attr_native_value = 0.0
        self._attr_last_reset = core.helpers.utcnow()
        self._last_energy_sensor_state = energy_state
        self.async_write_state()

    @core.callback
    def _update_cost(self) -> None:
        """Update incurred costs."""
        energy_state = self._shc.states.get(
            typing.cast(str, self._config[self._adapter.entity_energy_key])
        )

        if energy_state is None:
            return

        state_class = energy_state.attributes.get(core.Sensor.ATTR_STATE_CLASS)
        if state_class not in Const.SUPPORTED_STATE_CLASSES:
            if not self._wrong_state_class_reported:
                self._wrong_state_class_reported = True
                _LOGGER.warning(
                    f"Found unexpected state_class {state_class} for "
                    + f"{energy_state.entity_id}",
                )
            return

        # last_reset must be set if the sensor is SensorStateClass.MEASUREMENT
        if (
            state_class == core.Sensor.StateClass.MEASUREMENT
            and core.Sensor.ATTR_LAST_RESET not in energy_state.attributes
        ):
            return

        try:
            energy = float(energy_state.state)
        except ValueError:
            return

        # Determine energy price
        if self._config["entity_energy_price"] is not None:
            energy_price_state = self._shc.states.get(
                self._config["entity_energy_price"]
            )

            if energy_price_state is None:
                return

            try:
                energy_price = float(energy_price_state.state)
            except ValueError:
                return

            unit_of_measurement = energy_price_state.get(
                core.Const.ATTR_UNIT_OF_MEASUREMENT, ""
            )

            if unit_of_measurement.endswith(f"/{core.Const.UnitOfEnergy.WATT_HOUR}"):
                energy_price *= 1000.0

            if unit_of_measurement.endswith(
                f"/{core.Const.UnitOfEnergy.MEGA_WATT_HOUR}"
            ):
                energy_price /= 1000.0

        else:
            energy_price_state = None
            energy_price = typing.cast(float, self._config["number_energy_price"])

        if self._last_energy_sensor_state is None:
            # Initialize as it's the first time all required entities are in place.
            self._reset(energy_state)
            return

        energy_unit = energy_state.attributes.get(core.Const.ATTR_UNIT_OF_MEASUREMENT)

        if self._adapter.source_type == "grid":
            if energy_unit not in Const.VALID_ENERGY_UNITS:
                energy_unit = None

        elif self._adapter.source_type == "gas":
            if energy_unit not in Const.VALID_ENERGY_UNITS_GAS:
                energy_unit = None

        if energy_unit == core.Const.UnitOfEnergy.WATT_HOUR:
            energy_price /= 1000
        elif energy_unit == core.Const.UnitOfEnergy.MEGA_WATT_HOUR:
            energy_price *= 1000

        if energy_unit is None:
            if not self._wrong_unit_reported:
                self._wrong_unit_reported = True
                energy_unit = energy_state.attributes.get(
                    core.Const.ATTR_UNIT_OF_MEASUREMENT
                )
                _LOGGER.warning(
                    f"Found unexpected unit {energy_unit} for {energy_state.entity_id}"
                )
            return

        shc_comp = core.SmartHomeControllerComponent.get_component(
            core.Const.SENSOR_COMPONENT_NAME
        )
        if not isinstance(shc_comp, core.SensorComponent):
            shc_comp = None

        if (
            state_class != core.Sensor.StateClass.TOTAL_INCREASING
            and energy_state.attributes.get(core.Sensor.ATTR_LAST_RESET)
            != self._last_energy_sensor_state.attributes.get(
                core.Sensor.ATTR_LAST_RESET
            )
        ):
            # Energy meter was reset, reset cost sensor too
            energy_state_copy = copy.copy(energy_state)
            energy_state_copy.state = "0.0"
            self._reset(energy_state_copy)
        elif (
            state_class == core.Sensor.StateClass.TOTAL_INCREASING
            and shc_comp is not None
            and shc_comp.reset_detected(
                typing.cast(str, self._config[self._adapter.entity_energy_key]),
                energy,
                float(self._last_energy_sensor_state.state),
                self._last_energy_sensor_state,
            )
        ):
            # Energy meter was reset, reset cost sensor too
            energy_state_copy = copy.copy(energy_state)
            energy_state_copy.state = "0.0"
            self._reset(energy_state_copy)
        # Update with newly incurred cost
        old_energy_value = float(self._last_energy_sensor_state.state)
        cur_value = typing.cast(float, self._attr_native_value)
        self._attr_native_value = cur_value + (energy - old_energy_value) * energy_price

        self._last_energy_sensor_state = energy_state

    async def async_added_to_shc(self) -> None:
        """Register callbacks."""
        energy_state = self._shc.states.get(
            self._config[self._adapter.entity_energy_key]
        )
        if energy_state:
            name = energy_state.name
        else:
            name = core.helpers.split_entity_id(
                self._config[self._adapter.entity_energy_key]
            )[0].replace("_", " ")

        self._attr_name = f"{name} {self._adapter.name_suffix}"

        self._update_cost()

        # Store stat ID in hass.data so frontend can look it up
        _COST_SENSORS[self._config[self._adapter.entity_energy_key]] = self.entity_id

        @core.callback
        def async_state_changed_listener(*_: typing.Any) -> None:
            """Handle child updates."""
            self._update_cost()
            self.async_write_state()

        self.async_on_remove(
            self._shc.tracker.async_track_state_change_event(
                typing.cast(str, self._config[self._adapter.entity_energy_key]),
                async_state_changed_listener,
            )
        )
        self.add_finished.set()

    @core.callback
    def add_to_platform_abort(self) -> None:
        """Abort adding an entity to a platform."""
        self.add_finished.set()

    async def async_will_remove_from_shc(self) -> None:
        """Handle removing from Smart Home Controller."""
        _COST_SENSORS.pop(self._config[self._adapter.entity_energy_key])
        await super().async_will_remove_from_shc()

    @core.callback
    def update_config(self, config: dict) -> None:
        """Update the config."""
        self._config = config

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the units of measurement."""
        return self._shc.config.currency

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        entity_registry = self._shc.entity_registry
        if registry_entry := entity_registry.async_get(
            self._config[self._adapter.entity_energy_key]
        ):
            prefix = registry_entry.id
        else:
            prefix = self._config[self._adapter.entity_energy_key]

        return f"{prefix}_{self._adapter.source_type}_{self._adapter.entity_id_suffix}"
