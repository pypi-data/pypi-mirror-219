"""
Authentication Layer for Smart Home - The Next Generation.

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
import uuid

import attr

from . import permissions as perm
from .const import Const
from .credentials import Credentials
from .group import Group


if not typing.TYPE_CHECKING:

    class RefreshToken:
        ...


if typing.TYPE_CHECKING:
    from .refresh_token import RefreshToken


# pylint: disable=unused-variable
@attr.s(slots=True)
class User:
    """A user."""

    name: str = attr.ib()
    perm_lookup: perm.PermissionLookup = attr.ib(eq=False, order=False)
    id: str = attr.ib(factory=lambda: uuid.uuid4().hex)
    is_owner: bool = attr.ib(default=False)
    is_active: bool = attr.ib(default=False)
    system_generated: bool = attr.ib(default=False)
    local_only: bool = attr.ib(default=False)

    groups: list[Group] = attr.ib(factory=list, eq=False, order=False)

    # List of credentials of a user.
    credentials: list[Credentials] = attr.ib(factory=list, eq=False, order=False)

    # Tokens associated with a user.
    refresh_tokens: dict[str, RefreshToken] = attr.ib(
        factory=dict, eq=False, order=False
    )

    _permissions: perm.PolicyPermissions = attr.ib(
        init=False,
        eq=False,
        order=False,
        default=None,
    )

    @property
    def permissions(self) -> perm.AbstractPermissions:
        """Return permissions object for user."""
        if self.is_owner:
            return perm.OWNER_PERMISSIONS

        if self._permissions is not None:
            return self._permissions

        self._permissions = perm.PolicyPermissions(
            perm.merge_policies([group.policy for group in self.groups]),
            self.perm_lookup,
        )

        return self._permissions

    @property
    def is_admin(self) -> bool:
        """Return if user is part of the admin group."""
        if self.is_owner:
            return True

        return self.is_active and any(
            gr.id == Const.GROUP_ID_ADMIN for gr in self.groups
        )

    def invalidate_permission_cache(self) -> None:
        """Invalidate permission cache."""
        self._permissions = None
