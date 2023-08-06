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


# pylint: disable=unused-variable
class UrlManager(abc.ABC):
    """Manage urls to be used on the frontend.

    This is abstracted into a class because
    some integrations add a remove these directly
    on hass.data
    """

    @abc.abstractmethod
    def add(self, url: str) -> None:
        """Add a url to the set."""

    @abc.abstractmethod
    def remove(self, url: str) -> None:
        """Remove a url from the set."""

    @property
    @abc.abstractmethod
    def urls(self) -> list[str]:
        """Get the list of managed urls."""
