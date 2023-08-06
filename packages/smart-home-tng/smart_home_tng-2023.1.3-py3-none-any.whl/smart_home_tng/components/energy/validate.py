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

# pylint: disable=unused-variable

import collections.abc
import dataclasses
import functools
import typing

from ... import core
from .energy_cost_sensor import _COST_SENSORS
from .energy_manager import EnergyManager

_statistic: typing.TypeAlias = core.Statistic

_ENERGY_USAGE_DEVICE_CLASSES: typing.Final = (core.Sensor.DeviceClass.ENERGY,)
_ENERGY_USAGE_UNITS: typing.Final = {
    core.Sensor.DeviceClass.ENERGY: (
        core.Const.UnitOfEnergy.KILO_WATT_HOUR,
        core.Const.UnitOfEnergy.WATT_HOUR,
        core.Const.UnitOfEnergy.MEGA_WATT_HOUR,
        core.Const.UnitOfEnergy.GIGA_JOULE,
    )
}
_ENERGY_PRICE_UNITS: typing.Final = tuple(
    f"/{unit}" for units in _ENERGY_USAGE_UNITS.values() for unit in units
)
_ENERGY_UNIT_ERROR: typing.Final = "entity_unexpected_unit_energy"
_ENERGY_PRICE_UNIT_ERROR: typing.Final = "entity_unexpected_unit_energy_price"
_GAS_USAGE_DEVICE_CLASSES: typing.Final = (
    core.Sensor.DeviceClass.ENERGY,
    core.Sensor.DeviceClass.GAS,
)
_GAS_USAGE_UNITS: typing.Final = {
    core.Sensor.DeviceClass.ENERGY: _ENERGY_USAGE_UNITS[core.Sensor.DeviceClass.ENERGY],
    core.Sensor.DeviceClass.GAS: (
        core.Const.UnitOfVolume.CUBIC_METERS,
        core.Const.UnitOfVolume.CUBIC_FEET,
    ),
}
_GAS_PRICE_UNITS: typing.Final = tuple(
    f"/{unit}" for units in _GAS_USAGE_UNITS.values() for unit in units
)
_GAS_UNIT_ERROR: typing.Final = "entity_unexpected_unit_gas"
_GAS_PRICE_UNIT_ERROR: typing.Final = "entity_unexpected_unit_gas_price"
_WATER_USAGE_DEVICE_CLASSES = (core.Sensor.DeviceClass.WATER,)
_WATER_USAGE_UNITS = {
    core.Sensor.DeviceClass.WATER: (
        core.Const.UnitOfVolume.CUBIC_METERS,
        core.Const.UnitOfVolume.CUBIC_FEET,
        core.Const.UnitOfVolume.GALLONS,
        core.Const.UnitOfVolume.LITERS,
    ),
}
_WATER_PRICE_UNITS = tuple(
    f"/{unit}" for units in _WATER_USAGE_UNITS.values() for unit in units
)
_WATER_UNIT_ERROR = "entity_unexpected_unit_water"
_WATER_PRICE_UNIT_ERROR = "entity_unexpected_unit_water_price"


@dataclasses.dataclass()
class ValidationIssue:
    """Error or warning message."""

    type: str
    identifier: str
    value: typing.Any = None


@dataclasses.dataclass()
class EnergyPreferencesValidation:
    """Dictionary holding validation information."""

    energy_sources: list[list[ValidationIssue]] = dataclasses.field(
        default_factory=list
    )
    device_consumption: list[list[ValidationIssue]] = dataclasses.field(
        default_factory=list
    )

    def as_dict(self) -> dict:
        """Return dictionary version."""
        return dataclasses.asdict(self)


