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

import collections.abc
import contextlib
import contextvars
import datetime
import ipaddress
import logging
import os
import pathlib
import re
import secrets
import socket
import ssl
import tempfile
import typing
from urllib import parse

import aiohttp
import aiohttp_cors
import certifi
import jwt
import voluptuous as vol
import yaml
import yarl
from aiohttp import hdrs, web
from aiohttp import web_urldispatcher as web_url
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import oid

from .. import auth
from . import helpers
from .caching_static_resource import CachingStaticResource
from .callback import callback
from .config_validation import ConfigValidation as cv
from .const import Const
from .ip_ban import IpBan
from .no_url_available_error import NoURLAvailableError
from .persistent_notification_component import PersistentNotificationComponent
from .smart_home_controller_component import SmartHomeControllerComponent
from .smart_home_controller_error import SmartHomeControllerError
from .smart_home_controller_site import SmartHomeControllerSite
from .smart_home_controller_view import SmartHomeControllerView
from .store import Store
from .web_socket import WebSocket
from .yaml_loader import YamlLoader

_ALLOWED_CORS_HEADERS: typing.Final[list[str]] = [
    hdrs.ORIGIN,
    hdrs.ACCEPT,
    Const.HTTP_HEADER_X_REQUESTED_WITH,
    hdrs.CONTENT_TYPE,
    hdrs.AUTHORIZATION,
]
_VALID_CORS_TYPES: typing.Final = (
    web_url.Resource,
    web_url.ResourceRoute,
    web_url.StaticResource,
)

_current_request: contextvars.ContextVar[web.Request] = contextvars.ContextVar(
    "current_request", default=None
)
_MAX_CLIENT_SIZE: typing.Final = 1024**2 * 16
_SECURITY_FILTERS: typing.Final = re.compile(
    r"(?:"
    # Common exploits
    + r"proc/self/environ" r"|(<|%3C).*script.*(>|%3E)"
    # File Injections
    + r"|(\.\.//?)+"  # ../../anywhere
    + r"|[a-zA-Z0-9_]=/([a-z0-9_.]//?)+"  # .html?v=/.//test
    # SQL Injections
    + r"|union.*select.*\(" r"|union.*all.*select.*" r"|concat.*\(" r")",
    flags=re.IGNORECASE,
)
_SCHEMA_IP_BAN_ENTRY: typing.Final = vol.Schema(
    {vol.Optional("banned_at"): vol.Any(None, cv.datetime)}
)

_LOGGER: typing.Final = logging.getLogger(__name__)

_DATA_SIGN_SECRET: typing.Final = "http.auth.sign_secret"
_SIGN_QUERY_PARAM: typing.Final = "authSig"

