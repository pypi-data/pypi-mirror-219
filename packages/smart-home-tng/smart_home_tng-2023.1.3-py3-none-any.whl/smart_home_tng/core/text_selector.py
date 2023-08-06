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
from .text_selector_config import TextSelectorConfig
from .text_selector_type import TextSelectorType


# pylint: disable:unused-variable
class TextSelector(Selector):
    """Selector for a multi-line text string."""

    _CONFIG_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Optional("multiline", default=False): bool,
            vol.Optional("suffix"): str,
            # The "type" controls the input field in the browser, the resulting
            # data can be any string so we don't validate it.
            vol.Optional("type"): vol.All(
                vol.Coerce(TextSelectorType), lambda val: val.value
            ),
        }
    )

    def config_schema(self, config: typing.Any) -> typing.Callable:
        return TextSelector._CONFIG_SCHEMA(config)

    def __init__(self, config: TextSelectorConfig = None) -> None:
        """Instantiate a selector."""
        super().__init__("text", config)

    def __call__(self, data: typing.Any) -> str:
        """Validate the passed selection."""
        text: str = vol.Schema(str)(data)
        return text
