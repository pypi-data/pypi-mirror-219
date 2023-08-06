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

import asyncio
import collections.abc
import datetime as dt
import logging
import typing
import urllib.parse

import sqlalchemy as sql
import sqlalchemy.orm as sql_orm
import voluptuous as vol

from ... import core
from . import filters as recorder_filters
from . import history, model, queries, services, statistics, task, util
from .const import Const
from .queries.common import _PSEUDO_EVENT_STATE_CHANGED
from .recorder import Recorder

_cv: typing.TypeAlias = core.ConfigValidation
_statistic: typing.TypeAlias = core.Statistic

_T = typing.TypeVar("_T")
_LOGGER: typing.Final = logging.getLogger(__name__)
_PLATFORMS: typing.Final = dict[str, core.RecorderPlatform]()

_UNIT_SCHEMA: typing.Final = vol.Schema(
    {
        vol.Optional("data_rate"): vol.In(core.DataRateConverter.VALID_UNITS),
        vol.Optional("distance"): vol.In(core.DistanceConverter.VALID_UNITS),
        vol.Optional("electric_current"): vol.In(
            core.ElectricCurrentConverter.VALID_UNITS
        ),
        vol.Optional("voltage"): vol.In(core.ElectricPotentialConverter.VALID_UNITS),
        vol.Optional("energy"): vol.In(core.EnergyConverter.VALID_UNITS),
        vol.Optional("information"): vol.In(core.InformationConverter.VALID_UNITS),
        vol.Optional("mass"): vol.In(core.MassConverter.VALID_UNITS),
        vol.Optional("power"): vol.In(core.PowerConverter.VALID_UNITS),
        vol.Optional("pressure"): vol.In(core.PressureConverter.VALID_UNITS),
        vol.Optional("speed"): vol.In(core.SpeedConverter.VALID_UNITS),
        vol.Optional("temperature"): vol.In(core.TemperatureConverter.VALID_UNITS),
        vol.Optional("unitless"): vol.In(core.UnitlessRatioConverter.VALID_UNITS),
        vol.Optional("volume"): vol.In(core.VolumeConverter.VALID_UNITS),
    }
)

_LIST_STATISTICS: typing.Final = {
    vol.Required("type"): "recorder/list_statistic_ids",
    vol.Optional("statistic_type"): vol.Any("sum", "mean"),
}
_VALIDATE_STATISTICS: typing.Final = {
    vol.Required("type"): "recorder/validate_statistics",
}
_CLEAR_STATISTICS: typing.Final = {
    vol.Required("type"): "recorder/clear_statistics",
    vol.Required("statistic_ids"): [str],
}
_STATISTICS_DURING_PERIOD: typing.Final = {
    vol.Required("type"): "recorder/statistics_during_period",
    vol.Required("start_time"): str,
    vol.Optional("end_time"): str,
    vol.Required("statistic_ids"): vol.All([str], vol.Length(min=1)),
    vol.Required("period"): vol.Any("5minute", "hour", "day", "week", "month"),
    vol.Optional("units"): _UNIT_SCHEMA,
    vol.Optional("types"): vol.All(
        [vol.Any("change", "last_reset", "max", "mean", "min", "state", "sum")],
        vol.Coerce(set),
    ),
}
_STATISTICS_METADATA: typing.Final = {
    vol.Required("type"): "recorder/get_statistics_metadata",
    vol.Optional("statistic_ids"): [str],
}
_UPDATE_METADATA: typing.Final = {
    vol.Required("type"): "recorder/update_statistics_metadata",
    vol.Required("statistic_id"): str,
    vol.Required("unit_of_measurement"): vol.Any(str, None),
}
_RECORDER_INFO: typing.Final = {
    vol.Required("type"): "recorder/info",
}
_ADJUST_SUM_STATISTICS: typing.Final = {
    vol.Required("type"): "recorder/adjust_sum_statistics",
    vol.Required("statistic_id"): str,
    vol.Required("start_time"): str,
    vol.Required("adjustment"): vol.Any(float, int),
    vol.Required("adjustment_unit_of_measurement"): vol.Any(str, None),
}