_STORAGE_VERSION = 1
_STORAGE_KEY = "http.auth"
_CONTENT_USER_NAME = "Smart Home Controller Content"

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class SmartHomeControllerHTTP:
    """HTTP server for Smart Home - The Next Generation."""

    def __init__(
        self,
        shc: SmartHomeController,
        ssl_certificate: str,
        ssl_peer_certificate: str,
        ssl_key: str,
        server_host: list[str],
        server_port: int,
        trusted_proxies: list[ipaddress.IPv4Network | ipaddress.IPv6Network],
        ssl_profile: str,
    ) -> None:
        """Initialize the Smart Home Controller server."""
        self._app = web.Application(middlewares=[], client_max_size=_MAX_CLIENT_SIZE)
        self._shc = shc
        self._ssl_certificate = ssl_certificate
        self._ssl_peer_certificate = ssl_peer_certificate
        self._ssl_key = ssl_key
        self._server_host = server_host
        self._server_port = server_port
        self._trusted_proxies = trusted_proxies
        self._ssl_profile = ssl_profile
        self._runner: web.AppRunner = None
        self._site: SmartHomeControllerSite = None
        self._context: ssl.SSLContext = None

    @property
    def current_request(self) -> contextvars.ContextVar[web.Request]:
        return _current_request

    @property
    def server_port(self) -> int:
        return self._server_port

    async def async_initialize(
        self,
        *,
        cors_origins: list[str],
        use_x_forwarded_for: bool,
        login_threshold: int,
        is_ban_enabled: bool,
    ) -> None:
        """Initialize the server."""
        self._app[Const.KEY_SHC] = self._shc

        # Order matters, security filters middleware needs to go first,
        # forwarded middleware needs to go second.
        self.setup_security_filter()

        self.async_setup_forwarded(use_x_forwarded_for, self._trusted_proxies)

        self.setup_request_context(_current_request)

        if is_ban_enabled:
            self.setup_bans(login_threshold)

        await self.async_setup_auth()

        self.setup_cors(cors_origins)

        if self._ssl_certificate:
            self._context = await self._shc.async_add_executor_job(
                self._create_ssl_context
            )

    @callback
    def async_user_not_allowed_do_auth(
        self, user: auth.User, request: web.Request = None
    ) -> str:
        """Validate that user is not allowed to do auth things."""
        if not user.is_active:
            return "User is not active"

        if not user.local_only:
            return None

        # User is marked as local only, check if they are allowed to do auth
        if request is None:
            request = _current_request.get()

        if not request:
            return "No request available to validate local access"

        try:
            remote = ipaddress.ip_address(request.remote)
        except ValueError:
            return "Invalid remote IP"

        if helpers.is_local(remote):
            return None

        return "User cannot authenticate remotely"

    @callback
    def async_sign_path(
        self,
        path: str,
        expiration: datetime.timedelta,
        *,
        refresh_token_id: str = None,
    ) -> str:
        """Sign a path for temporary access without auth header."""
        if (secret := self._shc.data.get(_DATA_SIGN_SECRET)) is None:
            secret = self._shc.data[_DATA_SIGN_SECRET] = secrets.token_hex()

        if refresh_token_id is None:
            comp = self._shc.components.websocket_api
            connection = None
            if isinstance(comp, WebSocket.Component):
                active_conn = comp.active_connection
                if isinstance(active_conn, contextvars.ContextVar):
                    connection = active_conn.get()
                elif isinstance(active_conn, WebSocket.Connection):
                    connection = active_conn
            if connection:
                refresh_token_id = connection.refresh_token_id
            elif (
                request := _current_request.get()
            ) and Const.KEY_SHC_REFRESH_TOKEN_ID in request:
                refresh_token_id = request[Const.KEY_SHC_REFRESH_TOKEN_ID]
            else:
                refresh_token_id = self._shc.data[_STORAGE_KEY]

        now = helpers.utcnow()
        encoded = jwt.encode(
            {
                "iss": refresh_token_id,
                "path": parse.unquote(path),
                "iat": now,
                "exp": now + expiration,
            },
            secret,
            algorithm="HS256",
        )
        return f"{path}?{_SIGN_QUERY_PARAM}={encoded}"

    async def async_setup_auth(self) -> None:
        """Create auth middleware for the app."""

        store = Store[dict[str, typing.Any]](self._shc, _STORAGE_VERSION, _STORAGE_KEY)
        if (data := await store.async_load()) is None or not isinstance(data, dict):
            data = {}

        refresh_token = None
        if "content_user" in data:
            user = await self._shc.auth.async_get_user(data["content_user"])
            if user and user.refresh_tokens:
                refresh_token = list(user.refresh_tokens.values())[0]

        if refresh_token is None:
            user = await self._shc.auth.async_create_system_user(
                _CONTENT_USER_NAME, group_ids=[auth.Const.GROUP_ID_READ_ONLY]
            )
            refresh_token = await self._shc.auth.async_create_refresh_token(user)
            data["content_user"] = user.id
            await store.async_save(data)

        self._shc.data[_STORAGE_KEY] = refresh_token.id

        async def async_validate_auth_header(request: web.Request) -> bool:
            """
            Test authorization header against access token.

            Basic auth_type is legacy code, should be removed with api_password.
            """
            try:
                auth_type, auth_val = request.headers.get(hdrs.AUTHORIZATION, "").split(
                    " ", 1
                )
            except ValueError:
                # If no space in authorization header
                return False

            if auth_type != "Bearer":
                return False

            refresh_token = await self._shc.auth.async_validate_access_token(auth_val)

            if refresh_token is None:
                return False

            if self.async_user_not_allowed_do_auth(refresh_token.user, request):
                return False

            request[Const.KEY_SHC_USER] = refresh_token.user
            request[Const.KEY_SHC_REFRESH_TOKEN_ID] = refresh_token.id
            return True

        async def async_validate_signed_request(request: web.Request) -> bool:
            """Validate a signed request."""
            if (secret := self._shc.data.get(_DATA_SIGN_SECRET)) is None:
                return False

            if (signature := request.query.get(_SIGN_QUERY_PARAM)) is None:
                return False

            try:
                claims = jwt.decode(
                    signature,
                    secret,
                    algorithms=["HS256"],
                    options={"verify_iss": False},
                )
            except jwt.InvalidTokenError:
                return False

            if claims["path"] != request.path:
                return False

            refresh_token = await self._shc.auth.async_get_refresh_token(claims["iss"])

            if refresh_token is None:
                return False

            request[Const.KEY_SHC_USER] = refresh_token.user
            request[Const.KEY_SHC_REFRESH_TOKEN_ID] = refresh_token.id
            return True

        @web.middleware
        async def auth_middleware(
            request: web.Request,
            handler: collections.abc.Callable[
                [web.Request], collections.abc.Awaitable[web.StreamResponse]
            ],
        ) -> web.StreamResponse:
            """Authenticate as middleware."""
            authenticated = False

            if (
                hdrs.AUTHORIZATION in request.headers
                and await async_validate_auth_header(request)
            ):
                authenticated = True
                auth_type = "bearer token"

            # We first start with a string check to avoid parsing query params
            # for every request.
            elif (
                request.method == "GET"
                and _SIGN_QUERY_PARAM in request.query
                and await async_validate_signed_request(request)
            ):
                authenticated = True
                auth_type = "signed request"

            if authenticated:
                _LOGGER.debug(
                    f"Authenticated {request.remote} for {request.path} using {auth_type}",
                )

            request[Const.KEY_AUTHENTICATED] = authenticated
            return await handler(request)

        self._app.middlewares.append(auth_middleware)

    @callback
    def setup_cors(self, origins: list[str]) -> None:
        """Set up CORS."""
        # This import should remain here. That way the HTTP integration can always
        # be imported by other integrations without it's requirements being installed.
        # pylint: disable=import-outside-toplevel
        cors = aiohttp_cors.setup(
            self._app,
            defaults={
                host: aiohttp_cors.ResourceOptions(
                    allow_headers=_ALLOWED_CORS_HEADERS, allow_methods="*"
                )
                for host in origins
            },
        )

        cors_added = set()

        def _allow_cors(
            route: web_url.AbstractRoute | web_url.AbstractResource,
            config: dict[str, aiohttp_cors.ResourceOptions] = None,
        ) -> None:
            """Allow CORS on a route."""
            if isinstance(route, web_url.AbstractRoute):
                path = route.resource
            else:
                path = route

            if not isinstance(path, _VALID_CORS_TYPES):
                return

            path_str = path.canonical

            if path_str.startswith("/api/hassio_ingress/"):
                return

            if path_str in cors_added:
                return

            cors.add(route, config)
            cors_added.add(path_str)

        self._app["allow_all_cors"] = lambda route: _allow_cors(
            route,
            {
                "*": aiohttp_cors.ResourceOptions(
                    allow_headers=_ALLOWED_CORS_HEADERS, allow_methods="*"
                )
            },
        )

        if origins:
            self._app["allow_configured_cors"] = _allow_cors
        else:
            self._app["allow_configured_cors"] = lambda _: None

    @callback
    def setup_security_filter(self) -> None:
        """Create security filter middleware for the app."""

        @aiohttp.web_middlewares.middleware
        async def security_filter_middleware(
            request: web.Request,
            handler: typing.Callable[
                [web.Request],
                collections.abc.Awaitable[web.StreamResponse],
            ],
        ) -> web.StreamResponse:
            """Process request and tblock commonly known exploit attempts."""
            if _SECURITY_FILTERS.search(request.path):
                _LOGGER.warning(
                    f"Filtered a potential harmful request to: {request.raw_path}"
                )
                raise web.HTTPBadRequest

            if _SECURITY_FILTERS.search(request.query_string):
                _LOGGER.warning(
                    "Filtered a request with a potential harmful query string: "
                    + f"{request.raw_path}"
                )
                raise web.HTTPBadRequest

            return await handler(request)

        self._app.middlewares.append(security_filter_middleware)

    @callback
    def async_setup_forwarded(
        self,
        use_x_forwarded_for: bool,
        trusted_proxies: list[ipaddress.IPv4Network | ipaddress.IPv6Network],
    ) -> None:
        """Create forwarded middleware for the app.

        Process IP addresses, proto and host information in the forwarded for headers.

        `X-Forwarded-For: <client>, <proxy1>, <proxy2>`
        e.g., `X-Forwarded-For: 203.0.113.195, 70.41.3.18, 150.172.238.178`

        We go through the list from the right side, and skip all entries that are in our
        trusted proxies list. The first non-trusted IP is used as the client IP. If all
        items in the X-Forwarded-For are trusted, including the most left item (client),
        the most left item is used. In the latter case, the client connection originated
        from an IP that is also listed as a trusted proxy IP or network.

        `X-Forwarded-Proto: <client>, <proxy1>, <proxy2>`
        e.g., `X-Forwarded-Proto: https, http, http`
        OR `X-Forwarded-Proto: https` (one entry, even with multiple proxies)

        The X-Forwarded-Proto is determined based on the corresponding entry of the
        X-Forwarded-For header that is used/chosen as the client IP. However,
        some proxies, for example, Kubernetes NGINX ingress, only retain one element
        in the X-Forwarded-Proto header. In that case, we'll just use what we have.

        `X-Forwarded-Host: <host>`
        e.g., `X-Forwarded-Host: example.com`

        If the previous headers are processed successfully, and the X-Forwarded-Host is
        present, it will be used.

        Additionally:
        - If no X-Forwarded-For header is found, the processing of all headers is skipped.
        - Throw HTTP 400 status when untrusted connected peer provides
            X-Forwarded-For headers.
        - If multiple instances of X-Forwarded-For, X-Forwarded-Proto or
            X-Forwarded-Host are found, an HTTP 400 status code is thrown.
        - If malformed or invalid (IP) data in X-Forwarded-For header is found,
            an HTTP 400 status code is thrown.
        - The connected client peer on the socket of the incoming connection,
            must be trusted for any processing to take place.
        - If the number of elements in X-Forwarded-Proto does not equal 1 or
            is equal to the number of elements in X-Forwarded-For, an HTTP 400
            status code is thrown.
        - If an empty X-Forwarded-Host is provided, an HTTP 400 status code is thrown.
        - If an empty X-Forwarded-Proto is provided, or an empty element in the list,
            an HTTP 400 status code is thrown.
        """

        @aiohttp.web_middlewares.middleware
        async def forwarded_middleware(
            request: web.Request,
            handler: typing.Callable[
                [web.Request],
                collections.abc.Awaitable[web.StreamResponse],
            ],
        ) -> web.StreamResponse:
            """Process forwarded data by a reverse proxy."""
            # Handle X-Forwarded-For
            forwarded_for_headers: list[str] = request.headers.getall(
                aiohttp.hdrs.X_FORWARDED_FOR, []
            )
            if not forwarded_for_headers:
                # No forwarding headers, continue as normal
                return await handler(request)

            # Get connected IP
            if (
                request.transport is None
                or request.transport.get_extra_info("peername") is None
            ):
                # Connected IP isn't retrieveable from the request transport, continue
                return await handler(request)

            connected_ip = ipaddress.ip_address(
                request.transport.get_extra_info("peername")[0]
            )

            # We have X-Forwarded-For, but config does not agree
            if not use_x_forwarded_for:
                _LOGGER.error(
                    f"A request from a reverse proxy was received from {connected_ip}, "
                    + "but your HTTP integration is not set-up for reverse proxies"
                )
                raise web.HTTPBadRequest

            # Ensure the IP of the connected peer is trusted
            if not any(
                connected_ip in trusted_proxy for trusted_proxy in trusted_proxies
            ):
                _LOGGER.error(
                    f"Received X-Forwarded-For header from an untrusted proxy {connected_ip}",
                )
                raise web.HTTPBadRequest

            # Multiple X-Forwarded-For headers
            if len(forwarded_for_headers) > 1:
                _LOGGER.error(
                    f"Too many headers for X-Forwarded-For: {forwarded_for_headers}"
                )
                raise web.HTTPBadRequest

            # Process X-Forwarded-For from the right side (by reversing the list)
            forwarded_for_split = list(reversed(forwarded_for_headers[0].split(",")))
            try:
                forwarded_for = [
                    ipaddress.ip_address(addr.strip()) for addr in forwarded_for_split
                ]
            except ValueError as err:
                _LOGGER.error(
                    f"Invalid IP address in X-Forwarded-For: {forwarded_for_headers[0]}"
                )
                raise web.HTTPBadRequest from err

            overrides: dict[str, str] = {}

            # Find the last trusted index in the X-Forwarded-For list
            forwarded_for_index = 0
            for forwarded_ip in forwarded_for:
                if any(
                    forwarded_ip in trusted_proxy for trusted_proxy in trusted_proxies
                ):
                    forwarded_for_index += 1
                    continue
                overrides["remote"] = str(forwarded_ip)
                break
            else:
                # If all the IP addresses are from trusted networks, take the left-most.
                forwarded_for_index = -1
                overrides["remote"] = str(forwarded_for[-1])

            # Handle X-Forwarded-Proto
            forwarded_proto_headers: list[str] = request.headers.getall(
                aiohttp.hdrs.X_FORWARDED_PROTO, []
            )
            if forwarded_proto_headers:
                if len(forwarded_proto_headers) > 1:
                    _LOGGER.error(
                        f"Too many headers for X-Forward-Proto: {forwarded_proto_headers}"
                    )
                    raise web.HTTPBadRequest

                forwarded_proto_split = list(
                    reversed(forwarded_proto_headers[0].split(","))
                )
                forwarded_proto = [proto.strip() for proto in forwarded_proto_split]

                # Catch empty values
                if "" in forwarded_proto:
                    _LOGGER.error(
                        "Empty item received in X-Forward-Proto header: "
                        + f"{forwarded_proto_headers[0]}"
                    )
                    raise web.HTTPBadRequest

                # The X-Forwarded-Proto contains either one element, or the equals number
                # of elements as X-Forwarded-For
                if len(forwarded_proto) not in (1, len(forwarded_for)):
                    _LOGGER.error(
                        "Incorrect number of elements in X-Forward-Proto. "
                        + f"Expected 1 or {len(forwarded_for)}, got {len(forwarded_proto)}: "
                        + f"{forwarded_proto_headers[0]}"
                    )
                    raise web.HTTPBadRequest

                # Ideally this should take the scheme corresponding to the entry
                # in X-Forwarded-For that was chosen, but some proxies only retain
                # one element. In that case, use what we have.
                overrides["scheme"] = forwarded_proto[-1]
                if len(forwarded_proto) != 1:
                    overrides["scheme"] = forwarded_proto[forwarded_for_index]

            # Handle X-Forwarded-Host
            forwarded_host_headers: list[str] = request.headers.getall(
                aiohttp.hdrs.X_FORWARDED_HOST, []
            )
            if forwarded_host_headers:
                # Multiple X-Forwarded-Host headers
                if len(forwarded_host_headers) > 1:
                    _LOGGER.error(
                        f"Too many headers for X-Forwarded-Host: {forwarded_host_headers}"
                    )
                    raise web.HTTPBadRequest

                forwarded_host = forwarded_host_headers[0].strip()
                if not forwarded_host:
                    _LOGGER.error("Empty value received in X-Forward-Host header")
                    raise web.HTTPBadRequest

                overrides["host"] = forwarded_host

            # Done, create a new request based on gathered data.
            request = request.clone(**overrides)  # type: ignore[arg-type]
            return await handler(request)

        self._app.middlewares.append(forwarded_middleware)

    @callback
    def setup_request_context(
        self, context: contextvars.ContextVar[web.Request]
    ) -> None:
        """Create request context middleware for the app."""

        @aiohttp.web_middlewares.middleware
        async def request_context_middleware(
            request: web.Request,
            handler: typing.Callable[
                [web.Request],
                collections.abc.Awaitable[web.StreamResponse],
            ],
        ) -> web.StreamResponse:
            """Request context middleware."""
            context.set(request)
            return await handler(request)

        self._app.middlewares.append(request_context_middleware)

    @callback
    def setup_bans(self, login_threshold: int) -> None:
        """Create IP Ban middleware for the app."""
        self._app.middlewares.append(self.ban_middleware)
        self._app[Const.KEY_FAILED_LOGIN_ATTEMPTS] = collections.defaultdict(int)
        self._app[Const.KEY_LOGIN_THRESHOLD] = login_threshold

        async def ban_startup(_app: web.Application) -> None:
            """Initialize bans when app starts up."""
            self._app[Const.KEY_BANNED_IPS] = await self.async_load_ip_bans_config()

        self._app.on_startup.append(ban_startup)

    @aiohttp.web_middlewares.middleware
    async def ban_middleware(
        self,
        request: web.Request,
        handler: typing.Callable[
            [web.Request], collections.abc.Awaitable[web.StreamResponse]
        ],
    ) -> web.StreamResponse:
        """IP Ban middleware."""
        if Const.KEY_BANNED_IPS not in request.app:
            _LOGGER.error("IP Ban middleware loaded but banned IPs not loaded")
            return await handler(request)

        # Verify if IP is not banned
        ip_address_ = ipaddress.ip_address(request.remote)
        is_banned = any(
            ip_ban.ip_address == ip_address_
            for ip_ban in request.app[Const.KEY_BANNED_IPS]
        )

        if is_banned:
            raise web.HTTPForbidden()

        try:
            return await handler(request)
        except web.HTTPUnauthorized:
            await self.process_wrong_login(request)
            raise

    async def async_load_ip_bans_config(self) -> list[IpBan]:
        """Load list of banned IPs from config file."""
        ip_list: list[IpBan] = []
        path = self._shc.config.path(Const.IP_BANS_FILE)

        if not pathlib.Path(path).is_file():
            return ip_list

        try:
            list_ = await self._shc.async_add_executor_job(YamlLoader.load_yaml, path)
        except FileNotFoundError:
            return ip_list
        except SmartHomeControllerError as err:
            _LOGGER.error(f"Unable to load {path}: {err}")
            return ip_list

        for ip_ban, ip_info in list_.items():
            try:
                ip_info = _SCHEMA_IP_BAN_ENTRY(ip_info)
                ip_list.append(IpBan(ip_ban, ip_info["banned_at"]))
            except vol.Invalid as err:
                _LOGGER.error(f"Failed to load IP ban {ip_info}: {err}")
                continue

        return ip_list

    async def process_wrong_login(self, request: web.Request) -> None:
        """Process a wrong login attempt.

        Increase failed login attempts counter for remote IP address.
        Add ip ban entry if failed login attempts exceeds threshold.
        """

        remote_addr = ipaddress.ip_address(request.remote)
        remote_host = request.remote
        with contextlib.suppress(socket.herror):
            remote_host, _, _ = await self._shc.async_add_executor_job(
                socket.gethostbyaddr, request.remote
            )

        base_msg = (
            "Login attempt or request with invalid authentication from "
            + f"{remote_host} ({remote_addr})."
        )

        # The user-agent is unsanitized input so we only include it in the log
        user_agent = request.headers.get("user-agent")
        log_msg = f"{base_msg} ({user_agent})"

        notification_msg = f"{base_msg} See the log for details."

        _LOGGER.warning(log_msg)

        comp = SmartHomeControllerComponent.get_component(
            Const.PERSISTENT_NOTIFICATION_COMPONENT_NAME
        )
        if isinstance(comp, PersistentNotificationComponent):
            comp.async_create(
                notification_msg, "Login attempt failed", Const.NOTIFICATION_ID_LOGIN
            )

        # Check if ban middleware is loaded
        if (
            Const.KEY_BANNED_IPS not in request.app
            or request.app[Const.KEY_LOGIN_THRESHOLD] < 1
        ):
            return

        request.app[Const.KEY_FAILED_LOGIN_ATTEMPTS][remote_addr] += 1

        if (
            request.app[Const.KEY_FAILED_LOGIN_ATTEMPTS][remote_addr]
            >= request.app[Const.KEY_LOGIN_THRESHOLD]
        ):
            new_ban = IpBan(remote_addr)
            request.app[Const.KEY_BANNED_IPS].append(new_ban)

            await self._shc.async_add_executor_job(self.update_ip_bans_config, new_ban)

            _LOGGER.warning(f"Banned IP {remote_addr} for too many login attempts")

            comp = SmartHomeControllerComponent.get_component(
                Const.PERSISTENT_NOTIFICATION_COMPONENT_NAME
            )
            if isinstance(comp, PersistentNotificationComponent):
                comp.async_create(
                    f"Too many login attempts from {remote_addr}",
                    "Banning IP address",
                    Const.NOTIFICATION_ID_BAN,
                )

    def update_ip_bans_config(self, ip_ban: IpBan) -> None:
        """Update config file with new banned IP address."""
        path = self._shc.config.path(Const.IP_BANS_FILE)
        with open(path, "a", encoding="utf8") as out:
            ip_ = {
                str(ip_ban.ip_address): {
                    Const.ATTR_BANNED_AT: ip_ban.banned_at.isoformat()
                }
            }
            out.write("\n")
            out.write(yaml.dump(ip_))

    @staticmethod
    async def process_success_login(request: web.Request) -> None:
        """Process a success login attempt.

        Reset failed login attempts counter for remote IP address.
        No release IP address from banned list function, it can only be done by
        manual modify ip bans config file.
        """
        remote_addr = ipaddress.ip_address(request.remote)  # type: ignore[arg-type]

        # Check if ban middleware is loaded
        if (
            Const.KEY_BANNED_IPS not in request.app
            or request.app[Const.KEY_LOGIN_THRESHOLD] < 1
        ):
            return

        if (
            remote_addr in request.app[Const.KEY_FAILED_LOGIN_ATTEMPTS]
            and request.app[Const.KEY_FAILED_LOGIN_ATTEMPTS][remote_addr] > 0
        ):
            _LOGGER.debug(
                f"Login success, reset failed login attempts counter from {remote_addr}"
            )
            request.app[Const.KEY_FAILED_LOGIN_ATTEMPTS].pop(remote_addr)

    def register_view(
        self, view: SmartHomeControllerView | type[SmartHomeControllerView]
    ) -> None:
        """Register a view with the WSGI server.

        The view argument must be a class that inherits from NextGenerationView.
        It is optional to instantiate it before registering; this method will
        handle it either way.
        """
        if isinstance(view, type):
            # Instantiate the view, if needed
            view = view()

        if not hasattr(view, "url"):
            class_name = view.__class__.__name__
            raise AttributeError(f'{class_name} missing required attribute "url"')

        if not hasattr(view, "name"):
            class_name = view.__class__.__name__
            raise AttributeError(f'{class_name} missing required attribute "name"')

        view.register(self._app, self._app.router)

    def register_redirect(
        self,
        redirect_url: str,
        redirect_to: aiohttp.typedefs.StrOrURL,
        *,
        redirect_exc: type[web.HTTPRedirection] = web.HTTPMovedPermanently,
    ) -> None:
        """Register a redirect with the server.

        If given this must be either a string or callable. In case of a
        callable it's called with the url adapter that triggered the match and
        the values of the URL as keyword arguments and has to return the target
        for the redirect, otherwise it has to be a string with placeholders in
        rule syntax.
        """

        async def redirect(_request: web.Request) -> web.StreamResponse:
            """Redirect to location."""
            # Should be instance of aiohttp.web_exceptions._HTTPMove.
            raise redirect_exc(redirect_to)  # type: ignore[arg-type,misc]

        self._app["allow_configured_cors"](
            self._app.router.add_route("GET", redirect_url, redirect)
        )

    def register_static_path(
        self, url_path: str, path: str, cache_headers: bool = True
    ) -> None:
        """Register a folder or file to serve as a static path."""
        if os.path.isdir(path):
            if cache_headers:
                resource: CachingStaticResource | web.StaticResource = (
                    CachingStaticResource(url_path, path)
                )
            else:
                resource = web.StaticResource(url_path, path)
            self._app.router.register_resource(resource)
            self._app["allow_configured_cors"](resource)
            return

        async def serve_file(_request: web.Request) -> web.FileResponse:
            """Serve file from disk."""
            if cache_headers:
                return web.FileResponse(path, headers=Const.CACHE_HEADERS)
            return web.FileResponse(path)

        self._app["allow_configured_cors"](
            self._app.router.add_route("GET", url_path, serve_file)
        )

    def register_resource(self, resource: web.AbstractResource):
        self._app.router.register_resource(resource)

    def _create_ssl_context(self) -> ssl.SSLContext:
        context: ssl.SSLContext = None
        assert self._ssl_certificate is not None
        try:
            if self._ssl_profile == Const.SSL_INTERMEDIATE:
                context = self._server_context_intermediate()
            else:
                context = self._server_context_modern()
            context.load_cert_chain(self._ssl_certificate, self._ssl_key)
        except OSError as error:
            if not self._shc.in_safe_mode:
                raise SmartHomeControllerError(
                    f"Could not use SSL certificate from {self._ssl_certificate}: {error}"
                ) from error
            _LOGGER.error(
                f"Could not read SSL certificate from {self._ssl_certificate}: {error}"
            )
            try:
                context = self._create_emergency_ssl_context()
            except OSError as error2:
                _LOGGER.error(
                    f"Could not create an emergency self signed ssl certificate: {error2}"
                )
                context = None
            else:
                _LOGGER.critical(
                    "Home Assistant is running in safe mode with an emergency "
                    + "self signed ssl certificate because the configured SSL "
                    + "certificate was not usable."
                )
                return context

        if self._ssl_peer_certificate:
            if context is None:
                raise SmartHomeControllerError(
                    "Failed to create ssl context, no fallback available because a peer "
                    + "certificate is required."
                )

            context.verify_mode = ssl.CERT_REQUIRED
            context.load_verify_locations(self._ssl_peer_certificate)

        return context

    def _create_emergency_ssl_context(self) -> ssl.SSLContext:
        """Create an emergency ssl certificate so we can still startup."""
        context = self._server_context_modern()
        host: str
        try:
            host = typing.cast(
                str, yarl.URL(self._shc.get_url(prefer_external=True)).host
            )
        except NoURLAvailableError:
            host = "smart_home_tng.local"
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        subject = issuer = x509.Name(
            [
                x509.NameAttribute(
                    oid.NameOID.ORGANIZATION_NAME,
                    "Smart Home - The Next Generation Emergency Certificate",
                ),
                x509.NameAttribute(oid.NameOID.COMMON_NAME, host),
            ]
        )
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=30))
            .add_extension(
                x509.SubjectAlternativeName([x509.DNSName(host)]),
                critical=False,
            )
            .sign(key, hashes.SHA256())
        )
        with tempfile.NamedTemporaryFile() as cert_pem, tempfile.NamedTemporaryFile() as key_pem:
            cert_pem.write(cert.public_bytes(serialization.Encoding.PEM))
            key_pem.write(
                key.private_bytes(
                    serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
            cert_pem.flush()
            key_pem.flush()
            context.load_cert_chain(cert_pem.name, key_pem.name)
        return context

    @staticmethod
    def client_context() -> ssl.SSLContext:
        """Return an SSL context for making requests."""

        # Reuse environment variable definition from requests, since it's already a requirement
        # If the environment variable has no value, fall back to using certs from certifi package
        cafile = os.environ.get("REQUESTS_CA_BUNDLE", certifi.where())

        context = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH, cafile=cafile
        )
        return context

    @staticmethod
    def _server_context_modern() -> ssl.SSLContext:
        """Return an SSL context following the Mozilla recommendations.

        TLS configuration follows the best-practice guidelines specified here:
        https://wiki.mozilla.org/Security/Server_Side_TLS
        Modern guidelines are followed.
        """
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)

        context.options |= (
            ssl.OP_NO_SSLv2
            | ssl.OP_NO_SSLv3
            | ssl.OP_NO_TLSv1
            | ssl.OP_NO_TLSv1_1
            | ssl.OP_CIPHER_SERVER_PREFERENCE
        )
        if hasattr(ssl, "OP_NO_COMPRESSION"):
            context.options |= ssl.OP_NO_COMPRESSION

        context.set_ciphers(
            "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:"
            + "ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:"
            + "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:"
            + "ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:"
            + "ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256"
        )

        return context

    @staticmethod
    def _server_context_intermediate() -> ssl.SSLContext:
        """Return an SSL context following the Mozilla recommendations.

        TLS configuration follows the best-practice guidelines specified here:
        https://wiki.mozilla.org/Security/Server_Side_TLS
        Intermediate guidelines are followed.
        """
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)

        context.options |= (
            ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_CIPHER_SERVER_PREFERENCE
        )
        if hasattr(ssl, "OP_NO_COMPRESSION"):
            context.options |= ssl.OP_NO_COMPRESSION

        context.set_ciphers(
            "ECDHE-ECDSA-CHACHA20-POLY1305:"
            + "ECDHE-RSA-CHACHA20-POLY1305:"
            + "ECDHE-ECDSA-AES128-GCM-SHA256:"
            + "ECDHE-RSA-AES128-GCM-SHA256:"
            + "ECDHE-ECDSA-AES256-GCM-SHA384:"
            + "ECDHE-RSA-AES256-GCM-SHA384:"
            + "DHE-RSA-AES128-GCM-SHA256:"
            + "DHE-RSA-AES256-GCM-SHA384:"
            + "ECDHE-ECDSA-AES128-SHA256:"
            + "ECDHE-RSA-AES128-SHA256:"
            + "ECDHE-ECDSA-AES128-SHA:"
            + "ECDHE-RSA-AES256-SHA384:"
            + "ECDHE-RSA-AES128-SHA:"
            + "ECDHE-ECDSA-AES256-SHA384:"
            + "ECDHE-ECDSA-AES256-SHA:"
            + "ECDHE-RSA-AES256-SHA:"
            + "DHE-RSA-AES128-SHA256:"
            + "DHE-RSA-AES128-SHA:"
            + "DHE-RSA-AES256-SHA256:"
            + "DHE-RSA-AES256-SHA:"
            + "ECDHE-ECDSA-DES-CBC3-SHA:"
            + "ECDHE-RSA-DES-CBC3-SHA:"
            + "EDH-RSA-DES-CBC3-SHA:"
            + "AES128-GCM-SHA256:"
            + "AES256-GCM-SHA384:"
            + "AES128-SHA256:"
            + "AES256-SHA256:"
            + "AES128-SHA:"
            + "AES256-SHA:"
            + "DES-CBC3-SHA:"
            + "!DSS"
        )
        return context

    async def start(self) -> None:
        """Start the aiohttp server."""
        # Aiohttp freezes apps after start so that no changes can be made.
        # However in Home Assistant components can be discovered after boot.
        # This will now raise a RunTimeError.
        # To work around this we now prevent the router from getting frozen
        # pylint: disable=protected-access
        self._app._router.freeze = lambda: None  # type: ignore[assignment]

        self._runner = web.AppRunner(self._app)
        await self._runner.setup()

        self._site = SmartHomeControllerSite(
            self._runner,
            self._server_host,
            self._server_port,
            ssl_context=self._context,
        )
        try:
            await self._site.start()
        except OSError as error:
            _LOGGER.error(
                f"Failed to create HTTP server at port {self._server_port}: {error}"
            )

        _LOGGER.info(f"Now listening on port {self._server_port}")

    async def stop(self) -> None:
        """Stop the aiohttp server."""
        if self._site is not None:
            await self._site.stop()
        if self._runner is not None:
            await self._runner.cleanup()
