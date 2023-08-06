"""
Authentication Layer for Smart Home - The Next Generation.

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

import uuid

import attr


# pylint: disable=unused-variable
@attr.s(slots=True)
class Credentials:
    """Credentials for a user on an auth provider."""

    auth_provider_type: str = attr.ib()
    auth_provider_id: str = attr.ib()

    # Allow the auth provider to store data to represent their auth.
    data: dict = attr.ib()

    id: str = attr.ib(factory=lambda: uuid.uuid4().hex)
    is_new: bool = attr.ib(default=True)
