"""
Onboarding Component for Smart Home - The Next Generation.

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
import typing

from ... import core
from .const import Const
from .step import Step

if not typing.TYPE_CHECKING:

    class Onboarding:
        ...


if typing.TYPE_CHECKING:
    from .onboarding import Onboarding


# pylint: disable=unused-variable
class _BaseOnboardingView(core.SmartHomeControllerView):
    """Base class for onboarding."""

    def __init__(
        self,
        owner: Onboarding,
        url: str,
        name: str,
        step: Step,
        requires_auth: bool = True,
        data=None,
        store=None,
    ):
        """Initialize the onboarding view."""
        super().__init__(url, name, requires_auth=requires_auth)
        self._owner = owner
        self._step = step
        self._store = store
        self._data = data
        self._lock = asyncio.Lock()

    @core.callback
    def _async_is_done(self):
        """Return if this step is done."""
        return self._step.value in self._data["done"]

    # pylint: disable=unused-argument
    async def _async_mark_done(self, shc: core.SmartHomeController):
        """Mark step as done."""
        self._data["done"].append(self._step.value)
        await self._store.async_save(self._data)

        if set(self._data["done"]) == set(Const.STEPS):
            self._owner.mark_done()
