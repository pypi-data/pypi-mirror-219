"""
Google Assistant Integration  for Smart Home - The Next Generation.

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
class RequestData:
    """Hold data associated with a particular request."""

    def __init__(
        self,
        config: core.GoogleAssistant.AbstractConfig,
        user_id: str,
        source: str,
        request_id: str,
        devices: list[dict],
    ) -> None:
        """Initialize the request data."""
        self._config = config
        self._source = source
        self._request_id = request_id
        self._context = core.Context(user_id=user_id)
        self._devices = devices

    @property
    def config(self) -> core.GoogleAssistant.AbstractConfig:
        return self._config

    @property
    def context(self) -> core.Context:
        return self._context

    @property
    def devices(self) -> list[dict]:
        return self._devices

    @property
    def request_id(self) -> str:
        return self._request_id

    @property
    def source(self) -> str:
        return self._source

    @property
    def is_local_request(self):
        """Return if this is a local request."""
        return self.source == core.GoogleAssistant.SOURCE_LOCAL
