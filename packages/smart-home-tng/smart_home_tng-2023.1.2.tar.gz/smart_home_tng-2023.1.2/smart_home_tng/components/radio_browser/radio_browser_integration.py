"""
Radio Browser Integration for Smart Home - The Next Generation.

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

import radios

from ... import core
from .radio_browser_config_flow import RadioBrowserConfigFlow
from .radio_media_source import RadioMediaSource


# pylint: disable=unused-variable
class RadioBrowserIntegration(
    core.SmartHomeControllerComponent, core.MediaSourcePlatform, core.ConfigFlowPlatform
):
    """The Radio Browser integration."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._register_flow()
        self._supported_platforms = frozenset(
            [core.Platform.MEDIA_SOURCE, core.Platform.CONFIG_FLOW]
        )
        self._media_source: RadioMediaSource | asyncio.Event = None

    async def async_setup_entry(self, _entry: core.ConfigEntry) -> bool:
        """Set up Radio Browser from a config entry.

        This integration doesn't set up any enitites, as it provides a media source
        only.
        """
        session = core.HttpClient.async_get_clientsession(self._shc)
        browser = radios.RadioBrowser(
            session=session,
            user_agent=f"Smart Home - The Next Generation/{core.Const.__version__}",
        )

        try:
            await browser.stats()
            RadioMediaSource.set_radio_browser(browser)
        except radios.RadioBrowserError as err:
            raise core.ConfigEntryNotReady(
                "Could not connect to Radio Browser API"
            ) from err

        return True

    async def async_unload_entry(self, _entry: core.ConfigEntry) -> bool:
        RadioMediaSource.set_radio_browser(None)
        return True

    def create_config_flow(
        self, context: dict, init_data: typing.Any
    ) -> core.ConfigFlow:
        return RadioBrowserConfigFlow(self, context, init_data)

    async def async_get_media_source(self) -> core.MediaSource:
        """Set up Radio Browser media source."""
        if self._media_source is None:
            self._media_source = event = asyncio.Event()

            # Radio browser support only a single config entry
            entry = self.controller.config_entries.async_entries(self.domain)[0]

            self._media_source = RadioMediaSource(self, entry)
            event.set()
        else:
            evt_or_obj = self._media_source
            if isinstance(evt_or_obj, asyncio.Event):
                await evt_or_obj.wait()
        return self._media_source
