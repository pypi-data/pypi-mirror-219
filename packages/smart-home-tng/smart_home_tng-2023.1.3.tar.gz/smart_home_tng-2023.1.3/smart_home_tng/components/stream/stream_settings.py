"""
Stream Component for Smart Home - The Next Generation.

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

import attr

from .const import Const


@attr.s(slots=True)
class StreamSettings:
    """Stream settings."""

    ll_hls: bool = attr.ib()
    min_segment_duration: float = attr.ib()
    part_target_duration: float = attr.ib()
    hls_advance_part_limit: int = attr.ib()
    hls_part_timeout: float = attr.ib()


# pylint: disable=unused-variable
STREAM_SETTINGS_NON_LL_HLS: typing.Final = StreamSettings(
    ll_hls=False,
    min_segment_duration=(
        Const.TARGET_SEGMENT_DURATION_NON_LL_HLS - Const.SEGMENT_DURATION_ADJUSTER
    ),
    part_target_duration=Const.TARGET_SEGMENT_DURATION_NON_LL_HLS,
    hls_advance_part_limit=3,
    hls_part_timeout=Const.TARGET_SEGMENT_DURATION_NON_LL_HLS,
)
