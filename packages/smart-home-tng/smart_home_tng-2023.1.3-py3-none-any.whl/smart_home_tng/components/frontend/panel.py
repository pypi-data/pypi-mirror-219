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
import typing

from ... import core
from .const import Const
from .panel_response import PanelResponse


_LOGGER: typing.Final = logging.getLogger(__name__)


class Panel:
    """Abstract class for panels."""

    def __init__(
        self,
        component_name: str,
        sidebar_title: str,
        sidebar_icon: str,
        frontend_url_path: str,
        config: dict[str, typing.Any],
        require_admin: bool,
    ) -> None:
        """Initialize a built-in panel."""
        # Name of the webcomponent
        self._component_name = component_name

        # Title to show in the sidebar
        self._sidebar_title = sidebar_title

        # Icon to show in the sidebar
        self._sidebar_icon = sidebar_icon

        # Url to show the panel in the frontend
        self._frontend_url_path = frontend_url_path or component_name

        # Config to pass to the webcomponent
        self._config = config

        # If the panel should only be visible to admins
        self._require_admin = require_admin

    @property
    def component_name(self) -> str:
        return self._component_name

    @property
    def sidebar_title(self) -> str:
        return self._sidebar_title

    @property
    def sidebar_icon(self) -> str:
        return self._sidebar_icon

    @property
    def frontend_url_path(self) -> str:
        return self._frontend_url_path

    @property
    def require_admin(self) -> bool:
        return self._require_admin

    @property
    def config(self) -> core.ConfigType:
        return self._config

    @core.callback
    def to_response(self) -> PanelResponse:
        """Panel as dictionary."""
        return {
            "component_name": self.component_name,
            "icon": self.sidebar_icon,
            "title": self.sidebar_title,
            "config": self.config,
            "url_path": self.frontend_url_path,
            "require_admin": self.require_admin,
        }

    @staticmethod
    @core.callback
    def async_register_built_in_panel(
        shc: core.SmartHomeController,
        component_name: str,
        sidebar_title: str = None,
        sidebar_icon: str = None,
        frontend_url_path: str = None,
        config: core.ConfigType = None,
        require_admin: bool = False,
        *,
        update: bool = False,
    ) -> None:
        """Register a built-in panel."""
        panel = Panel(
            component_name,
            sidebar_title,
            sidebar_icon,
            frontend_url_path,
            config,
            require_admin,
        )

        if not update and panel.frontend_url_path in _PANELS:
            raise ValueError(f"Overwriting panel {panel.frontend_url_path}")

        _PANELS[panel.frontend_url_path] = panel

        shc.bus.async_fire(Const.EVENT_PANELS_UPDATED)

    @staticmethod
    @core.callback
    def async_remove_panel(
        shc: core.SmartHomeController, frontend_url_path: str
    ) -> None:
        """Remove a built-in panel."""
        panel = _PANELS.pop(frontend_url_path, None)

        if panel is None:
            _LOGGER.warning(f"Removing unknown panel {frontend_url_path}")

        shc.bus.async_fire(Const.EVENT_PANELS_UPDATED)

    @staticmethod
    def is_panel_registered(frontend_url_path: str) -> bool:
        return frontend_url_path in _PANELS

    @staticmethod
    def get_panel(frontend_url_path: str):
        return _PANELS.get(frontend_url_path, None)

    @staticmethod
    def get_info() -> list[str]:
        return list(_PANELS)

    @staticmethod
    def items():
        return _PANELS.items()


_PANELS: typing.Final = dict[str, Panel]()
