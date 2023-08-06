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

import asyncio
import ssl

import yarl
from aiohttp import web


# pylint: disable=unused-variable
class SmartHomeControllerSite(web.BaseSite):
    """Smart Home - The Next Generation specific aiohttp Site.

    Vanilla TCPSite accepts only str as host. However, the underlying asyncio's
    create_server() implementation does take a list of strings to bind to multiple
    host IP's. To support multiple server_host entries (e.g. to enable dual-stack
    explicitly), we would like to pass an array of strings. Bring our own
    implementation inspired by TCPSite.

    Custom TCPSite can be dropped when https://github.com/aio-libs/aiohttp/pull/4894
    is merged.
    """

    __slots__ = ("_host", "_port", "_reuse_address", "_reuse_port", "_hosturl")

    def __init__(
        self,
        runner: web.BaseRunner,
        host: None | str | list[str],
        port: int,
        *,
        shutdown_timeout: float = 10.0,
        ssl_context: ssl.SSLContext = None,
        backlog: int = 128,
        reuse_address: bool = None,
        reuse_port: bool = None,
    ) -> None:
        """Initialize SmartHomeControllerTCPSite."""
        super().__init__(
            runner,
            shutdown_timeout=shutdown_timeout,
            ssl_context=ssl_context,
            backlog=backlog,
        )
        self._host = host
        self._port = port
        self._reuse_address = reuse_address
        self._reuse_port = reuse_port

    @property
    def name(self) -> str:
        """Return server URL."""
        scheme = "https" if self._ssl_context else "http"
        host = self._host[0] if isinstance(self._host, list) else "0.0.0.0"  # nosec
        return str(yarl.URL.build(scheme=scheme, host=host, port=self._port))

    async def start(self) -> None:
        """Start server."""
        await super().start()
        loop = asyncio.get_running_loop()
        server = self._runner.server
        assert server is not None
        self._server = await loop.create_server(
            server,
            self._host,
            self._port,
            ssl=self._ssl_context,
            backlog=self._backlog,
            reuse_address=self._reuse_address,
            reuse_port=self._reuse_port,
        )
