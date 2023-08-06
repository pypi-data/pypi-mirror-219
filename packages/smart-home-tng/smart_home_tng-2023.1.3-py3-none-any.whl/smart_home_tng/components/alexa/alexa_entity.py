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
from .alexa_capability import AlexaCapability

_alexa: typing.TypeAlias = core.Alexa
_const: typing.TypeAlias = core.Const

_LOGGER: typing.Final = logging.getLogger(__name__)
_TRANSLATION_TABLE: typing.Final = dict.fromkeys(map(ord, r"}{\/|\"()[]+~!><*%"), None)


# pylint: disable=unused-variable
class AlexaEntity(_alexa.Entity):
    """An adaptation of an entity, expressed in Alexa's terms.

    The API handlers should manipulate entities only through this interface.
    """

    def __init__(
        self,
        shc: core.SmartHomeController,
        config: _alexa.AbstractConfig,
        entity: core.State,
    ) -> None:
        """Initialize Alexa Entity."""
        self._shc = shc
        self._config = config
        self._entity = entity
        self._entity_conf = config.entity_config.get(entity.entity_id, {})

    @property
    def entity_id(self):
        """Return the Entity ID."""
        return self._entity.entity_id

    @property
    def friendly_name(self):
        """Return the Alexa API friendly name."""
        return self._entity_conf.get(_const.CONF_NAME, self._entity.name).translate(
            _TRANSLATION_TABLE
        )

    @property
    def description(self):
        """Return the Alexa API description."""
        description = self._entity_conf.get(_const.CONF_DESCRIPTION, self.entity_id)
        if description is None:
            description = self.entity_id
        return description.translate(_TRANSLATION_TABLE)

    @property
    def alexa_id(self):
        """Return the Alexa API entity id."""
        return _generate_alexa_id(self._entity.entity_id)

    @property
    def display_categories(self):
        """Return a list of display categories."""
        entity_conf = self._config.entity_config.get(self._entity.entity_id, {})
        if _alexa.CONF_DISPLAY_CATEGORIES in entity_conf:
            return [entity_conf[_alexa.CONF_DISPLAY_CATEGORIES]]
        return self.default_display_categories

    @property
    def default_display_categories(self):
        """Return a list of default display categories.

        This can be overridden by the user in the Home Assistant configuration.

        See also DisplayCategory.
        """
        raise NotImplementedError

    def get_interface(self, capability) -> AlexaCapability:
        """Return the given AlexaInterface.

        Raises _UnsupportedInterface.
        """

    @property
    def interfaces(self) -> list[AlexaCapability]:
        """Return a list of supported interfaces.

        Used for discovery. The list should contain AlexaInterface instances.
        If the list is empty, this entity will not be discovered.
        """
        raise NotImplementedError

    def serialize_properties(self):
        """Yield each supported property in API format."""
        for interface in self.interfaces:
            if not interface.properties_proactively_reported():
                continue

            yield from interface.serialize_properties()

    @property
    def custom_identifier(self) -> str:
        user_identifier = self._config.user_identifier()
        if user_identifier:
            return f"{user_identifier}-{self.entity_id}"
        return self.entity_id

    def serialize_discovery(self):
        """Serialize the entity for discovery."""
        manufacturer = "Smart Home - The Next Generation"
        model = self._entity.domain

        result = {
            "displayCategories": self.display_categories,
            "cookie": {},
            "endpointId": self.alexa_id,
            "friendlyName": self.friendly_name,
            "description": self.description,
            "manufacturerName": manufacturer,
            "additionalAttributes": {
                "manufacturer": manufacturer,
                "model": model,
                "serialNumber": self.entity_id,
                "softwareVersion": _const.__version__,
                "customIdentifier": self.custom_identifier,
            },
        }

        locale = self._config.locale
        capabilities = []

        for i in self.interfaces:
            if locale not in i.supported_locales:
                continue

            try:
                capabilities.append(i.serialize_discovery())
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(
                    f"Error serializing {i.name()} discovery for {self._entity}"
                )

        result["capabilities"] = capabilities

        return result


def _generate_alexa_id(entity_id: str) -> str:
    """Return the alexa ID for an entity ID."""
    return entity_id.replace(".", "#").translate(_TRANSLATION_TABLE)
