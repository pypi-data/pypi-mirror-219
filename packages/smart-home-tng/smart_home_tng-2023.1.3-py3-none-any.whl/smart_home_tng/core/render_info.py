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
import datetime
import threading
import typing

from . import helpers
from .template_error import TemplateError

if not typing.TYPE_CHECKING:

    class Template:
        ...


if typing.TYPE_CHECKING:
    from .template import Template


# pylint: disable=unused-variable
class RenderInfo:
    """Holds information about a template render."""

    _active_instance: threading.local = threading.local()

    _ALL_STATES_RATE_LIMIT: typing.Final = datetime.timedelta(minutes=1)
    _DOMAIN_STATES_RATE_LIMIT: typing.Final = datetime.timedelta(seconds=1)

    @staticmethod
    def _true(_arg: str) -> bool:
        return True

    @staticmethod
    def _false(_arg: str) -> bool:
        return False

    @staticmethod
    def current():
        try:
            return RenderInfo._active_instance.instance
        except AttributeError:
            return None

    def __init__(self, template: Template) -> None:
        """Initialise."""

        RenderInfo._active_instance.instance = self
        self._template = template
        # Will be set sensibly once frozen.
        self._filter_lifecycle: typing.Callable[[str], bool] = RenderInfo._true
        self._filter: typing.Callable[[str], bool] = RenderInfo._true
        self._result: str = None
        self._is_static = False
        self._exception: TemplateError = None
        self._all_states = False
        self._all_states_lifecycle = False
        self._domains: collections.abc.Set[str] = set()
        self._domains_lifecycle: collections.abc.Set[str] = set()
        self._entities: collections.abc.Set[str] = set()
        self._rate_limit: datetime.timedelta = None
        self._has_time = False

    def __repr__(self) -> str:
        """Representation of RenderInfo."""
        result = (
            f"<RenderInfo {self._template} all_states={self._all_states} "
            + f"all_states_lifecycle={self._all_states_lifecycle} domains={self._domains} "
            + f"domains_lifecycle={self._domains_lifecycle} entities={self._entities} "
            + f"rate_limit={self._rate_limit}> has_time={self._has_time}"
        )
        return result

    def _filter_domains_and_entities(self, entity_id: str) -> bool:
        """
        Template should re-render if the entity state changes when
        we match specific domains or entities.
        """
        return (
            helpers.split_entity_id(entity_id)[0] in self._domains
            or entity_id in self._entities
        )

    def _filter_entities(self, entity_id: str) -> bool:
        """
        Template should re-render if the entity state changes when
        we match specific entities.
        """
        return entity_id in self._entities

    def _filter_lifecycle_domains(self, entity_id: str) -> bool:
        """Template should re-render if the entity is added or removed with domains watched."""
        return helpers.split_entity_id(entity_id)[0] in self._domains_lifecycle

    def result(self) -> str:
        """Results of the template computation."""
        if self._exception is not None:
            raise self._exception  # pylint: disable=raising-bad-type
        return typing.cast(str, self._result)

    def set_result(self, render_result: typing.Any):
        """Store the result of the rendering."""
        if isinstance(render_result, TemplateError):
            self._exception = render_result
        else:
            self._result = render_result

    def set_static_result(self, static_result: str):
        """No rendering required for static templates."""
        self._result = static_result
        self._freeze_static()

    def _freeze_static(self) -> None:
        self._active_instance.instance = None
        self._is_static = True
        self._freeze_sets()
        self._all_states = False

    def _freeze_sets(self) -> None:
        self._entities = frozenset(self._entities)
        self._domains = frozenset(self._domains)
        self._domains_lifecycle = frozenset(self._domains_lifecycle)

    def freeze(self) -> None:
        """Freeze the result of the template rendering."""
        self._active_instance.instance = None
        self._freeze_sets()

        if self._rate_limit is None:
            if self._all_states or self._exception:
                self._rate_limit = RenderInfo._ALL_STATES_RATE_LIMIT
            elif self._domains or self._domains_lifecycle:
                self._rate_limit = RenderInfo._DOMAIN_STATES_RATE_LIMIT

        if self._exception:
            return

        if not self._all_states_lifecycle:
            if self._domains_lifecycle:
                self._filter_lifecycle = self._filter_lifecycle_domains
            else:
                self._filter_lifecycle = RenderInfo._false

        if self._all_states:
            return

        if self._domains:
            self._filter = self._filter_domains_and_entities
        elif self._entities:
            self._filter = self._filter_entities
        else:
            self._filter = RenderInfo._false

    def add_domain(self, domain: str):
        if bool(domain):
            self._domains.add(domain)

    def add_domain_lifecycle(self, domain: str):
        if bool(domain):
            self._domains_lifecycle.add(domain)

    def add_entity(self, entity_id: str):
        if bool(entity_id):
            self._entities.add(entity_id)

    def collect_all_states(self):
        self._all_states = True

    def collect_all_states_lifecycle(self):
        self._all_states_lifecycle = True

    @property
    def exception(self) -> TemplateError:
        return self._exception

    @property
    def all_states(self) -> bool:
        return self._all_states

    @property
    def all_states_lifecycle(self) -> bool:
        return self._all_states_lifecycle

    @property
    def domains(self) -> collections.abc.Set[str]:
        return self._domains

    @property
    def domains_lifecycle(self) -> collections.abc.Set[str]:
        return self._domains_lifecycle

    @property
    def entities(self) -> collections.abc.Set[str]:
        return self._entities

    @property
    def rate_limit(self) -> datetime.timedelta:
        return self._rate_limit

    @property
    def has_time(self) -> bool:
        return self._has_time

    @property
    def filter(self) -> typing.Callable[[str], bool]:
        return self._filter

    @property
    def filter_lifecycle(self) -> typing.Callable[[str], bool]:
        return self._filter_lifecycle
