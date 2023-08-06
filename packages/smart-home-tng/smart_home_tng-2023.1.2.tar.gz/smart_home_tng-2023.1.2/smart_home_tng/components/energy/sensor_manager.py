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

import asyncio

from ... import core
from .const import Const
from .energy_cost_sensor import EnergyCostSensor
from .energy_manager import EnergyManager
from .source_adapter import SourceAdapter


# pylint: disable=unused-variable
class SensorManager:
    """Class to handle creation/removal of sensor data."""

    def __init__(
        self,
        manager: EnergyManager,
        async_add_entities: core.AddEntitiesCallback,
    ) -> None:
        """Initialize sensor manager."""
        self._manager = manager
        self.async_add_entities = async_add_entities
        self.current_entities: dict[tuple[str, str, str], EnergyCostSensor] = {}

    @property
    def manager(self) -> EnergyManager:
        return self._manager

    async def async_start(self) -> None:
        """Start."""
        self.manager.async_listen_updates(self._process_manager_data)

        if self.manager.data:
            await self._process_manager_data()

    async def _process_manager_data(self) -> None:
        """Process manager data."""
        to_add: list[EnergyCostSensor] = []
        to_remove = dict(self.current_entities)

        async def finish() -> None:
            if to_add:
                self.async_add_entities(to_add)
                await asyncio.gather(*(ent.add_finished.wait() for ent in to_add))

            for key, entity in to_remove.items():
                self.current_entities.pop(key)
                await entity.async_remove()

        if not self.manager.data:
            await finish()
            return

        for energy_source in self.manager.data["energy_sources"]:
            for adapter in Const.SOURCE_ADAPTERS:
                if adapter.source_type != energy_source["type"]:
                    continue

                if adapter.flow_type is None:
                    self._process_sensor_data(
                        adapter,
                        # Opting out of the type complexity because can't get it to work
                        energy_source,
                        to_add,
                        to_remove,
                    )
                    continue

                for flow in energy_source[adapter.flow_type]:
                    self._process_sensor_data(
                        adapter,
                        # Opting out of the type complexity because can't get it to work
                        flow,
                        to_add,
                        to_remove,
                    )

        await finish()

    @core.callback
    def _process_sensor_data(
        self,
        adapter: SourceAdapter,
        config: dict,
        to_add: list[EnergyCostSensor],
        to_remove: dict[tuple[str, str, str], EnergyCostSensor],
    ) -> None:
        """Process sensor data."""
        # No need to create an entity if we already have a cost stat
        if config.get(adapter.total_money_key) is not None:
            return

        key = (adapter.source_type, adapter.flow_type, config[adapter.stat_energy_key])

        # Make sure the right data is there
        # If the entity existed, we don't pop it from to_remove so it's removed
        if (
            config.get(adapter.entity_energy_key) is None
            or not core.helpers.valid_entity_id(config[adapter.entity_energy_key])
            or (
                config.get("entity_energy_price") is None
                and config.get("number_energy_price") is None
            )
        ):
            return

        if current_entity := to_remove.pop(key, None):
            current_entity.update_config(config)
            return

        self.current_entities[key] = EnergyCostSensor(
            adapter,
            config,
        )
        to_add.append(self.current_entities[key])
