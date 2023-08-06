"""
PyScript Component for Smart Home - The Next Generation.

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


This component is based on the custom_component

Pyscript: Python Scripting for Home Assistant, Copyright (c) 2020-2022 Craig Barrat,
which may be freely used and copied according tho the terms of the Apache 2.0 License.

Original source code and documentation can be found under:
https://github.com/custom-components/pyscript
"""

import typing


# pylint: disable=unused-variable
class Const:
    """pyscript-wide constants."""

    CONFIG_ENTRY: typing.Final = "config_entry"
    CONFIG_ENTRY_OLD: typing.Final = "config_entry_old"
    UNSUB_LISTENERS: typing.Final = "unsub_listeners"

    EVENT_PYSCRIPT_RUNNING: typing.Final = "pyscript.running"
    FOLDER: typing.Final = "pyscript"

    UNPINNED_VERSION: typing.Final = "_unpinned_version"

    ATTR_INSTALLED_VERSION: typing.Final = "installed_version"
    ATTR_SOURCES: typing.Final = "sources"
    ATTR_VERSION: typing.Final = "version"

    CONF_ALLOW_ALL_IMPORTS: typing.Final = "allow_all_imports"
    CONF_SHC_IS_GLOBAL: typing.Final = "shc_is_global"
    CONF_INSTALLED_PACKAGES: typing.Final = "_installed_packages"

    SERVICE_JUPYTER_KERNEL_START: typing.Final = "jupyter_kernel_start"

    REQUIREMENTS_FILE: typing.Final = "requirements.txt"
    REQUIREMENTS_PATHS: typing.Final = ("", "apps/*", "modules/*", "scripts/**")

    WATCHDOG_OBSERVER: typing.Final = "watch_dog_observer"
    WATCHDOG_TASK: typing.Final = "watch_dog_task"

    ALLOWED_IMPORTS: typing.Final = {
        "black",
        "cmath",
        "datetime",
        "decimal",
        "fractions",
        "smart_home_tng.core",
        "isort",
        "json",
        "math",
        "number",
        "random",
        "re",
        "sqlite3",
        "statistics",
        "string",
        "time",
        "typing",
        "voluptuous",
    }
    CONF_BOOL_ALL: typing.Final = {CONF_ALLOW_ALL_IMPORTS, CONF_SHC_IS_GLOBAL}