@core.callback
def _async_validate_usage_stat(
    shc: core.SmartHomeController,
    recorder: core.RecorderComponent,
    metadata: dict[str, tuple[int, _statistic.MetaData]],
    stat_id: str,
    allowed_device_classes: collections.abc.Sequence[str],
    allowed_units: collections.abc.Mapping[str, collections.abc.Sequence[str]],
    unit_error: str,
    result: list[ValidationIssue],
) -> None:
    """Validate a statistic."""
    if stat_id not in metadata:
        result.append(ValidationIssue("statistics_not_defined", stat_id))

    has_entity_source = core.helpers.valid_entity_id(stat_id)

    if not has_entity_source:
        return

    entity_id = stat_id

    if not recorder.is_entity_recorded(entity_id):
        result.append(
            ValidationIssue(
                "recorder_untracked",
                entity_id,
            )
        )
        return

    if (state := shc.states.get(entity_id)) is None:
        result.append(
            ValidationIssue(
                "entity_not_defined",
                entity_id,
            )
        )
        return

    if state.state in (core.Const.STATE_UNAVAILABLE, core.Const.STATE_UNKNOWN):
        result.append(ValidationIssue("entity_unavailable", entity_id, state.state))
        return

    try:
        current_value: float = float(state.state)
    except ValueError:
        result.append(
            ValidationIssue("entity_state_non_numeric", entity_id, state.state)
        )
        return

    if current_value is not None and current_value < 0:
        result.append(
            ValidationIssue("entity_negative_state", entity_id, current_value)
        )

    device_class = state.attributes.get(core.Const.ATTR_DEVICE_CLASS)
    if device_class not in allowed_device_classes:
        result.append(
            ValidationIssue(
                "entity_unexpected_device_class",
                entity_id,
                device_class,
            )
        )
    else:
        unit = state.attributes.get("unit_of_measurement")

        if device_class and unit not in allowed_units.get(device_class, []):
            result.append(ValidationIssue(unit_error, entity_id, unit))

    state_class = state.attributes.get(core.Sensor.ATTR_STATE_CLASS)

    allowed_state_classes = {
        core.Sensor.StateClass.MEASUREMENT,
        core.Sensor.StateClass.TOTAL,
        core.Sensor.StateClass.TOTAL_INCREASING,
    }
    if state_class not in allowed_state_classes:
        result.append(
            ValidationIssue(
                "entity_unexpected_state_class",
                entity_id,
                state_class,
            )
        )

    if (
        state_class == core.Sensor.StateClass.MEASUREMENT
        and core.Sensor.ATTR_LAST_RESET not in state.attributes
    ):
        result.append(
            ValidationIssue("entity_state_class_measurement_no_last_reset", entity_id)
        )


@core.callback
def _async_validate_price_entity(
    shc: core.SmartHomeController,
    entity_id: str,
    result: list[ValidationIssue],
    allowed_units: tuple[str, ...],
    unit_error: str,
) -> None:
    """Validate that the price entity is correct."""
    if (state := shc.states.get(entity_id)) is None:
        result.append(
            ValidationIssue(
                "entity_not_defined",
                entity_id,
            )
        )
        return

    try:
        float(state.state)
    except ValueError:
        result.append(
            ValidationIssue("entity_state_non_numeric", entity_id, state.state)
        )
        return

    unit = state.attributes.get("unit_of_measurement")

    if unit is None or not unit.endswith(allowed_units):
        result.append(ValidationIssue(unit_error, entity_id, unit))


@core.callback
def _async_validate_cost_stat(
    shc: core.SmartHomeController,
    recorder: core.RecorderComponent,
    metadata: dict[str, tuple[int, _statistic.MetaData]],
    stat_id: str,
    result: list[ValidationIssue],
) -> None:
    """Validate that the cost stat is correct."""
    if stat_id not in metadata:
        result.append(ValidationIssue("statistics_not_defined", stat_id))

    has_entity = core.helpers.valid_entity_id(stat_id)

    if not has_entity:
        return

    if not recorder.is_entity_recorded(stat_id):
        result.append(ValidationIssue("recorder_untracked", stat_id))

    if (state := shc.states.get(stat_id)) is None:
        result.append(ValidationIssue("entity_not_defined", stat_id))
        return

    state_class = state.attributes.get("state_class")

    supported_state_classes = {
        core.Sensor.StateClass.MEASUREMENT,
        core.Sensor.StateClass.TOTAL,
        core.Sensor.StateClass.TOTAL_INCREASING,
    }
    if state_class not in supported_state_classes:
        result.append(
            ValidationIssue("entity_unexpected_state_class", stat_id, state_class)
        )

    if (
        state_class == core.Sensor.StateClass.MEASUREMENT
        and core.Sensor.ATTR_LAST_RESET not in state.attributes
    ):
        result.append(
            ValidationIssue("entity_state_class_measurement_no_last_reset", stat_id)
        )


@core.callback
def _async_validate_auto_generated_cost_entity(
    recorder: core.RecorderComponent,
    energy_entity_id: str,
    result: list[ValidationIssue],
) -> None:
    """Validate that the auto generated cost entity is correct."""
    if energy_entity_id not in _COST_SENSORS:
        # The cost entity has not been setup
        return

    cost_entity_id = _COST_SENSORS[energy_entity_id]
    if not recorder.is_entity_recorded(cost_entity_id):
        result.append(ValidationIssue("recorder_untracked", cost_entity_id))


