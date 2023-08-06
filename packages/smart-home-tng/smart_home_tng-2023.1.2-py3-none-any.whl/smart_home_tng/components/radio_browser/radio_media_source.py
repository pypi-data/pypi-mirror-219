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

import mimetypes
import typing

import radios

from ... import core

_CODEC_TO_MIMETYPE: typing.Final = {
    "MP3": "audio/mpeg",
    "AAC": "audio/aac",
    "AAC+": "audio/aac",
    "OGG": "application/ogg",
}


# pylint: disable=unused-variable
class RadioMediaSource(core.MediaSource):
    """Provide Radio stations as media sources."""

    _name = "Radio Browser"
    _radio_browser: radios.RadioBrowser = None

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        entry: core.ConfigEntry,
    ) -> None:
        """Initialize CameraMediaSource."""
        super().__init__(owner.domain)
        self._owner = owner
        self._entry = entry

    @property
    def browser(self) -> radios.RadioBrowser:
        """Return the radio browser."""
        return self._radio_browser

    async def async_resolve_media(self, item: core.MediaSourceItem) -> core.PlayMedia:
        """Resolve selected Radio station to a streaming URL."""
        browser = self.browser

        if browser is None:
            raise core.Unresolvable("Radio Browser not initialized")

        station = await browser.station(uuid=item.identifier)
        if not station:
            raise core.Unresolvable("Radio station is no longer available")

        if not (mime_type := self._async_get_station_mime_type(station)):
            raise core.Unresolvable("Could not determine stream type of radio station")

        # Register "click" with Radio Browser
        await browser.station_click(uuid=station.uuid)

        return core.PlayMedia(station.url, mime_type)

    async def async_browse_media(
        self,
        item: core.MediaSourceItem,
    ) -> core.BrowseMediaSource:
        """Return media."""
        browser = self.browser

        if browser is None:
            raise core.MediaPlayer.BrowseError("Radio Browser not initialized")

        return core.BrowseMediaSource(
            domain=self._owner.domain,
            identifier=None,
            media_class=core.MediaPlayer.MediaClass.CHANNEL,
            media_content_type=core.MediaPlayer.MediaType.MUSIC,
            title=self._entry.title,
            can_play=False,
            can_expand=True,
            children_media_class=core.MediaPlayer.MediaClass.DIRECTORY,
            children=[
                *await self._async_build_popular(browser, item),
                *await self._async_build_by_tag(browser, item),
                *await self._async_build_by_language(browser, item),
                *await self._async_build_by_country(browser, item),
            ],
        )

    @core.callback
    @staticmethod
    def _async_get_station_mime_type(station: radios.Station) -> str:
        """Determine mime type of a radio station."""
        mime_type = _CODEC_TO_MIMETYPE.get(station.codec)
        if not mime_type:
            mime_type, _ = mimetypes.guess_type(station.url)
        return mime_type

    @core.callback
    def _async_build_stations(
        self, stations: list[radios.Station]
    ) -> list[core.BrowseMediaSource]:
        """Build list of media sources from radio stations."""
        items: list[core.BrowseMediaSource] = []

        for station in stations:
            if station.codec == "UNKNOWN" or not (
                mime_type := self._async_get_station_mime_type(station)
            ):
                continue

            items.append(
                core.BrowseMediaSource(
                    domain=self._owner.domain,
                    identifier=station.uuid,
                    media_class=core.MediaPlayer.MediaClass.MUSIC,
                    media_content_type=mime_type,
                    title=station.name,
                    can_play=True,
                    can_expand=False,
                    thumbnail=station.favicon,
                )
            )

        return items

    async def _async_build_by_country(
        self, browser: radios.RadioBrowser, item: core.MediaSourceItem
    ) -> list[core.BrowseMediaSource]:
        """Handle browsing radio stations by country."""
        category, _, country_code = (item.identifier or "").partition("/")
        if country_code:
            stations = await browser.stations(
                filter_by=radios.FilterBy.COUNTRY_CODE_EXACT,
                filter_term=country_code,
                hide_broken=True,
                order=radios.Order.NAME,
                reverse=False,
            )
            return self._async_build_stations(stations)

        # We show country in the root additionally, when there is no item
        if not item.identifier or category == "country":
            countries = await browser.countries(order=radios.Order.NAME)
            return [
                core.BrowseMediaSource(
                    domain=self._owner.domain,
                    identifier=f"country/{country.code}",
                    media_class=core.MediaPlayer.MediaClass.DIRECTORY,
                    media_content_type=core.MediaPlayer.MediaType.MUSIC,
                    title=country.name,
                    can_play=False,
                    can_expand=True,
                    thumbnail=country.favicon,
                )
                for country in countries
            ]

        return []

    async def _async_build_by_language(
        self, browser: radios.RadioBrowser, item: core.MediaSourceItem
    ) -> list[core.BrowseMediaSource]:
        """Handle browsing radio stations by language."""
        category, _, language = (item.identifier or "").partition("/")
        if category == "language" and language:
            stations = await browser.stations(
                filter_by=radios.FilterBy.LANGUAGE_EXACT,
                filter_term=language,
                hide_broken=True,
                order=radios.Order.NAME,
                reverse=False,
            )
            return self._async_build_stations(stations)

        if category == "language":
            languages = await browser.languages(
                order=radios.Order.NAME, hide_broken=True
            )
            return [
                core.BrowseMediaSource(
                    domain=self._owner.domain,
                    identifier=f"language/{language.code}",
                    media_class=core.MediaPlayer.MediaClass.DIRECTORY,
                    media_content_type=core.MediaPlayer.MediaType.MUSIC,
                    title=language.name,
                    can_play=False,
                    can_expand=True,
                    thumbnail=language.favicon,
                )
                for language in languages
            ]

        if not item.identifier:
            return [
                core.BrowseMediaSource(
                    domain=self._owner.domain,
                    identifier="language",
                    media_class=core.MediaPlayer.MediaClass.DIRECTORY,
                    media_content_type=core.MediaPlayer.MediaType.MUSIC,
                    title="By Language",
                    can_play=False,
                    can_expand=True,
                )
            ]

        return []

    async def _async_build_popular(
        self, browser: radios.RadioBrowser, item: core.MediaSourceItem
    ) -> list[core.BrowseMediaSource]:
        """Handle browsing popular radio stations."""
        if item.identifier == "popular":
            stations = await browser.stations(
                hide_broken=True,
                limit=250,
                order=radios.Order.CLICK_COUNT,
                reverse=True,
            )
            return self._async_build_stations(stations)

        if not item.identifier:
            return [
                core.BrowseMediaSource(
                    domain=self._owner.domain,
                    identifier="popular",
                    media_class=core.MediaPlayer.MediaClass.DIRECTORY,
                    media_content_type=core.MediaPlayer.MediaType.MUSIC,
                    title="Popular",
                    can_play=False,
                    can_expand=True,
                )
            ]

        return []

    async def _async_build_by_tag(
        self, browser: radios.RadioBrowser, item: core.MediaSourceItem
    ) -> list[core.BrowseMediaSource]:
        """Handle browsing radio stations by tags."""
        category, _, tag = (item.identifier or "").partition("/")
        if category == "tag" and tag:
            stations = await browser.stations(
                filter_by=radios.FilterBy.TAG_EXACT,
                filter_term=tag,
                hide_broken=True,
                order=radios.Order.NAME,
                reverse=False,
            )
            return self._async_build_stations(stations)

        if category == "tag":
            tags = await browser.tags(
                hide_broken=True,
                limit=100,
                order=radios.Order.STATION_COUNT,
                reverse=True,
            )

            # Now we have the top tags, reorder them by name
            tags.sort(key=lambda tag: tag.name)

            return [
                core.BrowseMediaSource(
                    domain=self._owner.domain,
                    identifier=f"tag/{tag.name}",
                    media_class=core.MediaPlayer.MediaClass.DIRECTORY,
                    media_content_type=core.MediaPlayer.MediaType.MUSIC,
                    title=tag.name.title(),
                    can_play=False,
                    can_expand=True,
                )
                for tag in tags
            ]

        if not item.identifier:
            return [
                core.BrowseMediaSource(
                    domain=self._owner.domain,
                    identifier="tag",
                    media_class=core.MediaPlayer.MediaClass.DIRECTORY,
                    media_content_type=core.MediaPlayer.MediaType.MUSIC,
                    title="By Category",
                    can_play=False,
                    can_expand=True,
                )
            ]

        return []

    @staticmethod
    def set_radio_browser(browser: radios.RadioBrowser):
        """Set radio browser api root."""
        RadioMediaSource._radio_browser = browser
