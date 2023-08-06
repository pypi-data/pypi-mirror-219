"""
Google Assistant Integration  for Smart Home - The Next Generation.

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

from ... import core


class SmartHomeError(Exception):
    """Google Assistant Smart Home errors.

    https://developers.google.com/actions/smarthome/create-app#error_responses
    """

    def __init__(self, code, msg):
        """Log error code."""
        super().__init__(msg)
        self.code = code

    def to_response(self):
        """Convert to a response format."""
        return {"errorCode": self.code}


# pylint: disable=unused-variable
class ChallengeNeeded(SmartHomeError):
    """Google Assistant Smart Home errors.

    https://developers.google.com/actions/smarthome/create-app#error_responses
    """

    def __init__(self, challenge_type):
        """Initialize challenge needed error."""
        super().__init__(
            core.GoogleAssistant.ERR_CHALLENGE_NEEDED,
            f"Challenge needed: {challenge_type}",
        )
        self.challenge_type = challenge_type

    def to_response(self):
        """Convert to a response format."""
        return {
            "errorCode": self.code,
            "challengeNeeded": {"type": self.challenge_type},
        }
