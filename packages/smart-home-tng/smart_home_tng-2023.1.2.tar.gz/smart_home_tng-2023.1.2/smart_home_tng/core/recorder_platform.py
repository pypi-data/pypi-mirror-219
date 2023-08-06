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

import datetime as dt
import inspect

from .platform_implementation import PlatformImplementation
from .recorder_component import RecorderComponent
from .statistic_business_model import Statistic


# pylint: disable=unused-variable
class RecorderPlatform(PlatformImplementation):
    """
    Required base class for all Recorder Platforms in
    Smart Home - The Next Generation Components.
    """

    @property
    def supports_statistics(self) -> bool:
        """
        Returns if the platform implementation support the extended
        statistics protocol.

        Default implementation does not support statistics.
        """
        current_impl = self.list_statistic_ids
        default_impl = RecorderPlatform.list_statistic_ids
        return inspect.getfile(current_impl) != inspect.getfile(default_impl)

    @property
    def supports_compile_statistics(self) -> bool:
        current_impl = self.compile_statistics
        default_impl = RecorderPlatform.compile_statistics
        return inspect.getfile(current_impl) != inspect.getfile(default_impl)

    @property
    def supports_validate_statistics(self) -> bool:
        current_impl = self.validate_statistics
        default_impl = RecorderPlatform.validate_statistics
        return inspect.getfile(current_impl) != inspect.getfile(default_impl)

    def exclude_attributes(self) -> set[str]:
        """Set of attributes, that should not be recorded."""
        return None

    # pylint: disable=unused-argument
    def list_statistic_ids(
        self,
        recorder: RecorderComponent,
        statistic_ids: list[str] | tuple[str] = None,
        statistic_type: str = None,
    ) -> dict:
        """
        Return all or filtered statistic_ids and meta data.

        Default implementation does nothing.

        Should be overwritten by components, that support statistics.
        """
        raise NotImplementedError()

    # pylint: disable=unused-argument
    def compile_statistics(
        self, recorder: RecorderComponent, start: dt.datetime, end: dt.datetime
    ) -> Statistic.PlatformCompiledStatistics:
        """Compile statistics for all entities during start-end.

        Note: This will query the database and must not be run in the event loop
        """
        raise NotImplementedError()

    # pylint: disable=unused-argument
    def validate_statistics(self, recorder: RecorderComponent):
        """Validate Statistics."""
        raise NotImplementedError()
