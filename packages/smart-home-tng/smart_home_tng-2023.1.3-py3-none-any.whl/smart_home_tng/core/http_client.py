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
import collections.abc
import contextlib
import ssl
import sys
import types
import typing

import aiohttp
import aiohttp.web_exceptions as web_ex
import async_timeout
from aiohttp import web

from . import helpers
from .callback import callback
from .config_entry import ConfigEntry
from .const import Const
from .event import Event


_DATA_CONNECTOR: typing.Final = "aiohttp.connector"
_DATA_CONNECTOR_NOTVERIFY: typing.Final = "aiohttp.connector.notverify"
_DATA_CLIENTSESSION: typing.Final = "aiohttp.clientsession"
_DATA_CLIENTSESSION_NOTVERIFY: typing.Final = "aiohttp.clientsession.notverify"
_SERVER_SOFTWARE: typing.Final = (
    f"Smart Home - The Next Generation/{Const.__version__} "
    + f"aiohttp/{aiohttp.__version__} "
    + f"Python/{sys.version_info[0]}.{sys.version_info[1]}"
)

_WARN_CLOSE_MSG: typing.Final = (
    "closes the Smart Home - The Next Generation aiohttp session"
)

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class HttpClient:
    """Helper for aiohttp webclient stuff."""

    @staticmethod
    @callback
    def async_get_clientsession(
        shc: SmartHomeController, verify_ssl: bool = True
    ) -> aiohttp.ClientSession:
        """Return default aiohttp ClientSession.

        This method must be run in the event loop.
        """
        key = _DATA_CLIENTSESSION if verify_ssl else _DATA_CLIENTSESSION_NOTVERIFY

        if key not in shc.data:
            shc.data[key] = _async_create_clientsession(
                shc,
                verify_ssl,
                auto_cleanup_method=_async_register_default_clientsession_shutdown,
            )

        return typing.cast(aiohttp.ClientSession, shc.data[key])

    @staticmethod
    @callback
    def async_create_clientsession(
        shc: SmartHomeController,
        verify_ssl: bool = True,
        auto_cleanup: bool = True,
        **kwargs: typing.Any,
    ) -> aiohttp.ClientSession:
        """Create a new ClientSession with kwargs, i.e. for cookies.

        If auto_cleanup is False, you need to call detach() after the session
        returned is no longer used. Default is True, the session will be
        automatically detached on homeassistant_stop or when being created
        in config entry setup, the config entry is unloaded.

        This method must be run in the event loop.
        """
        auto_cleanup_method = None
        if auto_cleanup:
            auto_cleanup_method = _async_register_clientsession_shutdown

        clientsession = _async_create_clientsession(
            shc,
            verify_ssl,
            auto_cleanup_method=auto_cleanup_method,
            **kwargs,
        )

        return clientsession

    @staticmethod
    async def async_aiohttp_proxy_web(
        shc: SmartHomeController,
        request: web.BaseRequest,
        web_coro: collections.abc.Awaitable[aiohttp.ClientResponse],
        buffer_size: int = 102400,
        timeout: int = 10,
    ) -> web.StreamResponse:
        """Stream websession request to aiohttp web response."""
        try:
            async with async_timeout.timeout(timeout):
                req = await web_coro

        except asyncio.CancelledError:
            # The user cancelled the request
            return None

        except asyncio.TimeoutError as err:
            # Timeout trying to start the web request
            raise web_ex.HTTPGatewayTimeout() from err

        except aiohttp.ClientError as err:
            # Something went wrong with the connection
            raise web_ex.HTTPBadGateway() from err

        try:
            return await HttpClient.async_aiohttp_proxy_stream(
                shc,
                request,
                req.content,
                req.headers.get(aiohttp.hdrs.CONTENT_TYPE),
                buffer_size,
                timeout,
            )
        finally:
            req.close()

    @staticmethod
    async def async_aiohttp_proxy_stream(
        shc: SmartHomeController,
        request: web.BaseRequest,
        stream: aiohttp.StreamReader,
        content_type: str,
        buffer_size: int = 102400,
        timeout: int = 10,
    ) -> web.StreamResponse:
        """Stream a stream to aiohttp web response."""
        response = web.StreamResponse()
        if content_type is not None:
            response.content_type = content_type
        await response.prepare(request)

        # Suppressing something went wrong fetching data, closed connection
        with contextlib.suppress(asyncio.TimeoutError, aiohttp.ClientError):
            while shc.is_running:
                async with async_timeout.timeout(timeout):
                    data = await stream.read(buffer_size)

                if not data:
                    break
                await response.write(data)

        return response


