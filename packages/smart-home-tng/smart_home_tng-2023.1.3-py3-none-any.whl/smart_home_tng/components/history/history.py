"""
History Component for Smart Home - The Next Generation.

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

import datetime
import typing

import voluptuous as vol

from ... import core
from .const import Const
from .history_period_view import (
    HistoryPeriodView,
    _entities_may_have_state_changes_after,
)

_STATISTICS_DURING_PERIOD: typing.Final = {
    vol.Required("type"): "history/statistics_during_period",
    vol.Required("start_time"): str,
    vol.Optional("end_time"): str,
    vol.Optional("statistic_ids"): [str],
    vol.Required("period"): vol.Any("5minute", "hour", "day", "month"),
}
_LIST_STATISTICS_IDS: typing.Final = {
    vol.Required("type"): "history/list_statistic_ids",
    vol.Optional("statistic_type"): vol.Any("sum", "mean"),
}
_HISTORY_DURING_PERIOD: typing.Final = {
    vol.Required("type"): "history/history_during_period",
    vol.Required("start_time"): str,
    vol.Optional("end_time"): str,
    vol.Optional("entity_ids"): [str],
    vol.Optional("include_start_time_state", default=True): bool,
    vol.Optional("significant_changes_only", default=True): bool,
    vol.Optional("minimal_response", default=False): bool,
    vol.Optional("no_attributes", default=False): bool,
}


# pylint: disable=unused-variable
class History(core.SmartHomeControllerComponent):
    """Provide pre-made queries on top of the recorder component."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._filters: core.RecorderFiltersBase = None
        self._recorder: core.RecorderComponent = None
        self._use_include_order: bool = False

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        schema = vol.Schema(
            {
                self.domain: core.EntityFilter.Const.INCLUDE_EXCLUDE_BASE_FILTER_SCHEMA.extend(
                    {
                        vol.Optional(
                            Const.CONF_ORDER, default=False
                        ): core.helpers.boolean
                    }
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        # pylint: disable=no-member
        if not await super().async_setup(config):
            return False

        if self._config is None:
            self._config = {}

        self._recorder = self.controller.components.recorder
        frontend = self.controller.components.frontend
        websocket_api = self.controller.components.websocket_api
        if (
            not isinstance(self._recorder, core.RecorderComponent)
            or not isinstance(frontend, core.FrontendComponent)
            or not isinstance(websocket_api, core.WebSocket.Component)
        ):
            return False

        self._filters = self._recorder.sqlalchemy_filter_from_include_exclude_conf(
            self._config
        )
        self._use_include_order = self._config.get(Const.CONF_ORDER, False)

        self._shc.register_view(
            HistoryPeriodView(self._recorder, self._filters, self._use_include_order)
        )
        frontend.async_register_built_in_panel("history", "history", "hass:chart-box")

        websocket_api.register_command(
            self._get_statistics_during_period, _STATISTICS_DURING_PERIOD
        )
        websocket_api.register_command(
            self._get_list_statistic_ids, _LIST_STATISTICS_IDS
        )
        websocket_api.register_command(
            self._get_history_during_period, _HISTORY_DURING_PERIOD
        )

        return True

    def _internal_get_statistics_during_period(
        self,
        comp: core.WebSocket.Component,
        msg_id: int,
        start_time: datetime.datetime,
        end_time: datetime.datetime = None,
        statistic_ids: list[str] = None,
        period: typing.Literal["5minute", "day", "hour", "month"] = "hour",
    ) -> str:
        """Fetch statistics and convert them to json in the executor."""
        return core.Const.JSON_DUMP(
            comp.result_message(
                msg_id,
                self._recorder.statistics.statistics_during_period(
                    start_time,
                    end_time,
                    statistic_ids,
                    period,
                    {"energy": "kWh", "volume": "m³"},
                    {"min", "sum", "max", "last_reset", "state", "mean", "change"},
                ),
            )
        )

    async def _get_statistics_during_period(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
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

        connection.send_message(
            await self._recorder.async_add_executor_job(
                self._internal_get_statistics_during_period,
                connection.owner,
                msg["id"],
                start_time,
                end_time,
                msg.get("statistic_ids"),
                msg.get("period"),
            )
        )

    def _internal_get_list_statistic_ids(
        self,
        comp: core.WebSocket.Component,
        msg_id: int,
        statistic_type: typing.Literal["mean"] | typing.Literal["sum"] = None,
    ) -> str:
        """Fetch a list of available statistic_id and convert them to json in the executor."""
        return core.Const.JSON_DUMP(
            comp.result_message(
                msg_id,
                self._recorder.statistics.list_statistic_ids(None, statistic_type),
            )
        )

    async def _get_list_statistic_ids(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Fetch a list of available statistic_id."""
        connection.send_message(
            await self._recorder.async_add_executor_job(
                self._internal_get_list_statistic_ids,
                connection.owner,
                msg["id"],
                msg.get("statistic_type"),
            )
        )

    def _internal_get_significant_states(
        self,
        comp: core.WebSocket.Component,
        msg_id: int,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        entity_ids: list[str],
        filters: core.RecorderFiltersBase,
        use_include_order: bool,
        include_start_time_state: bool,
        significant_changes_only: bool,
        minimal_response: bool,
        no_attributes: bool,
    ) -> str:
        """Fetch history significant_states and convert them to json in the executor."""
        states = self._recorder.history.get_significant_states(
            start_time,
            end_time,
            entity_ids,
            filters,
            include_start_time_state,
            significant_changes_only,
            minimal_response,
            no_attributes,
            True,
        )

        if not use_include_order or not filters:
            return core.Const.JSON_DUMP(comp.result_message(msg_id, states))

        return core.Const.JSON_DUMP(
            comp.result_message(
                msg_id,
                {
                    order_entity: states.pop(order_entity)
                    for order_entity in filters.included_entities
                    if order_entity in states
                }
                | states,
            )
        )

    async def _get_history_during_period(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle history during period websocket command."""
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

        if start_time > core.helpers.utcnow():
            connection.send_result(msg["id"], {})
            return

        entity_ids = msg.get("entity_ids")
        include_start_time_state = msg["include_start_time_state"]

        if (
            not include_start_time_state
            and entity_ids
            and not _entities_may_have_state_changes_after(
                self._shc, entity_ids, start_time
            )
        ):
            connection.send_result(msg["id"], {})
            return

        significant_changes_only = msg["significant_changes_only"]
        no_attributes = msg["no_attributes"]
        minimal_response = msg["minimal_response"]

        connection.send_message(
            await self._recorder.async_add_executor_job(
                self._internal_get_significant_states,
                connection.owner,
                msg["id"],
                start_time,
                end_time,
                entity_ids,
                self._filters,
                self._use_include_order,
                include_start_time_state,
                significant_changes_only,
                minimal_response,
                no_attributes,
            )
        )
