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

import abc


# pylint: disable=unused-variable
class AlexaCapability(abc.ABC):
    """Base class for Alexa capability interfaces.

    The Smart Home Skills API defines a number of "capability interfaces",
    roughly analogous to domains in Home Assistant. The supported interfaces
    describe what actions can be performed on a particular device.

    https://developer.amazon.com/docs/device-apis/message-guide.html

    Required base class for AlexaCapability in Alexa Component.
    """

    @abc.abstractmethod
    def name(self) -> str:
        """Return the Alexa API name of this interface."""

    @abc.abstractmethod
    def properties_supported(self) -> list[dict]:
        """Return what properties this entity supports."""

    @abc.abstractmethod
    def properties_proactively_reported(self) -> bool:
        """Return True if properties asynchronously reported."""

    @abc.abstractmethod
    def properties_retrievable(self) -> bool:
        """Return True if properties can be retrieved."""

    @abc.abstractmethod
    def properties_non_controllable(self) -> bool:
        """Return True if non controllable."""

    @abc.abstractmethod
    def get_property(self, name):
        """Read and return a property.

        Return value should be a dict, or raise UnsupportedProperty.

        Properties can also have a timeOfSample and uncertaintyInMilliseconds,
        but returning those metadata is not yet implemented.
        """

    @abc.abstractmethod
    def supports_deactivation(self):
        """Applicable only to scenes."""

    @abc.abstractmethod
    def capability_proactively_reported(self):
        """Return True if the capability is proactively reported.

        Set properties_proactively_reported() for proactively reported properties.
        Applicable to DoorbellEventSource.
        """

    @abc.abstractmethod
    def capability_resources(self):
        """Return the capability object.

        Applicable to ToggleController, RangeController, and ModeController interfaces.
        """

    @abc.abstractmethod
    def configuration(self):
        """Return the configuration object.

        Applicable to the ThermostatController, SecurityControlPanel, ModeController,
        RangeController and EventDetectionSensor.
        """

    @abc.abstractmethod
    def configurations(self):
        """Return the configurations object.

        The plural configurations object is different that the singular configuration object.
        Applicable to EqualizerController interface.
        """

    @abc.abstractmethod
    def inputs(self):
        """Applicable only to media players."""

    @abc.abstractmethod
    def semantics(self):
        """Return the semantics object.

        Applicable to ToggleController, RangeController, and ModeController interfaces.
        """

    @abc.abstractmethod
    def supported_operations(self):
        """Return the supportedOperations object."""

    @abc.abstractmethod
    def camera_stream_configurations(self):
        """Applicable only to CameraStreamController."""

    @abc.abstractmethod
    def serialize_discovery(self):
        """Serialize according to the Discovery API."""

    @abc.abstractmethod
    def serialize_properties(self):
        """Return properties serialized for an API response."""
