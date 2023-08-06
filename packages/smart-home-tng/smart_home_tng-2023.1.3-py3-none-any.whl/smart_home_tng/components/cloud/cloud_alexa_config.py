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
import contextlib
import datetime as dt
import http
import logging
import typing

import aiohttp
import async_timeout
import hass_nabucasa as nabucasa  # pylint: disable=import-error

from ... import core
from .cloud_preferences import CloudPreferences
from .const import Const

_alexa: typing.TypeAlias = core.Alexa
_cloud_api: typing.TypeAlias = nabucasa.cloud_api

_LOGGER: typing.Final = logging.getLogger(__name__)

# Time to wait when entity preferences have changed before syncing it to
# the cloud.
_SYNC_DELAY: typing.Final = 1


# pylint: disable=unused-variable
class CloudAlexaConfig(_alexa.AbstractConfig):
    """Alexa Configuration."""

    def __init__(
        self,
        shc: core.SmartHomeController,
        config: dict,
        cloud_user: str,
        prefs: CloudPreferences,
        cloud: nabucasa.Cloud,
    ) -> None:
        """Initialize the Alexa config."""
        super().__init__(shc)
        self._config = config
        self._cloud_user = cloud_user
        self._prefs = prefs
        self._cloud = cloud
        self._token = None
        self._token_valid = None
        self._cur_entity_prefs = prefs.alexa_entity_configs
        self._alexa_sync_unsub: typing.Callable[[], None] = None
        self._endpoint = None

    @property
    def enabled(self):
        """Return if Alexa is enabled."""
        return (
            self._cloud.is_logged_in
            and not self._cloud.subscription_expired
            and self._prefs.alexa_enabled
        )

    @property
    def supports_auth(self):
        """Return if config supports auth."""
        return True

    @property
    def should_report_state(self):
        """Return if states should be proactively reported."""
        return (
            self._prefs.alexa_enabled
            and self._prefs.alexa_report_state
            and self.authorized
        )

    @property
    def endpoint(self):
        """Endpoint for report state."""
        if self._endpoint is None:
            raise ValueError("No endpoint available. Fetch access token first")

        return self._endpoint

    @property
    def locale(self):
        """Return config locale."""
        # Not clear how to determine locale atm.
        return "en-US"

    @property
    def entity_config(self):
        """Return entity config."""
        return self._config.get(Const.CONF_ENTITY_CONFIG) or {}

    @core.callback
    def user_identifier(self):
        """Return an identifier for the user that represents this config."""
        return self._cloud_user

    async def async_initialize(self):
        """Initialize the Alexa config."""
        await super().async_initialize()

        async def shc_started(shc):
            if self.enabled and "alexa" not in shc.config.components:
                await shc.setup.async_setup_component("alexa", {})

        self._shc.async_at_start(shc_started)

        self._prefs.async_listen_updates(self._async_prefs_updated)
        self._shc.bus.async_listen(
            core.Const.EVENT_ENTITY_REGISTRY_UPDATED,
            self._handle_entity_registry_updated,
        )

    def should_expose(self, entity_id):
        """If an entity should be exposed."""
        if entity_id in core.Const.CLOUD_NEVER_EXPOSED_ENTITIES:
            return False

        if not self._config[Const.CONF_FILTER].empty_filter:
            return self._config[Const.CONF_FILTER](entity_id)

        entity_configs = self._prefs.alexa_entity_configs
        entity_config = entity_configs.get(entity_id, {})
        entity_expose = entity_config.get(Const.PREF_SHOULD_EXPOSE)
        if entity_expose is not None:
            return entity_expose

        entity_registry = self._shc.entity_registry
        if registry_entry := entity_registry.async_get(entity_id):
            auxiliary_entity = (
                registry_entry.entity_category is not None
                or registry_entry.hidden_by is not None
            )
        else:
            auxiliary_entity = False

        # Backwards compat
        if (default_expose := self._prefs.alexa_default_expose) is None:
            return not auxiliary_entity

        return (
            not auxiliary_entity
            and core.helpers.split_entity_id(entity_id)[0] in default_expose
        )

    @core.callback
    def async_invalidate_access_token(self):
        """Invalidate access token."""
        self._token_valid = None

    async def async_get_access_token(self):
        """Get an access token."""
        if self._token_valid is not None and self._token_valid > core.helpers.utcnow():
            return self._token

        resp = await _cloud_api.async_alexa_access_token(self._cloud)
        body = await resp.json()

        if resp.status == http.HTTPStatus.BAD_REQUEST:
            if body["reason"] in ("RefreshTokenNotFound", "UnknownRegion"):
                if self.should_report_state:
                    self._shc.components.persistent_notification.async_create(
                        f"There was an error reporting state to Alexa ({body['reason']}). "
                        + "Please re-link your Alexa skill via the Alexa app to "
                        + "continue using it.",
                        "Alexa state reporting disabled",
                        "cloud_alexa_report",
                    )
                raise _alexa.RequireRelink

            raise _alexa.NoTokenAvailable

        self._token = body["access_token"]
        self._endpoint = body["event_endpoint"]
        self._token_valid = core.helpers.utcnow() + dt.timedelta(
            seconds=body["expires_in"]
        )
        return self._token

    async def _async_prefs_updated(self, prefs: CloudPreferences) -> None:
        """Handle updated preferences."""
        if not self._cloud.is_logged_in:
            if self.is_reporting_states:
                await self.async_disable_proactive_mode()

            if self._alexa_sync_unsub:
                self._alexa_sync_unsub()
                self._alexa_sync_unsub = None
            return

        updated_prefs = prefs.last_updated

        if (
            "alexa" not in self._shc.config.components
            and self.enabled
            and self._shc.is_running
        ):
            await self._shc.setup.async_setup_component("alexa", {})

        if self.should_report_state != self.is_reporting_states:
            if self.should_report_state:
                try:
                    await self.async_enable_proactive_mode()
                except (_alexa.NoTokenAvailable, _alexa.RequireRelink):
                    await self.set_authorized(False)
            else:
                await self.async_disable_proactive_mode()

            # State reporting is reported as a property on entities.
            # So when we change it, we need to sync all entities.
            await self.async_sync_entities()
            return

        # Nothing to do if no Alexa related things have changed
        if not any(
            key in updated_prefs
            for key in (
                Const.PREF_ALEXA_DEFAULT_EXPOSE,
                Const.PREF_ALEXA_ENTITY_CONFIGS,
                Const.PREF_ALEXA_REPORT_STATE,
                Const.PREF_ENABLE_ALEXA,
            )
        ):
            return

        # If we update just entity preferences, delay updating
        # as we might update more
        if updated_prefs == {Const.PREF_ALEXA_ENTITY_CONFIGS}:
            if self._alexa_sync_unsub:
                self._alexa_sync_unsub()

            self._alexa_sync_unsub = self._shc.tracker.async_call_later(
                _SYNC_DELAY, self._sync_prefs
            )
            return

        await self.async_sync_entities()

    async def _sync_prefs(self, _now):
        """Sync the updated preferences to Alexa."""
        self._alexa_sync_unsub = None
        old_prefs = self._cur_entity_prefs
        new_prefs = self._prefs.alexa_entity_configs

        seen = set()
        to_update = []
        to_remove = []
        is_enabled = self.enabled

        for entity_id, info in old_prefs.items():
            seen.add(entity_id)

            if not is_enabled:
                to_remove.append(entity_id)

            old_expose = info.get(Const.PREF_SHOULD_EXPOSE)

            if entity_id in new_prefs:
                new_expose = new_prefs[entity_id].get(Const.PREF_SHOULD_EXPOSE)
            else:
                new_expose = None

            if old_expose == new_expose:
                continue

            if new_expose:
                to_update.append(entity_id)
            else:
                to_remove.append(entity_id)

        # Now all the ones that are in new prefs but never were in old prefs
        for entity_id, info in new_prefs.items():
            if entity_id in seen:
                continue

            new_expose = info.get(Const.PREF_SHOULD_EXPOSE)

            if new_expose is None:
                continue

            # Only test if we should expose. It can never be a remove action,
            # as it didn't exist in old prefs object.
            if new_expose:
                to_update.append(entity_id)

        # We only set the prefs when update is successful, that way we will
        # retry when next change comes in.
        alexa = self._shc.components.alexa
        if not isinstance(alexa, _alexa.Component):
            alexa = None

        if await self._sync_helper(alexa, to_update, to_remove):
            self._cur_entity_prefs = new_prefs

    async def async_sync_entities(self):
        """Sync all entities to Alexa."""
        # Remove any pending sync
        if self._alexa_sync_unsub:
            self._alexa_sync_unsub()
            self._alexa_sync_unsub = None

        to_update = []
        to_remove = []

        is_enabled = self.enabled

        alexa = self._shc.components.alexa
        if not isinstance(alexa, _alexa.Component):
            alexa = None
        else:
            for entity in alexa.async_get_entities(self):
                if is_enabled and self.should_expose(entity.entity_id):
                    to_update.append(entity.entity_id)
                else:
                    to_remove.append(entity.entity_id)

        return await self._sync_helper(alexa, to_update, to_remove)

    async def _sync_helper(self, alexa: _alexa.Component, to_update, to_remove) -> bool:
        """Sync entities to Alexa.

        Return boolean if it was successful.
        """
        if not to_update and not to_remove:
            return True

        if alexa is None:
            return False

        # Make sure it's valid.
        await self.async_get_access_token()

        tasks = []

        if to_update:
            tasks.append(alexa.async_send_add_or_update_message(self, to_update))

        if to_remove:
            tasks.append(alexa.async_send_delete_message(self, to_remove))

        try:
            async with async_timeout.timeout(10):
                await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

            return True

        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout trying to sync entities to Alexa")
            return False

        except aiohttp.ClientError as err:
            _LOGGER.warning(f"Error trying to sync entities to Alexa: {err}")
            return False

    async def _handle_entity_registry_updated(self, event):
        """Handle when entity registry updated."""
        if not self.enabled or not self._cloud.is_logged_in:
            return

        entity_id = event.data["entity_id"]

        if not self.should_expose(entity_id):
            return

        action = event.data["action"]
        to_update = []
        to_remove = []

        if action == "create":
            to_update.append(entity_id)
        elif action == "remove":
            to_remove.append(entity_id)
        elif action == "update" and bool(
            set(event.data["changes"])
            & core.EntityRegistry.ENTITY_DESCRIBING_ATTRIBUTES
        ):
            to_update.append(entity_id)
            if "old_entity_id" in event.data:
                to_remove.append(event.data["old_entity_id"])

        alexa = self._shc.components.alexa
        if not isinstance(alexa, _alexa.Component):
            alexa = None
        with contextlib.suppress(_alexa.NoTokenAvailable):
            await self._sync_helper(alexa, to_update, to_remove)
