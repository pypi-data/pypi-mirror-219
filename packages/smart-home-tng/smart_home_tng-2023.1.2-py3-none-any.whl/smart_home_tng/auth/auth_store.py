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

import asyncio
import collections
import datetime
import hmac
import logging
import typing

from ..core import helpers
from ..core.callback import callback
from ..core.store import Store
from . import permissions as perm
from .const import Const
from .credentials import Credentials
from .group import Group
from .refresh_token import RefreshToken
from .token_type import TokenType
from .user import User

_STORAGE_VERSION: typing.Final = 1
_STORAGE_KEY: typing.Final = "auth"
_GROUP_NAME_ADMIN: typing.Final = "Administrators"
_GROUP_NAME_USER: typing.Final = "Users"
_GROUP_NAME_READ_ONLY: typing.Final = "Read Only"

_LOGGER: typing.Final = logging.getLogger(__name__)


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from ..core.smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class AuthStore:
    """Stores authentication info.

    Any mutation to an object should happen inside the auth store.

    The auth store is lazy. It won't load the data from disk until a method is
    called that needs it.
    """

    def __init__(self, shc: SmartHomeController) -> None:
        """Initialize the auth store."""
        self._shc = shc
        self._users: dict[str, User] = None
        self._groups: dict[str, Group] = None
        self._perm_lookup: perm.PermissionLookup = None
        self._store = Store(
            shc, _STORAGE_VERSION, _STORAGE_KEY, private=True, atomic_writes=True
        )
        self._lock = asyncio.Lock()

    async def async_get_groups(self) -> list[Group]:
        """Retrieve all users."""
        if self._groups is None:
            await self._async_load()
            assert self._groups is not None

        return list(self._groups.values())

    async def async_get_group(self, group_id: str) -> Group:
        """Retrieve all users."""
        if self._groups is None:
            await self._async_load()
            assert self._groups is not None

        return self._groups.get(group_id)

    async def async_get_users(self) -> list[User]:
        """Retrieve all users."""
        if self._users is None:
            await self._async_load()
            assert self._users is not None

        return list(self._users.values())

    async def async_get_user(self, user_id: str) -> User:
        """Retrieve a user by id."""
        if self._users is None:
            await self._async_load()
            assert self._users is not None

        return self._users.get(user_id)

    async def async_create_user(
        self,
        name: str,
        is_owner: bool = None,
        is_active: bool = None,
        system_generated: bool = None,
        credentials: Credentials = None,
        group_ids: list[str] = None,
        local_only: bool = None,
    ) -> User:
        """Create a new user."""
        if self._users is None:
            await self._async_load()

        assert self._users is not None
        assert self._groups is not None

        groups = []
        for group_id in group_ids or []:
            if (group := self._groups.get(group_id)) is None:
                raise ValueError(f"Invalid group specified {group_id}")
            groups.append(group)

        kwargs: dict[str, typing.Any] = {
            "name": name,
            # Until we get group management, we just put everyone in the
            # same group.
            "groups": groups,
            "perm_lookup": self._perm_lookup,
        }

        for attr_name, value in (
            ("is_owner", is_owner),
            ("is_active", is_active),
            ("local_only", local_only),
            ("system_generated", system_generated),
        ):
            if value is not None:
                kwargs[attr_name] = value

        new_user = User(**kwargs)

        self._users[new_user.id] = new_user

        if credentials is None:
            self._async_schedule_save()
            return new_user

        # Saving is done inside the link.
        await self.async_link_user(new_user, credentials)
        return new_user

    async def async_link_user(self, user: User, credentials: Credentials) -> None:
        """Add credentials to an existing user."""
        user.credentials.append(credentials)
        self._async_schedule_save()
        credentials.is_new = False

    async def async_remove_user(self, user: User) -> None:
        """Remove a user."""
        if self._users is None:
            await self._async_load()
            assert self._users is not None

        self._users.pop(user.id)
        self._async_schedule_save()

    async def async_update_user(
        self,
        user: User,
        name: str = None,
        is_active: bool = None,
        group_ids: list[str] = None,
        local_only: bool = None,
    ) -> None:
        """Update a user."""
        assert self._groups is not None

        if group_ids is not None:
            groups = []
            for grid in group_ids:
                if (group := self._groups.get(grid)) is None:
                    raise ValueError("Invalid group specified.")
                groups.append(group)

            user.groups = groups
            user.invalidate_permission_cache()

        for attr_name, value in (
            ("name", name),
            ("is_active", is_active),
            ("local_only", local_only),
        ):
            if value is not None:
                setattr(user, attr_name, value)

        self._async_schedule_save()

    async def async_activate_user(self, user: User) -> None:
        """Activate a user."""
        user.is_active = True
        self._async_schedule_save()

    async def async_deactivate_user(self, user: User) -> None:
        """Activate a user."""
        user.is_active = False
        self._async_schedule_save()

    async def async_remove_credentials(self, credentials: Credentials) -> None:
        """Remove credentials."""
        if self._users is None:
            await self._async_load()
            assert self._users is not None

        for user in self._users.values():
            found = None

            for index, cred in enumerate(user.credentials):
                if cred is credentials:
                    found = index
                    break

            if found is not None:
                user.credentials.pop(found)
                break

        self._async_schedule_save()

    async def async_create_refresh_token(
        self,
        user: User,
        client_id: str = None,
        client_name: str = None,
        client_icon: str = None,
        token_type: str = str(TokenType.NORMAL),
        access_token_expiration: datetime.timedelta = Const.ACCESS_TOKEN_EXPIRATION,
        credential: Credentials = None,
    ) -> RefreshToken:
        """Create a new token for a user."""
        kwargs: dict[str, typing.Any] = {
            "user": user,
            "client_id": client_id,
            "token_type": token_type,
            "access_token_expiration": access_token_expiration,
            "credential": credential,
        }
        if client_name:
            kwargs["client_name"] = client_name
        if client_icon:
            kwargs["client_icon"] = client_icon

        refresh_token = RefreshToken(**kwargs)
        user.refresh_tokens[refresh_token.id] = refresh_token

        self._async_schedule_save()
        return refresh_token

    async def async_remove_refresh_token(self, refresh_token: RefreshToken) -> None:
        """Remove a refresh token."""
        if self._users is None:
            await self._async_load()
            assert self._users is not None

        for user in self._users.values():
            if user.refresh_tokens.pop(refresh_token.id, None):
                self._async_schedule_save()
                break

    async def async_get_refresh_token(self, token_id: str) -> RefreshToken:
        """Get refresh token by id."""
        if self._users is None:
            await self._async_load()
            assert self._users is not None

        for user in self._users.values():
            refresh_token = user.refresh_tokens.get(token_id)
            if refresh_token is not None:
                return refresh_token

        return None

    async def async_get_refresh_token_by_token(self, token: str) -> RefreshToken:
        """Get refresh token by token."""
        if self._users is None:
            await self._async_load()
            assert self._users is not None

        found = None

        for user in self._users.values():
            for refresh_token in user.refresh_tokens.values():
                if hmac.compare_digest(refresh_token.token, token):
                    found = refresh_token

        return found

    @callback
    def async_log_refresh_token_usage(
        self, refresh_token: RefreshToken, remote_ip: str = None
    ) -> None:
        """Update refresh token last used information."""
        refresh_token.last_used_at = helpers.utcnow()
        refresh_token.last_used_ip = remote_ip
        self._async_schedule_save()

    async def _async_load(self) -> None:
        """Load the users."""
        async with self._lock:
            if self._users is not None:
                return
            await self._async_load_task()

    async def _async_load_task(self) -> None:
        """Load the users."""
        dev_reg = self._shc.device_registry
        ent_reg = self._shc.entity_registry
        data = await self._store.async_load()

        # Make sure that we're not overriding data if 2 loads happened at the
        # same time
        if self._users is not None:
            return

        self._perm_lookup = perm_lookup = perm.PermissionLookup(ent_reg, dev_reg)

        if data is None or not isinstance(data, dict):
            self._set_defaults()
            return

        users: dict[str, User] = collections.OrderedDict()
        groups: dict[str, Group] = collections.OrderedDict()
        credentials: dict[str, Credentials] = collections.OrderedDict()

        # Soft-migrating data as we load. We are going to make sure we have a
        # read only group and an admin group. There are two states that we can
        # migrate from:
        # 1. Data from a recent version which has a single group without policy
        # 2. Data from old version which has no groups
        has_admin_group = False
        has_user_group = False
        has_read_only_group = False
        group_without_policy = None

        # When creating objects we mention each attribute explicitly. This
        # prevents crashing if user rolls back HA version after a new property
        # was added.

        for group_dict in data.get("groups", []):
            policy: perm.PolicyType = None

            if group_dict["id"] == Const.GROUP_ID_ADMIN:
                has_admin_group = True

                name = _GROUP_NAME_ADMIN
                policy = perm.SystemPolicies.ADMIN_POLICY
                system_generated = True

            elif group_dict["id"] == Const.GROUP_ID_USER:
                has_user_group = True

                name = _GROUP_NAME_USER
                policy = perm.SystemPolicies.USER_POLICY
                system_generated = True

            elif group_dict["id"] == Const.GROUP_ID_READ_ONLY:
                has_read_only_group = True

                name = _GROUP_NAME_READ_ONLY
                policy = perm.SystemPolicies.READ_ONLY_POLICY
                system_generated = True

            else:
                name = group_dict["name"]
                policy = group_dict.get("policy")
                system_generated = False

            # We don't want groups without a policy that are not system groups
            # This is part of migrating from state 1
            if policy is None:
                group_without_policy = group_dict["id"]
                continue

            groups[group_dict["id"]] = Group(
                id=group_dict["id"],
                name=name,
                policy=policy,
                system_generated=system_generated,
            )

        # If there are no groups, add all existing users to the admin group.
        # This is part of migrating from state 2
        migrate_users_to_admin_group = not groups and group_without_policy is None

        # If we find a no_policy_group, we need to migrate all users to the
        # admin group. We only do this if there are no other groups, as is
        # the expected state. If not expected state, not marking people admin.
        # This is part of migrating from state 1
        if groups and group_without_policy is not None:
            group_without_policy = None

        # This is part of migrating from state 1 and 2
        if not has_admin_group:
            admin_group = _system_admin_group()
            groups[admin_group.id] = admin_group

        # This is part of migrating from state 1 and 2
        if not has_read_only_group:
            read_only_group = _system_read_only_group()
            groups[read_only_group.id] = read_only_group

        if not has_user_group:
            user_group = _system_user_group()
            groups[user_group.id] = user_group

        for user_dict in data["users"]:
            # Collect the users group.
            user_groups = []
            for group_id in user_dict.get("group_ids", []):
                # This is part of migrating from state 1
                if group_id == group_without_policy:
                    group_id = Const.GROUP_ID_ADMIN
                user_groups.append(groups[group_id])

            # This is part of migrating from state 2
            if not user_dict["system_generated"] and migrate_users_to_admin_group:
                user_groups.append(groups[Const.GROUP_ID_ADMIN])

            users[user_dict["id"]] = User(
                name=user_dict["name"],
                groups=user_groups,
                id=user_dict["id"],
                is_owner=user_dict["is_owner"],
                is_active=user_dict["is_active"],
                system_generated=user_dict["system_generated"],
                perm_lookup=perm_lookup,
                # New in 2021.11
                local_only=user_dict.get("local_only", False),
            )

        for cred_dict in data["credentials"]:
            credential = Credentials(
                id=cred_dict["id"],
                is_new=False,
                auth_provider_type=cred_dict["auth_provider_type"],
                auth_provider_id=cred_dict["auth_provider_id"],
                data=cred_dict["data"],
            )
            credentials[cred_dict["id"]] = credential
            users[cred_dict["user_id"]].credentials.append(credential)

        for rt_dict in data["refresh_tokens"]:
            # Filter out the old keys that don't have jwt_key (pre-0.76)
            if "jwt_key" not in rt_dict:
                continue

            created_at = helpers.parse_datetime(rt_dict["created_at"])
            if created_at is None:
                _LOGGER.error(
                    "Ignoring refresh token %(id)s with invalid created_at "
                    + "%(created_at)s for user_id %(user_id)s",
                    rt_dict,
                )
                continue

            if (token_type := rt_dict.get("token_type")) is None:
                if rt_dict["client_id"] is None:
                    token_type = str(TokenType.SYSTEM)
                else:
                    token_type = str(TokenType.NORMAL)

            # old refresh_token don't have last_used_at (pre-0.78)
            if last_used_at_str := rt_dict.get("last_used_at"):
                last_used_at = helpers.parse_datetime(last_used_at_str)
            else:
                last_used_at = None

            token = RefreshToken(
                id=rt_dict["id"],
                user=users[rt_dict["user_id"]],
                client_id=rt_dict["client_id"],
                # use dict.get to keep backward compatibility
                client_name=rt_dict.get("client_name"),
                client_icon=rt_dict.get("client_icon"),
                token_type=token_type,
                created_at=created_at,
                access_token_expiration=datetime.timedelta(
                    seconds=rt_dict["access_token_expiration"]
                ),
                token=rt_dict["token"],
                jwt_key=rt_dict["jwt_key"],
                last_used_at=last_used_at,
                last_used_ip=rt_dict.get("last_used_ip"),
                credential=credentials.get(rt_dict.get("credential_id")),
                version=rt_dict.get("version"),
            )
            users[rt_dict["user_id"]].refresh_tokens[token.id] = token

        self._groups = groups
        self._users = users

    @callback
    def _async_schedule_save(self) -> None:
        """Save users."""
        if self._users is None:
            return

        self._store.async_delay_save(self._data_to_save, 1)

    @callback
    def _data_to_save(self) -> dict[str, list[dict[str, typing.Any]]]:
        """Return the data to store."""
        assert self._users is not None
        assert self._groups is not None

        users = [
            {
                "id": user.id,
                "group_ids": [group.id for group in user.groups],
                "is_owner": user.is_owner,
                "is_active": user.is_active,
                "name": user.name,
                "system_generated": user.system_generated,
                "local_only": user.local_only,
            }
            for user in self._users.values()
        ]

        groups = []
        for group in self._groups.values():
            g_dict: dict[str, typing.Any] = {
                "id": group.id,
                # Name not read for sys groups. Kept here for backwards compat
                "name": group.name,
            }

            if not group.system_generated:
                g_dict["policy"] = group.policy

            groups.append(g_dict)

        credentials = [
            {
                "id": credential.id,
                "user_id": user.id,
                "auth_provider_type": credential.auth_provider_type,
                "auth_provider_id": credential.auth_provider_id,
                "data": credential.data,
            }
            for user in self._users.values()
            for credential in user.credentials
        ]

        refresh_tokens = [
            {
                "id": refresh_token.id,
                "user_id": user.id,
                "client_id": refresh_token.client_id,
                "client_name": refresh_token.client_name,
                "client_icon": refresh_token.client_icon,
                "token_type": refresh_token.token_type,
                "created_at": refresh_token.created_at.isoformat(),
                "access_token_expiration": refresh_token.access_token_expiration.total_seconds(),
                "token": refresh_token.token,
                "jwt_key": refresh_token.jwt_key,
                "last_used_at": refresh_token.last_used_at.isoformat()
                if refresh_token.last_used_at
                else None,
                "last_used_ip": refresh_token.last_used_ip,
                "credential_id": refresh_token.credential.id
                if refresh_token.credential
                else None,
                "version": refresh_token.version,
            }
            for user in self._users.values()
            for refresh_token in user.refresh_tokens.values()
        ]

        return {
            "users": users,
            "groups": groups,
            "credentials": credentials,
            "refresh_tokens": refresh_tokens,
        }

    def _set_defaults(self) -> None:
        """Set default values for auth store."""
        self._users = collections.OrderedDict()

        groups: dict[str, Group] = collections.OrderedDict()
        admin_group = _system_admin_group()
        groups[admin_group.id] = admin_group
        user_group = _system_user_group()
        groups[user_group.id] = user_group
        read_only_group = _system_read_only_group()
        groups[read_only_group.id] = read_only_group
        self._groups = groups


def _system_admin_group() -> Group:
    """Create system admin group."""
    return Group(
        name=_GROUP_NAME_ADMIN,
        id=Const.GROUP_ID_ADMIN,
        policy=perm.SystemPolicies.ADMIN_POLICY,
        system_generated=True,
    )


def _system_user_group() -> Group:
    """Create system user group."""
    return Group(
        name=_GROUP_NAME_USER,
        id=Const.GROUP_ID_USER,
        policy=perm.SystemPolicies.USER_POLICY,
        system_generated=True,
    )


def _system_read_only_group() -> Group:
    """Create read only group."""
    return Group(
        name=_GROUP_NAME_READ_ONLY,
        id=Const.GROUP_ID_READ_ONLY,
        policy=perm.SystemPolicies.READ_ONLY_POLICY,
        system_generated=True,
    )
