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

# pylint: disable=unused-variable

from .analytics_onboarding_view import AnalyticsOnboardingView
from .const import Const
from .core_config_onboarding_view import CoreConfigOnboardingView
from .installation_type_onboarding_view import InstallationTypeOnboardingView
from .integration_onboarding_view import IntegrationOnboardingView
from .onboarding import Onboarding
from .onborading_view import OnboardingView
from .step import Step
from .user_onboarding_view import UserOnboardingView

_: typing.Final = Onboarding(__path__)
