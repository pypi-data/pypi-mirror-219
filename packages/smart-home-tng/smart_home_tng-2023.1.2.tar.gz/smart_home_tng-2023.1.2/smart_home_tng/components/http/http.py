"""
HTTP Component for Smart Home - The Next Generation.

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

import ipaddress
import typing

import voluptuous as vol

from ... import core

_cv: typing.TypeAlias = core.ConfigValidation

# Cast to be able to load custom cards.
# My to be able to check url and version info.
_DEFAULT_CORS: typing.Final = ["https://cast.home-assistant.io"]
_NO_LOGIN_ATTEMPT_THRESHOLD: typing.Final = -1

_SAVE_DELAY: typing.Final = 180

_HTTP_SCHEMA: typing.Final = vol.All(
    _cv.deprecated(core.Const.CONF_BASE_URL),
    vol.Schema(
        {
            vol.Optional(core.Const.CONF_SERVER_HOST): vol.All(
                _cv.ensure_list, vol.Length(min=1), [_cv.string]
            ),
            vol.Optional(
                core.Const.CONF_SERVER_PORT, default=core.Const.SERVER_PORT
            ): _cv.port,
            vol.Optional(core.Const.CONF_BASE_URL): _cv.string,
            vol.Optional(core.Const.CONF_SSL_CERTIFICATE): _cv.isfile,
            vol.Optional(core.Const.CONF_SSL_PEER_CERTIFICATE): _cv.isfile,
            vol.Optional(core.Const.CONF_SSL_KEY): _cv.isfile,
            vol.Optional(core.Const.CONF_CORS_ORIGINS, default=_DEFAULT_CORS): vol.All(
                _cv.ensure_list, [_cv.string]
            ),
            vol.Inclusive(core.Const.CONF_USE_X_FORWARDED_FOR, "proxy"): _cv.boolean,
            vol.Inclusive(core.Const.CONF_TRUSTED_PROXIES, "proxy"): vol.All(
                _cv.ensure_list, [ipaddress.ip_network]
            ),
            vol.Optional(
                core.Const.CONF_LOGIN_ATTEMPTS_THRESHOLD,
                default=_NO_LOGIN_ATTEMPT_THRESHOLD,
            ): vol.Any(_cv.positive_int, _NO_LOGIN_ATTEMPT_THRESHOLD),
            vol.Optional(core.Const.CONF_IP_BAN_ENABLED, default=True): _cv.boolean,
            vol.Optional(
                core.Const.CONF_SSL_PROFILE, default=core.Const.SSL_MODERN
            ): vol.In([core.Const.SSL_INTERMEDIATE, core.Const.SSL_MODERN]),
        }
    ),
)


class _ConfData(typing.TypedDict, total=False):
    """Typed dict for config data."""

    server_host: list[str]
    server_port: int
    base_url: str
    ssl_certificate: str
    ssl_peer_certificate: str
    ssl_key: str
    cors_allowed_origins: list[str]
    use_x_forwarded_for: bool
    trusted_proxies: list[ipaddress.IPv4Network | ipaddress.IPv6Network]
    login_attempts_threshold: int
    ip_ban_enabled: bool
    ssl_profile: str


# pylint: disable=unused-variable
class HTTP(core.SmartHomeControllerComponent):
    """HTTP Component for Smart Home - The Next Generation."""

    @property
    def config_schema(self) -> typing.Callable[[core.ConfigType], core.ConfigType]:
        return vol.Schema({self.domain: _HTTP_SCHEMA}, extra=vol.ALLOW_EXTRA)

    @property
    def storage_save_delay(self) -> int:
        return _SAVE_DELAY

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the HTTP API and debug interface."""
        if not await super().async_setup(config):
            return False

        network = self.controller.components.network
        if not isinstance(network, core.NetworkComponent):
            return False

        conf: _ConfData = self._config

        if conf is None:
            conf = typing.cast(_ConfData, _HTTP_SCHEMA({}))

        server_host = conf.get(core.Const.CONF_SERVER_HOST)
        server_port = conf[core.Const.CONF_SERVER_PORT]
        ssl_certificate = conf.get(core.Const.CONF_SSL_CERTIFICATE)
        ssl_peer_certificate = conf.get(core.Const.CONF_SSL_PEER_CERTIFICATE)
        ssl_key = conf.get(core.Const.CONF_SSL_KEY)
        cors_origins = conf[core.Const.CONF_CORS_ORIGINS]
        use_x_forwarded_for = conf.get(core.Const.CONF_USE_X_FORWARDED_FOR, False)
        trusted_proxies = conf.get(core.Const.CONF_TRUSTED_PROXIES) or []
        is_ban_enabled = conf[core.Const.CONF_IP_BAN_ENABLED]
        login_threshold = conf[core.Const.CONF_LOGIN_ATTEMPTS_THRESHOLD]
        ssl_profile = conf[core.Const.CONF_SSL_PROFILE]

        server = core.SmartHomeControllerHTTP(
            self._shc,
            server_host=server_host,
            server_port=server_port,
            ssl_certificate=ssl_certificate,
            ssl_peer_certificate=ssl_peer_certificate,
            ssl_key=ssl_key,
            trusted_proxies=trusted_proxies,
            ssl_profile=ssl_profile,
        )
        await server.async_initialize(
            cors_origins=cors_origins,
            use_x_forwarded_for=use_x_forwarded_for,
            login_threshold=login_threshold,
            is_ban_enabled=is_ban_enabled,
        )

        async def stop_server(_event: core.Event) -> None:
            """Stop the server."""
            await server.stop()

        async def start_server(*_: typing.Any) -> None:
            """Start the server."""
            with self._shc.setup.async_start_setup(["http"]):
                self._shc.bus.async_listen_once(core.Const.EVENT_SHC_STOP, stop_server)
                # We already checked it's not None.
                assert conf is not None
                await self._shc.start_http_server_and_save_config(dict(conf), server)

        # pylint: disable=protected-access
        self._shc._attach_server(server)
        self._shc.setup.async_when_setup_or_start("frontend", start_server)

        local_ip = await network.async_get_source_ip()

        host = local_ip
        if server_host is not None:
            # Assume the first server host name provided as API host
            host = server_host[0]

        self._shc.config.api = core.ApiConfig(
            local_ip, host, server_port, ssl_certificate is not None
        )

        return True
