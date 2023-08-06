"""
Permission Layer for Smart Home - The Next Generation.

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

import collections
import collections.abc
import functools
import typing
import voluptuous as vol

from .category_type import CategoryType
from .const import Const
from .permission_lookup import PermissionLookup
from .policy_type import PolicyType
from .sub_category_dict import SubCategoryDict
from .value_type import ValueType

LookupFunc = collections.abc.Callable[
    [PermissionLookup, SubCategoryDict, str], typing.Optional[ValueType]
]
SubCatLookupType = dict[str, LookupFunc]


def lookup_all(
    _perm_lookup: PermissionLookup, lookup_dict: SubCategoryDict, _object_id: str
) -> ValueType:
    """Look up permission for all."""
    # In case of ALL category, lookup_dict IS the schema.
    return typing.cast(ValueType, lookup_dict)


def compile_policy(
    policy: CategoryType, subcategories: SubCatLookupType, perm_lookup: PermissionLookup
) -> collections.abc.Callable[[str, str], bool]:
    """Compile policy into a function that tests policy.

    Subcategories are mapping key -> lookup function, ordered by highest
    priority first.
    """
    # None, False, empty dict
    if not policy:

        def apply_policy_deny_all(_entity_id: str, _key: str) -> bool:
            """Decline all."""
            return False

        return apply_policy_deny_all

    if policy is True:

        def apply_policy_allow_all(_entity_id: str, _key: str) -> bool:
            """Approve all."""
            return True

        return apply_policy_allow_all

    assert isinstance(policy, dict)

    funcs: list[collections.abc.Callable[[str, str], bool]] = []

    for key, lookup_func in subcategories.items():
        lookup_value = policy.get(key)

        # If any lookup value is `True`, it will always be positive
        if isinstance(lookup_value, bool):
            return lambda object_id, key: True

        if lookup_value is not None:
            funcs.append(_gen_dict_test_func(perm_lookup, lookup_func, lookup_value))

    if len(funcs) == 1:
        func = funcs[0]

        @functools.wraps(func)
        def apply_policy_func(object_id: str, key: str) -> bool:
            """Apply a single policy function."""
            return func(object_id, key) is True

        return apply_policy_func

    def apply_policy_funcs(object_id: str, key: str) -> bool:
        """Apply several policy functions."""
        for func in funcs:
            if (result := func(object_id, key)) is not None:
                return result
        return False

    return apply_policy_funcs


def _gen_dict_test_func(
    perm_lookup: PermissionLookup, lookup_func: LookupFunc, lookup_dict: SubCategoryDict
) -> collections.abc.Callable[[str, str], bool]:
    """Generate a lookup function."""

    def test_value(object_id: str, key: str) -> bool:
        """Test if permission is allowed based on the keys."""
        schema: ValueType = lookup_func(perm_lookup, lookup_dict, object_id)

        if schema is None or isinstance(schema, bool):
            return schema

        assert isinstance(schema, dict)

        return schema.get(key)

    return test_value


def test_all(policy: CategoryType, key: str) -> bool:
    """Test if a policy has an ALL access for a specific key."""
    if not isinstance(policy, dict):
        return bool(policy)

    all_policy = policy.get(Const.SUBCAT_ALL)

    if not isinstance(all_policy, dict):
        return bool(all_policy)

    return all_policy.get(key, False)


def merge_policies(policies: list[PolicyType]) -> PolicyType:
    """Merge policies."""
    new_policy: dict[str, CategoryType] = {}
    seen: set[str] = set()
    for policy in policies:
        for category in policy:
            if category in seen:
                continue
            seen.add(category)
            new_policy[category] = _merge_policies(
                [policy.get(category) for policy in policies]
            )
    typing.cast(PolicyType, new_policy)
    return new_policy


def _merge_policies(sources: list[CategoryType]) -> CategoryType:
    """Merge a policy."""
    # When merging policies, the most permissive wins.
    # This means we order it like this:
    # True > Dict > None
    #
    # True: allow everything
    # Dict: specify more granular permissions
    # None: no opinion
    #
    # If there are multiple sources with a dict as policy, we recursively
    # merge each key in the source.

    policy: CategoryType = None
    seen: set[str] = set()
    for source in sources:
        if source is None:
            continue

        # A source that's True will always win. Shortcut return.
        if source is True:
            return True

        assert isinstance(source, dict)

        if policy is None:
            policy = typing.cast(CategoryType, {})

        assert isinstance(policy, dict)

        for key in source:
            if key in seen:
                continue
            seen.add(key)

            key_sources = []
            for src in sources:
                if isinstance(src, dict):
                    key_sources.append(src.get(key))

            policy[key] = _merge_policies(key_sources)

    return policy


_SINGLE_ENTITY_SCHEMA: typing.Final = vol.Any(
    True,
    vol.Schema(
        {
            vol.Optional(Const.POLICY_READ): True,
            vol.Optional(Const.POLICY_CONTROL): True,
            vol.Optional(Const.POLICY_EDIT): True,
        }
    ),
)

_ENTITY_DOMAINS: typing.Final = "domains"
_ENTITY_AREAS: typing.Final = "area_ids"
_ENTITY_DEVICE_IDS: typing.Final = "device_ids"
_ENTITY_ENTITY_IDS: typing.Final = "entity_ids"

_ENTITY_VALUES_SCHEMA: typing.Final = vol.Any(
    True, vol.Schema({str: _SINGLE_ENTITY_SCHEMA})
)

_ENTITY_POLICY_SCHEMA: typing.Final = vol.Any(
    True,
    vol.Schema(
        {
            vol.Optional(Const.SUBCAT_ALL): _SINGLE_ENTITY_SCHEMA,
            vol.Optional(_ENTITY_AREAS): _ENTITY_VALUES_SCHEMA,
            vol.Optional(_ENTITY_DEVICE_IDS): _ENTITY_VALUES_SCHEMA,
            vol.Optional(_ENTITY_DOMAINS): _ENTITY_VALUES_SCHEMA,
            vol.Optional(_ENTITY_ENTITY_IDS): _ENTITY_VALUES_SCHEMA,
        }
    ),
)


def _lookup_domain(
    _perm_lookup: PermissionLookup, domains_dict: SubCategoryDict, entity_id: str
) -> ValueType:
    """Look up entity permissions by domain."""
    return domains_dict.get(entity_id.split(".", 1)[0])


def _lookup_area(
    perm_lookup: PermissionLookup, area_dict: SubCategoryDict, entity_id: str
) -> ValueType:
    """Look up entity permissions by area."""
    entity_entry = perm_lookup.entity_registry.async_get(entity_id)

    if entity_entry is None or entity_entry.device_id is None:
        return None

    device_entry = perm_lookup.device_registry.async_get(entity_entry.device_id)

    if device_entry is None or device_entry.area_id is None:
        return None

    return area_dict.get(device_entry.area_id)


def _lookup_device(
    perm_lookup: PermissionLookup, devices_dict: SubCategoryDict, entity_id: str
) -> ValueType:
    """Look up entity permissions by device."""
    entity_entry = perm_lookup.entity_registry.async_get(entity_id)

    if entity_entry is None or entity_entry.device_id is None:
        return None

    return devices_dict.get(entity_entry.device_id)


def _lookup_entity_id(
    _perm_lookup: PermissionLookup, entities_dict: SubCategoryDict, entity_id: str
) -> ValueType:
    """Look up entity permission by entity id."""
    return entities_dict.get(entity_id)


def compile_entities(
    policy: CategoryType, perm_lookup: PermissionLookup
) -> collections.abc.Callable[[str, str], bool]:
    """Compile policy into a function that tests policy."""
    subcategories: SubCatLookupType = collections.OrderedDict()
    subcategories[_ENTITY_ENTITY_IDS] = _lookup_entity_id
    subcategories[_ENTITY_DEVICE_IDS] = _lookup_device
    subcategories[_ENTITY_AREAS] = _lookup_area
    subcategories[_ENTITY_DOMAINS] = _lookup_domain
    subcategories[Const.SUBCAT_ALL] = lookup_all

    return compile_policy(policy, subcategories, perm_lookup)
