"""
Google Cast Integration for Smart Home - The Next Generation.

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

import pychromecast as google

from ... import core


# pylint: disable=unused-variable
class CastProtocol(core.Protocol):
    """Define the format of cast platforms."""

    @abc.abstractmethod
    async def async_get_media_browser_root_object(
        self, cast_type: str
    ) -> list[core.BrowseMedia]:
        """Create a list of root objects for media browsing."""

    @abc.abstractmethod
    async def async_browse_media(
        self,
        media_content_type: str,
        media_content_id: str,
        cast_type: str,
    ) -> core.BrowseMedia:
        """Browse media.

        Return a BrowseMedia object or None if the media does not belong to this platform.
        """

    @abc.abstractmethod
    async def async_play_media(
        self,
        cast_entity_id: str,
        chromecast: google.Chromecast,
        media_type: str,
        media_id: str,
    ) -> bool:
        """Play media.

        Return True if the media is played by the platform, False if not.
        """
