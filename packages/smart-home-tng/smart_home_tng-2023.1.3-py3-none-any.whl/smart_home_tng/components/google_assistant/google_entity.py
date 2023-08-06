"""
Google Assistant Integration  for Smart Home - The Next Generation.

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

from ... import core
from .google_errors import SmartHomeError
from .google_traits import TRAITS

_const: typing.TypeAlias = core.Const
_google: typing.TypeAlias = core.GoogleAssistant
_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class GoogleEntity(core.GoogleAssistant.Entity):
    """Adaptation of Entity expressed in Google's terms."""

    def __init__(
        self, config: core.GoogleAssistant.AbstractConfig, state: core.State
    ) -> None:
        """Initialize a Google entity."""
        self._config = config
        self._state = state
        self._traits = None

    @property
    def entity_id(self):
        """Return entity ID."""
        return self._state.entity_id

    @property
    def state(self) -> core.State:
        return self._state

    @core.callback
    def traits(self):
        """Return traits for entity."""
        if self._traits is not None:
            return self._traits

        state = self._state
        domain = state.domain
        attributes = state.attributes
        features = attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)

        if not isinstance(features, int):
            _LOGGER.warning(
                f"Entity {self.entity_id} contains invalid supported_features value {features}",
            )
            return []

        device_class = state.attributes.get(_const.ATTR_DEVICE_CLASS)

        self._traits = [
            Trait(state, self._config)
            for Trait in TRAITS
            if Trait.supported(domain, features, device_class, attributes)
        ]
        return self._traits

    @core.callback
    def should_expose(self):
        """If entity should be exposed."""
        return self._config.should_expose(self._state)

    @core.callback
    def should_expose_local(self) -> bool:
        """Return if the entity should be exposed locally."""
        return (
            self.should_expose()
            and _get_google_type(
                self._state.domain, self._state.attributes.get(_const.ATTR_DEVICE_CLASS)
            )
            not in _google.NOT_EXPOSE_LOCAL
            and not self.might_2fa()
        )

    @core.callback
    def is_supported(self) -> bool:
        """Return if the entity is supported by Google."""
        features: int = self._state.attributes.get(_const.ATTR_SUPPORTED_FEATURES)

        result = self._config.is_supported_cache.get(self.entity_id)

        if result is None or result[0] != features:
            result = self._config.is_supported_cache[self.entity_id] = (
                features,
                bool(self.traits()),
            )

        return result[1]

    @core.callback
    def might_2fa(self) -> bool:
        """Return if the entity might encounter 2FA."""
        if not self._config.should_2fa(self._state):
            return False

        return self.might_2fa_traits()

    @core.callback
    def might_2fa_traits(self) -> bool:
        """Return if the entity might encounter 2FA based on just traits."""
        state = self._state
        domain = state.domain
        features = state.attributes.get(_const.ATTR_SUPPORTED_FEATURES, 0)
        device_class = state.attributes.get(_const.ATTR_DEVICE_CLASS)

        return any(
            trait.might_2fa(domain, features, device_class) for trait in self.traits()
        )

    def sync_serialize(self, agent_user_id, instance_uuid):
        """Serialize entity for a SYNC response.

        https://developers.google.com/actions/smarthome/create-app#actiondevicessync
        """
        state = self._state
        traits = self.traits()
        entity_config = self._config.entity_config.get(state.entity_id, {})
        name = (entity_config.get(_const.CONF_NAME) or state.name).strip()

        # Find entity/device/area registry entries
        device_entry, area_entry = _get_registry_entries(
            self._config.controller, self.entity_id
        )

        # Build the device info
        device = {
            "id": state.entity_id,
            "name": {"name": name},
            "attributes": {},
            "traits": [trait.name for trait in traits],
            "willReportState": self._config.should_report_state,
            "type": _get_google_type(
                state.domain, state.attributes.get(_const.ATTR_DEVICE_CLASS)
            ),
        }

        # Add aliases
        if aliases := entity_config.get(_google.CONF_ALIASES):
            device["name"]["nicknames"] = [name] + aliases

        # Add local SDK info if enabled
        if self._config.is_local_sdk_active and self.should_expose_local():
            device["otherDeviceIds"] = [{"deviceId": self.entity_id}]
            device["customData"] = {
                "webhookId": self._config.get_local_webhook_id(agent_user_id),
                "httpPort": self._config.controller.http.server_port,
                "uuid": instance_uuid,
                # Below can be removed in HA 2022.9
                "httpSSL": self._config.controller.config.api.use_ssl,
                "baseUrl": self._config.controller.get_url(prefer_external=True),
                "proxyDeviceId": agent_user_id,
            }

        # Add trait sync attributes
        for trt in traits:
            device["attributes"].update(trt.sync_attributes())

        # Add roomhint
        if room := entity_config.get(_google.CONF_ROOM_HINT):
            device["roomHint"] = room
        elif area_entry and area_entry.name:
            device["roomHint"] = area_entry.name

        # Add deviceInfo
        if not device_entry:
            return device

        device_info = {}

        if device_entry.manufacturer:
            device_info["manufacturer"] = device_entry.manufacturer
        if device_entry.model:
            device_info["model"] = device_entry.model
        if device_entry.sw_version:
            device_info["swVersion"] = device_entry.sw_version

        if device_info:
            device["deviceInfo"] = device_info

        return device

    @core.callback
    def query_serialize(self):
        """Serialize entity for a QUERY response.

        https://developers.google.com/actions/smarthome/create-app#actiondevicesquery
        """
        state = self._state

        if state.state == _const.STATE_UNAVAILABLE:
            return {"online": False}

        attrs = {"online": True}

        for trt in self.traits():
            _deep_update(attrs, trt.query_attributes())

        return attrs

    @core.callback
    def reachable_device_serialize(self):
        """Serialize entity for a REACHABLE_DEVICE response."""
        return {"verificationId": self.entity_id}

    async def execute(self, data, command_payload):
        """Execute a command.

        https://developers.google.com/actions/smarthome/create-app#actiondevicesexecute
        """
        command = command_payload["command"]
        params = command_payload.get("params", {})
        challenge = command_payload.get("challenge", {})
        executed = False
        for trt in self.traits():
            if trt.can_execute(command, params):
                await trt.execute(command, data, params, challenge)
                executed = True
                break

        if not executed:
            raise SmartHomeError(
                _google.ERR_FUNCTION_NOT_SUPPORTED,
                f"Unable to execute {command} for {self.state.entity_id}",
            )

    @core.callback
    def async_update(self):
        """Update the entity with latest info from Home Assistant."""
        self._state = self._config.controller.states.get(self.entity_id)

        if self._traits is None:
            return

        for trt in self._traits:
            trt.state = self._state


