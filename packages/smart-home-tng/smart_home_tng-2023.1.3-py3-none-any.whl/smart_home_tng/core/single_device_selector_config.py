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

from .single_entity_selector_config import (
    SINGLE_ENTITY_SELECTOR_CONFIG_SCHEMA,
    SingleEntitySelectorConfig,
)

# pylint: disable=unused-variable
SINGLE_DEVICE_SELECTOR_CONFIG_SCHEMA = vol.Schema(
    {
        # Integration linked to it with a config entry
        vol.Optional("integration"): str,
        # Manufacturer of device
        vol.Optional("manufacturer"): str,
        # Model of device
        vol.Optional("model"): str,
        # Device has to contain entities matching this selector
        vol.Optional("entity"): SINGLE_ENTITY_SELECTOR_CONFIG_SCHEMA,
    }
)


class SingleDeviceSelectorConfig(typing.TypedDict, total=False):
    """Class to represent a single device selector config."""

    integration: str
    manufacturer: str
    model: str
    entity: SingleEntitySelectorConfig
