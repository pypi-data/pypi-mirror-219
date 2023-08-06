"""
Person Tracking Component for Smart Home - The Next Generation.

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

import voluptuous as vol

from ... import auth, core
from .const import Const
from .person import Person
from .person_storage_collection import PersonStorageCollection
from .person_store import PersonStore

_cv: typing.TypeAlias = core.ConfigValidation

_LOGGER: typing.Final = logging.getLogger(__name__)
_LIST_PERSONS: typing.Final = {vol.Required(core.Const.CONF_TYPE): "person/list"}


# pylint: disable=unused-variable
class PersonComponent(core.PersonComponent, core.GroupPlatform):
    """Support for tracking people."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._component: core.EntityComponent = None
        self._storage_collection: PersonStorageCollection = None
        self._yaml_collection: core.YamlCollection = None
        self._supported_platforms = frozenset([core.Platform.GROUP])

    @property
    def entity_component(self) -> core.EntityComponent:
        return self._component

    @property
    def storage_version(self) -> int:
        return Const.STORAGE_VERSION

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        schema = vol.Schema(
            {
                vol.Optional(self.domain, default=[]): vol.All(
                    _cv.ensure_list, _cv.remove_falsy, [Const.PERSON_SCHEMA]
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the person component."""
        if not await super().async_setup(config):
            return False

        websocket_api = self.controller.components.websocket_api
        if not isinstance(websocket_api, core.WebSocket.Component):
            return False

        entity_component = core.EntityComponent(_LOGGER, self.domain, self._shc)
        id_manager = core.IDManager()
        yaml_collection = core.YamlCollection(
            logging.getLogger(f"{__name__}.yaml_collection"), id_manager
        )
        storage_collection = PersonStorageCollection(
            PersonStore(self._shc, self.storage_version, self.storage_key),
            logging.getLogger(f"{__name__}.storage_collection"),
            id_manager,
            yaml_collection,
        )

        yaml_collection.sync_entity_lifecycle(
            self._shc, self.domain, self.domain, entity_component, Person
        )
        storage_collection.sync_entity_lifecycle(
            self._shc, self.domain, self.domain, entity_component, Person.from_yaml
        )

        self._component = entity_component
        self._storage_collection = storage_collection
        self._yaml_collection = yaml_collection

        await yaml_collection.async_load(
            await self._filter_yaml_data(config.get(self.domain, []))
        )
        await storage_collection.async_load()

        core.StorageCollectionWebSocket(
            storage_collection,
            self.domain,
            self.domain,
            Const.CREATE_FIELDS,
            Const.UPDATE_FIELDS,
        ).async_setup(create_list=False)

        websocket_api.register_command(self._list_person, _LIST_PERSONS)

        self._shc.bus.async_listen(
            auth.AuthManager.EVENT_USER_REMOVED, self._handle_user_removed
        )

        core.Service.async_register_admin_service(
            self._shc, self.domain, core.Const.SERVICE_RELOAD, self._reload_yaml
        )

        return True

    async def _reload_yaml(self, _call: core.ServiceCall) -> None:
        """Reload YAML."""
        conf = await self._component.async_prepare_reload(skip_reset=True)
        if conf is None:
            return
        await self._yaml_collection.async_load(
            await self._filter_yaml_data(conf.get(self.domain, []))
        )

    async def _handle_user_removed(self, event: core.Event) -> None:
        """Handle a user being removed."""
        user_id = event.data[Const.ATTR_USER_ID]
        for person in self._storage_collection.async_items():
            if person[Const.CONF_USER_ID] == user_id:
                await self._storage_collection.async_update_item(
                    person[core.Const.CONF_ID], {Const.CONF_USER_ID: None}
                )

    def _list_person(
        self,
        connection: core.WebSocket.Connection,
        msg: dict,
    ):
        """List persons."""
        connection.send_result(
            msg[core.Const.ATTR_ID],
            {
                "storage": self._storage_collection.async_items(),
                "config": self._yaml_collection.async_items(),
            },
        )

    async def _filter_yaml_data(self, persons: list[dict]) -> list[dict]:
        """Validate YAML data that we can't validate via schema."""
        filtered = []
        person_invalid_user = []
        persistent_notification = self.get_component(
            core.Const.PERSISTENT_NOTIFICATION_COMPONENT_NAME
        )
        if not isinstance(
            persistent_notification, core.PersistentNotificationComponent
        ):
            persistent_notification = None

        for person_conf in persons:
            user_id = person_conf.get(Const.CONF_USER_ID)

            if (
                user_id is not None
                and await self._shc.auth.async_get_user(user_id) is None
            ):
                _LOGGER.error(
                    f"Invalid user_id detected for person {person_conf[core.Const.CONF_ID]}",
                )
                person_invalid_user.append(
                    f"- Person {person_conf[core.Const.CONF_NAME]} (id: "
                    + f"{person_conf[core.Const.CONF_ID]}) points at invalid user {user_id}"
                )
                continue

            filtered.append(person_conf)

        if person_invalid_user and persistent_notification:
            persistent_notification.async_create(
                f"""
The following persons point at invalid users:

{"- ".join(person_invalid_user)}
                """,
                "Invalid Person Configuration",
                self.domain,
            )

        return filtered

    async def async_create_person(
        self, name: str, *, user_id: str = None, device_trackers: list[str] = None
    ):
        """Create a new person."""
        await self._storage_collection.async_create_item(
            {
                core.Const.ATTR_NAME: name,
                Const.ATTR_USER_ID: user_id,
                Const.CONF_DEVICE_TRACKERS: device_trackers or [],
            }
        )

    async def async_add_user_device_tracker(
        self, user_id: str, device_tracker_entity_id: str
    ):
        """Add a device tracker to a person linked to a user."""
        coll = self._storage_collection

        for person in coll.async_items():
            if person.get(Const.ATTR_USER_ID) != user_id:
                continue

            device_trackers = person[Const.CONF_DEVICE_TRACKERS]

            if device_tracker_entity_id in device_trackers:
                return

            await coll.async_update_item(
                person[core.Const.CONF_ID],
                {
                    Const.CONF_DEVICE_TRACKERS: device_trackers
                    + [device_tracker_entity_id]
                },
            )
            break

    @core.callback
    def async_describe_on_off_states(
        self, registry: core.GroupIntegrationRegistry
    ) -> None:
        """Describe group on off states."""
        registry.on_off_states({core.Const.STATE_HOME}, core.Const.STATE_NOT_HOME)
