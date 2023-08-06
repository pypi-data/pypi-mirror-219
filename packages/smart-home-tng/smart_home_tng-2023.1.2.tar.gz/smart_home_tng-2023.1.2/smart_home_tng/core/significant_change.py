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

import types
import typing

from .callback import callback
from .const import Const
from .platform import Platform
from .platform_implementation import PlatformImplementation
from .significant_change_platform import SignificantChangePlatform
from .state import State

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_PLATFORM: typing.Final = Platform.SIGNIFICANT_CHANGE

_CheckTypeFunc: typing.TypeAlias = typing.Callable[
    [
        str,
        typing.Union[dict, types.MappingProxyType],
        str,
        typing.Union[dict, types.MappingProxyType],
    ],
    typing.Optional[bool],
]

_ExtraCheckTypeFunc: typing.TypeAlias = typing.Callable[
    [
        str,
        typing.Union[dict, types.MappingProxyType],
        typing.Any,
        str,
        typing.Union[dict, types.MappingProxyType],
        typing.Any,
    ],
    typing.Optional[bool],
]


class _SignificantlyChangedChecker:
    """Class to keep track of entities to see if they have significantly changed.

    Will always compare the entity to the last entity that was considered significant.
    """

    def __init__(
        self,
        shc: SmartHomeController,
        extra_significant_check: _ExtraCheckTypeFunc = None,
    ) -> None:
        """Test if an entity has significantly changed."""
        self._shc = shc
        self._last_approved_entities: dict[str, tuple[State, typing.Any]] = {}
        self._extra_significant_check = extra_significant_check

    @property
    def last_approved_entities(self) -> dict[str, tuple[State, typing.Any]]:
        return self._last_approved_entities

    @property
    def extra_significant_check(self) -> _ExtraCheckTypeFunc:
        return self._extra_significant_check

    @callback
    def async_is_significant_change(
        self, new_state: State, *, extra_arg: typing.Any = None
    ) -> bool:
        """Return if this was a significant change.

        Extra kwargs are passed to the extra significant checker.
        """
        old_data = self.last_approved_entities.get(new_state.entity_id)

        # First state change is always ok to report
        if old_data is None:
            self.last_approved_entities[new_state.entity_id] = (new_state, extra_arg)
            return True

        old_state, old_extra_arg = old_data

        # Handle state unknown or unavailable
        if new_state.state in (Const.STATE_UNKNOWN, Const.STATE_UNAVAILABLE):
            if new_state.state == old_state.state:
                return False

            self.last_approved_entities[new_state.entity_id] = (new_state, extra_arg)
            return True

        # If last state was unknown/unavailable, also significant.
        if old_state.state in (Const.STATE_UNKNOWN, Const.STATE_UNAVAILABLE):
            self.last_approved_entities[new_state.entity_id] = (new_state, extra_arg)
            return True

        # pylint: disable=protected-access
        if SignificantChange._platforms is None:
            raise RuntimeError("Significant Change not initialized")

        platform = SignificantChange._platforms.get(new_state.domain)

        if platform is not None:
            result = platform.check_significant_change(
                old_state.state,
                old_state.attributes,
                new_state.state,
                new_state.attributes,
            )

            if result is False:
                return False

        if (extra_significant_check := self.extra_significant_check) is not None:
            result = extra_significant_check(
                old_state.state,
                old_state.attributes,
                old_extra_arg,
                new_state.state,
                new_state.attributes,
                extra_arg,
            )

            if result is False:
                return False

        # Result is either True or None.
        # None means the function doesn't know. For now assume it's True
        self.last_approved_entities[new_state.entity_id] = (
            new_state,
            extra_arg,
        )
        return True


# pylint: disable=invalid-name
class SignificantChange:
    """significant change namespace."""

    _platforms: dict[str, SignificantChangePlatform] = None

    CheckTypeFunc: typing.TypeAlias = _CheckTypeFunc
    ExtraCheckTypeFunc: typing.TypeAlias = _ExtraCheckTypeFunc
    SignificantlyChangedChecker: typing.TypeAlias = _SignificantlyChangedChecker

    @staticmethod
    async def create_checker(
        shc: SmartHomeController,
        _domain: str,
        extra_significant_check: _ExtraCheckTypeFunc = None,
    ):
        """Create a significantly changed checker for a domain."""
        await SignificantChange._initialize(shc)
        return _SignificantlyChangedChecker(shc, extra_significant_check)

    # Marked as singleton so multiple calls all wait for same output.
    @staticmethod
    async def _initialize(shc: SmartHomeController) -> None:
        """Initialize the functions."""
        if SignificantChange._platforms is not None:
            return

        functions = SignificantChange._platforms = {}

        async def process_platform(
            component_name: str, platform: PlatformImplementation
        ) -> None:
            """Process a significant change platform."""
            if isinstance(platform, SignificantChangePlatform):
                functions[component_name] = platform

        await shc.setup.async_process_integration_platforms(_PLATFORM, process_platform)

    @staticmethod
    def either_one_none(val1: typing.Any, val2: typing.Any) -> bool:
        """Test if exactly one value is None."""
        return (val1 is None and val2 is not None) or (
            val1 is not None and val2 is None
        )

    @staticmethod
    def _check_numeric_change(
        old_state: int | float,
        new_state: int | float,
        change: int | float,
        metric: typing.Callable[[int | float, int | float], int | float],
    ) -> bool:
        """Check if two numeric values have changed."""
        if old_state is None and new_state is None:
            return False

        if SignificantChange.either_one_none(old_state, new_state):
            return True

        assert old_state is not None
        assert new_state is not None

        if metric(old_state, new_state) >= change:
            return True

        return False

    @staticmethod
    def check_absolute_change(
        val1: int | float,
        val2: int | float,
        change: int | float,
    ) -> bool:
        """Check if two numeric values have changed."""
        return SignificantChange._check_numeric_change(
            val1, val2, change, lambda val1, val2: abs(val1 - val2)
        )

    @staticmethod
    def check_percentage_change(
        old_state: int | float,
        new_state: int | float,
        change: int | float,
    ) -> bool:
        """Check if two numeric values have changed."""

        def percentage_change(old_state: int | float, new_state: int | float) -> float:
            if old_state == new_state:
                return 0
            try:
                return (abs(new_state - old_state) / old_state) * 100.0
            except ZeroDivisionError:
                return float("inf")

        return SignificantChange._check_numeric_change(
            old_state, new_state, change, percentage_change
        )
