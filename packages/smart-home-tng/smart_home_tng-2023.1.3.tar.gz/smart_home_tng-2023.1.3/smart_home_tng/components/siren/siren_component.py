"""
Siren Component for Smart Home - The Next Generation.

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

import datetime as dt
import logging
import typing

from ... import core

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class SirenComponent(core.SmartHomeControllerComponent, core.RecorderPlatform):
    """Component to interface with various sirens/chimes."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._entities: core.EntityComponent = None
        self._supported_platforms = frozenset([core.Platform.RECORDER])

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._entities

    @property
    def scan_interval(self) -> dt.timedelta:
        return core.Siren.SCAN_INTERVAL

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up siren devices."""
        component = self._entities = core.EntityComponent(
            _LOGGER, self.domain, self.controller, self.scan_interval
        )
        await component.async_setup(config)

        async def async_handle_turn_on_service(
            siren: core.Siren.Entity, call: core.ServiceCall
        ) -> None:
            """Handle turning a siren on."""
            data = {
                k: v
                for k, v in call.data.items()
                if k
                in (
                    core.Siren.ATTR_TONE,
                    core.Siren.ATTR_DURATION,
                    core.Siren.ATTR_VOLUME_LEVEL,
                )
            }
            await siren.async_turn_on(
                **_process_turn_on_params(
                    siren, typing.cast(core.Siren.TurnOnServiceParameters, data)
                )
            )

        component.async_register_entity_service(
            core.Const.SERVICE_TURN_ON,
            core.Siren.TURN_ON_SCHEMA,
            async_handle_turn_on_service,
            [core.Siren.EntityFeature.TURN_ON],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_TURN_OFF,
            {},
            "async_turn_off",
            [core.Siren.EntityFeature.TURN_OFF],
        )
        component.async_register_entity_service(
            core.Const.SERVICE_TOGGLE,
            {},
            "async_toggle",
            [core.Siren.EntityFeature.TURN_ON & core.Siren.EntityFeature.TURN_OFF],
        )

        return True

    async def async_setup_entry(self, entry: core.ConfigEntry) -> bool:
        """Set up a config entry."""
        component = self._entities
        return await component.async_setup_entry(entry)

    async def async_unload_entry(self, entry: core.ConfigEntry) -> bool:
        """Unload a config entry."""
        component = self._entities
        return await component.async_unload_entry(entry)

    # ---------------------- Recorder Platform ----------------------------

    def exclude_attributes(self) -> set[str]:
        """Exclude static attributes from being recorded in the database."""
        return {core.Siren.ATTR_AVAILABLE_TONES}


def _process_turn_on_params(
    siren: core.Siren.Entity, params: core.Siren.TurnOnServiceParameters
) -> core.Siren.TurnOnServiceParameters:
    """
    Process turn_on service params.

    Filters out unsupported params and validates the rest.
    """
    supported_features = siren.supported_features or 0

    if not supported_features & core.Siren.EntityFeature.TONES:
        params.pop(core.Siren.ATTR_TONE, None)
    elif (tone := params.get(core.Siren.ATTR_TONE)) is not None:
        # Raise an exception if the specified tone isn't available
        is_tone_dict_value = bool(
            isinstance(siren.available_tones, dict)
            and tone in siren.available_tones.values()
        )
        if (
            not siren.available_tones
            or tone not in siren.available_tones
            and not is_tone_dict_value
        ):
            raise ValueError(
                f"Invalid tone specified for entity {siren.entity_id}: {tone}, "
                "check the available_tones attribute for valid tones to pass in"
            )

        # If available tones is a dict, and the tone provided is a dict value, we need
        # to transform it to the corresponding dict key before returning
        if is_tone_dict_value:
            assert isinstance(siren.available_tones, dict)
            params[core.Siren.ATTR_TONE] = next(
                key for key, value in siren.available_tones.items() if value == tone
            )

    if not supported_features & core.Siren.EntityFeature.DURATION:
        params.pop(core.Siren.ATTR_DURATION, None)
    if not supported_features & core.Siren.EntityFeature.VOLUME_SET:
        params.pop(core.Siren.ATTR_VOLUME_LEVEL, None)

    return params
