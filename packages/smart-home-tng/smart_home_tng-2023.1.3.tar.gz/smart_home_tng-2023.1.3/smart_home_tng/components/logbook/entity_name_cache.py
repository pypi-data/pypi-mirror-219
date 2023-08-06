"""
Logbook Component for Smart Home - The Next Generation.

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

from ... import core


# pylint: disable=unused-variable
class EntityNameCache:
    """A cache to lookup the name for an entity.

    This class should not be used to lookup attributes
    that are expected to change state.
    """

    def __init__(self, shc: core.SmartHomeController) -> None:
        """Init the cache."""
        self._shc = shc
        self._names: dict[str, str] = {}

    def get(self, entity_id: str) -> str:
        """Lookup an the friendly name."""
        if entity_id in self._names:
            return self._names[entity_id]
        if (current_state := self._shc.states.get(entity_id)) and (
            friendly_name := current_state.attributes.get(core.Const.ATTR_FRIENDLY_NAME)
        ):
            self._names[entity_id] = friendly_name
        else:
            return core.helpers.split_entity_id(entity_id)[1].replace("_", " ")

        return self._names[entity_id]
