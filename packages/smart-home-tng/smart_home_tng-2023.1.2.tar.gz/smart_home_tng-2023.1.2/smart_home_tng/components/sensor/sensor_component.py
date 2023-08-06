"""
Sensor Component for Smart Home - The Next Generation.

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
import typing

import voluptuous as vol

from ... import core
from .statistics_compiler import (
    _DEFAULT_STATISTICS,
    _compile_statistics,
)

_cv: typing.TypeAlias = core.ConfigValidation
_statistic: typing.TypeAlias = core.Statistic

_LOGGER: typing.Final = logging.getLogger(__name__)

_DEVICE_CLASS_NONE: typing.Final = "none"

_CONF_IS_APPARENT_POWER: typing.Final = "is_apparent_power"
_CONF_IS_BATTERY_LEVEL: typing.Final = "is_battery_level"
_CONF_IS_CO: typing.Final = "is_carbon_monoxide"
_CONF_IS_CO2: typing.Final = "is_carbon_dioxide"
_CONF_IS_CURRENT: typing.Final = "is_current"
_CONF_IS_ENERGY: typing.Final = "is_energy"
_CONF_IS_FREQUENCY: typing.Final = "is_frequency"
_CONF_IS_HUMIDITY: typing.Final = "is_humidity"
_CONF_IS_GAS: typing.Final = "is_gas"
_CONF_IS_ILLUMINANCE: typing.Final = "is_illuminance"
_CONF_IS_NITROGEN_DIOXIDE: typing.Final = "is_nitrogen_dioxide"
_CONF_IS_NITROGEN_MONOXIDE: typing.Final = "is_nitrogen_monoxide"
_CONF_IS_NITROUS_OXIDE: typing.Final = "is_nitrous_oxide"
_CONF_IS_OZONE: typing.Final = "is_ozone"
_CONF_IS_PM1: typing.Final = "is_pm1"
_CONF_IS_PM10: typing.Final = "is_pm10"
_CONF_IS_PM25: typing.Final = "is_pm25"
_CONF_IS_POWER: typing.Final = "is_power"
_CONF_IS_POWER_FACTOR: typing.Final = "is_power_factor"
_CONF_IS_PRESSURE: typing.Final = "is_pressure"
_CONF_IS_REACTIVE_POWER: typing.Final = "is_reactive_power"
_CONF_IS_SIGNAL_STRENGTH: typing.Final = "is_signal_strength"
_CONF_IS_SULPHUR_DIOXIDE: typing.Final = "is_sulphur_dioxide"
_CONF_IS_TEMPERATURE: typing.Final = "is_temperature"
_CONF_IS_VOLATILE_ORGANIC_COMPOUNDS: typing.Final = "is_volatile_organic_compounds"
_CONF_IS_VOLTAGE: typing.Final = "is_voltage"
_CONF_IS_VALUE: typing.Final = "is_value"

_ENTITY_CONDITIONS: typing.Final = {
    core.Sensor.DeviceClass.APPARENT_POWER: [
        {core.Const.CONF_TYPE: _CONF_IS_APPARENT_POWER}
    ],
    core.Sensor.DeviceClass.BATTERY: [{core.Const.CONF_TYPE: _CONF_IS_BATTERY_LEVEL}],
    core.Sensor.DeviceClass.CO: [{core.Const.CONF_TYPE: _CONF_IS_CO}],
    core.Sensor.DeviceClass.CO2: [{core.Const.CONF_TYPE: _CONF_IS_CO2}],
    core.Sensor.DeviceClass.CURRENT: [{core.Const.CONF_TYPE: _CONF_IS_CURRENT}],
    core.Sensor.DeviceClass.ENERGY: [{core.Const.CONF_TYPE: _CONF_IS_ENERGY}],
    core.Sensor.DeviceClass.FREQUENCY: [{core.Const.CONF_TYPE: _CONF_IS_FREQUENCY}],
    core.Sensor.DeviceClass.GAS: [{core.Const.CONF_TYPE: _CONF_IS_GAS}],
    core.Sensor.DeviceClass.HUMIDITY: [{core.Const.CONF_TYPE: _CONF_IS_HUMIDITY}],
    core.Sensor.DeviceClass.ILLUMINANCE: [{core.Const.CONF_TYPE: _CONF_IS_ILLUMINANCE}],
    core.Sensor.DeviceClass.NITROGEN_DIOXIDE: [
        {core.Const.CONF_TYPE: _CONF_IS_NITROGEN_DIOXIDE}
    ],
    core.Sensor.DeviceClass.NITROGEN_MONOXIDE: [
        {core.Const.CONF_TYPE: _CONF_IS_NITROGEN_MONOXIDE}
    ],
    core.Sensor.DeviceClass.NITROUS_OXIDE: [
        {core.Const.CONF_TYPE: _CONF_IS_NITROUS_OXIDE}
    ],
    core.Sensor.DeviceClass.OZONE: [{core.Const.CONF_TYPE: _CONF_IS_OZONE}],
    core.Sensor.DeviceClass.POWER: [{core.Const.CONF_TYPE: _CONF_IS_POWER}],
    core.Sensor.DeviceClass.POWER_FACTOR: [
        {core.Const.CONF_TYPE: _CONF_IS_POWER_FACTOR}
    ],
    core.Sensor.DeviceClass.PM1: [{core.Const.CONF_TYPE: _CONF_IS_PM1}],
    core.Sensor.DeviceClass.PM10: [{core.Const.CONF_TYPE: _CONF_IS_PM10}],
    core.Sensor.DeviceClass.PM25: [{core.Const.CONF_TYPE: _CONF_IS_PM25}],
    core.Sensor.DeviceClass.PRESSURE: [{core.Const.CONF_TYPE: _CONF_IS_PRESSURE}],
    core.Sensor.DeviceClass.REACTIVE_POWER: [
        {core.Const.CONF_TYPE: _CONF_IS_REACTIVE_POWER}
    ],
    core.Sensor.DeviceClass.SIGNAL_STRENGTH: [
        {core.Const.CONF_TYPE: _CONF_IS_SIGNAL_STRENGTH}
    ],
    core.Sensor.DeviceClass.SULPHUR_DIOXIDE: [
        {core.Const.CONF_TYPE: _CONF_IS_SULPHUR_DIOXIDE}
    ],
    core.Sensor.DeviceClass.TEMPERATURE: [{core.Const.CONF_TYPE: _CONF_IS_TEMPERATURE}],
    core.Sensor.DeviceClass.VOLATILE_ORGANIC_COMPOUNDS: [
        {core.Const.CONF_TYPE: _CONF_IS_VOLATILE_ORGANIC_COMPOUNDS}
    ],
    core.Sensor.DeviceClass.VOLTAGE: [{core.Const.CONF_TYPE: _CONF_IS_VOLTAGE}],
    _DEVICE_CLASS_NONE: [{core.Const.CONF_TYPE: _CONF_IS_VALUE}],
}

_CONDITION_SCHEMA: typing.Final = vol.All(
    _cv.DEVICE_CONDITION_BASE_SCHEMA.extend(
        {
            vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
            vol.Required(core.Const.CONF_TYPE): vol.In(
                [
                    _CONF_IS_APPARENT_POWER,
                    _CONF_IS_BATTERY_LEVEL,
                    _CONF_IS_CO,
                    _CONF_IS_CO2,
                    _CONF_IS_CURRENT,
                    _CONF_IS_ENERGY,
                    _CONF_IS_FREQUENCY,
                    _CONF_IS_GAS,
                    _CONF_IS_HUMIDITY,
                    _CONF_IS_ILLUMINANCE,
                    _CONF_IS_OZONE,
                    _CONF_IS_NITROGEN_DIOXIDE,
                    _CONF_IS_NITROGEN_MONOXIDE,
                    _CONF_IS_NITROUS_OXIDE,
                    _CONF_IS_POWER,
                    _CONF_IS_POWER_FACTOR,
                    _CONF_IS_PM1,
                    _CONF_IS_PM10,
                    _CONF_IS_PM25,
                    _CONF_IS_PRESSURE,
                    _CONF_IS_REACTIVE_POWER,
                    _CONF_IS_SIGNAL_STRENGTH,
                    _CONF_IS_SULPHUR_DIOXIDE,
                    _CONF_IS_TEMPERATURE,
                    _CONF_IS_VOLATILE_ORGANIC_COMPOUNDS,
                    _CONF_IS_VOLTAGE,
                    _CONF_IS_VALUE,
                ]
            ),
            vol.Optional(core.Const.CONF_BELOW): vol.Any(vol.Coerce(float)),
            vol.Optional(core.Const.CONF_ABOVE): vol.Any(vol.Coerce(float)),
        }
    ),
    _cv.has_at_least_one_key(core.Const.CONF_BELOW, core.Const.CONF_ABOVE),
)

_CONF_APPARENT_POWER: typing.Final = "apparent_power"
_CONF_BATTERY_LEVEL: typing.Final = "battery_level"
_CONF_CO: typing.Final = "carbon_monoxide"
_CONF_CO2: typing.Final = "carbon_dioxide"
_CONF_CURRENT: typing.Final = "current"
_CONF_ENERGY: typing.Final = "energy"
_CONF_FREQUENCY: typing.Final = "frequency"
_CONF_GAS: typing.Final = "gas"
_CONF_HUMIDITY: typing.Final = "humidity"
_CONF_ILLUMINANCE: typing.Final = "illuminance"
_CONF_NITROGEN_DIOXIDE: typing.Final = "nitrogen_dioxide"
_CONF_NITROGEN_MONOXIDE: typing.Final = "nitrogen_monoxide"
_CONF_NITROUS_OXIDE: typing.Final = "nitrous_oxide"
_CONF_OZONE: typing.Final = "ozone"
_CONF_PM1: typing.Final = "pm1"
_CONF_PM10: typing.Final = "pm10"
_CONF_PM25: typing.Final = "pm25"
_CONF_POWER: typing.Final = "power"
_CONF_POWER_FACTOR: typing.Final = "power_factor"
_CONF_PRESSURE: typing.Final = "pressure"
_CONF_REACTIVE_POWER: typing.Final = "reactive_power"
_CONF_SIGNAL_STRENGTH: typing.Final = "signal_strength"
_CONF_SULPHUR_DIOXIDE: typing.Final = "sulphur_dioxide"
_CONF_TEMPERATURE: typing.Final = "temperature"
_CONF_VOLATILE_ORGANIC_COMPOUNDS: typing.Final = "volatile_organic_compounds"
_CONF_VOLTAGE: typing.Final = "voltage"
_CONF_VALUE: typing.Final = "value"

_ENTITY_TRIGGERS: typing.Final = {
    core.Sensor.DeviceClass.APPARENT_POWER: [
        {core.Const.CONF_TYPE: _CONF_APPARENT_POWER}
    ],
    core.Sensor.DeviceClass.BATTERY: [{core.Const.CONF_TYPE: _CONF_BATTERY_LEVEL}],
    core.Sensor.DeviceClass.CO: [{core.Const.CONF_TYPE: _CONF_CO}],
    core.Sensor.DeviceClass.CO2: [{core.Const.CONF_TYPE: _CONF_CO2}],
    core.Sensor.DeviceClass.CURRENT: [{core.Const.CONF_TYPE: _CONF_CURRENT}],
    core.Sensor.DeviceClass.ENERGY: [{core.Const.CONF_TYPE: _CONF_ENERGY}],
    core.Sensor.DeviceClass.FREQUENCY: [{core.Const.CONF_TYPE: _CONF_FREQUENCY}],
    core.Sensor.DeviceClass.GAS: [{core.Const.CONF_TYPE: _CONF_GAS}],
    core.Sensor.DeviceClass.HUMIDITY: [{core.Const.CONF_TYPE: _CONF_HUMIDITY}],
    core.Sensor.DeviceClass.ILLUMINANCE: [{core.Const.CONF_TYPE: _CONF_ILLUMINANCE}],
    core.Sensor.DeviceClass.NITROGEN_DIOXIDE: [
        {core.Const.CONF_TYPE: _CONF_NITROGEN_DIOXIDE}
    ],
    core.Sensor.DeviceClass.NITROGEN_MONOXIDE: [
        {core.Const.CONF_TYPE: _CONF_NITROGEN_MONOXIDE}
    ],
    core.Sensor.DeviceClass.NITROUS_OXIDE: [
        {core.Const.CONF_TYPE: _CONF_NITROUS_OXIDE}
    ],
    core.Sensor.DeviceClass.OZONE: [{core.Const.CONF_TYPE: _CONF_OZONE}],
    core.Sensor.DeviceClass.PM1: [{core.Const.CONF_TYPE: _CONF_PM1}],
    core.Sensor.DeviceClass.PM10: [{core.Const.CONF_TYPE: _CONF_PM10}],
    core.Sensor.DeviceClass.PM25: [{core.Const.CONF_TYPE: _CONF_PM25}],
    core.Sensor.DeviceClass.POWER: [{core.Const.CONF_TYPE: _CONF_POWER}],
    core.Sensor.DeviceClass.POWER_FACTOR: [{core.Const.CONF_TYPE: _CONF_POWER_FACTOR}],
    core.Sensor.DeviceClass.PRESSURE: [{core.Const.CONF_TYPE: _CONF_PRESSURE}],
    core.Sensor.DeviceClass.REACTIVE_POWER: [
        {core.Const.CONF_TYPE: _CONF_REACTIVE_POWER}
    ],
    core.Sensor.DeviceClass.SIGNAL_STRENGTH: [
        {core.Const.CONF_TYPE: _CONF_SIGNAL_STRENGTH}
    ],
    core.Sensor.DeviceClass.SULPHUR_DIOXIDE: [
        {core.Const.CONF_TYPE: _CONF_SULPHUR_DIOXIDE}
    ],
    core.Sensor.DeviceClass.TEMPERATURE: [{core.Const.CONF_TYPE: _CONF_TEMPERATURE}],
    core.Sensor.DeviceClass.VOLATILE_ORGANIC_COMPOUNDS: [
        {core.Const.CONF_TYPE: _CONF_VOLATILE_ORGANIC_COMPOUNDS}
    ],
    core.Sensor.DeviceClass.VOLTAGE: [{core.Const.CONF_TYPE: _CONF_VOLTAGE}],
    _DEVICE_CLASS_NONE: [{core.Const.CONF_TYPE: _CONF_VALUE}],
}


_TRIGGER_SCHEMA: typing.Final = vol.All(
    _cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
        {
            vol.Required(core.Const.CONF_ENTITY_ID): _cv.entity_id,
            vol.Required(core.Const.CONF_TYPE): vol.In(
                [
                    _CONF_APPARENT_POWER,
                    _CONF_BATTERY_LEVEL,
                    _CONF_CO,
                    _CONF_CO2,
                    _CONF_CURRENT,
                    _CONF_ENERGY,
                    _CONF_FREQUENCY,
                    _CONF_GAS,
                    _CONF_HUMIDITY,
                    _CONF_ILLUMINANCE,
                    _CONF_NITROGEN_DIOXIDE,
                    _CONF_NITROGEN_MONOXIDE,
                    _CONF_NITROUS_OXIDE,
                    _CONF_OZONE,
                    _CONF_PM1,
                    _CONF_PM10,
                    _CONF_PM25,
                    _CONF_POWER,
                    _CONF_POWER_FACTOR,
                    _CONF_PRESSURE,
                    _CONF_REACTIVE_POWER,
                    _CONF_SIGNAL_STRENGTH,
                    _CONF_SULPHUR_DIOXIDE,
                    _CONF_TEMPERATURE,
                    _CONF_VOLATILE_ORGANIC_COMPOUNDS,
                    _CONF_VOLTAGE,
                    _CONF_VALUE,
                ]
            ),
            vol.Optional(core.Const.CONF_BELOW): vol.Any(vol.Coerce(float)),
            vol.Optional(core.Const.CONF_ABOVE): vol.Any(vol.Coerce(float)),
            vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict,
        }
    ),
    _cv.has_at_least_one_key(core.Const.CONF_BELOW, core.Const.CONF_ABOVE),
)


# pylint: disable=unused-variable
class SensorComponent(  # pylint: disable=too-many-ancestors
    core.SensorComponent,
    core.ConditionPlatform,
    core.GroupPlatform,
    core.RecorderPlatform,
    core.TriggerPlatform,
):
    """Component to interface with various sensors that can be monitored."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._component: core.EntityComponent = None
        self._recorder: core.RecorderComponent = None
        self._seen_dip = set[str]()
        self._warned_dip = set[str]()
        self._warned_neg = set[str]()
        self._unstable_unit = set[str]()
        self._warn_unsupported_unit = set[str]()

        self._supported_platforms = frozenset(
            [
                core.Platform.CONDITION,
                core.Platform.GROUP,
                core.Platform.RECORDER,
                core.Platform.SIGNIFICANT_CHANGE,
                core.Platform.TRIGGER,
            ]
        )

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    @property
    def scan_interval(self) -> dt.timedelta:
        return dt.timedelta(seconds=30)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Track states and offer events for sensors."""
        # pylint: disable=no-member
        if not await super().async_setup(config):
            return False

        comp = self.get_component(core.Const.RECORDER_COMPONENT_NAME)
        if isinstance(comp, core.RecorderComponent):
            self._recorder = comp
        else:
            return False

        component = self._component = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )
        await component.async_setup(config)
        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        component = self._component
        return await component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        component = self._component
        return await component.async_unload_entry(entry)

    @property
    def condition_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _CONDITION_SCHEMA

    async def async_get_conditions(
        self, device_id: str
    ) -> list[dict[str, typing.Any]] | typing.Awaitable[list[dict[str, typing.Any]]]:
        """List device conditions."""
        conditions: list[dict[str, str]] = []
        entity_registry = self.controller.entity_registry
        entries = [
            entry
            for entry in entity_registry.async_entries_for_device(device_id)
            if entry.domain == self.domain
        ]

        for entry in entries:
            device_class = (
                entity_registry.get_device_class(entry.entity_id) or _DEVICE_CLASS_NONE
            )
            state_class = entity_registry.get_capability(
                entry.entity_id, core.Sensor.ATTR_STATE_CLASS
            )
            unit_of_measurement = entity_registry.get_unit_of_measurement(
                entry.entity_id
            )

            if not unit_of_measurement and not state_class:
                continue

            templates = _ENTITY_CONDITIONS.get(
                device_class, _ENTITY_CONDITIONS[_DEVICE_CLASS_NONE]
            )

            conditions.extend(
                {
                    **template,
                    "condition": "device",
                    "device_id": device_id,
                    "entity_id": entry.entity_id,
                    "domain": self.domain,
                }
                for template in templates
            )

        return conditions

    async def async_condition_from_config(
        self, config: core.ConfigType
    ) -> core.ConditionCheckerType:
        """Evaluate state based on configuration."""
        numeric_state_config = {
            core.Const.CONF_CONDITION: "numeric_state",
            core.Const.CONF_ENTITY_ID: config[core.Const.CONF_ENTITY_ID],
        }
        if core.Const.CONF_ABOVE in config:
            numeric_state_config[core.Const.CONF_ABOVE] = config[core.Const.CONF_ABOVE]
        if core.Const.CONF_BELOW in config:
            numeric_state_config[core.Const.CONF_BELOW] = config[core.Const.CONF_BELOW]

        numeric_state_config = _cv.NUMERIC_STATE_CONDITION_SCHEMA(numeric_state_config)
        condition = core.ScriptCondition.get_action_condition_protocol(self.controller)
        numeric_state_config = condition.numeric_state_validate_config(
            numeric_state_config
        )
        return condition.async_numeric_state_from_config(numeric_state_config)

    async def async_get_condition_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema] | typing.Awaitable[dict[str, vol.Schema]]:
        """List condition capabilities."""
        er = self.controller.entity_registry
        try:
            unit_of_measurement = er.get_unit_of_measurement(
                config[core.Const.CONF_ENTITY_ID]
            )
        except core.SmartHomeControllerError:
            unit_of_measurement = None

        if not unit_of_measurement:
            raise core.InvalidDeviceAutomationConfig(
                "No unit of measurement found for condition entity {config[CONF_ENTITY_ID]}"
            )

        return {
            "extra_fields": vol.Schema(
                {
                    vol.Optional(
                        core.Const.CONF_ABOVE,
                        description={"suffix": unit_of_measurement},
                    ): vol.Coerce(float),
                    vol.Optional(
                        core.Const.CONF_BELOW,
                        description={"suffix": unit_of_measurement},
                    ): vol.Coerce(float),
                }
            )
        }

    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        registry.exclude_domain()

    def list_statistic_ids(
        self,
        recorder: core.RecorderComponent,
        statistic_ids: list[str] | tuple[str] = None,
        statistic_type: str = None,
    ) -> dict:
        """Return all or filtered statistic_ids and meta data."""
        entities = self._get_sensor_states()

        result = {}

        for state in entities:
            state_class = state.attributes[core.Sensor.ATTR_STATE_CLASS]
            state_unit = state.attributes.get(core.Const.ATTR_UNIT_OF_MEASUREMENT)

            provided_statistics = _DEFAULT_STATISTICS[state_class]
            if statistic_type is not None and statistic_type not in provided_statistics:
                continue

            if statistic_ids is not None and state.entity_id not in statistic_ids:
                continue

            if (
                "sum" in provided_statistics
                and core.Sensor.ATTR_LAST_RESET not in state.attributes
                and state.attributes.get(core.Sensor.ATTR_STATE_CLASS)
                == core.Sensor.StateClass.MEASUREMENT
            ):
                continue

            result[state.entity_id] = {
                "has_mean": "mean" in provided_statistics,
                "has_sum": "sum" in provided_statistics,
                "name": None,
                "source": recorder.domain,
                "statistic_id": state.entity_id,
                "unit_of_measurement": state_unit,
            }

        return result

    def _get_sensor_states(self) -> list[core.State]:
        """Get the current state of all sensors for which to compile statistics."""
        all_sensors = self.controller.states.all(self.domain)
        statistics_sensors = []

        for state in all_sensors:
            if not self._recorder.is_entity_recorded(state.entity_id):
                continue
            if (
                state.attributes.get(core.Sensor.ATTR_STATE_CLASS)
            ) not in core.Sensor.STATE_CLASSES:
                continue
            statistics_sensors.append(state)

        return statistics_sensors

    def reset_detected(
        self, entity_id: str, fstate: float, previous_fstate: float, state: core.State
    ) -> bool:
        """Test if a total_increasing sensor has been reset."""
        if previous_fstate is None:
            return False

        if 0.9 * previous_fstate <= fstate < previous_fstate:
            self._warn_dip(entity_id, state, previous_fstate)

        if fstate < 0:
            self._warn_negative(entity_id, state)
            raise core.SmartHomeControllerError()

        return fstate < 0.9 * previous_fstate

    def _warn_dip(
        self, entity_id: str, state: core.State, previous_fstate: float
    ) -> None:
        """Log a warning once if a sensor with state_class_total has a decreasing value.

        The log will be suppressed until two dips have been seen to prevent warning due to
        rounding issues with databases storing the state as a single precision float, which
        was fixed in recorder DB version 20.
        """
        if entity_id not in self._seen_dip:
            self._seen_dip.add(entity_id)
            return
        if entity_id not in self._warned_dip:
            self._warned_dip.add(entity_id)
            domain = self.controller.entity_sources.get(entity_id, {}).get("domain")
            if domain in ["energy", "growatt_server", "solaredge"]:
                return
            itg = f"from integration {domain} " if domain else ""
            issue = _suggest_report_issue(self.controller, entity_id)
            _LOGGER.warning(
                f"Entity {entity_id} {itg}has state class total_increasing, but its state is "
                + f"not strictly increasing. Triggered by state {state.state} ({previous_fstate}) "
                + f"with last_updated set to {state.last_updated.isoformat()}. "
                + f"Please {issue}",
            )

    def _warn_negative(self, entity_id: str, state: core.State) -> None:
        """Log a warning once if a sensor with state_class_total has a negative value."""
        if entity_id not in self._warned_neg:
            self._warned_neg.add(entity_id)
            domain = self.controller.entity_sources.get(entity_id, {}).get("domain")
            itg = f"from integration {domain} " if domain else ""
            issue = _suggest_report_issue(self.controller, entity_id)
            _LOGGER.warning(
                f"Entity {entity_id} {itg}has state class total_increasing, but its state is "
                + f"negative. Triggered by state {state.state} with last_updated set to "
                + f"{state.last_updated.isoformat()}. Please {issue}",
            )

    def compile_statistics(
        self, recorder: core.RecorderComponent, start: dt.datetime, end: dt.datetime
    ) -> _statistic.PlatformCompiledStatistics:
        """Compile statistics for all entities during start-end.

        Note: This will query the database and must not be run in the event loop
        """
        with recorder.session_scope() as session:
            compiled = _compile_statistics(
                self,
                recorder,
                session,
                start,
                end,
                self._get_sensor_states(),
                self._unstable_unit,
                self._warn_unsupported_unit,
            )
        return compiled

    @property
    def trigger_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return _TRIGGER_SCHEMA

    async def async_attach_trigger(
        self,
        config: core.ConfigType,
        action: core.TriggerActionType,
        trigger_info: core.TriggerInfo,
    ) -> core.CallbackType:
        numeric_state_config = {
            core.Const.CONF_PLATFORM: "numeric_state",
            core.Const.CONF_ENTITY_ID: config[core.Const.CONF_ENTITY_ID],
        }
        if core.Const.CONF_ABOVE in config:
            numeric_state_config[core.Const.CONF_ABOVE] = config[core.Const.CONF_ABOVE]
        if core.Const.CONF_BELOW in config:
            numeric_state_config[core.Const.CONF_BELOW] = config[core.Const.CONF_BELOW]
        if core.Const.CONF_FOR in config:
            numeric_state_config[core.Const.CONF_FOR] = config[core.Const.CONF_FOR]

        numeric_state_config = await core.Trigger.async_validate_trigger_config(
            numeric_state_config
        )
        return await core.Trigger.async_attach_numeric_state_trigger(
            self.controller,
            numeric_state_config,
            action,
            trigger_info,
            platform_type="device",
        )

    async def async_get_triggers(self, device_id: str) -> list[dict[str, str]]:
        """List device triggers."""
        triggers: list[dict[str, str]] = []
        entity_registry = self.controller.entity_registry

        entries = [
            entry
            for entry in entity_registry.async_entries_for_device(device_id)
            if entry.domain == self.domain
        ]

        for entry in entries:
            device_class = (
                entity_registry.get_device_class(entry.entity_id) or _DEVICE_CLASS_NONE
            )
            state_class = entity_registry.get_capability(
                entry.entity_id, core.Sensor.ATTR_STATE_CLASS
            )
            unit_of_measurement = entity_registry.get_unit_of_measurement(
                entry.entity_id
            )

            if not unit_of_measurement and not state_class:
                continue

            templates = _ENTITY_TRIGGERS.get(
                device_class, _ENTITY_TRIGGERS[_DEVICE_CLASS_NONE]
            )

            triggers.extend(
                {
                    **automation,
                    "platform": "device",
                    "device_id": device_id,
                    "entity_id": entry.entity_id,
                    "domain": self.domain,
                }
                for automation in templates
            )

        return triggers

    async def async_get_trigger_capabilities(
        self, config: core.ConfigType
    ) -> dict[str, vol.Schema]:
        """List trigger capabilities."""
        entity_registry = self.controller.entity_registry

        try:
            unit_of_measurement = entity_registry.get_unit_of_measurement(
                config[core.Const.CONF_ENTITY_ID]
            )
        except core.SmartHomeControllerError:
            unit_of_measurement = None

        if not unit_of_measurement:
            raise core.InvalidDeviceAutomationConfig(
                "No unit of measurement found for trigger entity "
                + f"{config[core.Const.CONF_ENTITY_ID]}"
            )

        return {
            "extra_fields": vol.Schema(
                {
                    vol.Optional(
                        core.Const.CONF_ABOVE,
                        description={"suffix": unit_of_measurement},
                    ): vol.Coerce(float),
                    vol.Optional(
                        core.Const.CONF_BELOW,
                        description={"suffix": unit_of_measurement},
                    ): vol.Coerce(float),
                    vol.Optional(core.Const.CONF_FOR): _cv.positive_time_period_dict,
                }
            )
        }


def _suggest_report_issue(shc: core.SmartHomeController, entity_id: str) -> str:
    """Suggest to report an issue."""
    entity_source = shc.entity_sources.get(entity_id, {})
    domain = entity_source.get("domain")
    custom_component = entity_source.get("custom_component")
    report_issue = ""
    if custom_component:
        report_issue = "report it to the custom component author."
    else:
        report_issue = (
            "create a bug report at "
            + "https://github.com/home-assistant/core/issues?q=is%3Aopen+is%3Aissue"
        )
        if domain:
            report_issue += f"+label%3A%22integration%3A+{domain}%22"

    return report_issue
