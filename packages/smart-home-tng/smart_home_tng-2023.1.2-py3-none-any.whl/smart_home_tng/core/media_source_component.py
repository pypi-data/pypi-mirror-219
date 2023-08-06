"""
Core components of Smart Home - The Next Generation.

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

import abc
import collections.abc

from .browse_media import BrowseMedia, BrowseMediaSource
from .play_media import PlayMedia
from .smart_home_controller_component import SmartHomeControllerComponent


# pylint: disable=unused-variable
class MediaSourceComponent(SmartHomeControllerComponent):
    """Required base class for Media Source Component."""

    @abc.abstractmethod
    async def async_browse_media(
        self,
        media_content_id: str,
        *,
        content_filter: collections.abc.Callable[[BrowseMedia], bool] = None,
    ) -> BrowseMediaSource:
        """Return media player browse media results."""

    @abc.abstractmethod
    async def async_resolve_media(
        self, media_content_id: str, target_media_player: str
    ) -> PlayMedia:
        """Get info to play media."""

    @abc.abstractmethod
    def is_media_source_id(self, media_content_id: str) -> bool:
        """Test if identifier is a media source."""

    @abc.abstractmethod
    def generate_media_source_id(self, domain: str, identifier: str) -> str:
        """Generate a media source ID."""
