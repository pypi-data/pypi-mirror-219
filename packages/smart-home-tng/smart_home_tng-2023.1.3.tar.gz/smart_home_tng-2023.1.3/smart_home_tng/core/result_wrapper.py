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

import typing


# pylint: disable=unused-variable
class ResultWrapper:
    """Result wrapper class to store render result."""

    def __init__(self, render_result: str) -> None:
        super().__init__()
        self.render_result = render_result

    @staticmethod
    def gen_result_wrapper(kls):
        """Generate a result wrapper."""

        class Wrapper(kls, ResultWrapper):
            """Wrapper of a kls that can store render_result."""

            def __init__(self, *args: typing.Any, render_result: str = None) -> None:
                super().__init__(*args)
                super().__init__(render_result)
                self.render_result = render_result

            def __str__(self) -> str:
                if self.render_result is None:
                    # Can't get set repr to work
                    if kls is set:
                        return str(set(self))

                    return typing.cast(str, kls.__str__(self))

                return self.render_result

        return Wrapper
