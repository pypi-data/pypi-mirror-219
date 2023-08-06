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

from .selector import Selector
from .theme_selector_config import ThemeSelectorConfig


# pylint: disable=unused-variable
class ThemeSelector(Selector):
    """Selector for an theme."""

    _CONFIG_SCHEMA: typing.Final = vol.Schema({})

    def config_schema(self, config: typing.Any) -> typing.Callable:
        return ThemeSelector._CONFIG_SCHEMA(config)

    def __init__(self, config: ThemeSelectorConfig = None) -> None:
        """Instantiate a selector."""
        super().__init__("theme", config)

    def __call__(self, data: typing.Any) -> str:
        """Validate the passed selection."""
        theme: str = vol.Schema(str)(data)
        return theme
