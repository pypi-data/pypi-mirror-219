"""
Logbook Component for Smart Home - The Next Generation.

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

from ... import core


# pylint: disable=unused-variable
class Const:
    """Constants for the Logbook Component."""

    ATTR_MESSAGE: typing.Final = "message"

    CONTEXT_USER_ID: typing.Final = "context_user_id"
    CONTEXT_ENTITY_ID: typing.Final = "context_entity_id"
    CONTEXT_ENTITY_ID_NAME: typing.Final = "context_entity_id_name"
    CONTEXT_EVENT_TYPE: typing.Final = "context_event_type"
    CONTEXT_DOMAIN: typing.Final = "context_domain"
    CONTEXT_STATE: typing.Final = "context_state"
    CONTEXT_SOURCE: typing.Final = "context_source"
    CONTEXT_SERVICE: typing.Final = "context_service"
    CONTEXT_NAME: typing.Final = "context_name"
    CONTEXT_MESSAGE: typing.Final = "context_message"

    LOGBOOK_ENTRY_DOMAIN: typing.Final = "domain"
    LOGBOOK_ENTRY_STATE: typing.Final = "state"
    LOGBOOK_ENTRY_WHEN: typing.Final = "when"
    LOGBOOK_ENTRY_CONTEXT_ID: typing.Final = "context_id"

    ALL_EVENT_TYPES_EXCEPT_STATE_CHANGED: typing.Final = {
        core.Const.EVENT_LOGBOOK_ENTRY,
        core.Const.EVENT_CALL_SERVICE,
    }
    ENTITY_EVENTS_WITHOUT_CONFIG_ENTRY: typing.Final = {
        core.Const.EVENT_LOGBOOK_ENTRY,
        core.Const.EVENT_AUTOMATION_TRIGGERED,
        core.Const.EVENT_SCRIPT_STARTED,
    }

    LOGBOOK_FILTERS: typing.Final = "logbook.filters"
    LOGBOOK_ENTITIES_FILTER: typing.Final = "entities.filter"
