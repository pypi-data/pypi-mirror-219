"""
Amazon Alexa MediaPlayer Integration for Smart Home - The Next Generation.

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

This integration is based custom_component "alexa_media_player"
from the Home Assistant Community Store (HACS), which is distributed
under the Terms of the Apache License, Version 2.0

The original source code and license terms can be found under:
https://github.com/custom_components/alexa_media_player
"""

import asyncio
import json
import logging
import typing

import alexapy
import voluptuous as vol

from ... import core

if not typing.TYPE_CHECKING:

    class AlexaMediaIntegration:
        pass


if typing.TYPE_CHECKING:
    from .alexa_media_integration import AlexaMediaIntegration

_const: typing.TypeAlias = core.Const

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable, protected-access
class AlexaNotificationService(core.BaseNotificationService):
    """Implement Alexa Media Player notification service."""

    def __init__(self, owner: AlexaMediaIntegration):
        """Initialize the service."""
        super().__init__(owner.controller)
        self._owner = owner
        self._last_called = True

    @property
    def last_called(self):
        return self._last_called

    def convert(self, names, type_="entities", filter_matches=False):
        """Return a list of converted Alexa devices based on names.

        Names may be matched either by serialNumber, accountName, or
        Homeassistant entity_id and can return any of the above plus entities

        Parameters
        ----------
        names : list(string)
            A list of names to convert
        type_ : string
            The type to return entities, entity_ids, serialnumbers, names
        filter_matches : bool
            Whether non-matching items are removed from the returned list.

        Returns
        -------
        list(string)
            List of home assistant entity_ids

        """
        devices = []
        if isinstance(names, str):
            names = [names]
        for item in names:
            matched = False
            for alexa in self.devices:
                if item in (
                    alexa,
                    alexa.name,
                    alexa.unique_id,
                    alexa.entity_id,
                    alexa.device_serial_number,
                ):
                    if type_ == "entities":
                        converted = alexa
                    elif type_ == "serialnumbers":
                        converted = alexa.device_serial_number
                    elif type_ == "names":
                        converted = alexa.name
                    elif type_ == "entity_ids":
                        converted = alexa.entity_id
                    devices.append(converted)
                    matched = True
                    # _LOGGER.debug("Converting: %s to (%s): %s", item, type_, converted)
            if not filter_matches and not matched:
                devices.append(item)
        return devices

    @property
    def targets(self):
        """Return a dictionary of Alexa devices."""
        devices = {}
        for email, info in self._owner._accounts.items():
            last_called_entity = None
            for _, entity in info.media_players.items():
                entity_name = (entity.entity_id).split(".")[1]
                devices[entity_name] = entity.unique_id
                if self._last_called and entity.extra_state_attributes.get(
                    "last_called"
                ):
                    if last_called_entity is None:
                        last_called_entity = entity
                    elif last_called_entity.extra_state_attributes.get(
                        "last_called_timestamp"
                    ) < entity.extra_state_attributes.get("last_called_timestamp"):
                        last_called_entity = entity
            if last_called_entity is not None:
                entity_name = (last_called_entity.entity_id).split(".")[1]
                entity_name_last_called = (
                    f"last_called{'_'+ email if entity_name[-1:].isdigit() else ''}"
                )
                devices[entity_name_last_called] = last_called_entity.unique_id
        return devices

    @property
    def devices(self):
        """Return a list of Alexa devices."""
        devices = []
        for _, info in self._owner._accounts.items():
            devices = devices + list(info.media_players.values())
        return devices

    def send_message(self, message: str, **kwargs: typing.Any) -> None:
        self._shc.run_coroutine_threadsafe(
            self.async_send_message(message=message, **kwargs)
        )

    async def async_send_message(self, message="", **kwargs):
        """Send a message to a Alexa device."""
        kwargs["message"] = message
        targets = kwargs.get(_const.ATTR_TARGET)
        title = kwargs.get(_const.ATTR_TITLE, _const.ATTR_TITLE_DEFAULT)
        data = kwargs.get(_const.ATTR_DATA, {}) or {}
        if isinstance(targets, str):
            try:
                targets = json.loads(targets)
            except json.JSONDecodeError:
                _LOGGER.error("Target must be a valid json")
                return
        processed_targets = []
        for target in targets:
            try:
                processed_targets += json.loads(target)
            except json.JSONDecodeError:
                if target.find(","):
                    processed_targets += list(
                        map(lambda x: x.strip(), target.split(","))
                    )
        entities = self.convert(processed_targets, type_="entities")
        try:
            entities.extend(
                self._owner.controller.components.group.expand_entity_ids(entities)
            )
        except ValueError:
            _LOGGER.debug(
                f"Invalid Smart Home - The Next Generation entity in {entities}"
            )
        tasks = []
        for account, info in self._owner._accounts.items():
            data_type = data.get("type", "tts")
            for alexa in info.media_players.values():
                if data_type == "tts":
                    targets = self.convert(
                        entities, type_="entities", filter_matches=True
                    )
                    if alexa in targets and alexa.available:
                        tasks.append(
                            alexa.async_send_tts(
                                message,
                                queue_delay=info.queue_delay,
                            )
                        )
                elif data_type == "announce":
                    targets = self.convert(
                        entities, type_="serialnumbers", filter_matches=True
                    )
                    if alexa.device_serial_number in targets and alexa.available:
                        tasks.append(
                            alexa.async_send_announcement(
                                message,
                                targets=targets,
                                title=title,
                                method=data.get("method", "all"),
                                queue_delay=info.queue_delay,
                            )
                        )
                        break
                elif data_type == "push":
                    targets = self.convert(
                        entities, type_="entities", filter_matches=True
                    )
                    if alexa in targets and alexa.available:
                        tasks.append(
                            alexa.async_send_mobilepush(
                                message,
                                title=title,
                                queue_delay=info.queue_delay,
                            )
                        )
                elif data_type == "dropin_notification":
                    targets = self.convert(
                        entities, type_="entities", filter_matches=True
                    )
                    if alexa in targets and alexa.available:
                        tasks.append(
                            alexa.async_send_dropin_notification(
                                message,
                                title=title,
                                queue_delay=info.queue_delay,
                            )
                        )
                else:
                    errormessage = (
                        f"{alexapy.hide_email(account)}: Data value `type={data_type}` "
                        + "is not implemented. "
                    )
                    _LOGGER.debug(errormessage)
                    raise vol.Invalid(errormessage)
        await asyncio.gather(*tasks)
