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

from .config_validation import ConfigValidation as cv
from .select_selector_config import SelectSelectorConfig
from .select_selector_mode import SelectSelectorMode
from .selector import Selector


# pylint: disable=unused-variable
class SelectSelector(Selector):
    """Selector for an single-choice input select."""

    _SELECT_OPTION: typing.Final = vol.All(
        dict,
        vol.Schema(
            {
                vol.Required("value"): str,
                vol.Required("label"): str,
            }
        ),
    )

    _CONFIG_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Required("options"): vol.All(vol.Any([str], [_SELECT_OPTION])),
            vol.Optional("multiple", default=False): cv.boolean,
            vol.Optional("custom_value", default=False): cv.boolean,
            vol.Optional("mode"): vol.All(
                vol.Coerce(SelectSelectorMode), lambda val: val.value
            ),
        }
    )

    def config_schema(self, config: typing.Any) -> typing.Callable:
        return SelectSelector._CONFIG_SCHEMA(config)

    def __init__(self, config: SelectSelectorConfig = None) -> None:
        """Instantiate a selector."""
        super().__init__("select", config)

    def __call__(self, data: typing.Any) -> typing.Any:
        """Validate the passed selection."""
        options = []
        if self._config["options"]:
            if isinstance(self._config["options"][0], str):
                options = self._config["options"]
            else:
                options = [option["value"] for option in self._config["options"]]

        parent_schema = vol.In(options)
        if self._config["custom_value"]:
            parent_schema = vol.Any(parent_schema, str)

        if not self._config["multiple"]:
            return parent_schema(vol.Schema(str)(data))
        if not isinstance(data, list):
            raise vol.Invalid("Value should be a list")
        return [parent_schema(vol.Schema(str)(val)) for val in data]
