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

import typing

from ... import auth, core
from .const import Const

_UNDEFINED: typing.Final = object()


# pylint: disable=unused-variable
class CloudPreferences:
    """Handle cloud preferences."""

    _webhook: core.WebhookComponent = None

    def __init__(self, owner: core.CloudComponent):
        """Initialize cloud prefs."""
        self._owner = owner
        self._store = core.Store(
            owner.controller, owner.storage_version, owner.storage_key
        )
        self._prefs = None
        self._listeners = []
        self._last_updated: set[str] = set()
        webhook = owner.get_component(core.Const.WEBHOOK_COMPONENT_NAME)
        if isinstance(webhook, core.WebhookComponent):
            CloudPreferences._webhook = webhook

    @property
    def last_updated(self) -> set[str]:
        return frozenset(self._last_updated)

    async def async_initialize(self):
        """Finish initializing the preferences."""
        if (prefs := await self._store.async_load()) is None:
            prefs = self._empty_config("")

        self._prefs = prefs

        if (
            Const.PREF_GOOGLE_LOCAL_WEBHOOK_ID not in self._prefs
            and self._webhook is not None
        ):
            await self._save_prefs(
                {
                    **self._prefs,
                    Const.PREF_GOOGLE_LOCAL_WEBHOOK_ID: self._webhook.async_generate_id(),
                }
            )

    @core.callback
    def async_listen_updates(self, listener):
        """Listen for updates to the preferences."""
        self._listeners.append(listener)

    async def async_update(
        self,
        *,
        google_enabled=_UNDEFINED,
        alexa_enabled=_UNDEFINED,
        remote_enabled=_UNDEFINED,
        google_secure_devices_pin=_UNDEFINED,
        cloudhooks=_UNDEFINED,
        cloud_user=_UNDEFINED,
        google_entity_configs=_UNDEFINED,
        alexa_entity_configs=_UNDEFINED,
        alexa_report_state=_UNDEFINED,
        google_report_state=_UNDEFINED,
        alexa_default_expose=_UNDEFINED,
        google_default_expose=_UNDEFINED,
        tts_default_voice=_UNDEFINED,
        remote_domain=_UNDEFINED,
    ):
        """Update user preferences."""
        prefs = {**self._prefs}

        for key, value in (
            (Const.PREF_ENABLE_GOOGLE, google_enabled),
            (Const.PREF_ENABLE_ALEXA, alexa_enabled),
            (Const.PREF_ENABLE_REMOTE, remote_enabled),
            (Const.PREF_GOOGLE_SECURE_DEVICES_PIN, google_secure_devices_pin),
            (Const.PREF_CLOUDHOOKS, cloudhooks),
            (Const.PREF_CLOUD_USER, cloud_user),
            (Const.PREF_GOOGLE_ENTITY_CONFIGS, google_entity_configs),
            (Const.PREF_ALEXA_ENTITY_CONFIGS, alexa_entity_configs),
            (Const.PREF_ALEXA_REPORT_STATE, alexa_report_state),
            (Const.PREF_GOOGLE_REPORT_STATE, google_report_state),
            (Const.PREF_ALEXA_DEFAULT_EXPOSE, alexa_default_expose),
            (Const.PREF_GOOGLE_DEFAULT_EXPOSE, google_default_expose),
            (Const.PREF_TTS_DEFAULT_VOICE, tts_default_voice),
            (Const.PREF_REMOTE_DOMAIN, remote_domain),
        ):
            if value is not _UNDEFINED:
                prefs[key] = value

        await self._save_prefs(prefs)

    async def async_update_google_entity_config(
        self,
        *,
        entity_id,
        override_name=_UNDEFINED,
        disable_2fa=_UNDEFINED,
        aliases=_UNDEFINED,
        should_expose=_UNDEFINED,
    ):
        """Update config for a Google entity."""
        entities = self.google_entity_configs
        entity = entities.get(entity_id, {})

        changes = {}
        for key, value in (
            (Const.PREF_OVERRIDE_NAME, override_name),
            (Const.PREF_DISABLE_2FA, disable_2fa),
            (Const.PREF_ALIASES, aliases),
            (Const.PREF_SHOULD_EXPOSE, should_expose),
        ):
            if value is not _UNDEFINED:
                changes[key] = value

        if not changes:
            return

        updated_entity = {**entity, **changes}

        updated_entities = {**entities, entity_id: updated_entity}
        await self.async_update(google_entity_configs=updated_entities)

    async def async_update_alexa_entity_config(
        self, *, entity_id, should_expose=_UNDEFINED
    ):
        """Update config for an Alexa entity."""
        entities = self.alexa_entity_configs
        entity = entities.get(entity_id, {})

        changes = {}
        for key, value in ((Const.PREF_SHOULD_EXPOSE, should_expose),):
            if value is not _UNDEFINED:
                changes[key] = value

        if not changes:
            return

        updated_entity = {**entity, **changes}

        updated_entities = {**entities, entity_id: updated_entity}
        await self.async_update(alexa_entity_configs=updated_entities)

    async def async_set_username(self, username) -> bool:
        """Set the username that is logged in."""
        # Logging out.
        if username is None:
            user = await self._load_cloud_user()

            if user is not None:
                await self._owner.controller.auth.async_remove_user(user)
                await self._save_prefs({**self._prefs, Const.PREF_CLOUD_USER: None})
            return False

        cur_username = self._prefs.get(Const.PREF_USERNAME)

        if cur_username == username:
            return False

        if cur_username is None:
            await self._save_prefs({**self._prefs, Const.PREF_USERNAME: username})
        else:
            await self._save_prefs(self._empty_config(username))

        return True

    def as_dict(self):
        """Return dictionary version."""
        return {
            Const.PREF_ALEXA_DEFAULT_EXPOSE: self.alexa_default_expose,
            Const.PREF_ALEXA_ENTITY_CONFIGS: self.alexa_entity_configs,
            Const.PREF_ALEXA_REPORT_STATE: self.alexa_report_state,
            Const.PREF_CLOUDHOOKS: self.cloudhooks,
            Const.PREF_ENABLE_ALEXA: self.alexa_enabled,
            Const.PREF_ENABLE_GOOGLE: self.google_enabled,
            Const.PREF_ENABLE_REMOTE: self.remote_enabled,
            Const.PREF_GOOGLE_DEFAULT_EXPOSE: self.google_default_expose,
            Const.PREF_GOOGLE_ENTITY_CONFIGS: self.google_entity_configs,
            Const.PREF_GOOGLE_REPORT_STATE: self.google_report_state,
            Const.PREF_GOOGLE_SECURE_DEVICES_PIN: self.google_secure_devices_pin,
            Const.PREF_TTS_DEFAULT_VOICE: self.tts_default_voice,
        }

    @property
    def remote_enabled(self):
        """Return if remote is enabled on start."""
        if not self._prefs.get(Const.PREF_ENABLE_REMOTE, False):
            return False

        return True

    @property
    def remote_domain(self):
        """Return remote domain."""
        return self._prefs.get(Const.PREF_REMOTE_DOMAIN)

    @property
    def alexa_enabled(self):
        """Return if Alexa is enabled."""
        return self._prefs[Const.PREF_ENABLE_ALEXA]

    @property
    def alexa_report_state(self):
        """Return if Alexa report state is enabled."""
        return self._prefs.get(
            Const.PREF_ALEXA_REPORT_STATE, Const.DEFAULT_ALEXA_REPORT_STATE
        )

    @property
    def alexa_default_expose(self) -> list[str] | None:
        """Return array of entity domains that are exposed by default to Alexa.

        Can return None, in which case for backwards should be interpreted as allow all domains.
        """
        return self._prefs.get(Const.PREF_ALEXA_DEFAULT_EXPOSE)

    @property
    def alexa_entity_configs(self):
        """Return Alexa Entity configurations."""
        return self._prefs.get(Const.PREF_ALEXA_ENTITY_CONFIGS, {})

    @property
    def google_enabled(self):
        """Return if Google is enabled."""
        return self._prefs[Const.PREF_ENABLE_GOOGLE]

    @property
    def google_report_state(self):
        """Return if Google report state is enabled."""
        return self._prefs.get(
            Const.PREF_GOOGLE_REPORT_STATE, Const.DEFAULT_GOOGLE_REPORT_STATE
        )

    @property
    def google_secure_devices_pin(self):
        """Return if Google is allowed to unlock locks."""
        return self._prefs.get(Const.PREF_GOOGLE_SECURE_DEVICES_PIN)

    @property
    def google_entity_configs(self):
        """Return Google Entity configurations."""
        return self._prefs.get(Const.PREF_GOOGLE_ENTITY_CONFIGS, {})

    @property
    def google_local_webhook_id(self):
        """Return Google webhook ID to receive local messages."""
        return self._prefs[Const.PREF_GOOGLE_LOCAL_WEBHOOK_ID]

    @property
    def google_default_expose(self) -> list[str] | None:
        """Return array of entity domains that are exposed by default to Google.

        Can return None, in which case for backwards should be interpreted as allow all domains.
        """
        return self._prefs.get(Const.PREF_GOOGLE_DEFAULT_EXPOSE)

    @property
    def cloudhooks(self):
        """Return the published cloud webhooks."""
        return self._prefs.get(Const.PREF_CLOUDHOOKS, {})

    @property
    def tts_default_voice(self):
        """Return the default TTS voice."""
        return self._prefs.get(
            Const.PREF_TTS_DEFAULT_VOICE, Const.DEFAULT_TTS_DEFAULT_VOICE
        )

    async def get_cloud_user(self) -> str:
        """Return ID of Home Assistant Cloud system user."""
        user = await self._load_cloud_user()

        if user:
            return user.id

        user = await self._owner.controller.auth.async_create_system_user(
            "Home Assistant Cloud",
            group_ids=[auth.Const.GROUP_ID_ADMIN],
            local_only=True,
        )
        assert user is not None
        await self.async_update(cloud_user=user.id)
        return user.id

    async def _load_cloud_user(self) -> auth.User:
        """Load cloud user if available."""
        if (user_id := self._prefs.get(Const.PREF_CLOUD_USER)) is None:
            return None

        # Fetch the user. It can happen that the user no longer exists if
        # an image was restored without restoring the cloud prefs.
        return await self._owner.controller.auth.async_get_user(user_id)

    async def _save_prefs(self, prefs):
        """Save preferences to disk."""
        self.last_updated = {
            key for key, value in prefs.items() if value != self._prefs.get(key)
        }
        self._prefs = prefs
        await self._store.async_save(self._prefs)

        for listener in self._listeners:
            self._owner.controller.async_create_task(
                core.helpers.async_create_catching_coro(listener(self))
            )

    @core.callback
    @staticmethod
    def _empty_config(username):
        """Return an empty config."""
        return {
            Const.PREF_ALEXA_DEFAULT_EXPOSE: Const.DEFAULT_EXPOSED_DOMAINS,
            Const.PREF_ALEXA_ENTITY_CONFIGS: {},
            Const.PREF_CLOUD_USER: None,
            Const.PREF_CLOUDHOOKS: {},
            Const.PREF_ENABLE_ALEXA: True,
            Const.PREF_ENABLE_GOOGLE: True,
            Const.PREF_ENABLE_REMOTE: False,
            Const.PREF_GOOGLE_DEFAULT_EXPOSE: Const.DEFAULT_EXPOSED_DOMAINS,
            Const.PREF_GOOGLE_ENTITY_CONFIGS: {},
            Const.PREF_GOOGLE_LOCAL_WEBHOOK_ID: CloudPreferences._webhook.async_generate_id(),
            Const.PREF_GOOGLE_SECURE_DEVICES_PIN: None,
            Const.PREF_REMOTE_DOMAIN: None,
            Const.PREF_USERNAME: username,
        }
