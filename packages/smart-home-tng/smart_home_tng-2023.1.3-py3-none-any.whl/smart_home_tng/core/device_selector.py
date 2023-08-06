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
from .device_selector_config import DeviceSelectorConfig
from .selector import Selector
from .single_device_selector_config import SINGLE_DEVICE_SELECTOR_CONFIG_SCHEMA

_CONFIG_SCHEMA: typing.Final = SINGLE_DEVICE_SELECTOR_CONFIG_SCHEMA.extend(
    {vol.Optional("multiple", default=False): cv.boolean}
)


# pylint: disable=unused-variable
class DeviceSelector(Selector):
    """Selector of a single or list of devices."""

    def __init__(self, config: DeviceSelectorConfig = None) -> None:
        """Instantiate a selector."""
        selector_type = "device"
        super().__init__(selector_type, config)

    def __call__(self, data: typing.Any) -> str | list[str]:
        """Validate the passed selection."""
        if not self._config["multiple"]:
            device_id: str = vol.Schema(str)(data)
            return device_id
        if not isinstance(data, list):
            raise vol.Invalid("Value should be a list")
        return [vol.Schema(str)(val) for val in data]

    def config_schema(self, config: typing.Any) -> typing.Any:
        return _CONFIG_SCHEMA(config)
