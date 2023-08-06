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


# pylint: disable=unused-variable
class AlexaModeResource(AlexaCapabilityResource):
    """Implements Alexa ModeResources.

    https://developer.amazon.com/docs/device-apis/resources-and-assets.html#capability-resources
    """

    def __init__(self, labels: typing.Iterable[str], ordered=False):
        """Initialize an Alexa modeResource."""
        super().__init__(labels)
        self._supported_modes = []
        self._mode_ordered = ordered

    def add_mode(self, value, labels: typing.Iterable[str]):
        """Add mode to the supportedModes object."""
        self._supported_modes.append({"value": value, "labels": labels})

    def serialize_configuration(self):
        """Return configuration for ModeResources friendlyNames serialized for an API response."""
        mode_resources = []
        for mode in self._supported_modes:
            result = {
                "value": mode["value"],
                "modeResources": self.serialize_labels(mode["labels"]),
            }
            mode_resources.append(result)

        return {"ordered": self._mode_ordered, "supportedModes": mode_resources}
