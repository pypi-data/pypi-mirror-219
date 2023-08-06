"""
Frontend Component for Smart Home - The Next Generation.

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

from ... import core


# pylint: disable=unused-variable
class UrlManager(core.UrlManager):
    """Manage urls to be used on the frontend.

    This is abstracted into a class because
    some integrations add a remove these directly
    on hass.data
    """

    def __init__(self, urls: list[str]) -> None:
        """Init the url manager."""
        self._urls = frozenset(urls)

    def add(self, url: str) -> None:
        """Add a url to the set."""
        self._urls = frozenset([*self._urls, url])

    def remove(self, url: str) -> None:
        """Remove a url from the set."""
        self._urls = self._urls - {url}

    @property
    def urls(self) -> list[str]:
        return self._urls
