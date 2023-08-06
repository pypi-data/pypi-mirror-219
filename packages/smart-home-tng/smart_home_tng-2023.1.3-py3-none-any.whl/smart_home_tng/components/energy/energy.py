"""
Energy Component for Smart Home - The Next Generation.

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
import collections.abc
import datetime
import itertools as it
import typing
import voluptuous as vol

from ... import core
from .const import Const
from .energy_preferences_update import EnergyPreferencesUpdate
from .energy_cost_sensor import _COST_SENSORS
from .energy_manager import EnergyManager
from .sensor_platform import SensorPlatform
from .validate import async_validate


_ENERGY_PLATFORMS_HELPER: typing.Final = core.Singleton

_GET_PREFS: typing.Final = {
    vol.Required("type"): "energy/get_prefs",
}
_SAVE_PREFS: typing.Final = {
    vol.Required("type"): "energy/save_prefs",
    vol.Optional("energy_sources"): Const.ENERGY_SOURCE_SCHEMA,
    vol.Optional("device_consumption"): [Const.DEVICE_CONSUMPTION_SCHEMA],
}
_ENERGY_INFO: typing.Final = {
    vol.Required("type"): "energy/info",
}
_ENERGY_VALIDATE: typing.Final = {
    vol.Required("type"): "energy/validate",
}
_SOLAR_FORECAST: typing.Final = {
    vol.Required("type"): "energy/solar_forecast",
}
_FOSSIL_CONSUMPTION: typing.Final = {
    vol.Required("type"): "energy/fossil_energy_consumption",
    vol.Required("start_time"): str,
    vol.Required("end_time"): str,
    vol.Required("energy_statistic_ids"): [str],
    vol.Required("co2_statistic_id"): str,
    vol.Required("period"): vol.Any("5minute", "hour", "day", "month"),
}


@core.Singleton.shc_singleton(_ENERGY_PLATFORMS_HELPER)
async def _async_get_energy_platforms(
    shc: core.SmartHomeController,
) -> dict[str, core.EnergyPlatform]:
    """Get energy platforms."""
    platforms: dict[str, core.EnergyPlatform] = {}

    async def _process_energy_platform(
        domain: str, platform: core.platform_implementation
    ) -> None:
        """Process energy platforms."""
        if not isinstance(platform, core.EnergyPlatform):
            return

        platforms[domain] = platform

    await shc.setup.async_process_integration_platforms(
        core.Platform.ENERGY, _process_energy_platform
    )

    return platforms


# pylint: disable=unused-variable
class Energy(core.EnergyComponent):
    """The Energy integration."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._manager: EnergyManager = None
        self._sensor_platform: core.PlatformImplementation = None

    def get_platform(self, platform: core.Platform) -> core.PlatformImplementation:
        if platform == core.Platform.SENSOR:
            return self.sensor_platform
        return None

    @property
    def sensor_platform(self) -> SensorPlatform:
        if self._sensor_platform is None:
            self._sensor_platform = SensorPlatform(self._shc, self._manager)
        return self._sensor_platform

    async def is_configured(self) -> bool:
        if self._manager.data is None:
            return False
        return bool(self._manager.data != self._manager.default_preferences())

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up Energy."""
        if not await super().async_setup(config):
            return False

        if self._manager is not None:
            return False

        self._manager = EnergyManager(self._shc, self.storage_version, self.storage_key)
        await self._manager.async_initialize()

        api = self.controller.components.websocket_api
        if not isinstance(api, core.WebSocket.Component):
            return False

        api.register_command(self._get_prefs, _GET_PREFS)
        api.register_command(self._save_prefs, _SAVE_PREFS)
        api.register_command(self._info, _ENERGY_INFO)
        api.register_command(self._validate, _ENERGY_VALIDATE)
        api.register_command(self._solar_forecast, _SOLAR_FORECAST)
        api.register_command(self._get_fossil_energy_consumption, _FOSSIL_CONSUMPTION)

        comp = self._shc.components.frontend
        if isinstance(comp, core.FrontendComponent):
            comp.async_register_built_in_panel(
                self.domain, self.domain, "mdi:lightning-bolt"
            )

        self._shc.async_create_task(
            self._shc.setup.async_load_platform(
                core.Platform.SENSOR, self.domain, {}, config
            )
        )
        return True

    @core.callback
    def _get_prefs(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle get prefs command."""
        if self._manager.data is None:
            connection.send_error(msg["id"], core.WebSocket.ERR_NOT_FOUND, "No prefs")
            return

        connection.send_result(msg["id"], self._manager.data)

    async def _save_prefs(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle get prefs command."""
        connection.require_admin()

        msg_id = msg.pop("id")
        msg.pop("type")
        await self._manager.async_update(typing.cast(EnergyPreferencesUpdate, msg))
        connection.send_result(msg_id, self._manager.data)

    async def _info(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle get info command."""
        forecast_platforms = await _async_get_energy_platforms(
            connection.owner.controller
        )
        connection.send_result(
            msg["id"],
            {
                "cost_sensors": _COST_SENSORS,
                "solar_forecast_domains": list(forecast_platforms),
            },
        )

    async def _validate(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle validate command."""
        recorder = connection.owner.controller.components.recorder
        if isinstance(recorder, core.RecorderComponent):
            connection.send_result(
                msg["id"],
                (
                    await async_validate(
                        connection.owner.controller, self._manager, recorder
                    )
                ).as_dict(),
            )
        else:
            connection.send_result(msg["id"], {})

    async def _solar_forecast(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Handle solar forecast command."""
        if self._manager.data is None:
            connection.send_result(msg["id"], {})
            return

        config_entries: dict[str, str] = {}

        for source in self._manager.data["energy_sources"]:
            if (
                source["type"] != "solar"
                or source.get("config_entry_solar_forecast") is None
            ):
                continue

            # typing is not catching the above guard for config_entry_solar_forecast being none
            for config_entry in source["config_entry_solar_forecast"]:
                config_entries[config_entry] = None

        if not config_entries:
            connection.send_result(msg["id"], {})
            return

        forecasts = {}

        forecast_platforms = await _async_get_energy_platforms(
            connection.owner.controller
        )

        for config_entry_id in config_entries:
            config_entry = self._shc.config_entries.async_get_entry(config_entry_id)
            # Filter out non-existing config entries or unsupported domains

            if config_entry is None or config_entry.domain not in forecast_platforms:
                continue

            forecast = await forecast_platforms[
                config_entry.domain
            ].async_get_solar_forecast(config_entry_id)

            if forecast is not None:
                forecasts[config_entry_id] = forecast

        connection.send_result(msg["id"], forecasts)

    async def _get_fossil_energy_consumption(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ) -> None:
        """Calculate amount of fossil based energy."""
        start_time_str = msg["start_time"]
        end_time_str = msg["end_time"]

        if start_time := core.helpers.parse_datetime(start_time_str):
            start_time = core.helpers.as_utc(start_time)
        else:
            connection.send_error(msg["id"], "invalid_start_time", "Invalid start_time")
            return

        if end_time := core.helpers.parse_datetime(end_time_str):
            end_time = core.helpers.as_utc(end_time)
        else:
            connection.send_error(msg["id"], "invalid_end_time", "Invalid end_time")
            return

        statistic_ids = list(msg["energy_statistic_ids"])
        statistic_ids.append(msg["co2_statistic_id"])

        recorder = connection.owner.controller.components.recorder
        if not isinstance(recorder, core.RecorderComponent):
            connection.send_result(msg["id"], {})

        # Fetch energy + CO2 statistics
        statistics = await recorder.async_add_executor_job(
            recorder.statistics.statistics_during_period,
            start_time,
            end_time,
            statistic_ids,
            "hour",
            {"energy": core.Const.UnitOfEnergy.KILO_WATT_HOUR},
            {"mean", "sum"},
        )

        def _combine_sum_statistics(
            stats: dict[str, list[dict[str, typing.Any]]], statistic_ids: list[str]
        ) -> dict[datetime.datetime, float]:
            """Combine multiple statistics, returns a dict indexed by start time."""
            result: collections.defaultdict[
                datetime.datetime, float
            ] = collections.defaultdict(float)

            for statistics_id, stat in stats.items():
                if statistics_id not in statistic_ids:
                    continue
                for period in stat:
                    if period["sum"] is None:
                        continue
                    result[period["start"]] += period["sum"]

            return {key: result[key] for key in sorted(result)}

        def _calculate_deltas(
            sums: dict[datetime.datetime, float]
        ) -> dict[datetime.datetime, float]:
            prev: float = None
            result: dict[datetime.datetime, float] = {}
            for period, sum_ in sums.items():
                if prev is not None:
                    result[period] = sum_ - prev
                prev = sum_
            return result

        def _reduce_deltas(
            stat_list: list[dict[str, typing.Any]],
            same_period: collections.abc.Callable[
                [datetime.datetime, datetime.datetime], bool
            ],
            period_start_end: collections.abc.Callable[
                [datetime.datetime], tuple[datetime.datetime, datetime.datetime]
            ],
            period: datetime.timedelta,
        ) -> list[dict[str, typing.Any]]:
            """Reduce hourly deltas to daily or monthly deltas."""
            result: list[dict[str, typing.Any]] = []
            deltas: list[float] = []
            if not stat_list:
                return result
            prev_stat: dict[str, typing.Any] = stat_list[0]

            # Loop over the hourly deltas + a fake entry to end the period
            for statistic in it.chain(
                stat_list, ({"start": stat_list[-1]["start"] + period},)
            ):
                if not same_period(prev_stat["start"], statistic["start"]):
                    start, _ = period_start_end(prev_stat["start"])
                    # The previous statistic was the last entry of the period
                    result.append(
                        {
                            "start": start.isoformat(),
                            "delta": sum(deltas),
                        }
                    )
                    deltas = []
                if statistic.get("delta") is not None:
                    deltas.append(statistic["delta"])
                prev_stat = statistic

            return result

        merged_energy_statistics = _combine_sum_statistics(
            statistics, msg["energy_statistic_ids"]
        )
        energy_deltas = _calculate_deltas(merged_energy_statistics)
        indexed_co2_statistics = {
            period["start"]: period["mean"]
            for period in statistics.get(msg["co2_statistic_id"], {})
        }

        # Calculate amount of fossil based energy, assume 100% fossil if missing
        fossil_energy = [
            {
                "start": start,
                "delta": delta * indexed_co2_statistics.get(start, 100) / 100,
            }
            for start, delta in energy_deltas.items()
        ]

        if msg["period"] == "hour":
            reduced_fossil_energy = [
                {"start": period["start"].isoformat(), "delta": period["delta"]}
                for period in fossil_energy
            ]

        elif msg["period"] == "day":
            reduced_fossil_energy = _reduce_deltas(
                fossil_energy,
                recorder.statistics.same_day,
                recorder.statistics.day_start_end,
                datetime.timedelta(days=1),
            )
        else:
            reduced_fossil_energy = _reduce_deltas(
                fossil_energy,
                recorder.statistics.same_month,
                recorder.statistics.month_start_end,
                datetime.timedelta(days=1),
            )

        result = {period["start"]: period["delta"] for period in reduced_fossil_energy}
        connection.send_result(msg["id"], result)
