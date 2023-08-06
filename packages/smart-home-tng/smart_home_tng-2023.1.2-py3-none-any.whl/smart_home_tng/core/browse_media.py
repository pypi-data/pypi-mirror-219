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

import typing

from .const import Const
from .media_player import MediaPlayer

_BrowseMediaT = typing.TypeVar("_BrowseMediaT", bound="BrowseMedia")
_BrowseMediaSourceT = typing.TypeVar("_BrowseMediaSourceT", bound="BrowseMediaSource")


# pylint: disable=unused-variable
class BrowseMedia:
    """Represent a browsable media file."""

    def __init__(
        self,
        *,
        media_class: str,
        media_content_id: str,
        media_content_type: str,
        title: str,
        can_play: bool,
        can_expand: bool,
        children: list[_BrowseMediaT] = None,
        children_media_class: str = None,
        thumbnail: str = None,
        not_shown: int = 0,
    ) -> None:
        """Initialize browse media item."""
        self._media_class = media_class
        self._media_content_id = media_content_id
        self._media_content_type = media_content_type
        self._title = title
        self._can_play = can_play
        self._can_expand = can_expand
        self._children: list[BrowseMedia] = children
        self._children_media_class = children_media_class
        self._thumbnail = thumbnail
        self._not_shown = not_shown

    @property
    def media_class(self) -> str:
        return self._media_class

    @property
    def media_content_id(self) -> str:
        return self._media_content_id

    @property
    def media_content_type(self) -> str:
        return self._media_content_type

    @property
    def title(self) -> str:
        return self._title

    @property
    def can_play(self) -> bool:
        return self._can_play

    @property
    def children(self):
        if self._children is None:
            return None
        return iter(self._children)

    def add_child(self, child: _BrowseMediaSourceT) -> None:
        if child is None:
            return
        if self._children is None:
            self._children = []
        self._children.append(child)
        if len(self._children) > 1:
            # Sort children showing directories first, then by name
            self._children.sort(key=lambda child: (child.can_play, child.title))

    @property
    def children_media_class(self) -> str:
        return self._children_media_class

    @property
    def thumbnail(self) -> str:
        return self._thumbnail

    @property
    def not_shown(self) -> int:
        return self._not_shown

    @not_shown.setter
    def not_shown(self, value: int) -> None:
        if self._children is not None and value <= len(self._children):
            self._not_shown = value

    @property
    def can_expand(self) -> bool:
        return self._can_expand

    def as_dict(self, *, parent: bool = True) -> dict:
        """Convert Media class to browse media dictionary."""
        if self.children_media_class is None and self.children:
            self.calculate_children_class()

        response: dict[str, typing.Any] = {
            "title": self.title,
            "media_class": self.media_class,
            "media_content_type": self.media_content_type,
            "media_content_id": self.media_content_id,
            "children_media_class": self.children_media_class,
            "can_play": self.can_play,
            "can_expand": self.can_expand,
            "thumbnail": self.thumbnail,
        }

        if not parent:
            return response

        response["not_shown"] = self.not_shown

        if self._children:
            response["children"] = [
                child.as_dict(parent=False) for child in self.children
            ]
        else:
            response["children"] = []

        return response

    def calculate_children_class(self) -> None:
        """Count the children media classes and calculate the correct class."""
        self._children_media_class = MediaPlayer.MediaClass.DIRECTORY
        assert self._children is not None
        proposed_class = self._children[0].media_class
        if all(child.media_class == proposed_class for child in self.children):
            self._children_media_class = proposed_class

    def __repr__(self) -> str:
        """Return representation of browse media."""
        return f"<BrowseMedia {self.title} ({self.media_class})>"


# pylint: disable=unused-variable
class BrowseMediaSource(BrowseMedia):
    """Represent a browsable media file."""

    def __init__(self, *, domain: str, identifier: str, **kwargs: typing.Any) -> None:
        """Initialize media source browse media."""
        media_content_id = f"{Const.MEDIA_SOURCE_URI_SCHEME}{domain or ''}"
        if identifier:
            media_content_id += f"/{identifier}"

        super().__init__(media_content_id=media_content_id, **kwargs)

        self._domain = domain
        self._identifier = identifier

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def identifier(self) -> str:
        return self._identifier
