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

import collections
import collections.abc
import fnmatch
import re
import typing

from .helpers import split_entity_id


# pylint: disable=unused-variable
class EntityValues:
    """Class to store entity id based values."""

    def __init__(
        self,
        exact: dict[str, dict[str, str]] = None,
        domain: dict[str, dict[str, str]] = None,
        glob: dict[str, dict[str, str]] = None,
    ) -> None:
        """Initialize an EntityConfigDict."""
        self._cache: dict[str, dict[str, str]] = {}
        self._exact = exact
        self._domain = domain

        if glob is None:
            compiled: dict[re.Pattern[str], typing.Any] = None
        else:
            compiled = collections.OrderedDict()
            for key, value in glob.items():
                compiled[re.compile(fnmatch.translate(key))] = value

        self._glob = compiled

    def get(self, entity_id: str) -> dict[str, str]:
        """Get config for an entity id."""
        if entity_id in self._cache:
            return self._cache[entity_id]

        domain, _ = split_entity_id(entity_id)
        result = self._cache[entity_id] = {}

        if self._domain is not None and domain in self._domain:
            result.update(self._domain[domain])

        if self._glob is not None:
            for pattern, values in self._glob.items():
                if pattern.match(entity_id):
                    result.update(values)

        if self._exact is not None and entity_id in self._exact:
            result.update(self._exact[entity_id])

        return result
