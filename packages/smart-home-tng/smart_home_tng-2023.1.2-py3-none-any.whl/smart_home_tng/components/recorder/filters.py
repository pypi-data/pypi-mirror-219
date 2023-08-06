"""
Recorder Component for Smart Home - The Next Generation.

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

# pylint: disable=unused-variable

import json
import typing
import collections.abc
import sqlalchemy as sql
import sqlalchemy.sql.elements as sql_elements

from ... import core
from . import model
from .model import _ENTITY_ID_IN_EVENT, _OLD_ENTITY_ID_IN_EVENT

_JSON_NULL: typing.Final = json.dumps(None)

_GLOB_TO_SQL_CHARS: typing.Final = {
    ord("*"): "%",
    ord("?"): "_",
    ord("%"): "\\%",
    ord("_"): "\\_",
    ord("\\"): "\\\\",
}

_FILTER_TYPES: typing.Final = (core.Const.CONF_EXCLUDE, core.Const.CONF_INCLUDE)
_FILTER_MATCHERS = (
    core.Const.CONF_ENTITIES,
    core.Const.CONF_DOMAINS,
    core.EntityFilter.Const.CONF_ENTITY_GLOBS,
)


def extract_include_exclude_filter_conf(conf: core.ConfigType) -> dict[str, typing.Any]:
    """Extract an include exclude filter from configuration.

    This makes a copy so we do not alter the original data.
    """
    return {
        filter_type: {
            matcher: set(conf.get(filter_type, {}).get(matcher) or [])
            for matcher in _FILTER_MATCHERS
        }
        for filter_type in _FILTER_TYPES
    }


def merge_include_exclude_filters(
    base_filter: dict[str, typing.Any], add_filter: dict[str, typing.Any]
) -> dict[str, typing.Any]:
    """Merge two filters.

    This makes a copy so we do not alter the original data.
    """
    return {
        filter_type: {
            matcher: base_filter[filter_type][matcher]
            | add_filter[filter_type][matcher]
            for matcher in _FILTER_MATCHERS
        }
        for filter_type in _FILTER_TYPES
    }


class Filters(core.RecorderFiltersBase):
    """Container for the configured include and exclude filters."""

    def __init__(self) -> None:
        """Initialise the include and exclude filters."""
        self._excluded_entities: collections.abc.Iterable[str] = []
        self._excluded_domains: collections.abc.Iterable[str] = []
        self._excluded_entity_globs: collections.abc.Iterable[str] = []

        self._included_entities: collections.abc.Iterable[str] = []
        self._included_domains: collections.abc.Iterable[str] = []
        self._included_entity_globs: collections.abc.Iterable[str] = []

    def __repr__(self) -> str:
        """Return human readable excludes/includes."""
        return (
            f"<Filters excluded_entities={self._excluded_entities} "
            + f"excluded_domains={self._excluded_domains} "
            + f"excluded_entity_globs={self._excluded_entity_globs} "
            + f"included_entities={self._included_entities} "
            + f"included_domains={self._included_domains} "
            + f"included_entity_globs={self._included_entity_globs}>"
        )

    @property
    def excluded_entities(self) -> collections.abc.Iterable[str]:
        return self._excluded_entities

    @property
    def excluded_domains(self) -> collections.abc.Iterable[str]:
        return self._excluded_domains

    @property
    def excluded_entity_globs(self) -> collections.abc.Iterable[str]:
        return self._excluded_entity_globs

    @property
    def included_entities(self) -> collections.abc.Iterable[str]:
        return self._included_entities

    @property
    def included_domains(self) -> collections.abc.Iterable[str]:
        return self._included_domains

    @property
    def included_entity_globs(self) -> collections.abc.Iterable[str]:
        return self._included_entity_globs

    @property
    def has_config(self) -> bool:
        """Determine if there is any filter configuration."""
        return bool(self._have_exclude or self._have_include)

    @property
    def _have_exclude(self) -> bool:
        return bool(
            self._excluded_entities
            or self._excluded_domains
            or self._excluded_entity_globs
        )

    @property
    def _have_include(self) -> bool:
        return bool(
            self._included_entities
            or self._included_domains
            or self._included_entity_globs
        )

    def _generate_filter_for_columns(
        self,
        columns: collections.abc.Iterable[sql.Column],
        encoder: collections.abc.Callable[[typing.Any], typing.Any],
    ) -> sql_elements.ClauseList:
        """Generate a filter from pre-computed sets and pattern lists.

        This must match exactly how homeassistant.helpers.entityfilter works.
        """
        i_domains = _domain_matcher(self.included_domains, columns, encoder)
        i_entities = _entity_matcher(self.included_entities, columns, encoder)
        i_entity_globs = _globs_to_like(self.included_entity_globs, columns, encoder)
        includes = [i_domains, i_entities, i_entity_globs]

        e_domains = _domain_matcher(self.excluded_domains, columns, encoder)
        e_entities = _entity_matcher(self.excluded_entities, columns, encoder)
        e_entity_globs = _globs_to_like(self.excluded_entity_globs, columns, encoder)
        excludes = [e_domains, e_entities, e_entity_globs]

        have_exclude = self._have_exclude
        have_include = self._have_include

        # Case 1 - no includes or excludes - pass all entities
        if not have_include and not have_exclude:
            return None

        # Case 2 - includes, no excludes - only include specified entities
        if have_include and not have_exclude:
            return sql.or_(*includes).self_group()

        # Case 3 - excludes, no includes - only exclude specified entities
        if not have_include and have_exclude:
            return sql.not_(sql.or_(*excludes).self_group())

        # Case 4 - both includes and excludes specified
        # Case 4a - include domain or glob specified
        #  - if domain is included, pass if entity not excluded
        #  - if glob is included, pass if entity and domain not excluded
        #  - if domain and glob are not included, pass if entity is included
        # note: if both include domain matches then exclude domains ignored.
        #   If glob matches then exclude domains and glob checked
        if self.included_domains or self.included_entity_globs:
            return sql.or_(
                (i_domains & ~(e_entities | e_entity_globs)),
                (
                    ~i_domains
                    & sql.or_(
                        (i_entity_globs & ~(sql.or_(*excludes))),
                        (~i_entity_globs & i_entities),
                    )
                ),
            ).self_group()

        # Case 4b - exclude domain or glob specified, include has no domain or glob
        # In this one case the traditional include logic is inverted. Even though an
        # include is specified since its only a list of entity IDs its used only to
        # expose specific entities excluded by domain or glob. Any entities not
        # excluded are then presumed included. Logic is as follows
        #  - if domain or glob is excluded, pass if entity is included
        #  - if domain is not excluded, pass if entity not excluded by ID
        if self.excluded_domains or self.excluded_entity_globs:
            return (sql.not_(sql.or_(*excludes)) | i_entities).self_group()

        # Case 4c - neither include or exclude domain specified
        #  - Only pass if entity is included.  Ignore entity excludes.
        return i_entities

    def states_entity_filter(self) -> sql_elements.ClauseList:
        """Generate the entity filter query."""

        def _encoder(data: typing.Any) -> typing.Any:
            """Nothing to encode for states since there is no json."""
            return data

        return self._generate_filter_for_columns((model.States.entity_id,), _encoder)

    def events_entity_filter(self) -> sql_elements.ClauseList:
        """Generate the entity filter query."""
        _encoder = json.dumps
        return sql.or_(
            # sqlalchemy's SQLite json implementation always
            # wraps everything with JSON_QUOTE so it resolves to 'null'
            # when its empty
            #
            # For MySQL and PostgreSQL it will resolve to a literal
            # NULL when its empty
            #
            ((_ENTITY_ID_IN_EVENT == _JSON_NULL) | _ENTITY_ID_IN_EVENT.is_(None))
            & (
                (_OLD_ENTITY_ID_IN_EVENT == _JSON_NULL)
                | _OLD_ENTITY_ID_IN_EVENT.is_(None)
            ),
            self._generate_filter_for_columns(
                (_ENTITY_ID_IN_EVENT, _OLD_ENTITY_ID_IN_EVENT), _encoder
            ).self_group(),
        )


def _globs_to_like(
    glob_strs: collections.abc.Iterable[str],
    columns: collections.abc.Iterable[sql.Column],
    encoder: collections.abc.Callable[[typing.Any], typing.Any],
) -> sql_elements.ClauseList:
    """Translate glob to sql."""
    matchers = [
        (
            column.is_not(None)
            & sql.cast(column, sql.Text()).like(
                encoder(glob_str).translate(_GLOB_TO_SQL_CHARS), escape="\\"
            )
        )
        for glob_str in glob_strs
        for column in columns
    ]
    return sql.or_(*matchers) if matchers else sql.or_(False)


def _entity_matcher(
    entity_ids: collections.abc.Iterable[str],
    columns: collections.abc.Iterable[sql.Column],
    encoder: collections.abc.Callable[[typing.Any], typing.Any],
) -> sql_elements.ClauseList:
    matchers = [
        (
            column.is_not(None)
            & sql.cast(column, sql.Text()).in_(
                [encoder(entity_id) for entity_id in entity_ids]
            )
        )
        for column in columns
    ]
    return sql.or_(*matchers) if matchers else sql.or_(False)


def _domain_matcher(
    domains: collections.abc.Iterable[str],
    columns: collections.abc.Iterable[sql.Column],
    encoder: collections.abc.Callable[[typing.Any], typing.Any],
) -> sql_elements.ClauseList:
    matchers = [
        (
            column.is_not(None)
            & sql.cast(column, sql.Text()).like(encoder(f"{domain}.%"))
        )
        for domain in domains
        for column in columns
    ]
    return sql.or_(*matchers) if matchers else sql.or_(False)


def sqlalchemy_filter_from_include_exclude_conf(conf: core.ConfigType) -> Filters:
    """Build a sql filter from config."""
    filters = Filters()
    if exclude := conf.get(core.Const.CONF_EXCLUDE):
        filters.excluded_entities = exclude.get(core.Const.CONF_ENTITIES, [])
        filters.excluded_domains = exclude.get(core.Const.CONF_DOMAINS, [])
        filters.excluded_entity_globs = exclude.get(
            core.EntityFilter.Const.CONF_ENTITY_GLOBS, []
        )
    if include := conf.get(core.Const.CONF_INCLUDE):
        filters.included_entities = include.get(core.Const.CONF_ENTITIES, [])
        filters.included_domains = include.get(core.Const.CONF_DOMAINS, [])
        filters.included_entity_globs = include.get(
            core.EntityFilter.Const.CONF_ENTITY_GLOBS, []
        )

    return filters if filters.has_config else None
