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
import pathlib
import typing

import aiohttp
import hass_nabucasa.client as nabucasa  # pylint: disable=import-error

from ... import core
from .const import Const
from .cloud_alexa_config import CloudAlexaConfig
from .cloud_google_config import CloudGoogleConfig
from .cloud_preferences import CloudPreferences


# pylint: disable=unused-variable
class CloudClient(nabucasa.CloudClient):
    """Interface class for Home Assistant Cloud."""

    def __init__(
        self,
        owner: core.CloudComponent,
        prefs: CloudPreferences,
        websession: aiohttp.ClientSession,
        alexa_user_config: dict[str, typing.Any],
        google_user_config: dict[str, typing.Any],
    ) -> None:
        """Initialize client interface to Cloud."""
        self._owner = owner
        self._prefs = prefs
        self._websession = websession
        self.google_user_config = google_user_config
        self.alexa_user_config = alexa_user_config
        self._alexa_config: CloudAlexaConfig = None
        self._google_config: CloudGoogleConfig = None
        self._alexa_config_init_lock = asyncio.Lock()
        self._google_config_init_lock = asyncio.Lock()
        self._webhook: core.WebhookComponent = None
        comp = owner.get_component(core.Const.WEBHOOK_COMPONENT_NAME)
        if isinstance(comp, core.WebhookComponent):
            self._webhook = comp

    @property
    def base_path(self) -> pathlib.Path:
        """Return path to base dir."""
        assert self._owner.controller.config.config_dir is not None
        return pathlib.Path(self._owner.controller.config.config_dir)

    @property
    def prefs(self) -> CloudPreferences:
        """Return Cloud preferences."""
        return self._prefs

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """Return client loop."""
        # pylint: disable=protected-access
        return self._owner.controller._loop

    @property
    def websession(self) -> aiohttp.ClientSession:
        """Return client session for aiohttp."""
        return self._websession

    @property
    def aiohttp_runner(self) -> aiohttp.web.AppRunner:
        """Return client webinterface aiohttp application."""
        # pylint: disable=protected-access
        return self._owner.controller.http._runner

    @property
    def cloudhooks(self) -> dict[str, dict[str, str]]:
        """Return list of cloudhooks."""
        return self._prefs.cloudhooks

    @property
    def remote_autostart(self) -> bool:
        """Return true if we want start a remote connection."""
        return self._prefs.remote_enabled

    async def get_alexa_config(self) -> CloudAlexaConfig:
        """Return Alexa config."""
        if self._alexa_config is None:
            async with self._alexa_config_init_lock:
                if self._alexa_config is not None:
                    return self._alexa_config

                assert self.cloud is not None

                cloud_user = await self._prefs.get_cloud_user()

                alexa_conf = CloudAlexaConfig(
                    self._owner.controller,
                    self.alexa_user_config,
                    cloud_user,
                    self._prefs,
                    self.cloud,
                )
                await alexa_conf.async_initialize()
                self._alexa_config = alexa_conf

        return self._alexa_config

    async def get_google_config(self) -> CloudGoogleConfig:
        """Return Google config."""
        if not self._google_config:
            async with self._google_config_init_lock:
                if self._google_config is not None:
                    return self._google_config

                assert self.cloud is not None

                cloud_user = await self._prefs.get_cloud_user()

                google_conf = CloudGoogleConfig(
                    self._owner.controller.components.google_assistant,
                    self.google_user_config,
                    cloud_user,
                    self._prefs,
                    self.cloud,
                )
                await google_conf.async_initialize()
                self._google_config = google_conf

        return self._google_config

    async def cloud_started(self) -> None:
        """When cloud is started."""
        is_new_user = await self.prefs.async_set_username(self.cloud.username)

        async def enable_alexa(_):
            """Enable Alexa."""
            aconf = await self.get_alexa_config()
            try:
                await aconf.async_enable_proactive_mode()
            except aiohttp.ClientError as err:  # If no internet available yet
                if self._owner.controller.is_running:
                    logging.getLogger(__package__).warning(
                        f"Unable to activate Alexa Report State: {err}. Retrying in 30 seconds",
                    )
                self._owner.controller.tracker.async_call_later(30, enable_alexa)
            except (core.Alexa.NoTokenAvailable, core.Alexa.RequireRelink):
                pass

        async def enable_google(_):
            """Enable Google."""
            gconf = await self.get_google_config()

            gconf.async_enable_local_sdk()

            if gconf.should_report_state:
                gconf.async_enable_report_state()

            if is_new_user:
                await gconf.async_sync_entities(gconf.agent_user_id)

        tasks = []

        if self._prefs.alexa_enabled and self._prefs.alexa_report_state:
            tasks.append(enable_alexa)

        if self._prefs.google_enabled:
            tasks.append(enable_google)

        if tasks:
            await asyncio.gather(*(task(None) for task in tasks))

    async def cloud_stopped(self) -> None:
        """When the cloud is stopped."""

    async def logout_cleanups(self) -> None:
        """Cleanup some stuff after logout."""
        await self.prefs.async_set_username(None)

        self._google_config = None

    @core.callback
    def user_message(self, identifier: str, title: str, message: str) -> None:
        """Create a message for user to UI."""
        self._owner.controller.persistent_notification.async_create(
            message, title, identifier
        )

    @core.callback
    def dispatcher_message(self, identifier: str, data: typing.Any = None) -> None:
        """Match cloud notification to dispatcher."""
        if identifier.startswith("remote_"):
            self._owner.controller.dispatcher.async_send(
                Const.DISPATCHER_REMOTE_UPDATE, data
            )

    async def async_cloud_connect_update(self, connect: bool) -> None:
        """Process cloud remote message to client."""
        await self._prefs.async_update(remote_enabled=connect)

    async def async_alexa_message(
        self, payload: dict[typing.Any, typing.Any]
    ) -> dict[typing.Any, typing.Any]:
        """Process cloud alexa message to client."""
        cloud_user = await self._prefs.get_cloud_user()
        aconfig = await self.get_alexa_config()
        alexa = self._owner.controller.components.alexa
        if not isinstance(alexa, core.Alexa.Component):
            return None

        return await alexa.async_handle_message(
            aconfig,
            payload,
            context=core.Context(user_id=cloud_user),
            enabled=self._prefs.alexa_enabled,
        )

    async def async_google_message(
        self, payload: dict[typing.Any, typing.Any]
    ) -> dict[typing.Any, typing.Any]:
        """Process cloud google message to client."""
        gconf = await self.get_google_config()
        ga = self._owner.controller.components.google_assistant
        if not isinstance(ga, core.GoogleAssistant.Component):
            return None

        if not self._prefs.google_enabled:
            return ga.api_disabled_response(payload, gconf.agent_user_id)

        return await ga.async_handle_message(
            gconf, gconf.cloud_user, payload, core.GoogleAssistant.SOURCE_CLOUD
        )

    async def async_webhook_message(
        self, payload: dict[typing.Any, typing.Any]
    ) -> dict[typing.Any, typing.Any]:
        """Process cloud webhook message to client."""
        cloudhook_id = payload["cloudhook_id"]

        found = None
        for cloudhook in self._prefs.cloudhooks.values():
            if cloudhook["cloudhook_id"] == cloudhook_id:
                found = cloudhook
                break

        if found is None:
            return {"status": http.HTTPStatus.OK}

        request = core.MockRequest(
            content=payload["body"].encode("utf-8"),
            headers=payload["headers"],
            method=payload["method"],
            query_string=payload["query"],
            mock_source=self._owner.domain,
        )

        response = await self._webhook.async_handle_webhook(
            found["webhook_id"], request
        )

        response_dict = core.helpers.serialize_response(response)
        body = response_dict.get("body")

        return {
            "body": body,
            "status": response_dict["status"],
            "headers": {"Content-Type": response.content_type},
        }

    async def async_cloudhooks_update(self, data: dict[str, dict[str, str]]) -> None:
        """Update local list of cloudhooks."""
        await self._prefs.async_update(cloudhooks=data)
