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
import datetime
import collections.abc
import typing

from .protocol import Protocol
from .recorder_filters_base import RecorderFiltersBase
from .sql_session import SqlSession
from .state import State


# pylint: disable=unused-variable
class RecorderHistoryBase(Protocol):
    """
    Required base class for history implementation of the
    recorder component.
    """

    @abc.abstractmethod
    def get_significant_states_with_session(
        self,
        session: SqlSession,
        start_time: datetime.datetime,
        end_time: datetime.datetime = None,
        entity_ids: list[str] = None,
        filters: RecorderFiltersBase = None,
        include_start_time_state: bool = True,
        significant_changes_only: bool = True,
        minimal_response: bool = False,
        no_attributes: bool = False,
        compressed_state_format: bool = False,
    ) -> collections.abc.MutableMapping[str, list[State | dict[str, typing.Any]]]:
        """
        Return states changes during UTC period start_time - end_time.

        entity_ids is an optional iterable of entities to include in the results.

        filters is an optional SQLAlchemy filter which will be applied to the database
        queries unless entity_ids is given, in which case its ignored.

        Significant states are all states where there is a state change,
        as well as all states from certain domains (for instance
        thermostat so that we get current temperature in our graphs).
        """

    @abc.abstractmethod
    def get_significant_states(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime = None,
        entity_ids: list[str] = None,
        filters: RecorderFiltersBase = None,
        include_start_time_state: bool = True,
        significant_changes_only: bool = True,
        minimal_response: bool = False,
        no_attributes: bool = False,
        compressed_state_format: bool = False,
    ) -> collections.abc.MutableMapping[str, list[State | dict[str, typing.Any]]]:
        """Wrap get_significant_states_with_session with an sql session."""
