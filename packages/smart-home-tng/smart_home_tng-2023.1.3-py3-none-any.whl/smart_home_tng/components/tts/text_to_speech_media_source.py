"""
TextToSpeech (TTS) Component for Smart Home - The Next Generation.

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

import yarl

from ... import core

if not typing.TYPE_CHECKING:

    class TextToSpeechComponent:
        pass


if typing.TYPE_CHECKING:
    from .text_to_speech_component import TextToSpeechComponent


# pylint: disable=unused-variable
class TextToSpeechMediaSource(core.MediaSource):
    """Provide text-to-speech providers as media sources."""

    name: str = "Text to Speech"

    def __init__(self, owner: TextToSpeechComponent) -> None:
        """Initialize TTSMediaSource."""
        super().__init__(owner.domain)
        self._owner = owner

    @property
    def controller(self) -> core.SmartHomeController:
        return self._owner.controller

    async def async_resolve_media(self, item: core.MediaSourceItem) -> core.PlayMedia:
        """Resolve media to a url."""
        parsed = yarl.URL(item.identifier)
        if "message" not in parsed.query:
            raise core.Unresolvable("No message specified.")

        options = dict(parsed.query)
        kwargs: dict[str, typing.Any] = {
            "engine": parsed.name,
            "message": options.pop("message"),
            "language": options.pop("language", None),
            "options": options,
        }
        if "cache" in options:
            kwargs["cache"] = options.pop("cache") == "true"

        manager = self._owner.tts

        try:
            url = await manager.async_get_url_path(**kwargs)
        except core.SmartHomeControllerError as err:
            raise core.Unresolvable(str(err)) from err

        mime_type = mimetypes.guess_type(url)[0] or "audio/mpeg"

        if manager.base_url and manager.base_url != self.controller.get_url():
            url = f"{manager.base_url}{url}"

        return core.PlayMedia(url, mime_type)

    async def async_browse_media(
        self,
        item: core.MediaSourceItem,
    ) -> core.BrowseMediaSource:
        """Return media."""
        if item.identifier:
            provider, _, params = item.identifier.partition("?")
            return self._provider_item(provider, params)

        # Root. List providers.
        manager = self._owner.tts
        # pylint: disable=protected-access
        children = [self._provider_item(provider) for provider in manager._providers]
        return core.BrowseMediaSource(
            domain=self._owner.domain,
            identifier=None,
            media_class=core.MediaPlayer.MediaClass.APP,
            media_content_type="",
            title=self.name,
            can_play=False,
            can_expand=True,
            children_media_class=core.MediaPlayer.MediaClass.APP,
            children=children,
        )

    @core.callback
    def _provider_item(
        self, provider_domain: str, params: str = None
    ) -> core.BrowseMediaSource:
        """Return provider item."""
        manager = self._owner.tts
        if (provider := manager.get_provider(provider_domain)) is None:
            raise core.MediaPlayer.BrowseError("Unknown provider")

        if params:
            params = f"?{params}"
        else:
            params = ""

        return core.BrowseMediaSource(
            domain=self._owner.domain,
            identifier=f"{provider_domain}{params}",
            media_class=core.MediaPlayer.MediaClass.APP,
            media_content_type="provider",
            title=provider.name,
            thumbnail=f"https://brands.home-assistant.io/_/{provider_domain}/logo.png",
            can_play=False,
            can_expand=True,
        )