# pylint: disable=unused-variable
class RecorderComponent(
    core.RecorderComponent,
    core.RecorderStatisticsBase,
    core.RecorderHistoryBase,
    core.SystemHealthPlatform,
    core.BackupPlatform,
):
    """Support for recording details."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._recorder: Recorder = None
        self._exclude_attributes_by_domain: dict[str, set[str]] = {}
        self._supported_platforms = frozenset(
            [core.Platform.SYSTEM_HEALTH, core.Platform.BACKUP]
        )

    @property
    def pseudo_event_state_changed(self) -> object:
        return _PSEUDO_EVENT_STATE_CHANGED

    @property
    def controller(self) -> core.SmartHomeController:
        return self._shc

    @property
    def recorder(self) -> Recorder:
        return self._recorder

    @property
    def config(self) -> core.Config:
        if self._shc is not None:
            return self._shc.config
        return None

    @property
    def bus(self) -> core.EventBus:
        if self._shc is None:
            return None
        return self._shc.bus

    @property
    def tracker(self) -> core.EventTracker:
        if self._shc is None:
            return None
        return self._shc.tracker

    @property
    def smart_home_controller_state(self) -> core.CoreState:
        if self._shc is None:
            return None
        return self._shc.state

    @property
    def is_controller_stopping(self) -> bool:
        if self._shc is None:
            return False
        return self._shc.is_stopping

    def is_entity_recorded(self, entity_id: str) -> bool:
        """Returns if entity is recorded."""
        if self._recorder is None:
            return False
        return self._recorder.is_entity_recorded(entity_id)

    @property
    def statistics(self) -> core.RecorderStatisticsBase:
        """Return the RecorderStatistics implementation."""
        return self

    @property
    def history(self) -> core.RecorderHistoryBase:
        """Return the History implementation."""
        return self

    async def async_can_shutdown(self, service: str) -> str:
        if util.async_migration_in_progress(self):
            return (
                f"The system cannot {service} "
                + "while a database upgrade is in progress."
            )
        return None

    def session_scope(
        self,
        *,
        session: core.SqlSession = None,
        exception_filter: collections.abc.Callable[[Exception], bool] = None,
    ) -> collections.abc.Generator[core.SqlSession, None, None]:
        """Provide a transactional scope around a series of operations."""
        return util.session_scope(session=session, rc=self)

    def sqlalchemy_filter_from_include_exclude_conf(
        self,
        conf: core.ConfigType,
    ) -> core.RecorderFiltersBase:
        """Build a sql filter from config."""
        return recorder_filters.sqlalchemy_filter_from_include_exclude_conf(conf)

    def statement_for_logbook_request(
        self,
        start_day: dt.datetime,
        end_day: dt.datetime,
        event_types: tuple[str, ...],
        entity_ids: list[str] = None,
        device_ids: list[str] = None,
        filters: core.RecorderFiltersBase = None,
        context_id: str = None,
    ) -> sql.sql.StatementLambdaElement:
        return queries.statement_for_logbook_request(
            start_day, end_day, event_types, entity_ids, device_ids, filters, context_id
        )

    @core.callback
    def async_add_executor_job(
        self, target: collections.abc.Callable[..., _T], *args: typing.Any
    ) -> asyncio.Future[_T]:
        """Add an executor job from within the event loop."""
        if self._recorder is None:
            return None
        return self._recorder.async_add_executor_job(target, *args)

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        schema = vol.Schema(
            {
                vol.Optional(self.domain, default=dict): vol.All(
                    _cv.deprecated(Const.CONF_PURGE_INTERVAL),
                    _cv.deprecated(Const.CONF_DB_INTEGRITY_CHECK),
                    Const.FILTER_SCHEMA.extend(
                        {
                            vol.Optional(
                                Const.CONF_AUTO_PURGE, default=True
                            ): _cv.boolean,
                            vol.Optional(
                                Const.CONF_AUTO_REPACK, default=True
                            ): _cv.boolean,
                            vol.Optional(
                                Const.CONF_PURGE_KEEP_DAYS, default=10
                            ): vol.All(vol.Coerce(int), vol.Range(min=1)),
                            vol.Optional(
                                Const.CONF_PURGE_INTERVAL, default=1
                            ): _cv.positive_int,
                            vol.Optional(Const.CONF_DB_URL): vol.All(
                                _cv.string, _validate_db_url
                            ),
                            vol.Optional(
                                Const.CONF_COMMIT_INTERVAL,
                                default=Const.DEFAULT_COMMIT_INTERVAL,
                            ): _cv.positive_int,
                            vol.Optional(
                                Const.CONF_DB_MAX_RETRIES,
                                default=Const.DEFAULT_DB_MAX_RETRIES,
                            ): _cv.positive_int,
                            vol.Optional(
                                Const.CONF_DB_RETRY_WAIT,
                                default=Const.DEFAULT_DB_RETRY_WAIT,
                            ): _cv.positive_int,
                            vol.Optional(
                                Const.CONF_DB_INTEGRITY_CHECK,
                                default=Const.DEFAULT_DB_INTEGRITY_CHECK,
                            ): _cv.boolean,
                        }
                    ),
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the recorder."""
        websocket_api = self.controller.components.websocket_api
        if not isinstance(websocket_api, core.WebSocket.Component):
            return False

        conf = config[self.domain]
        entity_filter = core.EntityFilter.convert_include_exclude_filter(conf)
        auto_purge = conf[Const.CONF_AUTO_PURGE]
        auto_repack = conf[Const.CONF_AUTO_REPACK]
        keep_days = conf[Const.CONF_PURGE_KEEP_DAYS]
        commit_interval = conf[Const.CONF_COMMIT_INTERVAL]
        db_max_retries = conf[Const.CONF_DB_MAX_RETRIES]
        db_retry_wait = conf[Const.CONF_DB_RETRY_WAIT]
        db_url = conf.get(Const.CONF_DB_URL) or Const.DEFAULT_URL.format(
            shc_config_path=self.config.path(Const.DEFAULT_DB_FILE)
        )
        exclude = conf[core.Const.CONF_EXCLUDE]
        exclude_t = exclude.get(Const.CONF_EVENT_TYPES, [])
        if core.Const.EVENT_STATE_CHANGED in exclude_t:
            _LOGGER.warning(
                "State change events are excluded, recorder will not record state changes."
                + "This is an error in Smart Home - The Next Generation."
            )
            raise core.SmartHomeControllerError(
                "State change events excluded in recorder config."
            )
        recorder = Recorder(
            self,
            auto_purge=auto_purge,
            auto_repack=auto_repack,
            keep_days=keep_days,
            commit_interval=commit_interval,
            uri=db_url,
            db_max_retries=db_max_retries,
            db_retry_wait=db_retry_wait,
            entity_filter=entity_filter,
            exclude_t=exclude_t,
            exclude_attributes_by_domain=self._exclude_attributes_by_domain,
        )
        self._recorder = recorder
        recorder.async_initialize()
        recorder.async_register()
        recorder.start()
        services.async_register_services(self._shc, self._recorder)

        # Set up the history hooks."""
        @core.callback
        def _async_entity_id_changed(event: core.Event) -> None:
            self._recorder.async_update_statistics_metadata(
                event.data["old_entity_id"], new_statistic_id=event.data["entity_id"]
            )

        @core.callback
        def entity_registry_changed_filter(event: core.Event) -> bool:
            """Handle entity_id changed filter."""
            if event.data["action"] != "update" or "old_entity_id" not in event.data:
                return False

            return True

        if self._shc.is_running:
            self._shc.bus.async_listen(
                core.Const.EVENT_ENTITY_REGISTRY_UPDATED,
                _async_entity_id_changed,
                event_filter=entity_registry_changed_filter,
            )
        self.async_websocket_setup(websocket_api)
        await self._shc.setup.async_process_integration_platforms(
            core.Platform.RECORDER, self._process_recorder_platform
        )

        return await self._recorder.async_db_ready

    async def _process_recorder_platform(
        self,
        domain: str,
        platform: core.PlatformImplementation,
    ) -> None:
        """Process a recorder platform."""
        if isinstance(platform, core.RecorderPlatform):
            self._recorder.queue_task(task.AddRecorderPlatformTask(domain, platform))

    def add_platform(self, domain: str, platform: core.RecorderPlatform):
        if platform is not None and domain is not None:
            _PLATFORMS[domain] = platform
            excluded = platform.exclude_attributes()
            if excluded is not None:
                self._exclude_attributes_by_domain[domain] = excluded

    @property
    def platforms(self) -> collections.abc.Iterable[core.RecorderPlatform]:
        return _PLATFORMS.values()

    def items(self):
        return _PLATFORMS.items()

    def extract_include_exclude_filter_conf(
        self, conf: core.ConfigType
    ) -> dict[str, typing.Any]:
        return recorder_filters.extract_include_exclude_filter_conf(conf)

    def merge_include_exclude_filters(
        self, base_filter: dict[str, typing.Any], add_filter: dict[str, typing.Any]
    ) -> dict[str, typing.Any]:
        return recorder_filters.merge_include_exclude_filters(base_filter, add_filter)

    def process_timestamp_to_utc_isoformat(self, timestamp: dt.datetime) -> str:
        """Process a timestamp into UTC isotime."""
        return model.process_timestamp_to_utc_isoformat(timestamp)

    def process_datetime_to_timestamp(self, timestamp: dt.datetime) -> float:
        """Process a datebase datetime to epoch.

        Mirrors the behavior of process_timestamp_to_utc_isoformat
        except it returns the epoch time.
        """
        return model.process_datetime_to_timestamp(timestamp)

    async def async_block_till_done(self) -> None:
        """Async version of block_till_done."""
        if self._recorder is not None:
            await self._recorder.async_block_till_done()
        else:
            raise NotImplementedError()

    # ---- StatisticsBase implementation ---------

    def get_metadata(
        self,
        statistic_ids: list[str] | tuple[str] = None,
        statistic_type: typing.Literal["mean"] | typing.Literal["sum"] = None,
        statistic_source: str = None,
    ) -> dict[str, tuple[int, _statistic.MetaData]]:
        """Return metadata for statistic_ids."""
        return statistics.get_metadata(
            self,
            statistic_ids=statistic_ids,
            statistic_type=statistic_type,
            statistic_source=statistic_source,
        )

    def get_metadata_with_session(
        self,
        session: core.SqlSession,
        *,
        statistic_ids: list[str] | tuple[str] = None,
        statistic_type: typing.Literal["mean"] | typing.Literal["sum"] = None,
        statistic_source: str = None,
    ) -> dict[str, tuple[int, _statistic.MetaData]]:
        return statistics.get_metadata_with_session(
            session,
            statistic_ids=statistic_ids,
            statistic_type=statistic_type,
            statistic_source=statistic_source,
        )

    def statistics_during_period(
        self,
        start_time: dt.datetime,
        end_time: dt.datetime,
        statistic_ids: list[str],
        period: typing.Literal["5minute", "day", "hour", "month"],
        units: dict[str, str],
        types: set[
            typing.Literal["change", "last_reset", "max", "mean", "min", "state", "sum"]
        ],
    ) -> dict[str, list[dict[str, typing.Any]]]:
        """Return statistics during UTC period start_time - end_time for the statistic_ids.

        If end_time is omitted, returns statistics newer than or equal to start_time.
        If statistic_ids is omitted, returns statistics for all statistics ids.
        """
        return statistics.statistics_during_period(
            self, start_time, end_time, statistic_ids, period, units, types
        )

    def list_statistic_ids(
        self,
        statistic_ids: list[str] | tuple[str] = None,
        statistic_type: typing.Literal["mean"] | typing.Literal["sum"] = None,
    ) -> list[dict]:
        """Return all statistic_ids (or filtered one) and unit of measurement.

        Queries the database for existing statistic_ids, as well as integrations with
        a recorder platform for statistic_ids which will be added in the next statistics
        period.
        """
        return statistics.list_statistic_ids(self, statistic_ids, statistic_type)

    # --------- RecorderHistoryBase Implementation -------------------

    def get_significant_states_with_session(
        self,
        session: core.SqlSession,
        start_time: dt.datetime,
        end_time: dt.datetime = None,
        entity_ids: list[str] = None,
        filters: core.RecorderFiltersBase = None,
        include_start_time_state: bool = True,
        significant_changes_only: bool = True,
        minimal_response: bool = False,
        no_attributes: bool = False,
        compressed_state_format: bool = False,
    ) -> collections.abc.MutableMapping[str, list[core.State | dict[str, typing.Any]]]:
        """
        Return states changes during UTC period start_time - end_time.

        entity_ids is an optional iterable of entities to include in the results.

        filters is an optional SQLAlchemy filter which will be applied to the database
        queries unless entity_ids is given, in which case its ignored.

        Significant states are all states where there is a state change,
        as well as all states from certain domains (for instance
        thermostat so that we get current temperature in our graphs).
        """
        return history.get_significant_states_with_session(
            self,
            session,
            start_time,
            end_time,
            entity_ids,
            filters,
            include_start_time_state,
            significant_changes_only,
            minimal_response,
            no_attributes,
            compressed_state_format,
        )

    def get_significant_states(
        self,
        start_time: dt.datetime,
        end_time: dt.datetime = None,
        entity_ids: list[str] = None,
        filters: core.RecorderFiltersBase = None,
        include_start_time_state: bool = True,
        significant_changes_only: bool = True,
        minimal_response: bool = False,
        no_attributes: bool = False,
        compressed_state_format: bool = False,
    ) -> collections.abc.MutableMapping[str, list[core.State | dict[str, typing.Any]]]:
        """Wrap get_significant_states_with_session with an sql session."""
        return history.get_significant_states(
            self,
            start_time,
            end_time,
            entity_ids,
            filters,
            include_start_time_state,
            significant_changes_only,
            minimal_response,
            no_attributes,
            compressed_state_format,
        )

    def get_full_significant_states_with_session(
        self,
        session: sql_orm.Session,
        start_time: dt.datetime,
        end_time: dt.datetime = None,
        entity_ids: list[str] = None,
        filters: core.RecorderFiltersBase = None,
        include_start_time_state: bool = True,
        significant_changes_only: bool = True,
        no_attributes: bool = False,
    ) -> collections.abc.MutableMapping[str, list[core.State]]:
        """Variant of get_significant_states_with_session that does not return minimal responses."""
        return history.get_full_significant_states_with_session(
            self,
            session,
            start_time,
            end_time,
            entity_ids,
            filters,
            include_start_time_state,
            significant_changes_only,
            no_attributes,
        )

    def get_latest_short_term_statistics(
        self,
        statistic_ids: list[str],
        types: set[typing.Literal["last_reset", "max", "mean", "min", "state", "sum"]],
        metadata: dict[str, tuple[int, _statistic.MetaData]] = None,
    ) -> dict[str, list[dict]]:
        """Return the latest short term statistics for a list of statistic_ids."""
        return statistics.get_latest_short_term_statistics(
            self, statistic_ids, types, metadata
        )

    @core.callback
    def async_websocket_setup(self, comp: core.WebSocket.Component) -> None:
        """Set up the recorder websocket API."""
        comp.register_command(self._list_statistics, _LIST_STATISTICS)
        comp.register_command(self._validate_statistics, _VALIDATE_STATISTICS)
        comp.register_command(self._clear_statistics, _CLEAR_STATISTICS)
        comp.register_command(self._get_statistics_metadata, _STATISTICS_METADATA)
        comp.register_command(self._update_statistics_metadata, _UPDATE_METADATA)
        comp.register_command(self._info, _RECORDER_INFO)
        comp.register_command(self._adjust_sum_statistics, _ADJUST_SUM_STATISTICS)
        comp.register_command(
            self._get_statistics_during_period, _STATISTICS_DURING_PERIOD
        )

    def _ws_list_statistic_ids(
        self,
        connection: core.WebSocket.Connection,
        msg_id: int,
        statistic_type: typing.Literal["mean"] | typing.Literal["sum"] | None = None,
    ) -> str:
        """Fetch a list of available statistic_id and convert them to json in the executor."""
        return core.Const.JSON_DUMP(
            connection.result_message(
                msg_id, self.list_statistic_ids(None, statistic_type)
            )
        )

    async def _get_statistics_during_period(
        self, connection: core.WebSocket.Connection, msg: dict
    ) -> None:
        """Handle statistics websocket command."""
        start_time_str = msg["start_time"]
        end_time_str = msg.get("end_time")

        if start_time := core.helpers.parse_datetime(start_time_str):
            start_time = core.helpers.as_utc(start_time)
        else:
            connection.send_error(msg["id"], "invalid_start_time", "Invalid start_time")
            return

        if end_time_str:
            if end_time := core.helpers.parse_datetime(end_time_str):
                end_time = core.helpers.as_utc(end_time)
            else:
                connection.send_error(msg["id"], "invalid_end_time", "Invalid end_time")
                return
        else:
            end_time = None

        if (types := msg.get("types")) is None:
            types = {"change", "last_reset", "max", "mean", "min", "state", "sum"}
        connection.send_message(
            await self.async_add_executor_job(
                self._ws_get_statistics_during_period,
                connection,
                msg["id"],
                start_time,
                end_time,
                set(msg["statistic_ids"]),
                msg.get("period"),
                msg.get("units"),
                types,
            )
        )

    def _ws_get_statistics_during_period(
        self,
        connection: core.WebSocket.Connection,
        msg_id: int,
        start_time: dt.datetime,
        end_time: dt.datetime | None,
        statistic_ids: set[str] | None,
        period: typing.Literal["5minute", "day", "hour", "week", "month"],
        units: dict[str, str],
        types: set[
            typing.Literal["change", "last_reset", "max", "mean", "min", "state", "sum"]
        ],
    ) -> str:
        result = self.statistics.statistics_during_period(
            start_time, end_time, statistic_ids, period, units, types
        )

        return core.Const.JSON_DUMP(connection.result_message(msg_id, result))

    async def _list_statistics(
        self, connection: core.WebSocket.Connection, msg: dict
    ) -> None:
        """Fetch a list of available statistic_id."""
        connection.send_message(
            await self._recorder.async_add_executor_job(
                self._ws_list_statistic_ids,
                connection,
                msg["id"],
                msg.get("statistic_type"),
            )
        )

    async def _validate_statistics(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Fetch a list of available statistic_id."""
        statistic_ids = await self._recorder.async_add_executor_job(
            statistics.validate_statistics,
            self,
        )
        connection.send_result(msg["id"], statistic_ids)

    @core.callback
    def _clear_statistics(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Clear statistics for a list of statistic_ids.

        Note: The WS call posts a job to the recorder's queue and then returns, it doesn't
        wait until the job is completed.
        """
        connection.require_admin()
        self._recorder.async_clear_statistics(msg["statistic_ids"])
        connection.send_result(msg["id"])

    async def _get_statistics_metadata(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Get metadata for a list of statistic_ids."""
        statistic_ids = await self._recorder.async_add_executor_job(
            statistics.list_statistic_ids, self, msg.get("statistic_ids")
        )
        connection.send_result(msg["id"], statistic_ids)

    @core.callback
    def _update_statistics_metadata(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Update statistics metadata for a statistic_id."""
        connection.require_admin()
        self._recorder.async_update_statistics_metadata(
            msg["statistic_id"], new_unit_of_measurement=msg["unit_of_measurement"]
        )
        connection.send_result(msg["id"])

    @core.callback
    async def _adjust_sum_statistics(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Adjust sum statistics.

        If the statistics is stored as NORMALIZED_UNIT,
        it's allowed to make an adjustment in VALID_UNIT
        """
        connection.require_admin()
        start_time_str = msg["start_time"]

        if start_time := core.helpers.parse_datetime(start_time_str):
            start_time = core.helpers.as_utc(start_time)
        else:
            connection.send_error(msg["id"], "invalid_start_time", "Invalid start time")
            return

        metadatas = await self._recorder.async_add_executor_job(
            statistics.list_statistic_ids, self._recorder, (msg["statistic_id"],)
        )
        if not metadatas:
            connection.send_error(
                msg["id"], "unknown_statistic_id", "Unknown statistic ID"
            )
            return
        metadata = metadatas[0]

        def valid_units(statistics_unit: str, adjustment_unit: str) -> bool:
            if statistics_unit == adjustment_unit:
                return True
            converter = _statistic.STATISTIC_UNIT_TO_UNIT_CONVERTER.get(statistics_unit)
            if converter is not None and adjustment_unit in converter.VALID_UNITS:
                return True
            return False

        stat_unit = metadata["statistics_unit_of_measurement"]
        adjustment_unit = msg["adjustment_unit_of_measurement"]
        if not valid_units(stat_unit, adjustment_unit):
            connection.send_error(
                msg["id"],
                "invalid_units",
                f"Can't convert {stat_unit} to {adjustment_unit}",
            )
            return

        self._recorder.async_adjust_statistics(
            msg["statistic_id"], start_time, msg["adjustment"], adjustment_unit
        )
        connection.send_result(msg["id"])

    @core.callback
    def _info(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Return status of the recorder."""

        backlog = self._recorder.backlog if self._recorder else None
        migration_in_progress = util.async_migration_in_progress(self)
        recording = self._recorder.recording if self._recorder else False
        thread_alive = self._recorder.is_alive() if self._recorder else False

        recorder_info = {
            "backlog": backlog,
            "max_backlog": Const.MAX_QUEUE_BACKLOG,
            "migration_in_progress": migration_in_progress,
            "recording": recording,
            "thread_running": thread_alive,
        }
        connection.send_result(msg["id"], recorder_info)

    def register_system_health_info(self, info: core.SystemHealthRegistration) -> None:
        """Register system health callbacks."""
        info.async_register_info(self._system_health_info)

    async def _system_health_info(self) -> dict[str, typing.Any]:
        """Get info for the info page."""
        instance = self._recorder

        run_history = instance.run_history
        database_name = urllib.parse.urlparse(instance.db_url).path.lstrip("/")
        db_engine_info = _async_get_db_engine_info(instance)
        db_stats: dict[str, typing.Any] = {}

        if instance.async_db_ready.done():
            db_stats = await instance.async_add_executor_job(
                self._get_db_stats, database_name
            )
            db_runs = {
                "oldest_recorder_run": run_history.first.start,
                "current_recorder_run": run_history.current.start,
            }
        return db_runs | db_stats | db_engine_info

    def _get_db_stats(self, database_name: str) -> dict[str, typing.Any]:
        """Get the stats about the database."""
        db_stats: dict[str, typing.Any] = {}
        with self.session_scope(session=self._recorder.get_session()) as session:
            if (
                (dialect_name := self._recorder.dialect_name)
                and (get_size := _DIALECT_TO_GET_SIZE.get(dialect_name))
                and (db_bytes := get_size(session, database_name))
            ):
                db_stats["estimated_db_size"] = f"{db_bytes/1024/1024:.2f} MiB"
        return db_stats

    async def async_pre_backup(self) -> None:
        """Perform operations before a backup starts."""
        _LOGGER.info("Backup start notification, locking database for writes")
        if util.async_migration_in_progress(self):
            raise core.SmartHomeControllerError("Database migration in progress")
        locked = await self._recorder.lock_database()
        if not locked:
            raise core.SmartHomeControllerError("Could not set database write lock.")

    async def async_post_backup(self) -> None:
        """Perform operations after a backup finishes."""
        _LOGGER.info("Backup end notification, releasing write lock")
        if not self._recorder.unlock_database():
            raise core.SmartHomeControllerError("Could not release database write lock")


@core.callback
def _async_get_db_engine_info(instance: Recorder) -> dict[str, typing.Any]:
    """Get database engine info."""
    db_engine_info: dict[str, typing.Any] = {}
    if dialect_name := instance.dialect_name:
        db_engine_info["database_engine"] = dialect_name.value
    if engine_version := instance.engine_version:
        db_engine_info["database_version"] = str(engine_version)
    return db_engine_info


def _sqlite_db_size_bytes(session: sql_orm.Session, _database_name: str) -> float:
    """Get the mysql database size."""
    return float(
        session.execute(
            sql.text(
                "SELECT page_count * page_size as size "
                + "FROM pragma_page_count(), pragma_page_size();"
            )
        ).first()[0]
    )


def _mysql_db_size_bytes(session: sql_orm.Session, database_name: str) -> float:
    """Get the mysql database size."""
    return float(
        session.execute(
            sql.text(
                "SELECT ROUND(SUM(DATA_LENGTH + INDEX_LENGTH), 2) "
                + "FROM information_schema.TABLES WHERE "
                + "TABLE_SCHEMA=:database_name"
            ),
            {"database_name": database_name},
        ).first()[0]
    )


def _postgresql_db_size_bytes(session: sql_orm.Session, database_name: str) -> float:
    """Get the mysql database size."""
    return float(
        session.execute(
            sql.text("select pg_database_size(:database_name);"),
            {"database_name": database_name},
        ).first()[0]
    )


_DIALECT_TO_GET_SIZE: typing.Final = {
    Const.SupportedDialect.SQLITE: _sqlite_db_size_bytes,
    Const.SupportedDialect.MYSQL: _mysql_db_size_bytes,
    Const.SupportedDialect.POSTGRESQL: _postgresql_db_size_bytes,
}


def _validate_db_url(db_url: str) -> typing.Any:
    """Validate database URL."""
    # Don't allow on-memory sqlite databases
    if (
        db_url == Const.SQLITE_URL_PREFIX or ":memory:" in db_url
    ) and not Const.ALLOW_IN_MEMORY_DB:
        raise vol.Invalid("In-memory SQLite database is not supported")

    return db_url
