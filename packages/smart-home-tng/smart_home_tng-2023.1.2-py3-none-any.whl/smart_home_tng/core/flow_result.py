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

import collections.abc
import typing

import voluptuous as vol


# pylint: disable=unused-variable
class FlowResult(typing.TypedDict, total=False):
    """Typed result dict."""

    version: int
    type: str
    flow_id: str
    handler: str
    title: str
    data: collections.abc.Mapping[str, typing.Any]
    step_id: str
    data_schema: vol.Schema
    extra: str
    required: bool
    errors: dict[str, str]
    description: str
    description_placeholders: dict[str, typing.Any]
    progress_action: str
    url: str
    reason: str
    context: dict[str, typing.Any]
    result: typing.Any
    last_step: bool
    options: collections.abc.Mapping[str, typing.Any]
    menu_options: list[str] | dict[str, str]
