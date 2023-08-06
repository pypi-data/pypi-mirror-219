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
from .const import Const
from .lazy_partial_state import LazyPartialState
from .logbook_callback import LogbookCallback
from .platform_implementation import PlatformImplementation


# pylint: disable=unused-variable
class LogbookPlatform(PlatformImplementation):
    """
    Required base class for the Logbook Platform
    of components .
    """

    # Die Konstanten für das "beschreibende" Dictionary,
    # über das der Eintrag ins Logbuch angepasst werden kann

    LOGBOOK_ENTRY_ICON: typing.Final = Const.LOGBOOK_ENTRY_ICON
    LOGBOOK_ENTRY_MESSAGE: typing.Final = Const.LOGBOOK_ENTRY_MESSAGE
    LOGBOOK_ENTRY_NAME: typing.Final = Const.LOGBOOK_ENTRY_NAME
    LOGBOOK_ENTRY_ENTITY_ID: typing.Final = Const.LOGBOOK_ENTRY_ENTITY_ID
    LOGBOOK_ENTRY_SOURCE: typing.Final = Const.LOGBOOK_ENTRY_SOURCE

    # Die Logbook Komponente übergibt beim Aufruf einen
    # callback (async_describe_event), der für jeden
    # Event der im Logbuch eingetragen werden soll
    # aufgerufen werden muss.
    #
    # Der Parameter des Callbacks ist der
    # event_type, der von der Componente ausgelöst
    # wird.

    @callback
    @abc.abstractmethod
    def async_describe_events(
        self,
        async_describe_event: LogbookCallback,
    ) -> None:
        """
        Describe logbook events, that are formatted
        by the Component.
        """

    @callback
    @abc.abstractmethod
    def async_describe_event(self, event: LazyPartialState) -> dict[str, str]:
        """
        Describe the fired event.

        Only events that where registered in describe_events
        will be processed.
        """
