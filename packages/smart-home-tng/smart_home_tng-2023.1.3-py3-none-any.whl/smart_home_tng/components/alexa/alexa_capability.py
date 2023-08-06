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

import logging
import typing

from ... import core

_alexa: typing.TypeAlias = core.Alexa

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class AlexaCapability(_alexa.Capability):
    """Base class for Alexa capability interfaces.

    The Smart Home Skills API defines a number of "capability interfaces",
    roughly analogous to domains in Home Assistant. The supported interfaces
    describe what actions can be performed on a particular device.

    https://developer.amazon.com/docs/device-apis/message-guide.html
    """

    _supported_locales = {"en-US"}
    _supports_deactivation: bool = None
    _properties_non_controllable: bool = None

    @property
    def supported_locales(self) -> set[str]:
        return self._supported_locales

    def __init__(self, entity: core.State, instance: str = None) -> None:
        """Initialize an Alexa capability."""
        self._entity = entity
        self._instance = instance

    def name(self) -> str:
        """Return the Alexa API name of this interface."""
        raise NotImplementedError

    def properties_supported(self) -> list[dict]:
        """Return what properties this entity supports."""
        return []

    def properties_proactively_reported(self) -> bool:
        """Return True if properties asynchronously reported."""
        return False

    def properties_retrievable(self) -> bool:
        """Return True if properties can be retrieved."""
        return False

    def properties_non_controllable(self) -> bool:
        """Return True if non controllable."""
        return self._properties_non_controllable

    def get_property(self, name: str):
        """Read and return a property.

        Return value should be a dict, or raise UnsupportedProperty.

        Properties can also have a timeOfSample and uncertaintyInMilliseconds,
        but returning those metadata is not yet implemented.
        """
        raise _alexa.UnsupportedProperty(name)

    def supports_deactivation(self):
        """Applicable only to scenes."""
        return self._supports_deactivation

    def capability_proactively_reported(self):
        """Return True if the capability is proactively reported.

        Set properties_proactively_reported() for proactively reported properties.
        Applicable to DoorbellEventSource.
        """
        return None

    def capability_resources(self):
        """Return the capability object.

        Applicable to ToggleController, RangeController, and ModeController interfaces.
        """
        return []

    def configuration(self):
        """Return the configuration object.

        Applicable to the ThermostatController, SecurityControlPanel, ModeController,
        RangeController, and EventDetectionSensor.
        """
        return []

    def configurations(self):
        """Return the configurations object.

        The plural configurations object is different that the singular configuration object.
        Applicable to EqualizerController interface.
        """
        return []

    def inputs(self):
        """Applicable only to media players."""
        return []

    def semantics(self):
        """Return the semantics object.

        Applicable to ToggleController, RangeController, and ModeController interfaces.
        """
        return []

    def supported_operations(self):
        """Return the supportedOperations object."""
        return []

    def camera_stream_configurations(self):
        """Applicable only to CameraStreamController."""
        return None

    def serialize_discovery(self):
        """Serialize according to the Discovery API."""
        # pylint: disable=assignment-from-none
        # Methods may be overridden and return a value.
        result = {"type": "AlexaInterface", "interface": self.name(), "version": "3"}

        if (instance := self._instance) is not None:
            result["instance"] = instance

        properties_supported = self.properties_supported()
        if properties_supported:
            result["properties"] = {
                "supported": self.properties_supported(),
                "proactivelyReported": self.properties_proactively_reported(),
                "retrievable": self.properties_retrievable(),
            }

        proactively_reported = self.capability_proactively_reported()
        if proactively_reported is not None:
            result["proactivelyReported"] = proactively_reported

        non_controllable = self.properties_non_controllable()
        if non_controllable is not None:
            result["properties"]["nonControllable"] = non_controllable

        supports_deactivation = self.supports_deactivation()
        if supports_deactivation is not None:
            result["supportsDeactivation"] = supports_deactivation

        capability_resources = self.capability_resources()
        if capability_resources:
            result["capabilityResources"] = capability_resources

        configuration = self.configuration()
        if configuration:
            result["configuration"] = configuration

        # The plural configurations object is different than the singular
        # configuration object above.
        configurations = self.configurations()
        if configurations:
            result["configurations"] = configurations

        semantics = self.semantics()
        if semantics:
            result["semantics"] = semantics

        supported_operations = self.supported_operations()
        if supported_operations:
            result["supportedOperations"] = supported_operations

        inputs = self.inputs()
        if inputs:
            result["inputs"] = inputs

        camera_stream_configurations = self.camera_stream_configurations()
        if camera_stream_configurations:
            result["cameraStreamConfigurations"] = camera_stream_configurations

        return result

    def serialize_properties(self):
        """Return properties serialized for an API response."""
        for prop in self.properties_supported():
            prop_name = prop["name"]
            try:
                prop_value = self.get_property(prop_name)
            except _alexa.UnsupportedProperty:
                raise
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(
                    f"Unexpected error getting {self.name()}.{prop_name} property "
                    + f"from {self._entity}",
                )
                prop_value = None

            if prop_value is None:
                continue

            result = {
                "name": prop_name,
                "namespace": self.name(),
                "value": prop_value,
                "timeOfSample": core.helpers.utcnow().strftime(_alexa.DATE_FORMAT),
                "uncertaintyInMilliseconds": 0,
            }
            if (instance := self._instance) is not None:
                result["instance"] = instance

            yield result
