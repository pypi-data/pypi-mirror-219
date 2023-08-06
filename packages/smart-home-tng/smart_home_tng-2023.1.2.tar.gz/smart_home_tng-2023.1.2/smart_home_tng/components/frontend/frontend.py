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

import logging
import os
import typing

import voluptuous as vol
from aiohttp import web

from ... import core
from .const import Const
from .index_view import IndexView, _frontend_root
from .manifest_view import ManifestView
from .panel import Panel
from .storage import Storage
from .url_manager import UrlManager

_cv: typing.TypeAlias = core.ConfigValidation
_LOGGER: typing.Final = logging.getLogger(__name__)

_GET_PANELS: typing.Final = {"type": "get_panels"}
_GET_THEMES: typing.Final = {"type": "frontend/get_themes"}
_GET_VERSION: typing.Final = {"type": "frontend/get_version"}
_GET_TRANSLATIONS: typing.Final = {
    "type": "frontend/get_translations",
    vol.Required("language"): str,
    vol.Required("category"): str,
    vol.Optional("integration"): vol.All(_cv.ensure_list, [str]),
    vol.Optional("config_flow"): bool,
}


# pylint: disable=unused-variable
class Frontend(core.FrontendComponent):
    """Handle the frontend for Smart Home - The Next Generation."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._extra_modules: UrlManager = None
        self._extra_js_es5: UrlManager = None
        self._themes: core.ConfigType = None
        self._store: core.Store = None
        self._default_theme: str = None
        self._default_dark_theme: str = None

    @property
    def storage_key(self) -> str:
        return self.domain + ".theme"

    @property
    def storage_save_delay(self) -> int:
        return 60

    @property
    def extra_modules(self) -> UrlManager:
        return self._extra_modules

    @property
    def extra_js_es5(self) -> UrlManager:
        return self._extra_js_es5

    def async_register_built_in_panel(
        self,
        component_name: str,
        sidebar_title: str = None,
        sidebar_icon: str = None,
        frontend_url_path: str = None,
        config: dict[str, typing.Any] = None,
        require_admin: bool = False,
        *,
        update: bool = False,
    ) -> None:
        return Panel.async_register_built_in_panel(
            self._shc,
            component_name,
            sidebar_title,
            sidebar_icon,
            frontend_url_path,
            config,
            require_admin,
            update=update,
        )

    def async_remove_panel(self, frontend_url_path: str) -> None:
        return Panel.async_remove_panel(self._shc, frontend_url_path)

    def is_panel_registered(self, frontend_url_path: str) -> bool:
        return Panel.is_panel_registered(frontend_url_path)

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        schema = vol.Schema(
            {
                self.domain: vol.Schema(
                    {
                        vol.Optional(Const.CONF_FRONTEND_REPO): _cv.isdir,
                        vol.Optional(Const.CONF_THEMES): Const.THEME_SCHEMA,
                        vol.Optional(Const.CONF_EXTRA_MODULE_URL): vol.All(
                            _cv.ensure_list, [_cv.string]
                        ),
                        vol.Optional(Const.CONF_EXTRA_JS_URL_ES5): vol.All(
                            _cv.ensure_list, [_cv.string]
                        ),
                        # We no longer use these options.
                        vol.Optional(Const.CONF_EXTRA_HTML_URL): _cv.match_all,
                        vol.Optional(Const.CONF_EXTRA_HTML_URL_ES5): _cv.match_all,
                        vol.Optional(Const.CONF_JS_VERSION): _cv.match_all,
                    },
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    def add_manifest_json_key(self, key: str, val: typing.Any) -> None:
        """Add a keyval to the manifest.json."""
        Const.MANIFEST_JSON.update_key(key, val)

    def get_manifest(self, key: str) -> typing.Any:
        return Const.MANIFEST_JSON.manifest.get(key)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the serving of the frontend."""
        if not await super().async_setup(config):
            return False

        api = self.controller.components.websocket_api
        if not isinstance(api, core.WebSocket.Component):
            return False

        await Storage.async_setup_frontend_storage(api)
        api.register_command(self._get_panels, _GET_PANELS)
        api.register_command(self._get_themes, _GET_THEMES)
        api.register_command(self._get_translations, _GET_TRANSLATIONS)
        api.register_command(self._get_version, _GET_VERSION)
        self._shc.register_view(ManifestView())

        conf = config.get(self.domain, {})

        for key in (
            Const.CONF_EXTRA_HTML_URL,
            Const.CONF_EXTRA_HTML_URL_ES5,
            Const.CONF_JS_VERSION,
        ):
            if key in conf:
                _LOGGER.error(
                    f"Please remove {key} from your frontend config. "
                    + "It is no longer supported",
                )

        repo_path = conf.get(Const.CONF_FRONTEND_REPO)
        is_dev = repo_path is not None
        root_path = _frontend_root(repo_path)

        for path, should_cache in (
            ("service_worker.js", False),
            ("robots.txt", False),
            ("onboarding.html", not is_dev),
            ("static", not is_dev),
            ("frontend_latest", not is_dev),
            ("frontend_es5", not is_dev),
        ):
            self._shc.http.register_static_path(
                f"/{path}", str(root_path / path), should_cache
            )

        self._shc.http.register_static_path(
            "/auth/authorize", str(root_path / "authorize.html"), False
        )
        # https://wicg.github.io/change-password-url/
        self._shc.http.register_redirect(
            "/.well-known/change-password", "/profile", redirect_exc=web.HTTPFound
        )

        local = self._shc.config.path("www")
        if os.path.isdir(local):
            self._shc.http.register_static_path("/local", local, not is_dev)

        # Can be removed in 2023
        self._shc.http.register_redirect(
            "/config/server_control", "/developer-tools/yaml"
        )

        self._shc.http.register_resource(IndexView(repo_path, self))

        Panel.async_register_built_in_panel(self._shc, "profile")

        Panel.async_register_built_in_panel(
            self._shc,
            "developer-tools",
            require_admin=True,
            sidebar_title="developer_tools",
            sidebar_icon="hass:hammer",
        )

        Panel.async_register_built_in_panel(
            self.controller, "config", "config", "mdi:cog", require_admin=True
        )
        self._extra_modules = UrlManager(conf.get(Const.CONF_EXTRA_MODULE_URL, []))
        self._extra_js_es5 = UrlManager(conf.get(Const.CONF_EXTRA_JS_URL_ES5, []))

        await self._async_setup_themes(conf.get(Const.CONF_THEMES))

        return True

    async def _async_setup_themes(self, themes: dict[str, typing.Any]) -> None:
        """Set up themes data and services."""
        self._themes = themes or {}

        store = self._store = core.Store(
            self._shc, self.storage_version, self.storage_key
        )

        if not (theme_data := await store.async_load()) or not isinstance(
            theme_data, dict
        ):
            theme_data = {}
        theme_name = theme_data.get(Const.DATA_DEFAULT_THEME, Const.DEFAULT_THEME)
        dark_theme_name = theme_data.get(Const.DATA_DEFAULT_DARK_THEME)

        if theme_name == Const.DEFAULT_THEME or theme_name in self._themes:
            self._default_theme = theme_name
        else:
            self._default_theme = Const.DEFAULT_THEME

        if dark_theme_name == Const.DEFAULT_THEME or dark_theme_name in self._themes:
            self._default_dark_theme = dark_theme_name
        else:
            self._default_dark_theme = Const.DEFAULT_THEME

        core.Service.async_register_admin_service(
            self._shc,
            self.domain,
            Const.SERVICE_SET_THEME,
            self._set_theme,
            vol.Schema(
                {
                    vol.Required(core.Const.CONF_NAME): _cv.string,
                    vol.Optional(core.Const.CONF_MODE): vol.Any("dark", "light"),
                }
            ),
        )

        core.Service.async_register_admin_service(
            self._shc, self.domain, Const.SERVICE_RELOAD_THEMES, self._reload_themes
        )

    @core.callback
    def update_theme_and_fire_event(self) -> None:
        """Update theme_color in manifest."""
        name = self._default_theme
        themes = self._themes
        if name != Const.DEFAULT_THEME:
            Const.MANIFEST_JSON.update_key(
                "theme_color",
                themes[name].get(
                    "app-header-background-color",
                    themes[name].get(Const.PRIMARY_COLOR, Const.DEFAULT_THEME_COLOR),
                ),
            )
        else:
            Const.MANIFEST_JSON.update_key("theme_color", Const.DEFAULT_THEME_COLOR)
        self._shc.bus.async_fire(core.Const.EVENT_THEMES_UPDATED)

    async def _set_theme(self, call: core.ServiceCall) -> None:
        """Set backend-preferred theme."""
        name = call.data[core.Const.CONF_NAME]
        mode = call.data.get("mode", "light")

        if (
            name not in (Const.DEFAULT_THEME, Const.VALUE_NO_THEME)
            and name not in self._themes
        ):
            _LOGGER.warning(f"Theme {name} not found")
            return

        light_mode = mode == "light"

        if name == Const.VALUE_NO_THEME:
            if light_mode:
                self._default_theme = Const.DEFAULT_THEME
            else:
                self._default_dark_theme = None
        else:
            _LOGGER.info(f"Theme {name} set as default {mode} theme")
            if light_mode:
                self._default_theme = name
            else:
                self._default_dark_theme = name

        self._store.async_delay_save(
            lambda: {
                Const.DATA_DEFAULT_THEME: self._default_theme,
                Const.DATA_DEFAULT_DARK_THEME: self._default_dark_theme,
            },
            self.storage_save_delay,
        )
        self.update_theme_and_fire_event()

    async def _reload_themes(self, _: core.ServiceCall) -> None:
        """Reload themes."""
        config = await self._shc.setup.async_shc_config_yaml()
        new_themes = config[self.domain].get(Const.CONF_THEMES, {})
        self._themes = new_themes
        if self._default_theme not in new_themes:
            self._default_theme = Const.DEFAULT_THEME
        if self._default_dark_theme and self._default_dark_theme not in new_themes:
            self._default_dark_theme = None
        self.update_theme_and_fire_event()

    @core.callback
    def _get_panels(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle get panels command."""
        user_is_admin = connection.user.is_admin
        panels = {
            panel_key: panel.to_response()
            for panel_key, panel in Panel.items()
            if user_is_admin or not panel.require_admin
        }

        connection.send_result(msg["id"], panels)

    @core.callback
    def _get_themes(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle get themes command."""
        shc = connection.owner.controller
        if shc.config.safe_mode:
            connection.send_result(
                msg["id"],
                {
                    "themes": {
                        "safe_mode": {
                            "primary-color": "#db4437",
                            "accent-color": "#ffca28",
                        }
                    },
                    "default_theme": "safe_mode",
                },
            )
            return

        connection.send_result(
            msg["id"],
            {
                "themes": self._themes,
                "default_theme": self._default_theme,
                "default_dark_theme": self._default_dark_theme,
            },
        )

    async def _get_translations(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle get translations command."""
        shc = connection.owner.controller
        resources = await shc.translations.async_get_translations(
            msg["language"],
            msg["category"],
            msg.get("integration"),
            msg.get("config_flow"),
        )
        connection.send_result(msg["id"], {"resources": resources})

    async def _get_version(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle get version command."""
        shc = connection.owner.controller
        integration = await shc.setup.async_get_integration(self.domain)

        frontend = None

        for req in integration.requirements:
            if req.startswith("home-assistant-frontend=="):
                frontend = req.split("==", 1)[1]

        if frontend is None:
            connection.send_error(msg["id"], "unknown_version", "Version not found")
        else:
            connection.send_result(msg["id"], {"version": frontend})
