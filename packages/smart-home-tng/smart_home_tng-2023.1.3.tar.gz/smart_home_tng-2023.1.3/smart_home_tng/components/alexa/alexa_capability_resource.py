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

from .alexa_global_catalog import AlexaGlobalCatalog


# pylint: disable=unused-variable
class AlexaCapabilityResource:
    """Base class for Alexa capabilityResources, modeResources, and presetResources objects.

    Resources objects labels must be unique across all modeResources and presetResources within
    the same device.
    To provide support for all supported locales, include one label from the AlexaGlobalCatalog
    in the labels array.
    You cannot use any words from the following list as friendly names:
    https://developer.amazon.com/docs/alexa/device-apis/resources-and-assets.html#names-you-cannot-use

    https://developer.amazon.com/docs/device-apis/resources-and-assets.html#capability-resources
    """

    def __init__(self, labels: typing.Iterable[str]):
        """Initialize an Alexa resource."""
        self._resource_labels = []
        for label in labels:
            self._resource_labels.append(label)

    def serialize_capability_resources(self):
        """Return capabilityResources object serialized for an API response."""
        return self.serialize_labels(self._resource_labels)

    def serialize_configuration(self):
        """Return ModeResources, PresetResources friendlyNames serialized for an API response."""
        return []

    def serialize_labels(self, resources):
        """Return resource label objects for friendlyNames serialized for an API response."""
        labels = []
        for label in resources:
            if label in AlexaGlobalCatalog.__dict__.values():
                label = {"@type": "asset", "value": {"assetId": label}}
            else:
                label = {"@type": "text", "value": {"text": label, "locale": "en-US"}}

            labels.append(label)

        return {"friendlyNames": labels}
