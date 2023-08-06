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

import asyncio
import functools
import typing

from .callback import is_callback
from .smart_home_controller_job_type import SmartHomeControllerJobType

_R_co = typing.TypeVar("_R_co", covariant=True)
_R = typing.TypeVar("_R")


# pylint: disable=unused-variable
class SmartHomeControllerJob(typing.Generic[_R_co]):
    """Represent a job to be run later.

    We check the callable type in advance
    so we can avoid checking it every time
    we run the job.
    """

    __slots__ = ("_job_type", "_target")

    @staticmethod
    def _get_callable_job_type(
        target: typing.Callable[..., typing.Any]
    ) -> SmartHomeControllerJobType:
        """Determine the job type from the callable."""
        # Check for partials to properly determine if coroutine function
        check_target = target
        while isinstance(check_target, functools.partial):
            check_target = check_target.func

        if asyncio.iscoroutinefunction(check_target):
            return SmartHomeControllerJobType.COROUTINE_FUNCTION
        if is_callback(check_target):
            return SmartHomeControllerJobType.CALLBACK
        if asyncio.iscoroutine(check_target):
            raise ValueError("Coroutine not allowed to be passed to HassJob")
        return SmartHomeControllerJobType.EXECUTOR

    @property
    def job_type(self) -> SmartHomeControllerJobType:
        return self._job_type

    @property
    def target(self) -> typing.Callable[..., _R_co]:
        return self._target

    def __init__(self, target: typing.Callable[..., _R_co]) -> None:
        """Create a job object."""
        self._target = target
        self._job_type = self._get_callable_job_type(target)

        if typing.TYPE_CHECKING:
            if self._job_type == SmartHomeControllerJobType.COROUTINE_FUNCTION:
                self._target = typing.cast(
                    typing.Callable[
                        ...,
                        typing.Union[
                            asyncio.coroutines.Coroutine[typing.Any, typing.Any, _R], _R
                        ],
                    ],
                    self._target,
                )
            elif self._job_type == SmartHomeControllerJobType.CALLBACK:
                self._target = typing.cast(typing.Callable[..., _R], self._target)
            else:
                self._target = typing.cast(typing.Callable[..., _R], self._target)

    def __repr__(self) -> str:
        """Return the job."""
        return f"<Job {self._job_type} {self._target}>"
