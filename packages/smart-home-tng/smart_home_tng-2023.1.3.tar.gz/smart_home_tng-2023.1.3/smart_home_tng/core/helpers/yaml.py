"""
Helpers for Components of Smart Home - The Next Generation.

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

import collections

import yaml

from ..input import Input
from ..node_list_class import NodeListClass


def dump(_dict: dict) -> str:
    """Dump YAML to a string and remove null."""
    return yaml.safe_dump(
        _dict, default_flow_style=False, allow_unicode=True, sort_keys=False
    ).replace(": null\n", ":\n")


# pylint: disable=unused-variable
def save_yaml(path: str, data: dict) -> None:
    """Save YAML to a file."""
    # Dump before writing to not truncate the file if dumping fails
    str_data = dump(data)
    with open(path, "w", encoding="utf-8") as outfile:
        outfile.write(str_data)


# From: https://gist.github.com/miracle2k/3184458
def represent_odict(
    dumper: yaml.SafeDumper, tag: str, mapping, flow_style=None
) -> yaml.MappingNode:
    """Like BaseRepresenter.represent_mapping but does not issue the sort()."""
    value: list = []
    node = yaml.MappingNode(tag, value, flow_style=flow_style)
    if dumper.alias_key is not None:
        dumper.represented_objects[dumper.alias_key] = node
    best_style = True
    if hasattr(mapping, "items"):
        mapping = mapping.items()
    for item_key, item_value in mapping:
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)
        if not (isinstance(node_key, yaml.ScalarNode) and not node_key.style):
            best_style = False
        if not (isinstance(node_value, yaml.ScalarNode) and not node_value.style):
            best_style = False
        value.append((node_key, node_value))
    if flow_style is None:
        if dumper.default_flow_style is not None:
            node.flow_style = dumper.default_flow_style
        else:
            node.flow_style = best_style
    return node


yaml.SafeDumper.add_representer(
    collections.OrderedDict,
    lambda dumper, value: represent_odict(dumper, "tag:yaml.org,2002:map", value),
)

yaml.SafeDumper.add_representer(
    NodeListClass,
    lambda dumper, value: dumper.represent_sequence("tag:yaml.org,2002:seq", value),
)

yaml.SafeDumper.add_representer(
    Input,
    lambda dumper, value: dumper.represent_scalar("!input", value.name),
)
