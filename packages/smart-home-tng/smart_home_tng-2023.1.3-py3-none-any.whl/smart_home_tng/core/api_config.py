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


class ApiConfig:  # pylint: disable=unused-variable
    """Configuration settings for API server."""

    def __init__(
        self,
        local_ip: str,
        host: str,
        port: int,
        use_ssl: bool,
    ) -> None:
        """Initialize a new API config object."""
        self._local_ip = local_ip
        self._host = host
        self._port = port
        self._use_ssl = use_ssl

    @property
    def local_ip(self) -> str:
        return self._local_ip

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def use_ssl(self) -> bool:
        return self._use_ssl
