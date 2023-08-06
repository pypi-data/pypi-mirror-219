"""
Media Source Component for Smart Home - The Next Generation.

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

# pylint: disable=unused-variable

import collections
import dataclasses
import typing

from ... import core

if not typing.TYPE_CHECKING:

    @typing.overload
    class MediaSourceComponent:
        def items(self) -> collections.abc.Iterable[core.MediaSource]:
            pass

        def get_item(self, domain: str) -> core.MediaSource:
            pass


if typing.TYPE_CHECKING:
    from .media_source_component import MediaSourceComponent


@dataclasses.dataclass()
class MediaSourceItem(core.MediaSourceItem):
    """A parsed media item."""

    owner: MediaSourceComponent
    domain: str
    identifier: str
    target_media_player: str

    async def async_browse(self) -> core.BrowseMediaSource:
        """Browse this item."""
        if self.domain is None:
            base = core.BrowseMediaSource(
                domain=None,
                identifier=None,
                media_class=core.MediaPlayer.MediaClass.APP,
                media_content_type=core.MediaPlayer.MediaType.APPS,
                title="Media Sources",
                can_play=False,
                can_expand=True,
                children_media_class=core.MediaPlayer.MediaClass.APP,
                children=sorted(
                    (
                        core.BrowseMediaSource(
                            domain=source.domain,
                            identifier=None,
                            media_class=core.MediaPlayer.MediaClass.APP,
                            media_content_type=core.MediaPlayer.MediaType.APPS,
                            thumbnail=(
                                f"https://brands.home-assistant.io/_/{source.domain}/logo.png"
                            ),
                            title=source.name,
                            can_play=False,
                            can_expand=True,
                        )
                        for source in self.owner.items()
                    ),
                    key=lambda item: item.title,
                ),
            )
            return base

        return await self.async_media_source().async_browse_media(self)

    async def async_resolve(self) -> core.PlayMedia:
        """Resolve to playable item."""
        return await self.async_media_source().async_resolve_media(self)

    @core.callback
    def async_media_source(self) -> core.MediaSource:
        """Return media source that owns this item."""
        return typing.cast(core.MediaSource, self.owner.get_item(self.domain))

    @classmethod
    def from_uri(cls, owner: MediaSourceComponent, uri: str, target_media_player: str):
        """Create an item from a uri."""
        if not (match := core.Const.MEDIA_SOURCE_URI_SCHEME_REGEX.match(uri)):
            raise ValueError("Invalid media source URI")

        domain = match.group("domain")
        identifier = match.group("identifier")

        return cls(owner, domain, identifier, target_media_player)
