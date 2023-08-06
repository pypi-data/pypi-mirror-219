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
import logging
import typing

from .alexa_component import AlexaComponent
from .alexa_config_store import AlexaConfigStore
from .callback import callback

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class AbstractAlexaConfig(abc.ABC):
    """Hold the configuration for Alexa."""

    _unsub_proactive_report = None

    def __init__(self, shc: SmartHomeController):
        """Initialize abstract config."""
        self._shc = shc
        self._store = None

    async def async_initialize(self):
        """Perform async initialization of config."""
        self._store = AlexaConfigStore(self._shc)
        await self._store.async_load()

    @property
    def supports_auth(self):
        """Return if config supports auth."""
        return False

    @property
    def should_report_state(self) -> bool:
        """Return if states should be proactively reported."""
        return False

    @property
    def endpoint(self):
        """Endpoint for report state."""
        return None

    @property
    @abc.abstractmethod
    def locale(self) -> str:
        """Return config locale."""

    @property
    def entity_config(self):
        """Return entity config."""
        return {}

    @property
    def is_reporting_states(self):
        """Return if proactive mode is enabled."""
        return self._unsub_proactive_report is not None

    @callback
    @abc.abstractmethod
    def user_identifier(self):
        """Return an identifier for the user that represents this config."""

    async def async_enable_proactive_mode(self):
        """Enable proactive mode."""
        alexa = self._shc.components.alexa
        if not isinstance(alexa, AlexaComponent):
            return

        _LOGGER.debug("Enable proactive mode")
        if self._unsub_proactive_report is None:
            self._unsub_proactive_report = self._shc.async_create_task(
                alexa.async_enable_proactive_mode(self)
            )
        try:
            await self._unsub_proactive_report
        except Exception:
            self._unsub_proactive_report = None
            raise

    async def async_disable_proactive_mode(self):
        """Disable proactive mode."""
        _LOGGER.debug("Disable proactive mode")
        if unsub_func := await self._unsub_proactive_report:
            unsub_func()
        self._unsub_proactive_report = None

    # pylint: disable=unused-argument
    @callback
    def should_expose(self, entity_id):
        """If an entity should be exposed."""
        return False

    @callback
    def async_invalidate_access_token(self):
        """Invalidate access token."""
        raise NotImplementedError

    async def async_get_access_token(self):
        """Get an access token."""
        raise NotImplementedError

    async def async_accept_grant(self, code):
        """Accept a grant."""
        raise NotImplementedError

    @property
    def authorized(self) -> bool:
        """Return authorization status."""
        return self._store.authorized

    async def set_authorized(self, authorized: bool):
        """Set authorization status.

        - Set when an incoming message is received from Alexa.
        - Unset if state reporting fails
        """
        self._store.set_authorized(authorized)
        if self.should_report_state != self.is_reporting_states:
            if self.should_report_state:
                try:
                    await self.async_enable_proactive_mode()
                except Exception:
                    # We failed to enable proactive mode, unset authorized flag
                    self._store.set_authorized(False)
                    raise
            else:
                await self.async_disable_proactive_mode()
