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

import typing

import boschshcpy as bosch

from ... import core


class IntrusionSystemAlarmControlPanel(core.AlarmControlPanel.Entity):
    """Representation of SHC intrusion detection control."""

    def __init__(
        self,
        owner: core.SmartHomeControllerComponent,
        device: bosch.SHCIntrusionSystem,
        parent_id: str,
        entry_id: str,
    ):
        """Initialize the intrusion detection control."""
        self._device = device
        self._parent_id = parent_id
        self._entry_id = entry_id
        self._domain = owner.domain

    async def async_added_to_shc(self):
        """Subscribe to SHC events."""
        await super().async_added_to_shc()

        def on_state_changed():
            self.schedule_update_state()

        self._device.subscribe_callback(self.entity_id, on_state_changed)

    async def async_will_remove_from_shc(self):
        """Unsubscribe from SHC events."""
        await super().async_will_remove_from_shc()
        self._device.unsubscribe_callback(self.entity_id)

    @property
    def unique_id(self):
        """Return the unique ID of the system."""
        return self._device.id

    @property
    def name(self):
        """Name of the entity."""
        return self._device.name

    @property
    def device_id(self):
        """Return the ID of the system."""
        return self._device.id

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(self._domain, self._device.id)},
            "name": self._device.name,
            "manufacturer": self._device.manufacturer,
            "model": self._device.device_model,
            "via_device": (
                self._domain,
                self._parent_id,
            ),
        }

    @property
    def available(self):
        """Return false if status is unavailable."""
        return self._device.system_availability

    @property
    def should_poll(self):
        """Report polling mode. System is communicating via long polling."""
        return False

    @property
    def state(self):
        """Return the state of the device."""
        if (
            self._device.arming_state
            == bosch.SHCIntrusionSystem.ArmingState.SYSTEM_ARMING
        ):
            return core.Const.STATE_ALARM_ARMING
        if (
            self._device.arming_state
            == bosch.SHCIntrusionSystem.ArmingState.SYSTEM_DISARMED
        ):
            return core.Const.STATE_ALARM_DISARMED
        if (
            self._device.arming_state
            == bosch.SHCIntrusionSystem.ArmingState.SYSTEM_ARMED
        ):
            if (
                self._device.active_configuration_profile
                == bosch.SHCIntrusionSystem.Profile.FULL_PROTECTION
            ):
                return core.Const.STATE_ALARM_ARMED_AWAY

            if (
                self._device.active_configuration_profile
                == bosch.SHCIntrusionSystem.Profile.PARTIAL_PROTECTION
            ):
                return core.Const.STATE_ALARM_ARMED_HOME

            if (
                self._device.active_configuration_profile
                == bosch.SHCIntrusionSystem.Profile.CUSTOM_PROTECTION
            ):
                return core.Const.STATE_ALARM_ARMED_CUSTOM_BYPASS
        return None

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return (
            core.AlarmControlPanel.EntityFeature.ARM_AWAY
            + core.AlarmControlPanel.EntityFeature.ARM_HOME
            + core.AlarmControlPanel.EntityFeature.ARM_CUSTOM_BYPASS
        )

    @property
    def manufacturer(self):
        """Return manufacturer of the device."""
        return self._device.manufacturer

    @property
    def code_format(self):
        """Return the regex for code format or None if no code is required."""
        return None
        # return core.AlarmControlPanel.CodeFormat.NUMBER

    @property
    def code_arm_required(self):
        """Whether the code is required for arm actions."""
        return False

    def alarm_disarm(self, code=None):
        """Send disarm command."""
        self._device.disarm()

    def alarm_arm_away(self, code=None):
        """Send arm away command."""
        self._device.arm_full_protection()

    def alarm_arm_home(self, code=None):
        """Send arm home command."""
        self._device.arm_partial_protection()

    def alarm_arm_custom_bypass(self, code=None):
        """Send arm home command."""
        self._device.arm_individual_protection()

    def alarm_mute(self):
        """Mute alarm command."""
        self._device.mute()


# pylint: disable=unused-variable
async def _async_setup_alarm_control_panel(
    owner: core.SmartHomeControllerComponent,
    session: bosch.SHCSession,
    config_entry: core.ConfigEntry,
) -> typing.Iterable[core.Entity]:
    """Set up the alarm control panel platform."""

    result = []
    intrusion_system = session.intrusion_system
    alarm_control_panel = IntrusionSystemAlarmControlPanel(
        owner=owner,
        device=intrusion_system,
        parent_id=session.information.unique_id,
        entry_id=config_entry.entry_id,
    )
    result.append(alarm_control_panel)
    return result