async def async_validate(
    shc: core.SmartHomeController,
    manager: EnergyManager,
    recorder: core.RecorderComponent,
) -> EnergyPreferencesValidation:
    """Validate the energy configuration."""
    statistics_metadata: dict[str, tuple[int, _statistic.MetaData]] = {}
    validate_calls = []
    wanted_statistics_metadata = set()

    result = EnergyPreferencesValidation()

    if manager.data is None:
        return result

    # Create a list of validation checks
    for source in manager.data["energy_sources"]:
        source_result: list[ValidationIssue] = []
        result.energy_sources.append(source_result)

        if source["type"] == "grid":
            for flow in source["flow_from"]:
                wanted_statistics_metadata.add(flow["stat_energy_from"])
                validate_calls.append(
                    functools.partial(
                        _async_validate_usage_stat,
                        shc,
                        recorder,
                        statistics_metadata,
                        flow["stat_energy_from"],
                        _ENERGY_USAGE_DEVICE_CLASSES,
                        _ENERGY_USAGE_UNITS,
                        _ENERGY_UNIT_ERROR,
                        source_result,
                    )
                )

                if stat_cost := flow.get("stat_cost") is not None:
                    wanted_statistics_metadata.add(stat_cost)
                    validate_calls.append(
                        functools.partial(
                            _async_validate_cost_stat,
                            shc,
                            recorder,
                            statistics_metadata,
                            stat_cost,
                            source_result,
                        )
                    )
                elif flow.get("entity_energy_price") is not None:
                    validate_calls.append(
                        functools.partial(
                            _async_validate_price_entity,
                            shc,
                            flow["entity_energy_price"],
                            source_result,
                            _ENERGY_PRICE_UNITS,
                            _ENERGY_PRICE_UNIT_ERROR,
                        )
                    )

                if (
                    flow.get("entity_energy_price") is not None
                    or flow.get("number_energy_price") is not None
                ):
                    validate_calls.append(
                        functools.partial(
                            _async_validate_auto_generated_cost_entity,
                            flow["stat_energy_from"],
                            source_result,
                        )
                    )

            for flow in source["flow_to"]:
                wanted_statistics_metadata.add(flow["stat_energy_to"])
                validate_calls.append(
                    functools.partial(
                        _async_validate_usage_stat,
                        shc,
                        statistics_metadata,
                        flow["stat_energy_to"],
                        _ENERGY_USAGE_DEVICE_CLASSES,
                        _ENERGY_USAGE_UNITS,
                        _ENERGY_UNIT_ERROR,
                        source_result,
                    )
                )

                if stat_compensation := flow.get("stat_compensation") is not None:
                    wanted_statistics_metadata.add(stat_compensation)
                    validate_calls.append(
                        functools.partial(
                            _async_validate_cost_stat,
                            shc,
                            recorder,
                            statistics_metadata,
                            stat_compensation,
                            source_result,
                        )
                    )
                elif flow.get("entity_energy_price") is not None:
                    validate_calls.append(
                        functools.partial(
                            _async_validate_price_entity,
                            shc,
                            flow["entity_energy_price"],
                            source_result,
                            _ENERGY_PRICE_UNITS,
                            _ENERGY_PRICE_UNIT_ERROR,
                        )
                    )

                if (
                    flow.get("entity_energy_price") is not None
                    or flow.get("number_energy_price") is not None
                ):
                    validate_calls.append(
                        functools.partial(
                            _async_validate_auto_generated_cost_entity,
                            recorder,
                            flow["stat_energy_to"],
                            source_result,
                        )
                    )

        elif source["type"] == "gas":
            wanted_statistics_metadata.add(source["stat_energy_from"])
            validate_calls.append(
                functools.partial(
                    _async_validate_usage_stat,
                    shc,
                    statistics_metadata,
                    recorder,
                    source["stat_energy_from"],
                    _GAS_USAGE_DEVICE_CLASSES,
                    _GAS_USAGE_UNITS,
                    _GAS_UNIT_ERROR,
                    source_result,
                )
            )

            if stat_cost := source.get("stat_cost") is not None:
                wanted_statistics_metadata.add(stat_cost)
                validate_calls.append(
                    functools.partial(
                        _async_validate_cost_stat,
                        shc,
                        recorder,
                        statistics_metadata,
                        stat_cost,
                        source_result,
                    )
                )
            elif source.get("entity_energy_price") is not None:
                validate_calls.append(
                    functools.partial(
                        _async_validate_price_entity,
                        shc,
                        source["entity_energy_price"],
                        source_result,
                        _GAS_PRICE_UNITS,
                        _GAS_PRICE_UNIT_ERROR,
                    )
                )

            if (
                source.get("entity_energy_price") is not None
                or source.get("number_energy_price") is not None
            ):
                validate_calls.append(
                    functools.partial(
                        _async_validate_auto_generated_cost_entity,
                        recorder,
                        source["stat_energy_from"],
                        source_result,
                    )
                )

        elif source["type"] == "water":
            wanted_statistics_metadata.add(source["stat_energy_from"])
            validate_calls.append(
                functools.partial(
                    _async_validate_usage_stat,
                    shc,
                    recorder,
                    statistics_metadata,
                    source["stat_energy_from"],
                    _WATER_USAGE_DEVICE_CLASSES,
                    _WATER_USAGE_UNITS,
                    _WATER_UNIT_ERROR,
                    source_result,
                )
            )

            if (stat_cost := source.get("stat_cost")) is not None:
                wanted_statistics_metadata.add(stat_cost)
                validate_calls.append(
                    functools.partial(
                        _async_validate_cost_stat,
                        shc,
                        recorder,
                        statistics_metadata,
                        stat_cost,
                        source_result,
                    )
                )
            elif source.get("entity_energy_price") is not None:
                validate_calls.append(
                    functools.partial(
                        _async_validate_price_entity,
                        shc,
                        source["entity_energy_price"],
                        source_result,
                        _WATER_PRICE_UNITS,
                        _WATER_PRICE_UNIT_ERROR,
                    )
                )

            if (
                source.get("entity_energy_price") is not None
                or source.get("number_energy_price") is not None
            ):
                validate_calls.append(
                    functools.partial(
                        _async_validate_auto_generated_cost_entity,
                        recorder,
                        source["stat_energy_from"],
                        source_result,
                    )
                )
        elif source["type"] == "solar":
            wanted_statistics_metadata.add(source["stat_energy_from"])
            validate_calls.append(
                functools.partial(
                    _async_validate_usage_stat,
                    recorder,
                    statistics_metadata,
                    source["stat_energy_from"],
                    _ENERGY_USAGE_DEVICE_CLASSES,
                    _ENERGY_USAGE_UNITS,
                    _ENERGY_UNIT_ERROR,
                    source_result,
                )
            )

        elif source["type"] == "battery":
            wanted_statistics_metadata.add(source["stat_energy_from"])
            validate_calls.append(
                functools.partial(
                    _async_validate_usage_stat,
                    shc,
                    recorder,
                    statistics_metadata,
                    source["stat_energy_from"],
                    _ENERGY_USAGE_DEVICE_CLASSES,
                    _ENERGY_USAGE_UNITS,
                    _ENERGY_UNIT_ERROR,
                    source_result,
                )
            )
            wanted_statistics_metadata.add(source["stat_energy_to"])
            validate_calls.append(
                functools.partial(
                    _async_validate_usage_stat,
                    shc,
                    recorder,
                    statistics_metadata,
                    source["stat_energy_to"],
                    _ENERGY_USAGE_DEVICE_CLASSES,
                    _ENERGY_USAGE_UNITS,
                    _ENERGY_UNIT_ERROR,
                    source_result,
                )
            )

    for device in manager.data["device_consumption"]:
        device_result: list[ValidationIssue] = []
        result.device_consumption.append(device_result)
        wanted_statistics_metadata.add(device["stat_consumption"])
        validate_calls.append(
            functools.partial(
                _async_validate_usage_stat,
                shc,
                recorder,
                statistics_metadata,
                device["stat_consumption"],
                _ENERGY_USAGE_DEVICE_CLASSES,
                _ENERGY_USAGE_UNITS,
                _ENERGY_UNIT_ERROR,
                device_result,
            )
        )

    # Fetch the needed statistics metadata
    statistics_metadata.update(
        await recorder.async_add_executor_job(
            functools.partial(
                recorder.statistics.get_metadata,
                statistic_ids=list(wanted_statistics_metadata),
            )
        )
    )

    # Execute all the validation checks
    for call in validate_calls:
        call()

    return result
