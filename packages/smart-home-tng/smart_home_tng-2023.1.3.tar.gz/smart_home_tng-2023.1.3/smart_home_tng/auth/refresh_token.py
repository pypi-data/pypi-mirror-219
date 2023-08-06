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

import datetime
import secrets
import uuid

import attr

from ..core import helpers
from ..core.const import Const
from .credentials import Credentials
from .token_type import TokenType
from .user import User


# pylint: disable=unused-variable
@attr.s(slots=True)
class RefreshToken:
    """RefreshToken for a user to grant new access tokens."""

    user: User = attr.ib()
    client_id: str = attr.ib()
    access_token_expiration: datetime.timedelta = attr.ib()
    client_name: str = attr.ib(default=None)
    client_icon: str = attr.ib(default=None)
    token_type: str = attr.ib(
        default=TokenType.NORMAL,
        validator=attr.validators.in_(
            (TokenType.NORMAL, TokenType.SYSTEM, TokenType.LONG_LIVED_ACCESS_TOKEN)
        ),
    )
    id: str = attr.ib(factory=lambda: uuid.uuid4().hex)
    created_at: datetime = attr.ib(factory=helpers.utcnow)
    token: str = attr.ib(factory=lambda: secrets.token_hex(64))
    jwt_key: str = attr.ib(factory=lambda: secrets.token_hex(64))

    last_used_at: datetime.datetime = attr.ib(default=None)
    last_used_ip: str = attr.ib(default=None)

    credential: Credentials = attr.ib(default=None)

    version: str = attr.ib(default=Const.__version__)
