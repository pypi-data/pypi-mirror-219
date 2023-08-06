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

import typing

import voluptuous as vol

from .const import Const
from .number_selector_config import NumberSelectorConfig
from .number_selector_mode import NumberSelectorMode
from .selector import Selector


# pylint: disable=unused-variable
class NumberSelector(Selector):
    """Selector of a numeric value."""

    @staticmethod
    def has_min_max_if_slider(data: typing.Any) -> typing.Any:
        """Validate configuration."""
        if data["mode"] == "box":
            return data

        if "min" not in data or "max" not in data:
            raise vol.Invalid("min and max are required in slider mode")
        return data

    _CONFIG_SCHEMA: typing.Final = vol.All(
        vol.Schema(
            {
                vol.Optional("min"): vol.Coerce(float),
                vol.Optional("max"): vol.Coerce(float),
                # Controls slider steps, and up/down keyboard binding for the box
                # user input is not rounded
                vol.Optional("step", default=1): vol.All(
                    vol.Coerce(float), vol.Range(min=1e-3)
                ),
                vol.Optional(Const.CONF_UNIT_OF_MEASUREMENT): str,
                vol.Optional(
                    Const.CONF_MODE, default=NumberSelectorMode.SLIDER
                ): vol.All(vol.Coerce(NumberSelectorMode), lambda val: val.value),
            }
        ),
        has_min_max_if_slider,
    )

    def config_schema(self, config: typing.Any) -> typing.Callable:
        return NumberSelector._CONFIG_SCHEMA(config)

    def __init__(self, config: NumberSelectorConfig = None) -> None:
        """Instantiate a selector."""
        super().__init__("number", config)

    def __call__(self, data: typing.Any) -> float:
        """Validate the passed selection."""
        value: float = vol.Coerce(float)(data)

        if "min" in self._config and value < self._config["min"]:
            raise vol.Invalid(f"Value {value} is too small")

        if "max" in self._config and value > self._config["max"]:
            raise vol.Invalid(f"Value {value} is too large")
        return value
