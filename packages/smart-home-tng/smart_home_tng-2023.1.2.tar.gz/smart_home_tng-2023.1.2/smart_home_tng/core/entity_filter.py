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
import fnmatch
import re
import typing

import voluptuous as vol

from . import helpers
from .config_validation import ConfigValidation as cv
from .const import Const


def _convert_filter(config: dict[str, list[str]]):
    """Convert the filter schema into a filter."""
    return EntityFilter(config)


def _convert_include_exclude_filter(config: dict[str, dict[str, list[str]]]):
    """Convert the include exclude filter schema into a filter."""
    include = config[Const.CONF_INCLUDE]
    exclude = config[Const.CONF_EXCLUDE]
    return _convert_filter(
        {
            _Const.CONF_INCLUDE_DOMAINS: include[Const.CONF_DOMAINS],
            _Const.CONF_INCLUDE_ENTITY_GLOBS: include[_Const.CONF_ENTITY_GLOBS],
            _Const.CONF_INCLUDE_ENTITIES: include[Const.CONF_ENTITIES],
            _Const.CONF_EXCLUDE_DOMAINS: exclude[Const.CONF_DOMAINS],
            _Const.CONF_EXCLUDE_ENTITY_GLOBS: exclude[_Const.CONF_ENTITY_GLOBS],
            _Const.CONF_EXCLUDE_ENTITIES: exclude[Const.CONF_ENTITIES],
        }
    )


class _Const:
    """Constants for entity filter."""

    CONF_INCLUDE_DOMAINS: typing.Final = "include_domains"
    CONF_INCLUDE_ENTITY_GLOBS: typing.Final = "include_entity_globs"
    CONF_INCLUDE_ENTITIES: typing.Final = "include_entities"
    CONF_EXCLUDE_DOMAINS: typing.Final = "exclude_domains"
    CONF_EXCLUDE_ENTITY_GLOBS: typing.Final = "exclude_entity_globs"
    CONF_EXCLUDE_ENTITIES: typing.Final = "exclude_entities"

    CONF_ENTITY_GLOBS: typing.Final = "entity_globs"

    BASE_FILTER_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Optional(CONF_EXCLUDE_DOMAINS, default=[]): vol.All(
                cv.ensure_list, [cv.string]
            ),
            vol.Optional(CONF_EXCLUDE_ENTITY_GLOBS, default=[]): vol.All(
                cv.ensure_list, [cv.string]
            ),
            vol.Optional(CONF_EXCLUDE_ENTITIES, default=[]): cv.entity_ids,
            vol.Optional(CONF_INCLUDE_DOMAINS, default=[]): vol.All(
                cv.ensure_list, [cv.string]
            ),
            vol.Optional(CONF_INCLUDE_ENTITY_GLOBS, default=[]): vol.All(
                cv.ensure_list, [cv.string]
            ),
            vol.Optional(CONF_INCLUDE_ENTITIES, default=[]): cv.entity_ids,
        }
    )

    FILTER_SCHEMA: typing.Final = vol.All(BASE_FILTER_SCHEMA, _convert_filter)

    INCLUDE_EXCLUDE_FILTER_SCHEMA_INNER: typing.Final = vol.Schema(
        {
            vol.Optional(Const.CONF_DOMAINS, default=[]): vol.All(
                cv.ensure_list, [cv.string]
            ),
            vol.Optional(CONF_ENTITY_GLOBS, default=[]): vol.All(
                cv.ensure_list, [cv.string]
            ),
            vol.Optional(Const.CONF_ENTITIES, default=[]): cv.entity_ids,
        }
    )

    INCLUDE_EXCLUDE_BASE_FILTER_SCHEMA: typing.Final = vol.Schema(
        {
            vol.Optional(
                Const.CONF_INCLUDE, default=INCLUDE_EXCLUDE_FILTER_SCHEMA_INNER({})
            ): INCLUDE_EXCLUDE_FILTER_SCHEMA_INNER,
            vol.Optional(
                Const.CONF_EXCLUDE, default=INCLUDE_EXCLUDE_FILTER_SCHEMA_INNER({})
            ): INCLUDE_EXCLUDE_FILTER_SCHEMA_INNER,
        }
    )

    INCLUDE_EXCLUDE_FILTER_SCHEMA: typing.Final = vol.All(
        INCLUDE_EXCLUDE_BASE_FILTER_SCHEMA, _convert_include_exclude_filter
    )


def _glob_to_re(glob: str) -> re.Pattern[str]:
    """Translate and compile glob string into pattern."""
    return re.compile(fnmatch.translate(glob))


def _test_against_patterns(patterns: list[re.Pattern[str]], entity_id: str) -> bool:
    """Test entity against list of patterns, true if any match."""
    for pattern in patterns:
        if pattern.match(entity_id):
            return True

    return False


def _convert_globs_to_pattern_list(globs: list[str]) -> list[re.Pattern[str]]:
    """Convert a list of globs to a re pattern list."""
    return list(map(_glob_to_re, set(globs or [])))


