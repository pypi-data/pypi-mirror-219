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

import enum
import typing
import voluptuous as vol

from ... import core
from ...backports import strenum

_cv: typing.TypeAlias = core.ConfigValidation


# pylint: disable=unused-variable
class Const:
    """Recorder constants."""

    SQLITE_URL_PREFIX: typing.Final = "sqlite+pysqlite:///"
    MYSQLDB_URL_PREFIX: typing.Final = "mysql://"

    CONF_DB_INTEGRITY_CHECK: typing.Final = "db_integrity_check"

    MAX_QUEUE_BACKLOG: typing.Final = 40000

    # The maximum number of rows (events) we purge in one delete statement

    # sqlite3 has a limit of 999 until version 3.32.0
    # in https://github.com/sqlite/sqlite/commit/efdba1a8b3c6c967e7fae9c1989c40d420ce64cc
    # We can increase this back to 1000 once most
    # have upgraded their sqlite version
    MAX_ROWS_TO_PURGE: typing.Final = 998

    DB_WORKER_PREFIX: typing.Final = "DbWorker"

    ALL_DOMAIN_EXCLUDE_ATTRS: typing.Final = {
        core.Const.ATTR_ATTRIBUTION,
        core.Const.ATTR_RESTORED,
        core.Const.ATTR_SUPPORTED_FEATURES,
    }

    ATTR_KEEP_DAYS: typing.Final = "keep_days"
    ATTR_REPACK: typing.Final = "repack"
    ATTR_APPLY_FILTER: typing.Final = "apply_filter"

    KEEPALIVE_TIME: typing.Final = 30

    POOL_SIZE: typing.Final = 5

    EXCLUDE_ATTRIBUTES: typing.Final = "recorder.exclude_attributes_by_domain"
    BACKUP_DIR: typing.Final = ".backup"

    class SupportedDialect(strenum.LowercaseStrEnum):
        """Supported dialects."""

        SQLITE = enum.auto()
        MYSQL = enum.auto()
        POSTGRESQL = enum.auto()

    DEFAULT_URL: typing.Final = "sqlite+pysqlite:///{shc_config_path}"
    DEFAULT_DB_FILE: typing.Final = "smart_home_tng.db"
    DEFAULT_DB_INTEGRITY_CHECK: typing.Final = True
    DEFAULT_DB_MAX_RETRIES: typing.Final = 10
    DEFAULT_DB_RETRY_WAIT: typing.Final = 3
    DEFAULT_COMMIT_INTERVAL: typing.Final = 1

    CONF_AUTO_PURGE: typing.Final = "auto_purge"
    CONF_AUTO_REPACK: typing.Final = "auto_repack"
    CONF_DB_URL: typing.Final = "db_url"
    CONF_DB_MAX_RETRIES: typing.Final = "db_max_retries"
    CONF_DB_RETRY_WAIT: typing.Final = "db_retry_wait"
    CONF_PURGE_KEEP_DAYS: typing.Final = "purge_keep_days"
    CONF_PURGE_INTERVAL: typing.Final = "purge_interval"
    CONF_EVENT_TYPES: typing.Final = "event_types"
    CONF_COMMIT_INTERVAL: typing.Final = "commit_interval"

    EXCLUDE_SCHEMA: typing.Final = (
        core.EntityFilter.Const.INCLUDE_EXCLUDE_FILTER_SCHEMA_INNER.extend(
            {vol.Optional(CONF_EVENT_TYPES): vol.All(_cv.ensure_list, [_cv.string])}
        )
    )

    FILTER_SCHEMA: typing.Final = (
        core.EntityFilter.Const.INCLUDE_EXCLUDE_BASE_FILTER_SCHEMA.extend(
            {
                vol.Optional(
                    core.Const.CONF_EXCLUDE, default=EXCLUDE_SCHEMA({})
                ): EXCLUDE_SCHEMA
            }
        )
    )

    ALLOW_IN_MEMORY_DB: typing.Final = False
