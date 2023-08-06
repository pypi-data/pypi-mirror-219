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
from .selector import Selector
from .single_device_selector_config import SINGLE_DEVICE_SELECTOR_CONFIG_SCHEMA
from .single_entity_selector_config import SINGLE_ENTITY_SELECTOR_CONFIG_SCHEMA
from .target_selector_config import TargetSelectorConfig

_CONFIG_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional("entity"): SINGLE_ENTITY_SELECTOR_CONFIG_SCHEMA,
        vol.Optional("device"): SINGLE_DEVICE_SELECTOR_CONFIG_SCHEMA,
    }
)

_TARGET_SELECTION_SCHEMA: typing.Final = vol.Schema(cv.TARGET_SERVICE_FIELDS)


# pylint: disable=unused-variable
class TargetSelector(Selector):
    """Selector of a target value (area ID, device ID, entity ID etc).

    Value should follow TARGET_SERVICE_FIELDS format.
    """

    CONFIG_SCHEMA: typing.Final = _CONFIG_SCHEMA

    def config_schema(self, config: typing.Any) -> typing.Callable:
        return _CONFIG_SCHEMA(config)

    def __init__(self, config: TargetSelectorConfig = None) -> None:
        """Instantiate a selector."""
        super().__init__("target", config)

    def __call__(self, data: typing.Any) -> dict[str, list[str]]:
        """Validate the passed selection."""
        target: dict[str, list[str]] = _TARGET_SELECTION_SCHEMA(data)
        return target
