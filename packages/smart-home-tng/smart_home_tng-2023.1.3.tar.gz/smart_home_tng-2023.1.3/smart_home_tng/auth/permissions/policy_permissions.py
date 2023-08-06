"""
Permission Layer for Smart Home - The Next Generation.

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

import collections.abc
import typing

from . import helpers
from .abstract_permissions import AbstractPermissions
from .const import Const
from .permission_lookup import PermissionLookup
from .policy_type import PolicyType


class PolicyPermissions(AbstractPermissions):
    """Handle permissions."""

    def __init__(self, policy: PolicyType, perm_lookup: PermissionLookup) -> None:
        """Initialize the permission class."""
        self._policy = policy
        self._perm_lookup = perm_lookup

    def access_all_entities(self, key: str) -> bool:
        """Check if we have a certain access to all entities."""
        return helpers.test_all(self._policy.get(Const.CAT_ENTITIES), key)

    def _entity_func(self) -> collections.abc.Callable[[str, str], bool]:
        """Return a function that can test entity access."""
        return helpers.compile_entities(
            self._policy.get(Const.CAT_ENTITIES), self._perm_lookup
        )

    # pylint: disable=protected-access
    def __eq__(self, other: typing.Any) -> bool:
        """Equals check."""
        return isinstance(other, PolicyPermissions) and other._policy == self._policy