def _get_google_type(domain, device_class):
    """Google type based on domain and device class."""
    typ = _google.DEVICE_CLASS_TO_GOOGLE_TYPES.get((domain, device_class))

    return typ if typ is not None else _google.DOMAIN_TO_GOOGLE_TYPES[domain]


@core.callback
def _get_registry_entries(
    shc: core.SmartHomeController, entity_id: str
) -> tuple[core.Device, core.Area]:
    """Get registry entries."""
    ent_reg = shc.entity_registry
    dev_reg = shc.device_registry
    area_reg = shc.area_registry

    if (entity_entry := ent_reg.async_get(entity_id)) and entity_entry.device_id:
        device_entry = dev_reg.devices.get(entity_entry.device_id)
    else:
        device_entry = None

    if entity_entry and entity_entry.area_id:
        area_id = entity_entry.area_id
    elif device_entry and device_entry.area_id:
        area_id = device_entry.area_id
    else:
        area_id = None

    if area_id is not None:
        area_entry = area_reg.async_get_area(area_id)
    else:
        area_entry = None

    return device_entry, area_entry


def _deep_update(target, source):
    """Update a nested dictionary with another nested dictionary."""
    for key, value in source.items():
        if isinstance(value, typing.Mapping):
            target[key] = _deep_update(target.get(key, {}), value)
        else:
            target[key] = value
    return target
