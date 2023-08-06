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

import collections
import collections.abc
import typing

import voluptuous as vol

from ... import core
from .flow_from_grid_source_type import FlowFromGridSourceType
from .source_adapter import SourceAdapter
from .source_type import SourceType

_cv: typing.TypeAlias = core.ConfigValidation


def _flow_from_ensure_single_price(
    val: FlowFromGridSourceType,
) -> FlowFromGridSourceType:
    """Ensure we use a single price source."""
    if (
        val["entity_energy_price"] is not None
        and val["number_energy_price"] is not None
    ):
        raise vol.Invalid("Define either an entity or a fixed number for the price")

    return val


def _generate_unique_value_validator(
    key: str,
) -> collections.abc.Callable[[list[dict]], list[dict]]:
    """Generate a validator that ensures a value is only used once."""

    def validate_uniqueness(
        val: list[dict],
    ) -> list[dict]:
        """Ensure that the user doesn't add duplicate values."""
        counts = collections.Counter(flow_from[key] for flow_from in val)

        for value, count in counts.items():
            if count > 1:
                raise vol.Invalid(f"Cannot specify {value} more than once")

        return val

    return validate_uniqueness


def _check_type_limits(value: list[SourceType]) -> list[SourceType]:
    """Validate that we don't have too many of certain types."""
    types = collections.Counter([val["type"] for val in value])

    if types.get("grid", 0) > 1:
        raise vol.Invalid("You cannot have more than 1 grid source")

    return value


# pylint: disable=unused-variable
class Const:
    """Constants for Energy Component."""

    FLOW_FROM_GRID_SOURCE_SCHEMA: typing.Final = vol.All(
        vol.Schema(
            {
                vol.Required("stat_energy_from"): str,
                vol.Optional("stat_cost"): vol.Any(str, None),
                vol.Optional("entity_energy_from"): vol.Any(str, None),
                vol.Optional("entity_energy_price"): vol.Any(str, None),
                vol.Optional("number_energy_price"): vol.Any(vol.Coerce(float), None),
            }
        ),
        _flow_from_ensure_single_price,
    )

    FLOW_TO_GRID_SOURCE_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required("stat_energy_to"): str,
            vol.Optional("stat_compensation"): vol.Any(str, None),
            vol.Optional("entity_energy_to"): vol.Any(str, None),
            vol.Optional("entity_energy_price"): vol.Any(str, None),
            vol.Optional("number_energy_price"): vol.Any(vol.Coerce(float), None),
        }
    )

    GRID_SOURCE_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required("type"): "grid",
            vol.Required("flow_from"): vol.All(
                [FLOW_FROM_GRID_SOURCE_SCHEMA],
                _generate_unique_value_validator("stat_energy_from"),
            ),
            vol.Required("flow_to"): vol.All(
                [FLOW_TO_GRID_SOURCE_SCHEMA],
                _generate_unique_value_validator("stat_energy_to"),
            ),
            vol.Required("cost_adjustment_day"): vol.Coerce(float),
        }
    )

    SOLAR_SOURCE_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required("type"): "solar",
            vol.Required("stat_energy_from"): str,
            vol.Optional("config_entry_solar_forecast"): vol.Any([str], None),
        }
    )

    BATTERY_SOURCE_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required("type"): "battery",
            vol.Required("stat_energy_from"): str,
            vol.Required("stat_energy_to"): str,
        }
    )

    GAS_SOURCE_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required("type"): "gas",
            vol.Required("stat_energy_from"): str,
            vol.Optional("stat_cost"): vol.Any(str, None),
            vol.Optional("entity_energy_from"): vol.Any(str, None),
            vol.Optional("entity_energy_price"): vol.Any(str, None),
            vol.Optional("number_energy_price"): vol.Any(vol.Coerce(float), None),
        }
    )

    ENERGY_SOURCE_SCHEMA: typing.Final = vol.All(
        vol.Schema(
            [
                _cv.key_value_schemas(
                    "type",
                    {
                        "grid": GRID_SOURCE_SCHEMA,
                        "solar": SOLAR_SOURCE_SCHEMA,
                        "battery": BATTERY_SOURCE_SCHEMA,
                        "gas": GAS_SOURCE_SCHEMA,
                    },
                )
            ]
        ),
        _check_type_limits,
    )

    DEVICE_CONSUMPTION_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required("stat_consumption"): str,
        }
    )

    SOURCE_ADAPTERS: typing.Final = (
        SourceAdapter(
            "grid",
            "flow_from",
            "stat_energy_from",
            "stat_cost",
            "Cost",
            "cost",
        ),
        SourceAdapter(
            "grid",
            "flow_to",
            "stat_energy_to",
            "stat_compensation",
            "Compensation",
            "compensation",
        ),
        SourceAdapter(
            "gas",
            None,
            "stat_energy_from",
            "stat_cost",
            "Cost",
            "cost",
        ),
        SourceAdapter(
            "water",
            None,
            "stat_energy_from",
            "stat_cost",
            "Cost",
            "cost",
        ),
    )

    SUPPORTED_STATE_CLASSES: typing.Final = {
        core.Sensor.StateClass.MEASUREMENT,
        core.Sensor.StateClass.TOTAL,
        core.Sensor.StateClass.TOTAL_INCREASING,
    }
    VALID_ENERGY_UNITS: typing.Final = {
        core.Const.UnitOfEnergy.WATT_HOUR,
        core.Const.UnitOfEnergy.KILO_WATT_HOUR,
        core.Const.UnitOfEnergy.MEGA_WATT_HOUR,
        core.Const.UnitOfEnergy.GIGA_JOULE,
    }
    VALID_ENERGY_UNITS_GAS: typing.Final = {
        core.Const.UnitOfVolume.CUBIC_METERS,
        core.Const.UnitOfVolume.CUBIC_FEET,
        *VALID_ENERGY_UNITS,
    }
    VALID_VOLUME_UNITS_WATER: typing.Final = {
        core.Const.UnitOfVolume.CUBIC_METERS,
        core.Const.UnitOfVolume.CUBIC_FEET,
        core.Const.UnitOfVolume.GALLONS,
        core.Const.UnitOfVolume.LITERS,
    }
