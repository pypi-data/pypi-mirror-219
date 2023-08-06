"""
Configuration API for Smart Home - The Next Generation.

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
import typing

import voluptuous as vol

from ... import auth, core
from .check_config_view import CheckConfigView
from .config_manager_available_flow_view import ConfigManagerAvailableFlowView
from .config_manager_entry_index_view import ConfigManagerEntryIndexView, _entry_json
from .config_manager_entry_resource_reload_view import (
    ConfigManagerEntryResourceReloadView,
)
from .config_manager_entry_resource_view import ConfigManagerEntryResourceView
from .config_manager_flow_index_view import ConfigManagerFlowIndexView
from .config_manager_flow_resource_view import ConfigManagerFlowResourceView
from .edit_automation_config_view import EditAutomationConfigView
from .edit_scene_config_view import EditSceneConfigView
from .edit_script_config_view import EditScriptConfigView
from .option_manager_flow_index_view import OptionManagerFlowIndexView
from .option_manager_flow_resource_view import OptionManagerFlowResourceView

_cv: typing.TypeAlias = core.ConfigValidation


_WS_TYPE_AUTH_LIST: typing.Final = "config/auth/list"
_WS_AUTH_LIST: typing.Final = {vol.Required("type"): _WS_TYPE_AUTH_LIST}
_WS_TYPE_AUTH_DELETE: typing.Final = "config/auth/delete"
_WS_AUTH_DELETE: typing.Final = {
    vol.Required("type"): _WS_TYPE_AUTH_DELETE,
    vol.Required("user_id"): str,
}
_WS_TYPE_DEVREG_LIST: typing.Final = "config/device_registry/list"
_WS_DEVREG_LIST: typing.Final = {vol.Required("type"): _WS_TYPE_DEVREG_LIST}
_WS_TYPE_DEVREG_UPDATE: typing.Final = "config/device_registry/update"
_WS_DEVREG_UPDATE = {
    vol.Required("type"): _WS_TYPE_DEVREG_UPDATE,
    vol.Required("device_id"): str,
    vol.Optional("area_id"): vol.Any(str, None),
    vol.Optional("name_by_user"): vol.Any(str, None),
    # We only allow setting disabled_by user via API.
    # No Enum support like this in voluptuous, use .value
    vol.Optional("disabled_by"): vol.Any(
        core.DeviceRegistryEntryDisabler.USER.value, None
    ),
}
_LIST_AREAS: typing.Final = {vol.Required("type"): "config/area_registry/list"}
_CREATE_AREA: typing.Final = {
    vol.Required("type"): "config/area_registry/create",
    vol.Required("name"): str,
    vol.Optional("picture"): vol.Any(str, None),
}
_DELETE_AREA: typing.Final = {
    vol.Required("type"): "config/area_registry/delete",
    vol.Required("area_id"): str,
}
_UPDATE_AREA: typing.Final = {
    vol.Required("type"): "config/area_registry/update",
    vol.Required("area_id"): str,
    vol.Optional("name"): str,
    vol.Optional("picture"): vol.Any(str, None),
}
_AUTH_CREATE: typing.Final = {
    vol.Required("type"): "config/auth/create",
    vol.Required("name"): str,
    vol.Optional("group_ids"): [str],
    vol.Optional("local_only"): bool,
}
_AUTH_UPDATE: typing.Final = {
    vol.Required("type"): "config/auth/update",
    vol.Required("user_id"): str,
    vol.Optional("name"): str,
    vol.Optional("is_active"): bool,
    vol.Optional("group_ids"): [str],
    vol.Optional("local_only"): bool,
}
_INTERNAL_CREATE: typing.Final = {
    vol.Required("type"): "config/auth_provider/internal/create",
    vol.Required("user_id"): str,
    vol.Required("username"): str,
    vol.Required("password"): str,
}
_INTERNAL_DELETE: typing.Final = {
    vol.Required("type"): "config/auth_provider/internal/delete",
    vol.Required("username"): str,
}
_CHANGE_PASSWORD: typing.Final = {
    vol.Required("type"): "config/auth_provider/internal/change_password",
    vol.Required("current_password"): str,
    vol.Required("new_password"): str,
}
_ADMIN_CHANGE_PASSWORD: typing.Final = {
    vol.Required("type"): "config/auth_provider/inernal/admin_change_password",
    vol.Required("user_id"): str,
    vol.Required("password"): str,
}
_CONFIG_ENTRIES_GET: typing.Final = {
    vol.Required("type"): "config_entries/get",
    vol.Optional("type_filter"): str,
    vol.Optional("domain"): str,
}
_CONFIG_ENTRY_DISABLE: typing.Final = {
    "type": "config_entries/disable",
    "entry_id": str,
    # We only allow setting disabled_by user via API.
    # No Enum support like this in voluptuous, use .value
    "disabled_by": vol.Any(core.ConfigEntryDisabler.USER.value, None),
}
_CONFIG_ENTRIES_SUBSCRIBE: typing.Final = {
    vol.Required("type"): "config_entries/subscribe",
    vol.Optional("type_filter"): vol.All(_cv.ensure_list, [str]),
}

_CONFIG_ENTRY_UPDATE: typing.Final = {
    "type": "config_entries/update",
    "entry_id": str,
    vol.Optional("title"): str,
    vol.Optional("pref_disable_new_entities"): bool,
    vol.Optional("pref_disable_polling"): bool,
}
_CONFIG_ENTRY_PROGRESS: typing.Final = {"type": "config_entries/flow/progress"}
_IGNORE_CONFIG_FLOW: typing.Final = {
    "type": "config_entries/ignore_flow",
    "flow_id": str,
    "title": str,
}
_CONFIG_UPDATE: typing.Final = {
    "type": "config/core/update",
    vol.Optional("latitude"): _cv.latitude,
    vol.Optional("longitude"): _cv.longitude,
    vol.Optional("elevation"): int,
    vol.Optional("unit_system"): _cv.unit_system,
    vol.Optional("location_name"): str,
    vol.Optional("time_zone"): _cv.time_zone,
    vol.Optional("external_url"): vol.Any(_cv.url_no_path, None),
    vol.Optional("internal_url"): vol.Any(_cv.url_no_path, None),
    vol.Optional("currency"): _cv.currency,
}
_CONFIG_DETECT: typing.Final = {"type": "config/core/detect"}
_REMOVE_FROM_DEVICE: typing.Final = {
    "type": "config/device_registry/remove_config_entry",
    "device_id": str,
    "config_entry_id": str,
}
_LIST_ENTITIES: typing.Final = {vol.Required("type"): "config/entity_registry/list"}
_GET_ENTITY: typing.Final = {
    vol.Required("type"): "config/entity_registry/get",
    vol.Required("entity_id"): _cv.entity_id,
}
_UPDATE_ENTITY: typing.Final = {
    vol.Required("type"): "config/entity_registry/update",
    vol.Required("entity_id"): _cv.entity_id,
    # If passed in, we update value. Passing None will remove old value.
    vol.Optional("area_id"): vol.Any(str, None),
    vol.Optional("device_class"): vol.Any(str, None),
    vol.Optional("icon"): vol.Any(str, None),
    vol.Optional("name"): vol.Any(str, None),
    vol.Optional("new_entity_id"): str,
    # We only allow setting disabled_by user via API.
    vol.Optional("disabled_by"): vol.Any(
        None,
        vol.All(
            vol.Coerce(core.EntityRegistryEntryDisabler),
            core.EntityRegistryEntryDisabler.USER.value,
        ),
    ),
    # We only allow setting hidden_by user via API.
    vol.Optional("hidden_by"): vol.Any(
        None,
        vol.All(
            vol.Coerce(core.EntityRegistryEntryHider),
            core.EntityRegistryEntryHider.USER.value,
        ),
    ),
    vol.Inclusive("options_domain", "entity_option"): str,
    vol.Inclusive("options", "entity_option"): vol.Any(None, dict),
}
_REMOVE_ENTITY: typing.Final = {
    vol.Required("type"): "config/entity_registry/remove",
    vol.Required("entity_id"): _cv.entity_id,
}


# pylint: disable=unused-variable
class ConfigAPI(core.SmartHomeControllerComponent):
    """Component to configure Smart Home - The Next Generation via an API."""

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the config component."""
        if not await super().async_setup(config):
            return False

        api = self.controller.components.websocket_api
        if not isinstance(api, core.WebSocket.Component):
            return False

        comp = self.controller.components.automation
        if isinstance(comp, core.AutomationComponent):
            self._shc.register_view(EditAutomationConfigView(comp))
            key = f"{self.domain}.{comp.domain}"
            self._shc.bus.async_fire(
                core.Const.EVENT_COMPONENT_LOADED, {core.Const.ATTR_COMPONENT: key}
            )
        else:
            self._shc.setup.async_when_setup(
                "automation", self._async_automation_loaded
            )

        shc = self._shc
        domain = self.domain

        # Enable the Area Registry views.
        api.register_command(self._list_areas, _LIST_AREAS)
        api.register_command(self._create_area, _CREATE_AREA)
        api.register_command(self._delete_area, _DELETE_AREA)
        api.register_command(self._update_area, _UPDATE_AREA)
        key = f"{domain}.area_registry"
        shc.bus.async_fire(
            core.Const.EVENT_COMPONENT_LOADED, {core.Const.ATTR_COMPONENT: key}
        )

        # Enable the Auth views.
        api.register_command(_WS_TYPE_AUTH_LIST, _WS_AUTH_LIST, self._auth_list)
        api.register_command(_WS_TYPE_AUTH_DELETE, _WS_AUTH_DELETE, self._auth_delete)
        api.register_command(self._auth_create, _AUTH_CREATE)
        api.register_command(self._auth_update, _AUTH_UPDATE)
        key = f"{domain}.auth"
        shc.bus.async_fire(
            core.Const.EVENT_COMPONENT_LOADED, {core.Const.ATTR_COMPONENT: key}
        )

        # Enable the Internal Auth Provider views.
        api.register_command(self._internal_create, _INTERNAL_CREATE)
        api.register_command(self._internal_delete, _INTERNAL_DELETE)
        api.register_command(self._change_password, _CHANGE_PASSWORD)
        api.register_command(self._admin_change_password, _ADMIN_CHANGE_PASSWORD)
        key = f"{domain}.auth_provider"
        shc.bus.async_fire(
            core.Const.EVENT_COMPONENT_LOADED, {core.Const.ATTR_COMPONENT: key}
        )

        # Enable the ConfigEnties views.
        shc.register_view(ConfigManagerEntryIndexView())
        shc.register_view(ConfigManagerEntryResourceView())
        shc.register_view(ConfigManagerEntryResourceReloadView())
        shc.register_view(ConfigManagerFlowIndexView(shc.config_entries.flow))
        shc.register_view(ConfigManagerFlowResourceView(shc.config_entries.flow))
        shc.register_view(ConfigManagerAvailableFlowView())

        shc.register_view(OptionManagerFlowIndexView(shc.config_entries.options))
        shc.register_view(OptionManagerFlowResourceView(shc.config_entries.options))

        api.register_command(self._config_entries_get, _CONFIG_ENTRIES_GET)
        api.register_command(self._config_entry_disable, _CONFIG_ENTRY_DISABLE)
        api.register_command(self._config_entry_update, _CONFIG_ENTRY_UPDATE)
        api.register_command(self._config_entries_subscribe, _CONFIG_ENTRIES_SUBSCRIBE)
        api.register_command(self._config_entries_progress, _CONFIG_ENTRY_PROGRESS)
        api.register_command(self._ignore_config_flow, _IGNORE_CONFIG_FLOW)
        key = f"{domain}.config_entries"
        shc.bus.async_fire(
            core.Const.EVENT_COMPONENT_LOADED, {core.Const.ATTR_COMPONENT: key}
        )

        # Enable the core config views.
        shc.register_view(CheckConfigView)
        api.register_command(self._update_core_config, _CONFIG_UPDATE)
        api.register_command(self._detect_core_config, _CONFIG_DETECT)
        key = f"{domain}.core"
        shc.bus.async_fire(
            core.Const.EVENT_COMPONENT_LOADED, {core.Const.ATTR_COMPONENT: key}
        )

        # Enable the Device Registry views.
        api.register_command(_WS_TYPE_DEVREG_LIST, _WS_DEVREG_LIST, self._list_devices)
        api.register_command(
            _WS_TYPE_DEVREG_UPDATE, _WS_DEVREG_UPDATE, self._update_device
        )
        api.register_command(self._remove_config_entry_from_device, _REMOVE_FROM_DEVICE)
        key = f"{domain}.device_registry"
        shc.bus.async_fire(
            core.Const.EVENT_COMPONENT_LOADED, {core.Const.ATTR_COMPONENT: key}
        )

        # Enable the Entity Registry views.
        api.register_command(self._list_entities, _LIST_ENTITIES)
        api.register_command(self._get_entity, _GET_ENTITY)
        api.register_command(self._update_entity, _UPDATE_ENTITY)
        api.register_command(self._remove_entity, _REMOVE_ENTITY)
        key = f"{domain}.entity_registry"
        shc.bus.async_fire(
            core.Const.EVENT_COMPONENT_LOADED, {core.Const.ATTR_COMPONENT: key}
        )

        comp = shc.components.scene
        if comp is not None:
            shc.register_view(EditSceneConfigView(comp))
            key = f"{domain}.scene"
            shc.bus.async_fire(
                core.Const.EVENT_COMPONENT_LOADED, {core.Const.ATTR_COMPONENT: key}
            )

        comp = self.controller.components.script
        if isinstance(comp, core.ScriptComponent):
            shc.register_view(EditScriptConfigView(comp))
            key = f"{domain}.script"
            shc.bus.async_fire(
                core.Const.EVENT_COMPONENT_LOADED, {core.Const.ATTR_COMPONENT: key}
            )
        return True

    async def _async_automation_loaded(
        self, _shc: core.SmartHomeController, _domain: str
    ):
        """Loaded Automation Component after config component. Register edit view."""
        comp = self.controller.components.automation
        if isinstance(comp, core.AutomationComponent):
            self._shc.register_view(EditAutomationConfigView(comp))
            key = f"{self.domain}.{comp.domain}"
            self._shc.bus.async_fire(
                core.Const.EVENT_COMPONENT_LOADED, {core.Const.ATTR_COMPONENT: key}
            )

    @core.callback
    def _list_areas(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle list areas command."""
        shc = connection.owner.controller
        registry = shc.area_registry
        connection.send_result(
            msg["id"],
            [_area_entry_dict(entry) for entry in registry.async_list_areas()],
        )

    @core.callback
    def _create_area(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Create area command."""
        connection.require_admin()

        registry = connection.owner.controller.area_registry

        data = dict(msg)
        data.pop("type")
        data.pop("id")

        try:
            entry = registry.async_create(**data)
        except ValueError as err:
            connection.send_error(msg["id"], "invalid_info", str(err))
        else:
            connection.send_result(msg["id"], _area_entry_dict(entry))

    @core.callback
    def _delete_area(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Delete area command."""
        connection.require_admin()

        registry = connection.owner.controller.area_registry

        try:
            registry.async_delete(msg["area_id"])
        except KeyError:
            connection.send_error(msg["id"], "invalid_info", "Area ID doesn't exist")
        else:
            connection.send_result(msg["id"], "success")

    @core.callback
    def _update_area(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle update area websocket command."""
        connection.require_admin()

        registry = connection.owner.controller.area_registry

        data = dict(msg)
        data.pop("type")
        data.pop("id")

        try:
            entry = registry.async_update(**data)
        except ValueError as err:
            connection.send_error(msg["id"], "invalid_info", str(err))
        else:
            connection.send_result(msg["id"], _area_entry_dict(entry))

    async def _auth_list(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Return a list of users."""
        connection.require_admin()

        shc = connection.owner.controller
        result = [_user_info(u) for u in await shc.auth.async_get_users()]

        connection.send_result(msg["id"], result)

    async def _auth_delete(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Delete a user."""
        connection.require_admin()

        shc = connection.owner.controller

        if msg["user_id"] == connection.user.id:
            connection.send_error(
                msg["id"], "no_delete_self", "Unable to delete your own account"
            )
            return

        if not (user := await shc.auth.async_get_user(msg["user_id"])):
            connection.send_error(msg["id"], "not_found", "User not found")
            return

        await shc.auth.async_remove_user(user)

        connection.send_result(msg["id"])

    async def _auth_create(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Create a user."""
        connection.require_admin()

        shc = connection.owner.controller

        user = await shc.auth.async_create_user(
            msg["name"],
            group_ids=msg.get("group_ids"),
            local_only=msg.get("local_only"),
        )

        connection.send_result(msg["id"], {"user": _user_info(user)})

    async def _auth_update(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Update a user."""
        connection.require_admin()

        shc = connection.owner.controller

        if not (user := await shc.auth.async_get_user(msg.pop("user_id"))):
            connection.send_error(
                msg["id"], core.WebSocket.ERR_NOT_FOUND, "User not found"
            )
            return

        if user.system_generated:
            connection.send_error(
                msg["id"],
                "cannot_modify_system_generated",
                "Unable to update system generated users.",
            )
            return

        if user.is_owner and msg.get("is_active") is False:
            connection.send_error(
                msg["id"],
                "cannot_deactivate_owner",
                "Unable to deactivate owner.",
            )
            return

        msg.pop("type")
        msg_id = msg.pop("id")

        await shc.auth.async_update_user(user, **msg)

        connection.send_result(msg_id, {"user": _user_info(user)})

    async def _internal_create(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Create credentials and attach to a user."""
        connection.require_admin()
        shc = connection.owner.controller
        provider = shc.async_get_shc_auth_provider()

        if (user := await shc.auth.async_get_user(msg["user_id"])) is None:
            connection.send_error(msg["id"], "not_found", "User not found")
            return

        if user.system_generated:
            connection.send_error(
                msg["id"],
                "system_generated",
                "Cannot add credentials to a system generated user.",
            )
            return

        try:
            await provider.async_add_auth(msg["username"], msg["password"])
        except auth.InvalidUser:
            connection.send_error(
                msg["id"], "username_exists", "Username already exists"
            )
            return

        credentials = await provider.async_get_or_create_credentials(
            {"username": msg["username"]}
        )
        await shc.auth.async_link_user(user, credentials)

        connection.send_result(msg["id"])

    async def _internal_delete(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Delete username and related credential."""
        connection.require_admin()
        shc = connection.owner.controller
        provider = shc.async_get_shc_auth_provider()
        credentials = await provider.async_get_or_create_credentials(
            {"username": msg["username"]}
        )

        # if not new, an existing credential exists.
        # Removing the credential will also remove the auth.
        if not credentials.is_new:
            await shc.auth.async_remove_credentials(credentials)

            connection.send_result(msg["id"])
            return

        try:
            await provider.async_remove_auth(msg["username"])
        except auth.InvalidUser:
            connection.send_error(
                msg["id"], "auth_not_found", "Given username was not found."
            )
            return

        connection.send_result(msg["id"])

    async def _change_password(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Change current user password."""
        shc = connection.owner.controller
        if (user := connection.user) is None:
            connection.send_error(msg["id"], "user_not_found", "User not found")
            return

        provider = shc.async_get_shc_auth_provider()
        username = None
        for credential in user.credentials:
            if credential.auth_provider_type == provider.type:
                username = credential.data["username"]
                break

        if username is None:
            connection.send_error(
                msg["id"], "credentials_not_found", "Credentials not found"
            )
            return

        try:
            await provider.async_validate_login(username, msg["current_password"])
        except auth.InvalidAuthError:
            connection.send_error(
                msg["id"], "invalid_current_password", "Invalid current password"
            )
            return

        await provider.async_change_password(username, msg["new_password"])

        connection.send_result(msg["id"])

    async def _admin_change_password(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Change password of any user."""
        connection.require_admin()
        shc = connection.owner.controller
        if not connection.user.is_owner:
            raise core.Unauthorized(context=connection.context(msg))

        if (user := await shc.auth.async_get_user(msg["user_id"])) is None:
            connection.send_error(msg["id"], "user_not_found", "User not found")
            return

        provider = shc.async_get_shc_auth_provider()

        username = None
        for credential in user.credentials:
            if credential.auth_provider_type == provider.type:
                username = credential.data["username"]
                break

        if username is None:
            connection.send_error(
                msg["id"], "credentials_not_found", "Credentials not found"
            )
            return

        try:
            await provider.async_change_password(username, msg["password"])
            connection.send_result(msg["id"])
        except auth.InvalidUser:
            connection.send_error(
                msg["id"], "credentials_not_found", "Credentials not found"
            )
            return

    async def _config_entries_subscribe(
        self,
        connection: core.WebSocket.Connection,
        msg: dict[str, typing.Any],
    ) -> None:
        """Subscribe to config entry updates."""
        type_filter = msg.get("type_filter")

        async def async_forward_config_entry_changes(
            change: core.ConfigEntryChange, entry: core.ConfigEntry
        ) -> None:
            """Forward config entry state events to websocket."""
            if type_filter:
                integration = await self.controller.setup.async_get_integration(
                    entry.domain
                )
                if integration.integration_type not in type_filter:
                    return

            connection.send_event_message(
                msg["id"],
                [
                    {
                        "type": change,
                        "entry": _entry_json(entry),
                    }
                ],
            )

        current_entries = await self._async_matching_config_entries(type_filter, None)
        connection.subscriptions[msg["id"]] = self.controller.dispatcher.async_connect(
            core.ConfigEntry.SIGNAL_CONFIG_ENTRY_CHANGED,
            async_forward_config_entry_changes,
        )
        connection.send_result(msg["id"])
        connection.send_event_message(
            msg["id"], [{"type": None, "entry": entry} for entry in current_entries]
        )

    async def _async_matching_config_entries(
        self, type_filter: list[str] | None, domain: str | None
    ) -> list[dict[str, typing.Any]]:
        """Return matching config entries by type and/or domain."""
        kwargs = {}
        if domain:
            kwargs["domain"] = domain
        entries = self.controller.config_entries.async_entries(**kwargs)

        if not type_filter:
            return [_entry_json(entry) for entry in entries]

        integrations = {}
        # Fetch all the integrations so we can check their type
        tasks = (
            self.controller.setup.async_get_integration(domain)
            for domain in {entry.domain for entry in entries}
        )
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for integration_or_exc in results:
            if isinstance(integration_or_exc, core.Integration):
                integrations[integration_or_exc.domain] = integration_or_exc
            elif not isinstance(integration_or_exc, core.IntegrationNotFound):
                raise integration_or_exc

        # Filter out entries that don't match the type filter
        # when only helpers are requested, also filter out entries
        # from unknown integrations. This prevent them from showing
        # up in the helpers UI.
        entries = [
            entry
            for entry in entries
            if (type_filter != ["helper"] and entry.domain not in integrations)
            or (
                entry.domain in integrations
                and integrations[entry.domain].integration_type in type_filter
            )
        ]

        return [_entry_json(entry) for entry in entries]

    def _config_entries_progress(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """List flows that are in progress but not started by a user.

        Example of a non-user initiated flow is a discovered Hue hub that
        requires user interaction to finish setup.
        """
        connection.require_admin()
        shc = connection.owner.controller
        connection.send_result(
            msg["id"],
            [
                flw
                for flw in shc.config_entries.flow.async_progress()
                if flw["context"]["source"] != core.ConfigEntrySource.USER
            ],
        )

    async def _config_entry_update(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Update config entry."""
        connection.require_admin()
        shc = connection.owner.controller
        changes = dict(msg)
        changes.pop("id")
        changes.pop("type")
        changes.pop("entry_id")

        entry = _get_entry(shc, connection, msg["entry_id"], msg["id"])
        if entry is None:
            return

        old_disable_polling = entry.pref_disable_polling

        shc.config_entries.async_update_entry(entry, **changes)

        result = {
            "config_entry": _entry_json(entry),
            "require_restart": False,
        }

        if (
            old_disable_polling != entry.pref_disable_polling
            and entry.state is core.ConfigEntryState.LOADED
        ):
            if not await shc.config_entries.async_reload(entry.entry_id):
                result["require_restart"] = (
                    entry.state is core.ConfigEntryState.FAILED_UNLOAD
                )

        connection.send_result(msg["id"], result)

    async def _config_entries_get(
        self,
        connection: core.WebSocket.Connection,
        msg: dict[str, typing.Any],
    ) -> None:
        """Return matching config entries by type and/or domain."""
        connection.send_result(
            msg["id"],
            await _async_matching_config_entries(
                self.controller, msg.get("type_filter"), msg.get("domain")
            ),
        )

    async def _config_entry_disable(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Disable config entry."""
        connection.require_admin()
        shc = connection.owner.controller
        if (disabled_by := msg["disabled_by"]) is not None:
            disabled_by = core.ConfigEntryDisabler(disabled_by)

        result = False
        try:
            result = await shc.config_entries.async_set_disabled_by(
                msg["entry_id"], disabled_by
            )
        except core.OperationNotAllowed:
            # Failed to unload the config entry
            pass
        except core.UnknownEntry:
            _send_entry_not_found(connection, msg["id"])
            return

        result = {"require_restart": not result}

        connection.send_result(msg["id"], result)

    async def _ignore_config_flow(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Ignore a config flow."""
        connection.require_admin()
        shc = connection.owner.controller
        flow = next(
            (
                flw
                for flw in shc.config_entries.flow.async_progress()
                if flw["flow_id"] == msg["flow_id"]
            ),
            None,
        )

        if flow is None:
            _send_entry_not_found(connection, msg["id"])
            return

        if "unique_id" not in flow["context"]:
            connection.send_error(
                msg["id"], "no_unique_id", "Specified flow has no unique ID."
            )
            return

        await shc.config_entries.flow.async_init(
            flow["handler"],
            context={"source": core.ConfigEntrySource.IGNORE},
            data={"unique_id": flow["context"]["unique_id"], "title": msg["title"]},
        )
        connection.send_result(msg["id"])

    async def _update_core_config(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle update core config command."""
        connection.require_admin()
        shc = connection.owner.controller
        data = dict(msg)
        data.pop("id")
        data.pop("type")

        try:
            await shc.config.async_update(**data)
            connection.send_result(msg["id"])
        except ValueError as err:
            connection.send_error(msg["id"], "invalid_info", str(err))

    async def _detect_core_config(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Detect core config."""
        connection.require_admin()
        shc = connection.owner.controller
        session = core.HttpClient.async_get_clientsession(shc)
        location_info = await core.LocationInfo.async_detect_location_info(session)

        info = {}

        if location_info is None:
            connection.send_result(msg["id"], info)
            return

        if location_info.use_metric:
            info["unit_system"] = core.Const.CONF_UNIT_SYSTEM_METRIC
        else:
            info["unit_system"] = core.Const.CONF_UNIT_SYSTEM_IMPERIAL

        if location_info.latitude:
            info["latitude"] = location_info.latitude

        if location_info.longitude:
            info["longitude"] = location_info.longitude

        if location_info.time_zone:
            info["time_zone"] = location_info.time_zone

        if location_info.currency:
            info["currency"] = location_info.currency

        connection.send_result(msg["id"], info)

    @core.callback
    def _update_device(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle update area websocket command."""
        connection.require_admin()
        shc = connection.owner.controller
        registry = shc.device_registry

        msg.pop("type")
        msg_id = msg.pop("id")

        if msg.get("disabled_by") is not None:
            msg["disabled_by"] = core.DeviceRegistryEntryDisabler(msg["disabled_by"])

        entry = registry.async_update_device(**msg)

        connection.send_result(msg_id, _device_entry_dict(entry))

    async def _remove_config_entry_from_device(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Remove config entry from a device."""
        connection.require_admin()
        shc = connection.owner.controller
        registry = shc.device_registry
        config_entry_id = msg["config_entry_id"]
        device_id = msg["device_id"]

        if (
            config_entry := shc.config_entries.async_get_entry(config_entry_id)
        ) is None:
            raise core.SmartHomeControllerError("Unknown config entry")

        if not config_entry.supports_remove_device:
            raise core.SmartHomeControllerError(
                "Config entry does not support device removal"
            )

        if (device_entry := registry.async_get(device_id)) is None:
            raise core.SmartHomeControllerError("Unknown device")

        if config_entry_id not in device_entry.config_entries:
            raise core.SmartHomeControllerError("Config entry not in device")

        try:
            comp = core.SmartHomeControllerComponent.get_component(config_entry.domain)
            component = None
            if (
                not isinstance(comp, core.SmartHomeControllerComponent)
                or not comp.supports_remove_from_device
            ):
                comp = None
                integration = await shc.setup.async_get_integration(config_entry.domain)
                component = integration.get_component()
        except (ImportError, core.IntegrationNotFound) as exc:
            raise core.SmartHomeControllerError("Integration not found") from exc

        removed = False
        if comp is not None:
            removed = await comp.async_remove_config_entry_device(
                config_entry, device_entry
            )
        else:
            removed = await component.async_remove_config_entry_device(
                shc, config_entry, device_entry
            )
        if not removed:
            raise core.SmartHomeControllerError(
                "Failed to remove device entry, rejected by integration"
            )

        entry = registry.async_update_device(
            device_id, remove_config_entry_id=config_entry_id
        )

        entry_as_dict = _device_entry_dict(entry) if entry else None

        connection.send_result(msg["id"], entry_as_dict)

    @core.callback
    def _list_devices(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle list devices command."""
        registry = connection.owner.controller.device_registry
        connection.send_result(
            msg["id"],
            [_device_entry_dict(entry) for entry in registry.devices.values()],
        )

    @core.callback
    def _list_entities(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle list registry entries command."""
        shc = connection.owner.controller
        registry = shc.entity_registry
        connection.send_result(
            msg["id"],
            [_entity_entry_dict(entry) for entry in registry.entities.values()],
        )

    @core.callback
    def _get_entity(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle get entity registry entry command.

        Async friendly.
        """
        shc = connection.owner.controller
        registry = shc.entity_registry

        if (entry := registry.entities.get(msg["entity_id"])) is None:
            connection.send_error(
                msg["id"], core.WebSocket.ERR_NOT_FOUND, "Entity not found"
            )
            return

        connection.send_result(msg["id"], _entity_entry_ext_dict(entry))

    @core.callback
    def _update_entity(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle update entity websocket command.

        Async friendly.
        """
        connection.require_admin()
        shc = connection.owner.controller
        registry = shc.entity_registry

        entity_id = msg["entity_id"]
        if not (entity_entry := registry.async_get(entity_id)):
            connection.send_error(
                msg["id"], core.WebSocket.ERR_NOT_FOUND, "Entity not found"
            )
            return

        changes = {}

        for key in (
            "area_id",
            "device_class",
            "disabled_by",
            "hidden_by",
            "icon",
            "name",
        ):
            if key in msg:
                changes[key] = msg[key]

        if "new_entity_id" in msg and msg["new_entity_id"] != entity_id:
            changes["new_entity_id"] = msg["new_entity_id"]
            if shc.states.get(msg["new_entity_id"]) is not None:
                connection.send_error(
                    msg["id"],
                    "invalid_info",
                    "Entity with this ID is already registered",
                )
                return

        if "disabled_by" in msg and msg["disabled_by"] is None:
            # Don't allow enabling an entity of a disabled device
            if entity_entry.device_id:
                device_registry = shc.device_registry
                device = device_registry.async_get(entity_entry.device_id)
                if device.disabled:
                    connection.send_error(
                        msg["id"], "invalid_info", "Device is disabled"
                    )
                    return

        try:
            if changes:
                entity_entry = registry.async_update_entity(entity_id, **changes)
        except ValueError as err:
            connection.send_error(msg["id"], "invalid_info", str(err))
            return

        if "new_entity_id" in msg:
            entity_id = msg["new_entity_id"]

        try:
            if "options_domain" in msg:
                entity_entry = registry.async_update_entity_options(
                    entity_id, msg["options_domain"], msg["options"]
                )
        except ValueError as err:
            connection.send_error(msg["id"], "invalid_info", str(err))
            return

        result = {"entity_entry": _entity_entry_ext_dict(entity_entry)}
        if "disabled_by" in changes and changes["disabled_by"] is None:
            # Enabling an entity requires a config entry reload, or HA restart
            config_entry = shc.config_entries.async_get_entry(
                entity_entry.config_entry_id
            )
            if config_entry and not config_entry.supports_unload:
                result["require_restart"] = True
            else:
                result["reload_delay"] = core.ConfigEntries.RELOAD_AFTER_UPDATE_DELAY
        connection.send_result(msg["id"], result)

    @core.callback
    def _remove_entity(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """Handle remove entity websocket command.

        Async friendly.
        """
        connection.require_admin()
        shc = connection.owner.controller
        registry = shc.entity_registry

        if msg["entity_id"] not in registry.entities:
            connection.send_error(
                msg["id"], core.WebSocket.ERR_NOT_FOUND, "Entity not found"
            )
            return

        registry.async_remove(msg["entity_id"])
        connection.send_result(msg["id"])


async def _async_matching_config_entries(
    shc: core.SmartHomeController, type_filter: str, domain: str
) -> list[dict[str, typing.Any]]:
    """Return matching config entries by type and/or domain."""
    kwargs = {}
    if domain:
        kwargs["domain"] = domain
    entries = shc.config_entries.async_entries(**kwargs)

    if type_filter is None:
        return [_entry_json(entry) for entry in entries]

    integrations = {}
    # Fetch all the integrations so we can check their type
    tasks = (
        shc.setup.async_get_integration(domain)
        for domain in {entry.domain for entry in entries}
    )
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for integration_or_exc in results:
        if isinstance(integration_or_exc, core.Integration):
            integrations[integration_or_exc.domain] = integration_or_exc
        elif not isinstance(integration_or_exc, core.IntegrationNotFound):
            raise integration_or_exc

    entries = [
        entry
        for entry in entries
        if (type_filter != "helper" and entry.domain not in integrations)
        or (
            entry.domain in integrations
            and integrations[entry.domain].integration_type == type_filter
        )
    ]

    return [_entry_json(entry) for entry in entries]


def _user_info(user):
    """Format a user."""

    shc_username = next(
        (
            cred.data.get("username")
            for cred in user.credentials
            if cred.auth_provider_type == core.Const.CORE_COMPONENT_NAME
        ),
        None,
    )

    return {
        "id": user.id,
        "username": shc_username,
        "name": user.name,
        "is_owner": user.is_owner,
        "is_active": user.is_active,
        "local_only": user.local_only,
        "system_generated": user.system_generated,
        "group_ids": [group.id for group in user.groups],
        "credentials": [{"type": c.auth_provider_type} for c in user.credentials],
    }


@core.callback
def _area_entry_dict(entry):
    """Convert entry to API format."""
    return {"area_id": entry.id, "name": entry.name, "picture": entry.picture}


def _send_entry_not_found(connection: core.WebSocket.Connection, msg_id: int) -> None:
    """Send Config entry not found error."""
    connection.send_error(
        msg_id, core.WebSocket.ERR_NOT_FOUND, "Config entry not found"
    )


def _get_entry(
    shc: core.SmartHomeController,
    connection: core.WebSocket.Connection,
    entry_id: str,
    msg_id: int,
) -> core.ConfigEntry:
    """Get entry, send error message if it doesn't exist."""
    if (entry := shc.config_entries.async_get_entry(entry_id)) is None:
        _send_entry_not_found(connection, msg_id)
    return entry


@core.callback
def _device_entry_dict(entry):
    """Convert entry to API format."""
    return {
        "area_id": entry.area_id,
        "configuration_url": entry.configuration_url,
        "config_entries": list(entry.config_entries),
        "connections": list(entry.connections),
        "disabled_by": entry.disabled_by,
        "entry_type": entry.entry_type,
        "id": entry.id,
        "identifiers": list(entry.identifiers),
        "manufacturer": entry.manufacturer,
        "model": entry.model,
        "name_by_user": entry.name_by_user,
        "name": entry.name,
        "sw_version": entry.sw_version,
        "hw_version": entry.hw_version,
        "via_device_id": entry.via_device_id,
    }


@core.callback
def _entity_entry_dict(entry: core.EntityRegistryEntry) -> dict[str, typing.Any]:
    """Convert entry to API format."""
    return {
        "area_id": entry.area_id,
        "config_entry_id": entry.config_entry_id,
        "device_id": entry.device_id,
        "disabled_by": entry.disabled_by,
        "has_entity_name": entry.has_entity_name,
        "entity_category": entry.entity_category,
        "entity_id": entry.entity_id,
        "hidden_by": entry.hidden_by,
        "icon": entry.icon,
        "id": entry.id,
        "unique_id": entry.unique_id,
        "name": entry.name,
        "original_name": entry.original_name,
        "platform": entry.platform,
    }


@core.callback
def _entity_entry_ext_dict(entry: core.EntityRegistryEntry) -> dict[str, typing.Any]:
    """Convert entry to API format."""
    data = _entity_entry_dict(entry)
    data["capabilities"] = entry.capabilities
    data["device_class"] = entry.device_class
    data["options"] = entry.options
    data["original_device_class"] = entry.original_device_class
    data["original_icon"] = entry.original_icon
    return data
