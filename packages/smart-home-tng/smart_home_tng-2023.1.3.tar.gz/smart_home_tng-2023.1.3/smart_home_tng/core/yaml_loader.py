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

import collections
import fnmatch
import logging
import os
import typing

import yaml

from . import helpers
from .const import Const
from .input import Input
from .json_type import JsonType
from .node_list_class import NodeListClass
from .node_str_class import NodeStrClass
from .smart_home_controller_error import SmartHomeControllerError
from .undefined_substitution import UndefinedSubstitution

_LOGGER: typing.Final = logging.getLogger(__name__)


if not typing.TYPE_CHECKING:

    class Secrets:
        ...


if typing.TYPE_CHECKING:
    from .secrets import Secrets


# pylint: disable=unused-variable
class YamlLoader(yaml.SafeLoader):
    """Loader class that keeps track of line numbers."""

    def __init__(self, stream: typing.Any, secrets: Secrets = None) -> None:
        """Initialize a safe line loader."""
        super().__init__(stream)
        self._secrets = secrets

    def compose_node(self, parent: yaml.nodes.Node, index: int) -> yaml.nodes.Node:
        """Annotate a node with the first line it was seen."""
        last_line: int = self.line
        node: yaml.nodes.Node = super().compose_node(parent, index)
        node.__line__ = last_line + 1
        return node

    @staticmethod
    def load_yaml(fname: str, secrets: Secrets = None) -> JsonType:
        """Load a YAML file."""
        try:
            with open(fname, encoding="utf-8") as conf_file:
                return YamlLoader.parse_yaml(conf_file, secrets)
        except UnicodeDecodeError as exc:
            _LOGGER.error(f"Unable to read file {fname}: {exc}")
            raise SmartHomeControllerError(exc) from exc

    @staticmethod
    def parse_yaml(content: str | typing.TextIO, secrets: Secrets = None) -> JsonType:
        """Load a YAML file."""
        try:
            # If configuration file is empty YAML returns None
            # We convert that to an empty dict
            return (
                yaml.load(  # nosec
                    content, Loader=lambda stream: YamlLoader(stream, secrets)
                )
                or collections.OrderedDict()
            )
        except yaml.YAMLError as exc:
            _LOGGER.error(str(exc))
            raise SmartHomeControllerError(exc) from exc

    def _add_reference(self, obj, node: yaml.nodes.Node):
        """Add file reference information to an object."""
        if isinstance(obj, list):
            obj = NodeListClass(obj)
        if isinstance(obj, str):
            obj = NodeStrClass(obj)
        setattr(obj, "__config_file__", self.name)
        setattr(obj, "__line__", node.start_mark.line)
        return obj

    def _include_yaml(self, node: yaml.nodes.Node) -> JsonType:
        """Load another YAML file and embeds it using the !include tag.

        Example:
            device_tracker: !include device_tracker.yaml

        """
        fname = os.path.join(os.path.dirname(self.name), node.value)
        try:
            return self._add_reference(YamlLoader.load_yaml(fname, self._secrets), node)
        except FileNotFoundError as exc:
            raise SmartHomeControllerError(
                f"{node.start_mark}: Unable to read file {fname}."
            ) from exc

    @staticmethod
    def _is_file_valid(name: str) -> bool:
        """Decide if a file is valid."""
        return not name.startswith(".")

    @staticmethod
    def _find_files(directory: str, pattern: str) -> collections.abc.Iterator[str]:
        """Recursively load files in a directory."""
        for root, dirs, files in os.walk(directory, topdown=True):
            dirs[:] = [d for d in dirs if YamlLoader._is_file_valid(d)]
            for basename in sorted(files):
                if YamlLoader._is_file_valid(basename) and fnmatch.fnmatch(
                    basename, pattern
                ):
                    filename = os.path.join(root, basename)
                    yield filename

    def _include_dir_named_yaml(self, node: yaml.nodes.Node) -> collections.OrderedDict:
        """Load multiple files from directory as a dictionary."""
        mapping: collections.OrderedDict = collections.OrderedDict()
        loc = os.path.join(os.path.dirname(self.name), node.value)
        for fname in YamlLoader._find_files(loc, "*.yaml"):
            filename = os.path.splitext(os.path.basename(fname))[0]
            if os.path.basename(fname) == Const.SECRET_YAML:
                continue
            mapping[filename] = YamlLoader.load_yaml(fname, self._secrets)
        return self._add_reference(mapping, node)

    def _include_dir_merge_named_yaml(
        self, node: yaml.nodes.Node
    ) -> collections.OrderedDict:
        """Load multiple files from directory as a merged dictionary."""
        mapping: collections.OrderedDict = collections.OrderedDict()
        loc = os.path.join(os.path.dirname(self.name), node.value)
        for fname in YamlLoader._find_files(loc, "*.yaml"):
            if os.path.basename(fname) == Const.SECRET_YAML:
                continue
            loaded_yaml = YamlLoader.load_yaml(fname, self._secrets)
            if isinstance(loaded_yaml, dict):
                mapping.update(loaded_yaml)
        return self._add_reference(mapping, node)

    def _include_dir_list_yaml(self, node: yaml.nodes.Node) -> list[JsonType]:
        """Load multiple files from directory as a list."""
        loc = os.path.join(os.path.dirname(self.name), node.value)
        return [
            YamlLoader.load_yaml(f, self._secrets)
            for f in YamlLoader._find_files(loc, "*.yaml")
            if os.path.basename(f) != Const.SECRET_YAML
        ]

    def _include_dir_merge_list_yaml(self, node: yaml.nodes.Node) -> JsonType:
        """Load multiple files from directory as a merged list."""
        loc: str = os.path.join(os.path.dirname(self.name), node.value)
        merged_list: list[JsonType] = []
        for fname in YamlLoader._find_files(loc, "*.yaml"):
            if os.path.basename(fname) == Const.SECRET_YAML:
                continue
            loaded_yaml = YamlLoader.load_yaml(fname, self._secrets)
            if isinstance(loaded_yaml, list):
                merged_list.extend(loaded_yaml)
        return self._add_reference(merged_list, node)

    def _ordered_dict(self, node: yaml.nodes.MappingNode) -> collections.OrderedDict:
        """Load YAML mappings into an ordered dictionary to preserve key order."""
        self.flatten_mapping(node)
        nodes = self.construct_pairs(node)

        seen: dict = {}
        for (key, _), (child_node, _) in zip(nodes, node.value):
            line = child_node.start_mark.line

            try:
                hash(key)
            except TypeError as exc:
                fname = getattr(self.stream, "name", "")
                raise yaml.MarkedYAMLError(
                    context=f'invalid key: "{key}"',
                    context_mark=yaml.Mark(fname, 0, line, -1, None, None),
                ) from exc

            if key in seen:
                fname = getattr(self.stream, "name", "")
                _LOGGER.warning(
                    f"YAML file {fname} contains duplicate key '{key}'. "
                    + f"Check lines {seen[key]} and {line}"
                )
            seen[key] = line

        return self._add_reference(collections.OrderedDict(nodes), node)

    def _construct_seq(self, node: yaml.nodes.Node) -> JsonType:
        """Add line number and file name to Load YAML sequence."""
        (obj,) = self.construct_yaml_seq(node)
        return self._add_reference(obj, node)

    def _env_var_yaml(self, node: yaml.nodes.Node) -> str:
        """Load environment variables and embed it into the configuration YAML."""
        args = node.value.split()

        # Check for a default value
        if len(args) > 1:
            return os.getenv(args[0], " ".join(args[1:]))
        if args[0] in os.environ:
            return os.environ[args[0]]
        _LOGGER.error(f"Environment variable {node.value} not defined")
        raise SmartHomeControllerError(node.value)

    def _secret_yaml(self, node: yaml.nodes.Node) -> JsonType:
        """Load secrets and embed it into the configuration YAML."""
        if self._secrets is None:
            raise SmartHomeControllerError("Secrets not supported in this YAML file")
        return self._secrets.get(self.name, node.value)

    @staticmethod
    def __static_init__() -> None:
        YamlLoader.add_constructor("!include", YamlLoader._include_yaml)
        YamlLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, YamlLoader._ordered_dict
        )
        YamlLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_SEQUENCE_TAG, YamlLoader._construct_seq
        )
        YamlLoader.add_constructor("!env_var", YamlLoader._env_var_yaml)
        YamlLoader.add_constructor("!secret", YamlLoader._secret_yaml)
        YamlLoader.add_constructor(
            "!include_dir_list", YamlLoader._include_dir_list_yaml
        )
        YamlLoader.add_constructor(
            "!include_dir_merge_list", YamlLoader._include_dir_merge_list_yaml
        )
        YamlLoader.add_constructor(
            "!include_dir_named", YamlLoader._include_dir_named_yaml
        )
        YamlLoader.add_constructor(
            "!include_dir_merge_named", YamlLoader._include_dir_merge_named_yaml
        )
        YamlLoader.add_constructor("!input", Input.from_node)

    @staticmethod
    def substitute(obj: typing.Any, substitutions: dict[str, typing.Any]) -> typing.Any:
        """Substitute values."""
        if isinstance(obj, Input):
            if obj.name not in substitutions:
                raise UndefinedSubstitution(obj.name)
            return substitutions[obj.name]

        if isinstance(obj, list):
            return [YamlLoader.substitute(val, substitutions) for val in obj]

        if isinstance(obj, dict):
            return {
                key: YamlLoader.substitute(val, substitutions)
                for key, val in obj.items()
            }

        return obj

    @staticmethod
    def extract_inputs(obj: typing.Any) -> set[str]:
        """Extract input from a structure."""
        found: set[str] = set()
        _extract_inputs(obj, found)
        return found


def _extract_inputs(obj: typing.Any, found: set[str]) -> None:
    """Extract input from a structure."""
    if isinstance(obj, Input):
        found.add(obj.name)
        return

    if isinstance(obj, list):
        for val in obj:
            _extract_inputs(val, found)
        return

    if isinstance(obj, dict):
        for val in obj.values():
            _extract_inputs(val, found)
        return


helpers.block_async_io()
YamlLoader.__static_init__()
