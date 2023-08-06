"""
Analytics Component for Smart Home - The Next Generation.

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
import uuid

import aiohttp
import async_timeout

from ... import core
from .const import Const

if not typing.TYPE_CHECKING:

    class AnalyticsComponent:
        ...


if typing.TYPE_CHECKING:
    from .analytics_component import AnalyticsComponent


# pylint: disable=unused-variable
class Analytics:
    """Analytics helper class for the analytics integration."""

    def __init__(self, owner: AnalyticsComponent) -> None:
        """Initialize the Analytics class."""
        self._owner = owner
        self._session = core.HttpClient.async_get_clientsession(owner.controller)
        self._pref_base = False
        self._pref_diagnostice = False
        self._pref_usage = False
        self._pref_statistics = False
        self._onboarded = False
        self._uuid: str = None
        self._store = core.Store[dict[str, typing.Any]](
            owner.controller, owner.storage_version, owner.storage_key
        )

    @property
    def preferences(self) -> dict:
        """Return the current active preferences."""
        return {
            Const.ATTR_BASE: self._pref_base,
            Const.ATTR_DIAGNOSTICS: self._pref_diagnostice,
            Const.ATTR_USAGE: self._pref_usage,
            Const.ATTR_STATISTICS: self._pref_statistics,
        }

    @property
    def onboarded(self) -> bool:
        """Return bool if the user has made a choice."""
        return self._onboarded

    @property
    def uuid(self) -> str:
        """Return the uuid for the analytics integration."""
        return self._uuid

    @property
    def endpoint(self) -> str:
        """Return the endpoint that will receive the payload."""
        if core.Const.__version__.endswith("0.dev0"):
            # dev installations will contact the dev analytics environment
            return Const.ANALYTICS_ENDPOINT_URL_DEV
        return Const.ANALYTICS_ENDPOINT_URL

    @property
    def supervisor(self) -> bool:
        """Return bool if a supervisor is present."""
        return False

    async def load(self) -> None:
        """Load preferences."""
        stored = typing.cast(dict, await self._store.async_load())
        if stored:
            self._uuid = stored.get(Const.ATTR_UUID)
            self._onboarded = stored.get(Const.ATTR_ONBOARDED, False)
            prefs = stored.get(Const.ATTR_PREFERENCES)
            self._pref_base = prefs.get(Const.ATTR_BASE, False)
            self._pref_diagnostice = prefs.get(Const.ATTR_DIAGNOSTICS, False)
            self._pref_statistics = prefs.get(Const.ATTR_STATISTICS, False)
            self._pref_usage = prefs.get(Const.ATTR_USAGE, False)

        if self.supervisor:
            supervisor_info = {
                Const.ATTR_DIAGNOSTICS: False
            }  # hassio.get_supervisor_info(self.hass)
            if not self.onboarded:
                # User have not configured analytics, get this setting from the supervisor
                if supervisor_info[Const.ATTR_DIAGNOSTICS] and not self.preferences.get(
                    Const.ATTR_DIAGNOSTICS, False
                ):
                    self._pref_diagnostice = True
                elif not supervisor_info[
                    Const.ATTR_DIAGNOSTICS
                ] and self.preferences.get(Const.ATTR_DIAGNOSTICS, False):
                    self._pref_diagnostice = False

    async def save_preferences(self, preferences: dict) -> None:
        """Save preferences."""
        preferences = Const.PREFERENCE_SCHEMA(preferences)
        self._pref_base = preferences.get(Const.ATTR_BASE, False)
        self._pref_diagnostice = preferences.get(Const.ATTR_DIAGNOSTICS, False)
        self._pref_statistics = preferences.get(Const.ATTR_STATISTICS, False)
        self._pref_usage = preferences.get(Const.ATTR_USAGE, False)

        data = {
            Const.ATTR_ONBOARDED: True,
            Const.ATTR_UUID: self._uuid,
            Const.ATTR_PREFERENCES: self.preferences,
        }

        await self._store.async_save(data)

        # if self.supervisor:
        #    await hassio.async_update_diagnostics(
        #        self.hass, self.preferences.get(ATTR_DIAGNOSTICS, False)
        #    )

    async def send_analytics(self, _=None) -> None:
        """Send analytics."""
        supervisor_info = None
        operating_system_info = {}
        shc = self._owner.controller

        if not self.onboarded or not self._pref_base:
            Const.LOGGER.debug("Nothing to submit")
            return

        if self._uuid is None:
            self._uuid = uuid.uuid4().hex
            await self.save_preferences(self.preferences)

        if self.supervisor:
            # supervisor_info = hassio.get_supervisor_info(self.hass)
            # operating_system_info = hassio.get_os_info(self.hass)
            supervisor_info = {}

        system_info = await core.helpers.async_get_system_info(shc)
        integrations = []
        custom_integrations = []
        addons = []
        payload: dict = {
            Const.ATTR_UUID: self.uuid,
            Const.ATTR_VERSION: core.Const.__version__,
            Const.ATTR_INSTALLATION_TYPE: system_info[Const.ATTR_INSTALLATION_TYPE],
        }

        if supervisor_info is not None:
            payload[Const.ATTR_SUPERVISOR] = {
                Const.ATTR_HEALTHY: supervisor_info[Const.ATTR_HEALTHY],
                Const.ATTR_SUPPORTED: supervisor_info[Const.ATTR_SUPPORTED],
                Const.ATTR_ARCH: supervisor_info[Const.ATTR_ARCH],
            }

        if operating_system_info.get(Const.ATTR_BOARD) is not None:
            payload[Const.ATTR_OPERATING_SYSTEM] = {
                Const.ATTR_BOARD: operating_system_info[Const.ATTR_BOARD],
                Const.ATTR_VERSION: operating_system_info[Const.ATTR_VERSION],
            }

        if self.preferences.get(Const.ATTR_USAGE, False) or self.preferences.get(
            Const.ATTR_STATISTICS, False
        ):
            setup = shc.setup
            configured_integrations = await asyncio.gather(
                *(
                    setup.async_get_integration(domain)
                    for domain in setup.async_get_loaded_integrations()
                ),
                return_exceptions=True,
            )

            for integration in configured_integrations:
                if isinstance(integration, core.IntegrationNotFound):
                    continue

                if isinstance(integration, BaseException):
                    raise integration

                if integration.disabled:
                    continue

                if not integration.is_built_in:
                    custom_integrations.append(
                        {
                            core.Const.ATTR_DOMAIN: integration.domain,
                            Const.ATTR_VERSION: integration.version,
                        }
                    )
                    continue

                integrations.append(integration.domain)

            if supervisor_info is not None:
                installed_addons = {}
                # installed_addons = await asyncio.gather(
                #    *(
                #        hassio.async_get_addon_info(self.hass, addon[ATTR_SLUG])
                #        for addon in supervisor_info[ATTR_ADDONS]
                #    )
                # )
                for addon in installed_addons:
                    addons.append(
                        {
                            Const.ATTR_SLUG: addon[Const.ATTR_SLUG],
                            Const.ATTR_PROTECTED: addon[Const.ATTR_PROTECTED],
                            Const.ATTR_VERSION: addon[Const.ATTR_VERSION],
                            Const.ATTR_AUTO_UPDATE: addon[Const.ATTR_AUTO_UPDATE],
                        }
                    )

        if self.preferences.get(Const.ATTR_USAGE, False):
            payload[Const.ATTR_CERTIFICATE] = shc.http.ssl_certificate is not None
            payload[Const.ATTR_INTEGRATIONS] = integrations
            payload[Const.ATTR_CUSTOM_INTEGRATIONS] = custom_integrations
            if supervisor_info is not None:
                payload[Const.ATTR_ADDONS] = addons

            if "energy" in integrations:
                comp = self._owner.controller.components.energy
                if isinstance(comp, core.EnergyComponent):
                    payload[Const.ATTR_ENERGY] = {
                        Const.ATTR_CONFIGURED: await comp.is_configured()
                    }

        if self.preferences.get(Const.ATTR_STATISTICS, False):
            payload[Const.ATTR_STATE_COUNT] = len(shc.states.async_all())
            payload[Const.ATTR_AUTOMATION_COUNT] = len(
                shc.states.async_all("automation")
            )
            payload[Const.ATTR_INTEGRATION_COUNT] = len(integrations)
            if supervisor_info is not None:
                payload[Const.ATTR_ADDON_COUNT] = len(addons)
            payload[Const.ATTR_USER_COUNT] = len(
                [
                    user
                    for user in await shc.auth.async_get_users()
                    if not user.system_generated
                ]
            )

        try:
            async with async_timeout.timeout(30):
                response = await self._session.post(self.endpoint, json=payload)
                if response.status == 200:
                    Const.LOGGER.info(
                        (
                            "Submitted analytics to Home Assistant servers. "
                            + f"Information submitted includes {payload}"
                        ),
                    )
                else:
                    Const.LOGGER.warning(
                        f"Sending analytics failed with statuscode {response.status} "
                        + f"from {self.endpoint}",
                    )
        except asyncio.TimeoutError:
            Const.LOGGER.error(f"Timeout sending analytics to {self.endpoint}")
        except aiohttp.ClientError as err:
            Const.LOGGER.error(f"Error sending analytics to {self.endpoint}: {err:r}")