@callback
def _async_register_clientsession_shutdown(
    shc: SmartHomeController, clientsession: aiohttp.ClientSession
) -> None:
    """Register ClientSession close on Home Assistant shutdown or config entry unload.

    This method must be run in the event loop.
    """

    @callback
    def _async_close_websession(*_: typing.Any) -> None:
        """Close websession."""
        clientsession.detach()

    unsub = shc.bus.async_listen_once(Const.EVENT_SHC_CLOSE, _async_close_websession)

    if not (config_entry := ConfigEntry.current_entry().get()):
        return

    config_entry.async_on_unload(unsub)
    config_entry.async_on_unload(_async_close_websession)


@callback
def _async_register_default_clientsession_shutdown(
    shc: SmartHomeController, clientsession: aiohttp.ClientSession
) -> None:
    """Register default ClientSession close on Home Assistant shutdown.

    This method must be run in the event loop.
    """

    @callback
    def _async_close_websession(_event: Event) -> None:
        """Close websession."""
        clientsession.detach()

    shc.bus.async_listen_once(Const.EVENT_SHC_CLOSE, _async_close_websession)


@callback
def _async_get_connector(
    shc: SmartHomeController, verify_ssl: bool = True
) -> aiohttp.BaseConnector:
    """Return the connector pool for aiohttp.

    This method must be run in the event loop.
    """
    key = _DATA_CONNECTOR if verify_ssl else _DATA_CONNECTOR_NOTVERIFY

    if key in shc.data:
        return typing.cast(aiohttp.BaseConnector, shc.data[key])

    if verify_ssl and shc.http:
        ssl_context: bool | ssl.SSLContext = shc.http.client_context()
    else:
        ssl_context = False

    connector = aiohttp.TCPConnector(enable_cleanup_closed=True, ssl=ssl_context)
    shc.data[key] = connector

    async def _async_close_connector(_event: Event) -> None:
        """Close connector pool."""
        await connector.close()

    shc.bus.async_listen_once(Const.EVENT_SHC_CLOSE, _async_close_connector)

    return connector


@callback
def _async_create_clientsession(
    shc: SmartHomeController,
    verify_ssl: bool = True,
    auto_cleanup_method: collections.abc.Callable[
        [SmartHomeController, aiohttp.ClientSession], None
    ] = None,
    **kwargs: typing.Any,
) -> aiohttp.ClientSession:
    """Create a new ClientSession with kwargs, i.e. for cookies."""
    clientsession = aiohttp.ClientSession(
        connector=_async_get_connector(shc, verify_ssl),
        **kwargs,
    )
    # Prevent packages accidentally overriding our default headers
    # It's important that we identify as Home Assistant
    # If a package requires a different user agent, override it by passing a headers
    # dictionary to the request method.
    # pylint: disable=protected-access
    clientsession._default_headers = types.MappingProxyType(
        {aiohttp.hdrs.USER_AGENT: _SERVER_SOFTWARE}
    )

    clientsession.close = helpers.warn_use(clientsession.close, _WARN_CLOSE_MSG)

    if auto_cleanup_method:
        auto_cleanup_method(shc, clientsession)

    return clientsession
