"""
Home Assistant Cloud Component for Smart Home - The Next Generation.

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
import http
import logging
import typing

import hass_nabucasa as nabucasa  # pylint: disable=import-error

from ... import core
from .cloud_preferences import CloudPreferences
from .const import Const

_cloud_api: typing.TypeAlias = nabucasa.cloud_api
_report_state: typing.TypeAlias = nabucasa.google_report_state

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class CloudGoogleConfig(core.GoogleAssistant.AbstractConfig):
    """Smart Home TNG Cloud Configuration for Google Assistant."""

    def __init__(
        self,
        owner: core.GoogleAssistant.Component,
        config,
        cloud_user: str,
        prefs: CloudPreferences,
        cloud: nabucasa.Cloud,
    ):
        """Initialize the Google config."""
        super().__init__(owner)
        self._config = config
        self._user = cloud_user
        self._prefs = prefs
        self._cloud = cloud
        self._cur_entity_prefs = self._prefs.google_entity_configs
        self._cur_default_expose = self._prefs.google_default_expose
        self._sync_entities_lock = asyncio.Lock()

    @property
    def enabled(self):
        """Return if Google is enabled."""
        return (
            self._cloud.is_logged_in
            and not self._cloud.subscription_expired
            and self._prefs.google_enabled
        )

    @property
    def entity_config(self):
        """Return entity config."""
        return self._config.get(Const.CONF_ENTITY_CONFIG) or {}

    @property
    def secure_devices_pin(self):
        """Return entity config."""
        return self._prefs.google_secure_devices_pin

    @property
    def should_report_state(self):
        """Return if states should be proactively reported."""
        return self.enabled and self._prefs.google_report_state

    def get_local_webhook_id(self, agent_user_id):
        """
        Return the webhook ID to be used for actions for a given
        agent user id via the local SDK.
        """
        return self._prefs.google_local_webhook_id

    def get_local_agent_user_id(self, webhook_id):
        """Return the user ID to be used for actions received via the local SDK."""
        return self._user

    @property
    def cloud_user(self):
        """Return Cloud User account."""
        return self._user

    async def async_initialize(self):
        """Perform async initialization of config."""
        await super().async_initialize()

        async def shc_started(shc: core.SmartHomeController):
            if self.enabled and "google_assistant" not in shc.config.components:
                await shc.setup.async_setup_component("google_assistant", {})

        self.controller.async_at_start(shc_started)

        # Remove any stored user agent id that is not ours
        remove_agent_user_ids = []
        for agent_user_id in self._store.agent_user_ids:
            if agent_user_id != self.agent_user_id:
                remove_agent_user_ids.append(agent_user_id)

        for agent_user_id in remove_agent_user_ids:
            await self.async_disconnect_agent_user(agent_user_id)

        self._prefs.async_listen_updates(self._async_prefs_updated)

        self.controller.bus.async_listen(
            core.Const.EVENT_ENTITY_REGISTRY_UPDATED,
            self._handle_entity_registry_updated,
        )
        self.controller.bus.async_listen(
            core.Const.EVENT_DEVICE_REGISTRY_UPDATED,
            self._handle_device_registry_updated,
        )

    def should_expose(self, state):
        """If a state object should be exposed."""
        return self._should_expose_entity_id(state.entity_id)

    def _should_expose_entity_id(self, entity_id):
        """If an entity ID should be exposed."""
        if entity_id in core.Const.CLOUD_NEVER_EXPOSED_ENTITIES:
            return False

        if not self._config["filter"].empty_filter:
            return self._config["filter"](entity_id)

        entity_configs = self._prefs.google_entity_configs
        entity_config = entity_configs.get(entity_id, {})
        entity_expose = entity_config.get(Const.PREF_SHOULD_EXPOSE)
        if entity_expose is not None:
            return entity_expose

        entity_registry = self.controller.entity_registry
        if registry_entry := entity_registry.async_get(entity_id):
            auxiliary_entity = (
                registry_entry.entity_category is not None
                or registry_entry.hidden_by is not None
            )
        else:
            auxiliary_entity = False

        default_expose = self._prefs.google_default_expose

        # Backwards compat
        if default_expose is None:
            return not auxiliary_entity

        return (
            not auxiliary_entity
            and core.helpers.split_entity_id(entity_id)[0] in default_expose
        )

    @property
    def agent_user_id(self):
        """Return Agent User Id to use for query responses."""
        return self._cloud.username

    @property
    def has_registered_user_agent(self):
        """Return if we have a Agent User Id registered."""
        return len(self._store.agent_user_ids) > 0

    def get_agent_user_id(self, context):
        """Get agent user ID making request."""
        return self.agent_user_id

    def should_2fa(self, state):
        """If an entity should be checked for 2FA."""
        entity_configs = self._prefs.google_entity_configs
        entity_config = entity_configs.get(state.entity_id, {})
        return not entity_config.get(Const.PREF_DISABLE_2FA, Const.DEFAULT_DISABLE_2FA)

    async def async_report_state(self, message, agent_user_id: str):
        """Send a state report to Google."""
        try:
            await self._cloud.google_report_state.async_send_message(message)
        except _report_state.ErrorResponse as err:
            _LOGGER.warning(f"Error reporting state - {err.code}: {err.message}")

    async def _async_request_sync_devices(self, agent_user_id: str):
        """Trigger a sync with Google."""
        if self._sync_entities_lock.locked():
            return http.HTTPStatus.OK

        async with self._sync_entities_lock:
            resp = await _cloud_api.async_google_actions_request_sync(self._cloud)
            return resp.status

    async def _async_prefs_updated(self, prefs):
        """Handle updated preferences."""
        if not self._cloud.is_logged_in:
            if self.is_reporting_state:
                self.async_disable_report_state()
            if self.is_local_sdk_active:
                self.async_disable_local_sdk()
            return

        if (
            self.enabled
            and "google_assistant" not in self.controller.config.components
            and self.controller.is_running
        ):
            await self.controller.setup.async_setup_component("google_assistant", {})

        sync_entities = False

        if self.should_report_state != self.is_reporting_state:
            if self.should_report_state:
                self.async_enable_report_state()
            else:
                self.async_disable_report_state()

            # State reporting is reported as a property on entities.
            # So when we change it, we need to sync all entities.
            sync_entities = True

        # If entity prefs are the same or we have filter in config.yaml,
        # don't sync.
        elif (
            self._cur_entity_prefs is not prefs.google_entity_configs
            or self._cur_default_expose is not prefs.google_default_expose
        ) and self._config["filter"].empty_filter:
            self.async_schedule_google_sync_all()

        if self.enabled and not self.is_local_sdk_active:
            self.async_enable_local_sdk()
            sync_entities = True
        elif not self.enabled and self.is_local_sdk_active:
            self.async_disable_local_sdk()
            sync_entities = True

        self._cur_entity_prefs = prefs.google_entity_configs
        self._cur_default_expose = prefs.google_default_expose

        if sync_entities and self.controller.is_running:
            await self.async_sync_entities_all()

    @core.callback
    def _handle_entity_registry_updated(self, event: core.Event) -> None:
        """Handle when entity registry updated."""
        if (
            not self.enabled
            or not self._cloud.is_logged_in
            or self.controller.state != core.CoreState.RUNNING
        ):
            return

        # Only consider entity registry updates if info relevant for Google has changed
        if event.data["action"] == "update" and not bool(
            set(event.data["changes"])
            & core.EntityRegistry.ENTITY_DESCRIBING_ATTRIBUTES
        ):
            return

        entity_id = event.data["entity_id"]

        if not self._should_expose_entity_id(entity_id):
            return

        self.async_schedule_google_sync_all()

    @core.callback
    def _handle_device_registry_updated(self, event: core.Event) -> None:
        """Handle when device registry updated."""
        if (
            not self.enabled
            or not self._cloud.is_logged_in
            or self.controller.state != core.CoreState.RUNNING
        ):
            return

        # Device registry is only used for area changes. All other changes are ignored.
        if event.data["action"] != "update" or "area_id" not in event.data["changes"]:
            return

        # Check if any exposed entity uses the device area
        er = self.controller.entity_registry
        if not any(
            entity_entry.area_id is None
            and self._should_expose_entity_id(entity_entry.entity_id)
            for entity_entry in er.async_entries_for_device(event.data["device_id"])
        ):
            return

        self.async_schedule_google_sync_all()
