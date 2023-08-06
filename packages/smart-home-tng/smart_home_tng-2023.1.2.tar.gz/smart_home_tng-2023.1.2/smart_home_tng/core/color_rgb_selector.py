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

from .color_rgb_selector_config import ColorRGBSelectorConfig
from .config_validation import ConfigValidation as cv
from .selector import Selector


# pylint: disable=unused-variable
class ColorRGBSelector(Selector):
    """Selector of an RGB color value."""

    _CONFIG_SCHEMA: typing.Final = vol.Schema({})

    def config_schema(self, config: typing.Any) -> typing.Callable:
        return ColorRGBSelector._CONFIG_SCHEMA(config)

    def __init__(self, config: ColorRGBSelectorConfig = None) -> None:
        """Instantiate a selector."""
        super().__init__("color_rgb", config)

    def __call__(self, data: typing.Any) -> list[int]:
        """Validate the passed selection."""
        value: list[int] = vol.All(list, vol.ExactSequence((cv.byte,) * 3))(data)
        return value
