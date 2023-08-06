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

import typing

from ... import core
from .analytics_onboarding_view import AnalyticsOnboardingView
from .const import Const
from .core_config_onboarding_view import CoreConfigOnboardingView
from .installation_type_onboarding_view import InstallationTypeOnboardingView
from .integration_onboarding_view import IntegrationOnboardingView
from .onboarding_store import OnboadingStorage
from .onborading_view import OnboardingView
from .step import Step
from .user_onboarding_view import UserOnboardingView


# pylint: disable=unused-variable
class Onboarding(core.OnboardingComponent):
    """Support to help onboard new users."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._data = None

    @property
    def storage_version(self) -> int:
        return 4

    @core.callback
    def async_is_onboarded(self) -> bool:
        """Return if Home Assistant has been onboarded."""
        data = self._data
        return data is None or data is True

    @core.callback
    def async_is_user_onboarded(self) -> bool:
        """Return if a user has been created as part of onboarding."""
        return self.async_is_onboarded() or Step.USER.value in self._data["done"]

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the onboarding component."""
        if not await super().async_setup(config):
            return False

        store = OnboadingStorage(
            self._shc, self.storage_version, self.storage_key, private=True
        )
        if (data := await store.async_load()) is None:
            data = {"done": []}

        assert isinstance(data, dict)

        if Step.USER.value not in data["done"]:
            # Users can already have created an owner account via the command line
            # If so, mark the user step as done.
            has_owner = False

            for user in await self._shc.auth.async_get_users():
                if user.is_owner:
                    has_owner = True
                    break

            if has_owner:
                data["done"].append(Step.USER.value)
                await store.async_save(data)

        if set(data["done"]).issuperset(set(Const.STEPS)):
            self._data = True
            return True

        self._data = data

        await self._async_setup_views(data, store)

        return True

    async def _async_setup_views(self, data, store):
        """Set up the onboarding view."""
        shc = self._shc
        shc.register_view(OnboardingView(data))
        shc.register_view(InstallationTypeOnboardingView(data))
        shc.register_view(UserOnboardingView(self, data, store))
        shc.register_view(CoreConfigOnboardingView(self, data, store))
        shc.register_view(IntegrationOnboardingView(self, data, store))
        shc.register_view(AnalyticsOnboardingView(self, data, store))

    def mark_done(self) -> None:
        self._data = True
