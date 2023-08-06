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

import typing
import voluptuous as vol
from ... import core
from .manifest import _Manifest

_cv: typing.TypeAlias = core.ConfigValidation


# pylint: disable=unused-variable
class Const:
    """Constants for Frontend Component."""

    CONF_THEMES: typing.Final = "themes"
    CONF_THEMES_MODES: typing.Final = "modes"
    CONF_THEMES_LIGHT: typing.Final = "light"
    CONF_THEMES_DARK: typing.Final = "dark"
    CONF_EXTRA_HTML_URL: typing.Final = "extra_html_url"
    CONF_EXTRA_HTML_URL_ES5: typing.Final = "extra_html_url_es5"
    CONF_EXTRA_MODULE_URL: typing.Final = "extra_module_url"
    CONF_EXTRA_JS_URL_ES5: typing.Final = "extra_js_url_es5"
    CONF_FRONTEND_REPO: typing.Final = "development_repo"
    CONF_JS_VERSION: typing.Final = "javascript_version"
    EVENT_PANELS_UPDATED: typing.Final = "panels.updated"

    DEFAULT_THEME_COLOR: typing.Final = "#03A9F4"

    DEFAULT_THEME: typing.Final = "default"
    VALUE_NO_THEME: typing.Final = "none"

    PRIMARY_COLOR: typing.Final = "primary-color"
    DATA_DEFAULT_THEME: typing.Final = "frontend_default_theme"
    DATA_DEFAULT_DARK_THEME: typing.Final = "frontend_default_dark_theme"

    EXTENDED_THEME_SCHEMA: typing.Final = vol.Schema(
        {
            # Theme variables that apply to all modes
            _cv.string: _cv.string,
            # Mode specific theme variables
            vol.Optional(CONF_THEMES_MODES): vol.Schema(
                {
                    vol.Optional(CONF_THEMES_LIGHT): vol.Schema(
                        {_cv.string: _cv.string}
                    ),
                    vol.Optional(CONF_THEMES_DARK): vol.Schema(
                        {_cv.string: _cv.string}
                    ),
                }
            ),
        }
    )

    THEME_SCHEMA: typing.Final = vol.Schema(
        {
            _cv.string: (
                vol.Any(
                    # Legacy theme scheme
                    {_cv.string: _cv.string},
                    # New extended schema with mode support
                    EXTENDED_THEME_SCHEMA,
                )
            )
        }
    )

    SERVICE_SET_THEME: typing.Final = "set_theme"
    SERVICE_RELOAD_THEMES: typing.Final = "reload_themes"

    MANIFEST_JSON: typing.Final = _Manifest(
        {
            "background_color": "#FFFFFF",
            "description": "Home automation platform that puts local control and privacy first.",
            "dir": "ltr",
            "display": "standalone",
            "icons": [
                {
                    "src": f"/static/icons/favicon-{size}x{size}.png",
                    "sizes": f"{size}x{size}",
                    "type": "image/png",
                    "purpose": "maskable any",
                }
                for size in (192, 384, 512, 1024)
            ],
            "screenshots": [
                {
                    "src": "/static/images/screenshots/screenshot-1.png",
                    "sizes": "413x792",
                    "type": "image/png",
                }
            ],
            "lang": "en-US",
            "name": "Smart Home - The Next Generation",
            "short_name": "Smart Home TNG",
            "start_url": "/?homescreen=1",
            "theme_color": DEFAULT_THEME_COLOR,
            "prefer_related_applications": True,
            "related_applications": [
                {"platform": "play", "id": "io.homeassistant.companion.android"}
            ],
        }
    )
