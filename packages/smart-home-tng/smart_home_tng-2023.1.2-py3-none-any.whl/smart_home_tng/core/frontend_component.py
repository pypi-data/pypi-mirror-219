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
import typing

from .callback import callback
from .smart_home_controller_component import SmartHomeControllerComponent
from .url_manager import UrlManager


# pylint: disable=unused-variable
class FrontendComponent(SmartHomeControllerComponent):
    """Required base class for the Frontend Component."""

    @callback
    @abc.abstractmethod
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
        """Register a built-in panel."""

    @callback
    @abc.abstractmethod
    def async_remove_panel(self, frontend_url_path: str) -> None:
        """Remove a built-in panel."""

    @abc.abstractmethod
    def is_panel_registered(self, frontend_url_path: str) -> bool:
        """
        Can be used to check, if frontend_url_path is already registered
        to avoid exception in async_register_builtin_panel
        """

    @property
    @abc.abstractmethod
    def extra_modules(self) -> UrlManager:
        """Get the Url-Manager for extra modules."""

    @property
    @abc.abstractmethod
    def extra_js_es5(self) -> UrlManager:
        """Get the Url-Manager for javascript es5."""

    @abc.abstractmethod
    def add_manifest_json_key(self, key: str, val: typing.Any) -> None:
        """Add a keyval to the manifest.json."""

    @abc.abstractmethod
    def get_manifest(self, key: str) -> typing.Any:
        """Get the MANIFEST_JSON entry."""
