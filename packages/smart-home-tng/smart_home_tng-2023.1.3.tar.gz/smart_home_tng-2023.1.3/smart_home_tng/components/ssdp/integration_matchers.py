"""
Simple Service Discovery Protocol (SSDP) for Smart Home - The Next Generation.

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

import async_upnp_client.utils as upnp_utils

from ... import core

_ssdp: typing.TypeAlias = core.SSDP


# pylint: disable=unused-variable
class IntegrationMatchers:
    """Optimized integration matching."""

    def __init__(self) -> None:
        """Init optimized integration matching."""
        self._match_by_key: dict[
            str, dict[str, list[tuple[str, dict[str, str]]]]
        ] | None = None

    @core.callback
    def async_setup(
        self, integration_matchers: dict[str, list[dict[str, str]]]
    ) -> None:
        """Build matchers by key.

        Here we convert the primary match keys into their own
        dicts so we can do lookups of the primary match
        key to find the match dict.
        """
        self._match_by_key = {}
        for key in _ssdp.PRIMARY_MATCH_KEYS:
            matchers_by_key = self._match_by_key[key] = {}
            for domain, matchers in integration_matchers.items():
                for matcher in matchers:
                    if match_value := matcher.get(key):
                        matchers_by_key.setdefault(match_value, []).append(
                            (domain, matcher)
                        )

    @core.callback
    def async_matching_domains(
        self, info_with_desc: upnp_utils.CaseInsensitiveDict
    ) -> set[str]:
        """Find domains matching the passed CaseInsensitiveDict."""
        assert self._match_by_key is not None
        domains = set()
        for key, matchers_by_key in self._match_by_key.items():
            if not (match_value := info_with_desc.get(key)):
                continue
            for domain, matcher in matchers_by_key.get(match_value, []):
                if domain in domains:
                    continue
                if all(info_with_desc.get(k) == v for (k, v) in matcher.items()):
                    domains.add(domain)
        return domains
