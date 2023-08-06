"""
Zeroconf Component for Smart Home - The Next Generation.

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
import zeroconf
from zeroconf import asyncio as async_zc

_TYPE_AAAA: typing.Final = 28


# pylint: disable=unused-variable
class AsyncServiceBrowser(async_zc.AsyncServiceBrowser):
    """ServiceBrowser that only consumes DNSPointer records."""

    def __init__(self, ipv6: bool, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Create service browser that filters ipv6 if it is disabled."""
        self._ipv6 = ipv6
        super().__init__(*args, **kwargs)

    def update_record(
        self, zc: zeroconf.Zeroconf, now: float, record: zeroconf.DNSRecord
    ) -> None:
        """Pre-Filter AAAA records if IPv6 is not enabled."""
        if (
            not self._ipv6
            and isinstance(record, zeroconf.DNSAddress)
            and record.type == _TYPE_AAAA
        ):
            return
        super().update_record(zc, now, record)
