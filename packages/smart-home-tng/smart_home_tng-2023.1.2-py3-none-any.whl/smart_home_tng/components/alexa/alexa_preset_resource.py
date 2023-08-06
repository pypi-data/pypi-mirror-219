"""
Amazon Alexa Integration for Smart Home - The Next Generation.

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

from .alexa_capability_resource import AlexaCapabilityResource
from .alexa_global_catalog import AlexaGlobalCatalog


# pylint: disable=unused-variable
class AlexaPresetResource(AlexaCapabilityResource):
    """Implements Alexa PresetResources.

    Use presetResources with RangeController to provide a set of friendlyNames for each
    RangeController preset.

    https://developer.amazon.com/docs/device-apis/resources-and-assets.html#presetresources
    """

    def __init__(
        self, labels: typing.Iterable[str], min_value, max_value, precision, unit=None
    ):
        """Initialize an Alexa presetResource."""
        super().__init__(labels)
        self._presets = []
        self._minimum_value = min_value
        self._maximum_value = max_value
        self._precision = precision
        self._unit_of_measure = None
        if unit in AlexaGlobalCatalog.__dict__.values():
            self._unit_of_measure = unit

    def add_preset(self, value, labels: typing.Iterable[str]):
        """Add preset to configuration presets array."""
        self._presets.append({"value": value, "labels": labels})

    def serialize_configuration(self):
        """Return configuration for PresetResources friendlyNames serialized for an API response."""
        configuration = {
            "supportedRange": {
                "minimumValue": self._minimum_value,
                "maximumValue": self._maximum_value,
                "precision": self._precision,
            }
        }

        if self._unit_of_measure:
            configuration["unitOfMeasure"] = self._unit_of_measure

        if self._presets:
            preset_resources = [
                {
                    "rangeValue": preset["value"],
                    "presetResources": self.serialize_labels(preset["labels"]),
                }
                for preset in self._presets
            ]
            configuration["presets"] = preset_resources

        return configuration
