"""
Code Generator for Smart Home - The Next Generation.

Generates helper code from component manifests.

Smart Home - TNG is a Home Automation framework for observing the state
of entities and react to changes. It is based on Home Assistant from
home-assistant.io and the Home Assistant Community.

Copyright (c) 2022, Andreas Nixdorf

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

import pathlib
import typing

import attr

from .error import Error


# pylint: disable=unused-variable
@attr.s
class Config:
    """Config for the run."""

    specific_integrations: pathlib.Path = attr.ib()
    root: pathlib.Path = attr.ib()
    action: str = attr.ib()
    requirements: bool = attr.ib()
    errors: list[Error] = attr.ib(factory=list)
    cache: dict[str, typing.Any] = attr.ib(factory=dict)
    plugins: set[str] = attr.ib(factory=set)

    def add_error(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Add an error."""
        self.errors.append(Error(*args, **kwargs))
