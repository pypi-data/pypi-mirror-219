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

from .alexa_capability import AlexaCapability


# pylint: disable=unused-variable
class AlexaEntity(abc.ABC):
    """An adaptation of an entity, expressed in Alexa's terms.

    Required base class for AlexaEntity in Alexa Component.
    """

    @property
    @abc.abstractmethod
    def entity_id(self):
        """Return the Entity ID."""

    @property
    @abc.abstractmethod
    def friendly_name(self):
        """Return the Alexa API friendly name."""

    @property
    @abc.abstractmethod
    def description(self):
        """Return the Alexa API description."""

    @property
    @abc.abstractmethod
    def alexa_id(self):
        """Return the Alexa API entity id."""

    @property
    @abc.abstractmethod
    def display_categories(self):
        """Return a list of display categories."""

    @property
    @abc.abstractmethod
    def default_display_categories(self):
        """Return a list of default display categories.

        This can be overridden by the user in the Home Assistant configuration.

        See also DisplayCategory.
        """

    @abc.abstractmethod
    def get_interface(self, capability) -> AlexaCapability:
        """Return the given AlexaInterface.

        Raises _UnsupportedInterface.
        """

    @property
    @abc.abstractmethod
    def interfaces(self) -> list[AlexaCapability]:
        """Return a list of supported interfaces.

        Used for discovery. The list should contain AlexaInterface instances.
        If the list is empty, this entity will not be discovered.
        """

    @abc.abstractmethod
    def serialize_properties(self):
        """Yield each supported property in API format."""

    @abc.abstractmethod
    def serialize_discovery(self):
        """Serialize the entity for discovery."""
