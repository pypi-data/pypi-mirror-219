"""
Smart Home - The Next Generation command line scripts..

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

import argparse
import asyncio
import collections.abc
import importlib
import logging
import os
import sys

from smart_home_tng.core.setup_manager import SetupManager

from ..core.the_next_generation import TheNextGeneration
from ..core.event_loop_policy import EventLoopPolicy


# pylint: disable=unused-variable
def run(args: list[str]) -> int:
    """Run a script."""
    scripts = []
    path = os.path.dirname(__file__)
    for fil in os.listdir(path):
        if fil == "__pycache__":
            continue

        if os.path.isdir(os.path.join(path, fil)):
            scripts.append(fil)
        elif fil != "__init__.py" and fil.endswith(".py"):
            scripts.append(fil[:-3])

    if not args:
        print("Please specify a script to run.")
        print("Available scripts:", ", ".join(scripts))
        return 1

    if args[0] not in scripts:
        print("Invalid script specified.")
        print("Available scripts:", ", ".join(scripts))
        return 1

    script = importlib.import_module(f"smart_home_tng.scripts.{args[0]}")

    config_dir = _extract_config_dir()

    loop = asyncio.get_event_loop()

    current_shc = TheNextGeneration.current()
    if current_shc is None:
        current_shc = TheNextGeneration()
        current_shc.config.config_dir = config_dir

    if not current_shc.is_virtual_env():
        loop.run_until_complete(current_shc.setup.async_mount_local_lib_path())

    _pip_kwargs = current_shc.setup.pip_kwargs()

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    for req in getattr(script, "REQUIREMENTS", []):
        if current_shc.setup.is_installed(req):
            continue

        if not current_shc.setup.install_package(req, **_pip_kwargs):
            print("Aborting script, could not install dependency", req)
            return 1

    asyncio.set_event_loop_policy(EventLoopPolicy(False))

    return script.run(args[1:])


def _extract_config_dir(args: collections.abc.Sequence[str] = None) -> str:
    """Extract the config dir from the arguments or get the default."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-c", "--config", default=None)
    parsed_args = parser.parse_known_args(args)[0]
    return (
        os.path.join(os.getcwd(), parsed_args.config)
        if parsed_args.config
        else SetupManager.get_default_config_dir()
    )