def _generate_filter_from_sets_and_pattern_lists(
    include_d: set[str],
    include_e: set[str],
    exclude_d: set[str],
    exclude_e: set[str],
    include_eg: list[re.Pattern[str]],
    exclude_eg: list[re.Pattern[str]],
) -> collections.abc.Callable[[str], bool]:
    """Generate a filter from pre-computed sets and pattern lists."""
    have_exclude = bool(exclude_e or exclude_d or exclude_eg)
    have_include = bool(include_e or include_d or include_eg)

    def entity_included(domain: str, entity_id: str) -> bool:
        """Return true if entity matches inclusion filters."""
        return (
            entity_id in include_e
            or domain in include_d
            or bool(include_eg and _test_against_patterns(include_eg, entity_id))
        )

    def entity_excluded(domain: str, entity_id: str) -> bool:
        """Return true if entity matches exclusion filters."""
        return (
            entity_id in exclude_e
            or domain in exclude_d
            or bool(exclude_eg and _test_against_patterns(exclude_eg, entity_id))
        )

    # Case 1 - no includes or excludes - pass all entities
    if not have_include and not have_exclude:
        return lambda entity_id: True

    # Case 2 - includes, no excludes - only include specified entities
    if have_include and not have_exclude:

        def entity_filter_2(entity_id: str) -> bool:
            """Return filter function for case 2."""
            domain = helpers.split_entity_id(entity_id)[0]
            return entity_included(domain, entity_id)

        return entity_filter_2

    # Case 3 - excludes, no includes - only exclude specified entities
    if not have_include and have_exclude:

        def entity_filter_3(entity_id: str) -> bool:
            """Return filter function for case 3."""
            domain = helpers.split_entity_id(entity_id)[0]
            return not entity_excluded(domain, entity_id)

        return entity_filter_3

    # Case 4 - both includes and excludes specified
    # Case 4a - include domain or glob specified
    #  - if domain is included, pass if entity not excluded
    #  - if glob is included, pass if entity and domain not excluded
    #  - if domain and glob are not included, pass if entity is included
    # note: if both include domain matches then exclude domains ignored.
    #   If glob matches then exclude domains and glob checked
    if include_d or include_eg:

        def entity_filter_4a(entity_id: str) -> bool:
            """Return filter function for case 4a."""
            domain = helpers.split_entity_id(entity_id)[0]
            if domain in include_d:
                return not (
                    entity_id in exclude_e
                    or bool(
                        exclude_eg and _test_against_patterns(exclude_eg, entity_id)
                    )
                )
            if _test_against_patterns(include_eg, entity_id):
                return not entity_excluded(domain, entity_id)
            return entity_id in include_e

        return entity_filter_4a

    # Case 4b - exclude domain or glob specified, include has no domain or glob
    # In this one case the traditional include logic is inverted. Even though an
    # include is specified since its only a list of entity IDs its used only to
    # expose specific entities excluded by domain or glob. Any entities not
    # excluded are then presumed included. Logic is as follows
    #  - if domain or glob is excluded, pass if entity is included
    #  - if domain is not excluded, pass if entity not excluded by ID
    if exclude_d or exclude_eg:

        def entity_filter_4b(entity_id: str) -> bool:
            """Return filter function for case 4b."""
            domain = helpers.split_entity_id(entity_id)[0]
            if domain in exclude_d or (
                exclude_eg and _test_against_patterns(exclude_eg, entity_id)
            ):
                return entity_id in include_e
            return entity_id not in exclude_e

        return entity_filter_4b

    # Case 4c - neither include or exclude domain specified
    #  - Only pass if entity is included.  Ignore entity excludes.
    return lambda entity_id: entity_id in include_e


class EntityFilter:
    """A entity filter."""

    def __init__(self, config: dict[str, list[str]]) -> None:
        """Init the filter."""
        self.empty_filter: bool = sum(len(val) for val in config.values()) == 0
        self.config = config
        self._include_e = set(config[_Const.CONF_INCLUDE_ENTITIES])
        self._exclude_e = set(config[_Const.CONF_EXCLUDE_ENTITIES])
        self._include_d = set(config[_Const.CONF_INCLUDE_DOMAINS])
        self._exclude_d = set(config[_Const.CONF_EXCLUDE_DOMAINS])
        self._include_eg = _convert_globs_to_pattern_list(
            config[_Const.CONF_INCLUDE_ENTITY_GLOBS]
        )
        self._exclude_eg = _convert_globs_to_pattern_list(
            config[_Const.CONF_EXCLUDE_ENTITY_GLOBS]
        )
        self._filter: collections.abc.Callable[[str], bool] = None

    # pylint: disable=invalid-name
    Const: typing.TypeAlias = _Const

    def explicitly_included(self, entity_id: str) -> bool:
        """Check if an entity is explicitly included."""
        return entity_id in self._include_e or _test_against_patterns(
            self._include_eg, entity_id
        )

    def explicitly_excluded(self, entity_id: str) -> bool:
        """Check if an entity is explicitly excluded."""
        return entity_id in self._exclude_e or _test_against_patterns(
            self._exclude_eg, entity_id
        )

    def __call__(self, entity_id: str) -> bool:
        """Run the filter."""
        if self._filter is None:
            self._filter = _generate_filter_from_sets_and_pattern_lists(
                self._include_d,
                self._include_e,
                self._exclude_d,
                self._exclude_e,
                self._include_eg,
                self._exclude_eg,
            )
        return self._filter(entity_id)

    @staticmethod
    def convert_filter(config: dict[str, list[str]]):
        return _convert_filter(config)

    @staticmethod
    def convert_include_exclude_filter(config: dict[str, dict[str, list[str]]]):
        """Convert the include exclude filter schema into a filter."""
        return _convert_include_exclude_filter(config)

    @staticmethod
    def generate_filter(
        include_domains: list[str],
        include_entities: list[str],
        exclude_domains: list[str],
        exclude_entities: list[str],
        include_entity_globs: list[str] = None,
        exclude_entity_globs: list[str] = None,
    ) -> collections.abc.Callable[[str], bool]:
        """Return a function that will filter entities based on the args."""
        return _generate_filter_from_sets_and_pattern_lists(
            set(include_domains),
            set(include_entities),
            set(exclude_domains),
            set(exclude_entities),
            _convert_globs_to_pattern_list(include_entity_globs),
            _convert_globs_to_pattern_list(exclude_entity_globs),
        )
