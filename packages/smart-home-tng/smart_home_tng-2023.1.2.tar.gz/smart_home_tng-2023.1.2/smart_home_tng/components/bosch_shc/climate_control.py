"""
Bosch SHC Integration for Smart Home - The Next Generation.

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

import logging
import typing

import boschshcpy as bosch

from ... import core
from .bosch_entity import BoschEntity

if not typing.TYPE_CHECKING:

    class BoschShcIntegration:
        pass


if typing.TYPE_CHECKING:
    from .bosch_shc_integration import BoschShcIntegration

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class ClimateControl(BoschEntity, core.Climate.Entity):
    """Representation of a SHC room climate control."""

    def __init__(
        self,
        owner: BoschShcIntegration,
        device: bosch.SHCClimateControl,
        parent_id: str,
        name: str,
        entry_id: str,
    ):
        """Initialize the SHC device."""
        super().__init__(owner, device=device, parent_id=parent_id, entry_id=entry_id)
        self._name = name

    @property
    def name(self):
        """Name of the entity."""
        return self._name

    @property
    def device_name(self):
        """Name of the device."""
        return self._name

    @property
    def temperature_unit(self):
        """Return the temperature unit."""
        return core.Const.UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._device.temperature

    @property
    def max_temp(self):
        """Return the maximum temperature allowed."""
        return 30.0

    @property
    def min_temp(self):
        """Return the minimum temperature allowed."""
        return 5.0

    @property
    def target_temperature(self):
        """Return the target temperature setpoint."""
        return self._device.setpoint_temperature

    @property
    def target_temperature_step(self):
        """Return the temperature step."""
        return 0.5

    @property
    def hvac_mode(self):
        """Return the hvac mode."""
        if self._device.summer_mode:
            return core.Climate.HVACMode.OFF

        if (
            self._device.operation_mode
            == bosch.SHCClimateControl.RoomClimateControlService.OperationMode.AUTOMATIC
        ):
            return core.Climate.HVACMode.AUTO

        return core.Climate.HVACMode.HEAT

    @property
    def hvac_modes(self):
        """Return available hvac modes."""
        return [
            core.Climate.HVACMode.AUTO,
            core.Climate.HVACMode.HEAT,
            core.Climate.HVACMode.OFF,
        ]

    # @property
    # def hvac_action(self):
    #     if self.valve_tappet_position > 5:
    #         return CURRENT_HVAC_HEAT
    #     else:
    #         return CURRENT_HVAC_IDLE

    @property
    def preset_mode(self):
        """Return preset mode."""
        if self._device.supports_boost_mode:
            if self._device.boost_mode:
                return core.Climate.PRESET_BOOST

        if self._device.low:
            return core.Climate.PRESET_ECO

        return core.Climate.PRESET_NONE

    @property
    def preset_modes(self):
        """Return available preset modes."""
        presets = [core.Climate.PRESET_NONE, core.Climate.PRESET_ECO]
        if self._device.supports_boost_mode:
            presets += [core.Climate.PRESET_BOOST]
        return presets

    @property
    def supported_features(self):
        """Return supported features."""
        return (
            core.Climate.EntityFeature.TARGET_TEMPERATURE
            + core.Climate.EntityFeature.PRESET_MODE
        )

    def set_temperature(self, **kwargs):
        """Set the temperature."""
        temperature = kwargs.get(core.Const.ATTR_TEMPERATURE)
        if temperature is None:
            return

        self.set_hvac_mode(
            kwargs.get(core.Climate.ATTR_HVAC_MODE)
        )  # set_temperature args may provide HVAC mode as well

        if (
            self.hvac_mode == core.Climate.HVACMode.OFF
            or self.preset_mode == core.Climate.PRESET_ECO
        ):
            _LOGGER.debug(
                f"Skipping setting temperature as device {self.device_name} is off or in low_mode.",
            )
            return

        if self.min_temp <= temperature <= self.max_temp:
            self._device.setpoint_temperature = float(temperature)

    def set_hvac_mode(self, hvac_mode: str):
        """Set hvac mode."""
        if hvac_mode not in self.hvac_modes:
            return
        if self.preset_mode == core.Climate.PRESET_ECO:
            return

        if hvac_mode == core.Climate.HVACMode.AUTO:
            self._device.summer_mode = False
            self._device.operation_mode = (
                bosch.SHCClimateControl.RoomClimateControlService.OperationMode.AUTOMATIC
            )
        if hvac_mode == core.Climate.HVACMode.HEAT:
            self._device.summer_mode = False
            self._device.operation_mode = (
                bosch.SHCClimateControl.RoomClimateControlService.OperationMode.MANUAL
            )
        if hvac_mode == core.Climate.HVACMode.OFF:
            self._device.summer_mode = True

    def set_preset_mode(self, preset_mode: str):
        """Set preset mode."""
        if preset_mode not in self.preset_modes:
            return

        if preset_mode == core.Climate.PRESET_NONE:
            if self._device.supports_boost_mode:
                if self._device.boost_mode:
                    self._device.boost_mode = False

            if self._device.low:
                self._device.low = False

        elif preset_mode == core.Climate.PRESET_BOOST:
            if not self._device.boost_mode:
                self._device.boost_mode = True

            if self._device.low:
                self._device.low = False

        elif preset_mode == core.Climate.PRESET_ECO:
            if self._device.supports_boost_mode:
                if self._device.boost_mode:
                    self._device.boost_mode = False

            if not self._device.low:
                self._device.low = True


# pylint: disable=unused-variable
async def _async_setup_climate_controls(
    owner: BoschShcIntegration,
    session: bosch.SHCSession,
    config_entry: core.ConfigEntry,
) -> typing.Iterable[core.Entity]:
    """Set up the SHC climate platform."""
    entities = []

    for climate in session.device_helper.climate_controls:
        room_id = climate.room_id
        entities.append(
            ClimateControl(
                owner,
                device=climate,
                parent_id=session.information.unique_id,
                entry_id=config_entry.entry_id,
                name=f"Room Climate {session.room(room_id).name}",
            )
        )
    return entities
