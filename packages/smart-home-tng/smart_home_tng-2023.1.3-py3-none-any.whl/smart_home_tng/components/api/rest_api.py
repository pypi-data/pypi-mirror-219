"""
Rest API for Smart Home - The Next Generation.

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

import pathlib

from ... import core
from .api_components_view import APIComponentsView
from .api_config_view import APIConfigView
from .api_domain_services_view import APIDomainServicesView
from .api_entity_state_view import APIEntityStateView
from .api_error_log import APIErrorLog
from .api_event_listeners_view import APIEventListenersView
from .api_event_stream import APIEventStream
from .api_event_view import APIEventView
from .api_services_view import APIServicesView
from .api_states_view import APIStatesView
from .api_status_view import APIStatusView
from .api_template_view import APITemplateView


# pylint: disable=unused-variable
class RestAPI(core.SmartHomeControllerComponent):
    """Rest API for Smart Home - The Next Generation."""

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Register the API with the HTTP interface."""
        if not await super().async_setup(config):
            return False

        shc = self._shc

        shc.register_view(APIStatusView())
        shc.register_view(APIEventStream())
        shc.register_view(APIConfigView())
        shc.register_view(APIStatesView())
        shc.register_view(APIEntityStateView())
        shc.register_view(APIEventListenersView())
        shc.register_view(APIEventView())
        shc.register_view(APIServicesView())
        shc.register_view(APIDomainServicesView())
        shc.register_view(APIComponentsView())
        shc.register_view(APITemplateView())

        if pathlib.Path(shc.config.error_log_path).is_file():
            shc.register_view(APIErrorLog())

        return True
