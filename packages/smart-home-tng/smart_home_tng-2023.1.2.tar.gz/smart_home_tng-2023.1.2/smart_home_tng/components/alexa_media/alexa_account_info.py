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
import datetime as dt
import json
import logging
import time
import typing

import alexapy
import async_timeout

from ... import core
from .alexa_client import AlexaClient
from .alexa_device import AlexaDevice
from .alexa_media_switch import AlexaMediaSwitch
from .const import Const
from .dnd_switch import DNDSwitch
from .helpers import _calculate_uuid, _catch_login_errors, add_devices
from .repeat_switch import RepeatSwitch
from .shuffle_switch import ShuffleSwitch

_const: typing.TypeAlias = core.Const
_platform: typing.TypeAlias = core.Platform

if not typing.TYPE_CHECKING:

    class AlexaMediaIntegration:
        pass


if typing.TYPE_CHECKING:
    from .alexa_media_integration import AlexaMediaIntegration


_LOGGER: typing.Final = logging.getLogger(__name__)
_SWITCH_TYPES: typing.Final = [
    ("dnd", DNDSwitch),
    ("shuffle", ShuffleSwitch),
    ("repeat", RepeatSwitch),
]


# pylint: disable=unused-variable
class AlexaAccountInfo:
    """Handles information for one alexa account."""

    def __init__(
        self,
        owner: AlexaMediaIntegration,
        config_entry: core.ConfigEntry,
        login: alexapy.AlexaLogin = None,
    ):
        self._owner = owner
        self._config_entry = config_entry
        self._queue_delay: float = config_entry.options.get(
            Const.CONF_QUEUE_DELAY, Const.DEFAULT_QUEUE_DELAY
        )
        self._extended_entity_discovery: bool = config_entry.options.get(
            Const.CONF_EXTENDED_ENTITY_DISCOVERY,
            Const.DEFAULT_EXTENDED_ENTITY_DISCOVERY,
        )
        self._remove_update_listener = config_entry.add_update_listener(
            self._update_listener
        )
        self._login: alexapy.AlexaLogin = login
        self._index: int = 0
        if login is not None:
            self._uuid = login.uuid
        self._new_devices = True
        self._auth_info = None
        self._excluded: dict[str, typing.Any] = {}
        self._media_player_devices: dict[str, typing.Any] = {}
        self._media_player_entities: dict[str, AlexaClient] = {}
        self._dnd_switches: dict[str, typing.Any] = {}
        self._dnd_entities: dict[str, dict[str, AlexaMediaSwitch]] = {}
        self._websocket_client: alexapy.WebsocketEchoClient = None
        self._coordinator: core.DataUpdateCoordinator = None
        self._notifications: dict[str, typing.Any] = {}
        self._last_called: dict = None
        self._websocket_commands: dict[str, float] = {}
        self._websocket_history: dict[str, list[tuple[str, float]]] = {}
        self._websocket_error: int = 0
        self._websocket_lastattempt: float = None
        self._scan_interval: float = None
        self._entry_setup = False
        self._switch_entry_setup = False

    @property
    def controller(self) -> core.SmartHomeController:
        return self._owner.controller

    @property
    def coordinator(self):
        return self._coordinator

    @property
    def email(self) -> str:
        if not self._login:
            return None
        return self._login.email

    @property
    def media_players(self) -> dict[str, AlexaClient]:
        if self._media_player_entities:
            return self._media_player_entities.copy()
        return None

    @property
    def media_player_devices(self):
        return self._media_player_devices.copy()

    @property
    def url(self) -> str:
        if not self._login:
            return None
        return self._login.url

    @property
    def queue_delay(self):
        return self._queue_delay

    @property
    def last_called(self) -> dict:
        if self._last_called:
            return self._last_called.copy()
        return None

    @property
    def login(self) -> alexapy.AlexaLogin:
        return self._login

    @property
    def password(self) -> str:
        if not self._login:
            return None
        return self._login.password

    @property
    def second_account_index(self) -> int:
        return self._index

    @property
    def seen_commands(self):
        return self._websocket_commands.keys()

    @property
    def websocket_enabled(self):
        return bool(self._websocket_client)

    async def async_init(self) -> None:
        uuid, self._index = await self._calculate_uuid()
        if self._login is None:
            config = self._config_entry.data
            self._login = alexapy.AlexaLogin(
                url=config.get(_const.CONF_URL),
                email=config.get(_const.CONF_EMAIL),
                password=config.get(_const.CONF_PASSWORD),
                outputpath=self.controller.config.path,
                debug=config.get(Const.CONF_DEBUG),
                otp_secret=config.get(Const.CONF_OTPSECRET, ""),
                oauth=config.get(Const.CONF_OAUTH, {}),
                uuid=uuid,
                oauth_login=True,
            )

    async def _calculate_uuid(self) -> tuple[str, int]:
        """
        Return uuid and index of email/url.
        """
        email: str = self._config_entry.data.get(_const.CONF_EMAIL, "")
        url: str = self._config_entry.data.get(_const.CONF_URL, "")
        return await _calculate_uuid(self._owner, email, url)

    async def _update_listener(
        self, controller: core.SmartHomeController, config_entry: core.ConfigEntry
    ):
        """Update when config_entry options update."""
        account = config_entry.data
        email: str = account.get(_const.CONF_EMAIL)
        url: str = account.get(_const.CONF_URL)
        reload_needed: bool = email != self.email or url != self.url
        new_value = config_entry.options.get(Const.CONF_EXTENDED_ENTITY_DISCOVERY, None)
        if new_value is not None and new_value != self._extended_entity_discovery:
            reload_needed = True
        new_value = config_entry.options.get(Const.CONF_QUEUE_DELAY)
        if new_value is not None:
            self._queue_delay = new_value
        if reload_needed:
            await controller.config_entries.async_reload(config_entry.entry_id)

    def remove_update_listener(self) -> None:
        if self._remove_update_listener:
            self._remove_update_listener()
            self._remove_update_listener = None

    async def async_test_login_status(self) -> bool:
        """Test the login status and spawn requests for info."""

        in_progress = self._in_progress_instances()
        _LOGGER.debug(f"Testing login status: {self._login.status}")
        if self._login.status and self._login.status.get("login_successful"):
            return True
        account = self._config_entry.data
        _LOGGER.debug(f"Logging in: {alexapy.obfuscate(account)} {in_progress}")
        _LOGGER.debug(f"Login stats: {self._login.stats}")
        message = (
            f"Reauthenticate {self._login.email} on the "
            + "[Integrations](/config/integrations) page. "
        )
        if self._login.stats.get("login_timestamp") != dt.datetime(1, 1, 1):
            elaspsed_time: str = str(
                dt.datetime.now() - self._login.stats.get("login_timestamp")
            )
            api_calls: int = self._login.stats.get("api_calls")
            message += (
                f"Relogin required after {elaspsed_time} and {api_calls} api calls."
            )
        persistent_notification: core.PersistentNotificationComponent = (
            self.controller.components.persistent_notification
        )
        if persistent_notification:
            persistent_notification.async_create(
                title="Alexa Media Reauthentication Required",
                message=message,
                notification_id=(
                    f"alexa_media_{core.helpers.slugify(self.email)}"
                    + f"{core.helpers.slugify(self.url[7:])}"
                ),
            )
        flow = self._owner.get_config_flow(self.email, self.url)
        if flow:
            flow_id = flow.get("flow_id")
            if flow_id in in_progress:
                _LOGGER.debug("Existing config flow detected")
                return False
            _LOGGER.debug(f"Stopping orphaned config flow {flow_id}")
            try:
                self.controller.config_entries.flow.async_abort(flow_id)
                self._owner.register_config_flow(self.email, self.url)
            except core.UnknownFlow:
                pass
        _LOGGER.debug("Creating new config flow to login")
        config = self._config_entry.data
        self._owner.register_config_flow(
            self.email,
            self.url,
            await self.controller.config_entries.flow.async_init(
                self._owner.domain,
                context={"source": core.ConfigEntrySource.REAUTH},
                data={
                    _const.CONF_EMAIL: self.email,
                    _const.CONF_PASSWORD: self.password,
                    _const.CONF_URL: self.url,
                    Const.CONF_DEBUG: config[Const.CONF_DEBUG],
                    Const.CONF_INCLUDE_DEVICES: config[Const.CONF_INCLUDE_DEVICES],
                    Const.CONF_EXCLUDE_DEVICES: config[Const.CONF_EXCLUDE_DEVICES],
                    _const.CONF_SCAN_INTERVAL: self._scan_interval,
                    Const.CONF_OTPSECRET: config.get(Const.CONF_OTPSECRET, ""),
                },
            ),
        )
        return False

    @core.callback
    def _in_progress_instances(self):
        """Return a set of in progress Alexa Media flows."""
        return {
            entry["flow_id"]
            for entry in self.controller.config_entries.flow.async_progress()
        }

    async def async_relogin(self) -> bool:
        self._login.oauth_login = True
        await self._login.reset()
        if await self.async_test_login_status():
            await self.async_setup_alexa()
            return True
        return False

    async def async_login(self) -> bool:
        login = self._login
        await login.login(cookies=await login.load_cookie())
        if await self.async_test_login_status():
            await self.async_setup_alexa()
            return True
        return False

    async def async_close_connection(self) -> None:
        await self._login.save_cookiefile()
        await self._login.close()
        _LOGGER.debug(
            f"{alexapy.hide_email(self.email)}: Connection closed: {self._login.session.closed}"
        )

    async def async_setup_alexa(self):
        """Set up a alexa api based on host parameter."""

        _LOGGER.debug(
            f"Setting up Alexa devices for {alexapy.hide_email(self._login.email)}",
        )
        config = self._config_entry.data
        email = self.email
        scan_interval = config.get(_const.CONF_SCAN_INTERVAL)
        if isinstance(scan_interval, dt.timedelta):
            scan_interval = scan_interval.total_seconds()
        self._scan_interval = scan_interval
        websocket_enabled = self._websocket_client = await self._ws_connect()
        coordinator = self._coordinator
        if coordinator is None:
            _LOGGER.debug(f"{alexapy.hide_email(email)}: Creating coordinator")
            self._coordinator = coordinator = core.DataUpdateCoordinator(
                self.controller,
                _LOGGER,
                # Name of the data. For logging purposes.
                name="alexa_media",
                update_method=self._async_update_data,
                # Polling interval. Will only be polled if there are subscribers.
                update_interval=dt.timedelta(
                    seconds=scan_interval * 10 if websocket_enabled else scan_interval
                ),
            )
        else:
            _LOGGER.debug(f"{alexapy.hide_email(email)}: Reusing coordinator")
            coordinator.update_interval = dt.timedelta(
                seconds=scan_interval * 10 if websocket_enabled else scan_interval
            )
        # Fetch initial data so we have data when entities subscribe
        _LOGGER.debug(f"{alexapy.hide_email(email)}: Refreshing coordinator")
        await coordinator.async_refresh()

        return True

    def _existing_serials(self) -> list:
        existing_serials = list(self._media_player_entities.keys())
        for serial in existing_serials:
            device = self._media_player_devices[serial]
            if app_list := device.get("appDeviceList"):
                apps = list(
                    map(
                        lambda x: x.get("serialNumber"),
                        app_list,
                    )
                )
                # _LOGGER.debug("Combining %s with %s",
                #               existing_serials, apps)
                existing_serials = existing_serials + apps
        return existing_serials

    async def _async_update_data(self) -> dict:
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.

        This will ping Alexa API to identify all devices, bluetooth, and the last
        called device.

        If any guards, temperature sensors, or lights are configured, their
        current state will be acquired. This data is returned directly so that it is
        available on the coordinator.

        This will add new devices and services when discovered. By default this
        runs every SCAN_INTERVAL seconds unless another method calls it. if
        websockets is connected, it will increase the delay 10-fold between updates.
        While throttled at MIN_TIME_BETWEEN_SCANS, care should be taken to
        reduce the number of runs to avoid flooding. Slow changing states
        should be checked here instead of in spawned components like
        media_player since this object is one per account.
        Each AlexaAPI call generally results in two webpage requests.
        """
        email = self._config_entry.data.get(_const.CONF_EMAIL)
        if (
            not self._owner.is_account_defined(email)
            or not self._login.status.get("login_successful")
            or self._login.session.closed
            or self._login.close_requested
        ):
            return
        existing_serials = self._existing_serials()
        existing_entities = self._media_player_entities.values()
        auth_info = self._auth_info
        new_devices = self._new_devices

        config = self._config_entry.data
        include: list[str] = config.get(Const.CONF_INCLUDE_DEVICES)
        exclude: list[str] = config.get(Const.CONF_EXCLUDE_DEVICES)
        if exclude:
            if isinstance(exclude, str):
                exclude = list(map(lambda x: x.strip(), exclude.split(",")))
        else:
            exclude = []
        if include:
            if isinstance(include, str):
                include = list(map(lambda x: x.strip(), include.split(",")))
        else:
            include = []

        devices = {}
        bluetooth = {}
        preferences = {}
        dnd = {}
        raw_notifications = {}
        entity_state = {}
        tasks = [
            alexapy.AlexaAPI.get_devices(self._login),
            alexapy.AlexaAPI.get_bluetooth(self._login),
            alexapy.AlexaAPI.get_device_preferences(self._login),
            alexapy.AlexaAPI.get_dnd_state(self._login),
        ]
        if new_devices:
            tasks.append(alexapy.AlexaAPI.get_authentication(self._login))

        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(30):
                (
                    devices,
                    bluetooth,
                    preferences,
                    dnd,
                    *optional_task_results,
                ) = await asyncio.gather(*tasks)

                if new_devices:
                    auth_info = optional_task_results.pop()
                    found_devices = len(devices) if devices else 0
                    bluetooth_states = (
                        bluetooth.get("bluetoothStates", []) if bluetooth else []
                    )
                    _LOGGER.debug(
                        f"{alexapy.hide_email(email)}: Found {found_devices} devices, "
                        + f"{bluetooth_states} bluetooth",
                    )

            await self._process_notifications(raw_notifications)
            # Process last_called data to fire events
            await self._async_update_last_called()
        except (alexapy.AlexapyLoginError, json.JSONDecodeError):
            _LOGGER.debug(
                f"{alexapy.hide_email(email)}: Alexa API disconnected; "
                + f"attempting to relogin : status {self._login.status}",
            )
            if self._login.status:
                self.controller.bus.async_fire(
                    "alexa_media.relogin_required",
                    event_data={
                        "email": alexapy.hide_email(email),
                        "url": self._login.url,
                    },
                )
            return
        except BaseException as err:
            raise core.UpdateFailed(f"Error communicating with API: {err}")

        new_alexa_clients = []  # list of newly discovered device names
        exclude_filter = []
        include_filter = []

        for device in devices:
            serial = device["serialNumber"]
            dev_name = device["accountName"]
            if include and dev_name not in include:
                include_filter.append(dev_name)
                if "appDeviceList" in device:
                    for app in device["appDeviceList"]:
                        (self._excluded[app["serialNumber"]]) = device
                self._excluded[serial] = device
                continue
            if exclude and dev_name in exclude:
                exclude_filter.append(dev_name)
                if "appDeviceList" in device:
                    for app in device["appDeviceList"]:
                        self._excluded[app["serialNumber"]] = device
                self._excluded[serial] = device
                continue

            if (
                dev_name not in include_filter
                and device.get("capabilities")
                and not any(
                    x in device["capabilities"]
                    for x in ["MUSIC_SKILL", "TIMERS_AND_ALARMS", "REMINDERS"]
                )
            ):
                # skip devices without music or notification skill
                _LOGGER.debug(f"Excluding {dev_name} for lacking capability")
                continue

            if bluetooth is not None and "bluetoothStates" in bluetooth:
                for b_state in bluetooth["bluetoothStates"]:
                    if serial == b_state["deviceSerialNumber"]:
                        device["bluetooth_state"] = b_state
                        break

            if "devicePreferences" in preferences:
                for dev in preferences["devicePreferences"]:
                    if dev["deviceSerialNumber"] == serial:
                        device["locale"] = dev["locale"]
                        device["timeZoneId"] = dev["timeZoneId"]
                        _LOGGER.debug(
                            f"{dev_name}: Locale {device['locale']} timezone "
                            + f"{device['timeZoneId']}",
                        )
                        break

            if "doNotDisturbDeviceStatusList" in dnd:
                for dev in dnd["doNotDisturbDeviceStatusList"]:
                    if dev["deviceSerialNumber"] == serial:
                        device["dnd"] = dev["enabled"]
                        _LOGGER.debug(f"{dev_name}: DND {device['dnd']}")
                        self._dnd_switches.setdefault(serial, {"dnd": True})
                        break
            self._auth_info = device["auth_info"] = auth_info
            self._media_player_devices[serial] = AlexaDevice(device)

            media_player = self._media_player_entities.get(serial, None)
            if serial not in existing_serials:
                new_alexa_clients.append(dev_name)
            elif media_player and media_player.enabled:
                await media_player.refresh(device, skip_api=True)
        _LOGGER.debug(
            f"{alexapy.hide_email(email)}: Existing: {list(existing_entities)} "
            + f"New: {new_alexa_clients}; "
            + f"Filtered out by not being in include: {include_filter} "
            + f"or in exclude: {exclude_filter}",
        )

        if new_alexa_clients:
            cleaned_config = config.copy()
            cleaned_config.pop(_const.CONF_PASSWORD, None)
            # CONF_PASSWORD contains sensitive info which is no longer needed
            platform = _platform.MEDIA_PLAYER
            if not self._entry_setup:
                _LOGGER.debug(f"Loading config entry for {platform}")
                self._entry_setup = await self.controller.async_add_job(
                    self.controller.config_entries.async_forward_entry_setup(
                        self._config_entry, platform
                    )
                )
            else:
                _LOGGER.debug(f"Loading {platform}")
                self.controller.async_create_task(
                    self.controller.setup.async_load_platform(
                        platform,
                        self._owner.domain,
                        {
                            _const.CONF_NAME: self._owner.domain,
                            "config": cleaned_config,
                        },
                        cleaned_config,
                    )
                )

        self._new_devices = False
        # prune stale devices
        device_registry = self.controller.device_registry
        for device_entry in device_registry.async_entries_for_config_entry(
            self._config_entry.entry_id
        ):
            for _, identifier in device_entry.identifiers:
                if identifier in self._media_player_devices or identifier in map(
                    lambda key: core.helpers.slugify(f"{key}_{email}"),
                    self._media_player_devices,
                ):
                    break
            else:
                device_registry.async_remove_device(device_entry.id)
                _LOGGER.debug(
                    f"{alexapy.hide_email(email)}: Removing stale device {device_entry.name}",
                )

        await self._login.save_cookiefile()
        if self._login.access_token:
            self.controller.config_entries.async_update_entry(
                self._config_entry,
                data={
                    **self._config_entry.data,
                    Const.CONF_OAUTH: {
                        "access_token": self._login.access_token,
                        "refresh_token": self._login.refresh_token,
                        "expires_in": self._login.expires_in,
                        "mac_dms": self._login.mac_dms,
                    },
                },
            )
        return entity_state

    @_catch_login_errors
    async def _process_notifications(self, raw_notifications=None):
        """Process raw notifications json."""
        if not raw_notifications:
            raw_notifications = await alexapy.AlexaAPI.get_notifications(self._login)
        email = self.email
        previous = self._notifications
        now = core.helpers.utcnow()
        notifications = {"process_timestamp": now}
        if raw_notifications is not None:
            for notification in raw_notifications:
                n_dev_id = notification.get("deviceSerialNumber")
                if n_dev_id is None:
                    # skip notifications untied to a device for now
                    # https://github.com/custom-components/alexa_media_player/issues/633#issuecomment-610705651
                    continue
                n_type = notification.get("type")
                if n_type is None:
                    continue
                if n_type == "MusicAlarm":
                    n_type = "Alarm"
                n_id = notification["notificationIndex"]
                if n_type == "Alarm":
                    n_date = notification.get("originalDate")
                    n_time = notification.get("originalTime")
                    notification["date_time"] = (
                        f"{n_date} {n_time}" if n_date and n_time else None
                    )
                    previous_alarm = (
                        previous.get(n_dev_id, {}).get("Alarm", {}).get(n_id)
                    )
                    if previous_alarm and _alarm_just_dismissed(
                        notification,
                        previous_alarm.get("status"),
                        previous_alarm.get("version"),
                    ):
                        self.controller.bus.async_fire(
                            "alexa_media.alarm_dismissal_event",
                            event_data={
                                "device": {"id": n_dev_id},
                                "event": notification,
                            },
                        )

                if n_dev_id not in notifications:
                    notifications[n_dev_id] = {}
                if n_type not in notifications[n_dev_id]:
                    notifications[n_dev_id][n_type] = {}
                notifications[n_dev_id][n_type][n_id] = notification
        self._notifications = notifications
        _LOGGER.debug(
            f"{alexapy.hide_email(email)}: Updated {len(raw_notifications)} notifications "
            + f"for {len(notifications)} devices at "
            + f"{core.helpers.as_local(now)}",
        )

    @_catch_login_errors
    async def _async_update_last_called(self, last_called: dict = None, force=False):
        """Update the last called device for the login_obj.

        This will store the last_called in hass.data and also fire an event
        to notify listeners.
        """
        if not last_called or not (last_called and last_called.get("summary")):
            try:
                last_called = await alexapy.AlexaAPI.get_last_device_serial(self._login)
            except TypeError:
                _LOGGER.debug(
                    f"{alexapy.hide_email(self.email)}: Error updating last_called: "
                    + f"{alexapy.hide_serial(last_called)}",
                )
                return
        _LOGGER.debug(
            f"{alexapy.hide_email(self.email)}: Updated last_called: "
            + f"{alexapy.hide_serial(last_called)}",
        )
        stored_data = self._last_called
        if (force or stored_data is not None and last_called != stored_data) or (
            stored_data is None and last_called is not None
        ):
            _LOGGER.debug(
                f"{alexapy.hide_email(self.email)}: last_called changed: "
                + f"{alexapy.hide_serial(stored_data)} to {alexapy.hide_serial(last_called)}",
            )
            self.controller.dispatcher.async_send(
                f"{self._owner.domain}_{alexapy.hide_email(self.email)}"[0:32],
                {"last_called_change": last_called},
            )
        self._last_called = last_called

    async def async_update_last_called(self):
        await self._async_update_last_called()

    @_catch_login_errors
    async def _update_bluetooth_state(self, device_serial: str):
        """Update the bluetooth state on ws bluetooth event."""
        bluetooth = await alexapy.AlexaAPI.get_bluetooth(self._login)
        device = self._media_player_devices[device_serial]

        if bluetooth is not None and "bluetoothStates" in bluetooth:
            for b_state in bluetooth["bluetoothStates"]:
                if device_serial == b_state["deviceSerialNumber"]:
                    device["bluetooth_state"] = b_state
                    return b_state
        _LOGGER.debug(
            f"{alexapy.hide_email(self.email)}: get_bluetooth for: "
            + f"{alexapy.hide_serial(device_serial)} failed with "
            + f"{alexapy.hide_serial(bluetooth)}",
        )
        return None

    @core.Throttle(Const.MIN_TIME_BETWEEN_SCANS, Const.MIN_TIME_BETWEEN_FORCED_SCANS)
    @_catch_login_errors
    async def _update_dnd_state(self) -> None:
        """Update the dnd state on ws dnd combo event."""
        dnd = await alexapy.AlexaAPI.get_dnd_state(self._login)

        if dnd is not None and "doNotDisturbDeviceStatusList" in dnd:
            self.controller.dispatcher.async_send(
                f"{self._owner.domain}_{alexapy.hide_email(self.email)}"[0:32],
                {"dnd_update": dnd["doNotDisturbDeviceStatusList"]},
            )
            return
        _LOGGER.debug(f"{alexapy.hide_email(self.email)}: get_dnd_state failed: {dnd}")
        return

    async def _ws_connect(self) -> alexapy.WebsocketEchoClient:
        """Open WebSocket connection.

        This will only attempt one login before failing.
        """
        websocket: alexapy.WebsocketEchoClient = None
        email = self._login.email
        try:
            if self._login.session.closed:
                _LOGGER.debug(
                    f"{alexapy.hide_email(email)}: Websocket creation aborted. "
                    + "Session is closed.",
                )
                return
            websocket = alexapy.WebsocketEchoClient(
                self._login,
                self._ws_handler,
                self._ws_open_handler,
                self._ws_close_handler,
                self._ws_error_handler,
            )
            _LOGGER.debug(
                f"{alexapy.hide_email(email)}: Websocket created: {websocket}"
            )
            await websocket.async_run()
        except alexapy.AlexapyLoginError as err:
            _LOGGER.debug(
                f"{alexapy.hide_email(email)}: Login Error detected from websocket: {err}",
            )
            self.controller.bus.async_fire(
                "alexa_media.relogin_required",
                event_data={"email": alexapy.hide_email(email), "url": self._login.url},
            )
            return
        except BaseException as err:  # pylint: disable=broad-except
            _LOGGER.debug(
                f"{alexapy.hide_email(email)}: Websocket creation failed: {err}"
            )
            return
        return websocket

    async def _ws_handler(self, message_obj):
        """Handle websocket messages.

        This allows push notifications from Alexa to update last_called
        and media state.
        """

        signal = f"{self._owner.domain}_{alexapy.hide_email(self.email)}"[0:32]

        command: str = (
            message_obj.json_payload["command"]
            if isinstance(message_obj.json_payload, dict)
            and "command" in message_obj.json_payload
            else None
        )
        json_payload = (
            message_obj.json_payload["payload"]
            if isinstance(message_obj.json_payload, dict)
            and "payload" in message_obj.json_payload
            else None
        )
        existing_serials = self._existing_serials()
        seen_commands = self._websocket_commands
        coord = self._coordinator
        if command and json_payload:
            _LOGGER.debug(
                f"{alexapy.hide_email(self.email)}: Received websocket command: "
                + f"{command} : {alexapy.hide_serial(json_payload)}",
            )
            serial = None
            command_time = time.time()
            if command not in seen_commands:
                _LOGGER.debug(f"Adding {command} to seen_commands: {seen_commands}")
            seen_commands[command] = command_time

            if (
                "dopplerId" in json_payload
                and "deviceSerialNumber" in json_payload["dopplerId"]
            ):
                serial = json_payload["dopplerId"]["deviceSerialNumber"]
            elif (
                "key" in json_payload
                and "entryId" in json_payload["key"]
                and json_payload["key"]["entryId"].find("#") != -1
            ):
                serial = (json_payload["key"]["entryId"]).split("#")[2]
                json_payload["key"]["serialNumber"] = serial
            else:
                serial = None
            if command == "PUSH_ACTIVITY":
                #  Last_Alexa Updated
                last_called = {
                    "serialNumber": serial,
                    "timestamp": json_payload["timestamp"],
                }
                try:
                    await coord.async_request_refresh()
                    if serial and serial in existing_serials:
                        await self._async_update_last_called(last_called)
                    self.controller.dispatcher.async_send(
                        signal,
                        {"push_activity": json_payload},
                    )
                except alexapy.AlexapyConnectionError:
                    # Catch case where activities doesn't report valid json
                    pass
            elif command in (
                "PUSH_AUDIO_PLAYER_STATE",
                "PUSH_MEDIA_CHANGE",
                "PUSH_MEDIA_PROGRESS_CHANGE",
            ):
                # Player update/ Push_media from tune_in
                if serial and serial in existing_serials:
                    _LOGGER.debug(
                        f"Updating media_player: {alexapy.hide_serial(json_payload)}"
                    )
                    self.controller.dispatcher.async_send(
                        signal,
                        {"player_state": json_payload},
                    )
            elif command == "PUSH_VOLUME_CHANGE":
                # Player volume update
                if serial and serial in existing_serials:
                    _LOGGER.debug(
                        f"Updating media_player volume: {alexapy.hide_serial(json_payload)}",
                    )
                    self.controller.dispatcher.async_send(
                        signal,
                        {"player_state": json_payload},
                    )
            elif command in (
                "PUSH_DOPPLER_CONNECTION_CHANGE",
                "PUSH_EQUALIZER_STATE_CHANGE",
            ):
                # Player availability update
                if serial and serial in existing_serials:
                    _LOGGER.debug(
                        f"Updating media_player availability {alexapy.hide_serial(json_payload)}",
                    )
                    self.controller.dispatcher.async_send(
                        signal,
                        {"player_state": json_payload},
                    )
            elif command == "PUSH_BLUETOOTH_STATE_CHANGE":
                # Player bluetooth update
                bt_event = json_payload["bluetoothEvent"]
                bt_success = json_payload["bluetoothEventSuccess"]
                if (
                    serial
                    and serial in existing_serials
                    and bt_success
                    and bt_event
                    and bt_event in ["DEVICE_CONNECTED", "DEVICE_DISCONNECTED"]
                ):
                    _LOGGER.debug(
                        f"Updating media_player bluetooth {alexapy.hide_serial(json_payload)}",
                    )
                    bluetooth_state = await self._update_bluetooth_state(serial)
                    # _LOGGER.debug("bluetooth_state %s",
                    #               hide_serial(bluetooth_state))
                    if bluetooth_state:
                        self.controller.dispatcher.async_send(
                            signal,
                            {"bluetooth_change": bluetooth_state},
                        )
            elif command == "PUSH_MEDIA_QUEUE_CHANGE":
                # Player availability update
                if serial and serial in existing_serials:
                    _LOGGER.debug(
                        f"Updating media_player queue {alexapy.hide_serial(json_payload)}"
                    )
                    self.controller.dispatcher.async_send(
                        signal,
                        {"queue_state": json_payload},
                    )
            elif command == "PUSH_NOTIFICATION_CHANGE":
                # Player update
                await self._process_notifications()
                if serial and serial in existing_serials:
                    _LOGGER.debug(
                        f"Updating mediaplayer notifications: {alexapy.hide_serial(json_payload)}",
                    )
                    self.controller.dispatcher.async_send(
                        signal,
                        {"notification_update": json_payload},
                    )
            elif command in [
                "PUSH_DELETE_DOPPLER_ACTIVITIES",  # delete Alexa history
                "PUSH_LIST_CHANGE",  # clear a shopping list
                # https://github.com/custom-components/alexa_media_player/issues/1190
                "PUSH_LIST_ITEM_CHANGE",  # update shopping list
                "PUSH_CONTENT_FOCUS_CHANGE",  # likely prime related refocus
                "PUSH_DEVICE_SETUP_STATE_CHANGE",  # likely device changes mid setup
                "PUSH_MEDIA_PREFERENCE_CHANGE",  # disliking or liking songs,
                # https://github.com/custom-components/alexa_media_player/issues/1599
            ]:
                pass
            else:
                _LOGGER.warning(
                    f"Unhandled command: {command} with data {alexapy.hide_serial(json_payload)}."
                )
            if serial in existing_serials:
                history = self._websocket_history.get(serial)
                if history is None or (
                    history and command_time - history[len(history) - 1][1] > 2
                ):
                    history = [(command, command_time)]
                else:
                    history.append([command, command_time])
                self._websocket_history[serial] = history
                events = []
                for old_command, old_command_time in history:
                    if (
                        old_command
                        in {"PUSH_VOLUME_CHANGE", "PUSH_EQUALIZER_STATE_CHANGE"}
                        and command_time - old_command_time < 0.25
                    ):
                        events.append(
                            (old_command, round(command_time - old_command_time, 2))
                        )
                    elif old_command in {"PUSH_AUDIO_PLAYER_STATE"}:
                        # There is a potential false positive generated during this event
                        events = []
                if len(events) >= 4:
                    _LOGGER.debug(
                        f"{alexapy.hide_serial(serial)}: Detected potential DND websocket "
                        + f"change with {len(events)} events {events}",
                    )
                    await self._update_dnd_state()
            if (
                serial
                and serial not in existing_serials
                and serial not in self._excluded
            ):
                _LOGGER.debug(f"Discovered new media_player {serial}")
                self._new_devices = True
                coordinator = self._coordinator
                if coordinator:
                    await coordinator.async_request_refresh()

    async def _ws_open_handler(self):
        """Handle websocket open."""

        email = self.email
        _LOGGER.debug(f"{alexapy.hide_email(email)}: Websocket successfully connected")
        self._websocket_error = 0  # set errors to 0
        self._websocket_lastattempt = time.time()

    async def _ws_close_handler(self):
        """Handle websocket close.

        This should attempt to reconnect up to 5 times
        """

        email = self.email
        if self._login.close_requested:
            _LOGGER.debug(
                f"{alexapy.hide_email(email)}: Close requested; will not reconnect websocket",
            )
            return
        if not self._login.status.get("login_successful"):
            _LOGGER.debug(
                f"{alexapy.hide_email(email)}: Login error; will not reconnect websocket"
            )
            return
        errors: int = self._websocket_error
        delay: int = 5 * 2**errors
        last_attempt = self._websocket_lastattempt
        now = time.time()
        if (now - last_attempt) < delay:
            return
        websocket_enabled = bool(self._websocket_client)
        while errors < 5 and not websocket_enabled:
            _LOGGER.debug(
                f"{alexapy.hide_email(email)}: Websocket closed; reconnect #{errors} in {delay}s",
            )
            self._websocket_lastattempt = time.time()
            websocket_enabled = self._websocket_client = await self._ws_connect()
            errors = self._websocket_error = self._websocket_error + 1
            delay = 5 * 2**errors
            await asyncio.sleep(delay)
        if not websocket_enabled:
            _LOGGER.debug(
                f"{alexapy.hide_email(email)}: Websocket closed; retries exceeded; polling"
            )
        coordinator = self._coordinator
        if coordinator:
            coordinator.update_interval = dt.timedelta(
                seconds=self._scan_interval * 10
                if websocket_enabled
                else self._scan_interval
            )
            await coordinator.async_request_refresh()

    async def _ws_error_handler(self, message):
        """Handle websocket error.

        This currently logs the error.  In the future, this should invalidate
        the websocket and determine if a reconnect should be done. By
        specification, websockets will issue a close after every error.
        """
        email = self.email
        errors = self._websocket_error
        _LOGGER.debug(
            f"{alexapy.hide_email(email)}: Received websocket error #{errors} {message}: "
            + f"type {type(message)}",
        )
        self._websocket_client = None
        if not self._login.close_requested and (
            self._login.session.closed
            or message == "<class 'aiohttp.streams.EofStream'>"
        ):
            self._websocket_error = 5
            _LOGGER.debug(f"{alexapy.hide_email(email)}: Immediate abort on EoFstream")
            return
        self._websocket_error = errors + 1

    async def async_setup_media_player_devices(
        self, entry: core.ConfigEntry, add_entities_callback: core.AddEntitiesCallback
    ) -> bool:
        """Setup media player entities"""
        if await self.async_setup_media_player_platform(
            entry.data, add_entities_callback, discovery_info=None
        ):
            for component in Const.DEPENDENT_ALEXA_COMPONENTS:
                entry_setup = self._switch_entry_setup
                if entry_setup or component == "notify":
                    _LOGGER.debug(
                        f"{alexapy.hide_email(self.email)}: Loading {component}"
                    )
                    cleaned_config = entry.data.copy()
                    cleaned_config.pop(_const.CONF_PASSWORD, None)
                    # CONF_PASSWORD contains sensitive info which is no longer needed
                    self.controller.async_create_task(
                        self.controller.setup.async_load_platform(
                            component,
                            self._owner.domain,
                            {
                                _const.CONF_NAME: self._owner.domain,
                                "config": cleaned_config,
                            },
                            cleaned_config,
                        )
                    )
                else:
                    _LOGGER.debug(
                        f"{alexapy.hide_email(self.email)}: Loading config entry for {component}"
                    )
                    self._switch_entry_setup = await self.controller.async_add_job(
                        self.controller.config_entries.async_forward_entry_setup(
                            entry, component
                        )
                    )
            return True
        raise core.ConfigEntryNotReady

    async def async_setup_media_player_platform(  # pylint: disable=unused-argument
        self,
        config: core.ConfigType,
        add_entities_callback: core.AddEntitiesCallback,
        discovery_info: core.DiscoveryInfoType,
    ) -> bool:
        """Setup MediaPlayer platform"""
        devices = []  # type: list[AlexaClient]
        entry_setup = self._entry_setup
        alexa_client = None
        for key, device in self._media_player_devices.items():
            if key not in self._media_player_entities:
                alexa_client = AlexaClient(
                    self,
                    device,
                    self.login,
                    self.second_account_index,
                )
                await alexa_client.init(device)
                devices.append(alexa_client)
                self._media_player_entities[key] = alexa_client
            else:
                _LOGGER.debug(
                    f"{alexapy.hide_email(self.email)}: Skipping already added device: "
                    + f"{alexapy.hide_serial(key)}:{alexa_client}",
                )
        result = await add_devices(
            alexapy.hide_email(self.email), devices, add_entities_callback
        )
        if result and entry_setup:
            _LOGGER.debug("Detected config entry already setup, using load platform")
            for component in Const.DEPENDENT_ALEXA_COMPONENTS:
                self.controller.async_create_task(
                    self.controller.setup.async_load_platform(
                        component,
                        self._owner.domain,
                        {_const.CONF_NAME: self._owner.domain, "config": config},
                        config,
                    )
                )
        return result

    async def async_setup_switch_platform(
        self,
        config: core.ConfigType,
        add_entities_callback: core.AddEntitiesCallback,
        discovery_info: core.DiscoveryInfoType = None,
    ):
        """Set up the Alexa switch platform."""
        devices = []  # type: list[DNDSwitch]
        if not config:
            config = discovery_info["config"]
        account = alexapy.hide_email(config[_const.CONF_EMAIL])
        _LOGGER.debug(f"{account}: Loading switches")
        for key, _ in self._media_player_devices.items():
            if key not in self._media_player_entities:
                _LOGGER.debug(
                    f"{account}: Media player {alexapy.hide_serial(key)} not "
                    + "loaded yet; delaying load",
                )
                raise core.ConfigEntryNotReady
            if key not in self._dnd_entities:
                self._dnd_entities[key] = {}
                for switch_key, class_ in _SWITCH_TYPES:
                    if (
                        switch_key == "dnd"
                        and not self._dnd_switches.get(key, {}).get("dnd")
                    ) or (
                        switch_key in ["shuffle", "repeat"]
                        and "MUSIC_SKILL"
                        not in self._media_player_devices.get(key, {}).get(
                            "capabilities", {}
                        )
                    ):
                        _LOGGER.debug(
                            f"{account}: Skipping {switch_key} for {alexapy.hide_serial(key)}",
                        )
                        continue
                    alexa_client = class_(
                        self, self._media_player_entities[key]
                    )  # type: AlexaMediaSwitch
                    _LOGGER.debug(
                        f"{account}: Found {alexapy.hide_serial(key)} {switch_key} switch "
                        + f"with status: {alexa_client.is_on}",
                    )
                    devices.append(alexa_client)
                    self._dnd_entities[key][switch_key] = alexa_client
            else:
                for alexa_client in self._dnd_entities[key].values():
                    _LOGGER.debug(
                        f"{account}: Skipping already added device: {alexa_client}",
                    )
        return await add_devices(
            account,
            devices,
            add_entities_callback,
        )

    async def async_setup_switch_devices(
        self,
        config_entry: core.ConfigEntry,
        add_entities_callback: core.AddEntitiesCallback,
    ):
        """Set up the Alexa switch platform by config_entry."""
        return await self.async_setup_switch_platform(
            config_entry.data, add_entities_callback, discovery_info=None
        )


def _alarm_just_dismissed(
    alarm: dict[str, typing.Any],
    previous_status: str,
    previous_version: str,
) -> bool:
    """Given the previous state of an alarm, determine if it has just been dismissed."""

    if previous_status not in ("SNOOZED", "ON"):
        # The alarm had to be in a status that supported being dismissed
        return False

    if previous_version is None:
        # The alarm was probably just created
        return False

    if not alarm:
        # The alarm that was probably just deleted.
        return False

    if alarm.get("status") not in ("OFF", "ON"):
        # A dismissed alarm is guaranteed to be turned off(one-off alarm) or
        # left on(recurring alarm)
        return False

    if previous_version == alarm.get("version"):
        # A dismissal always has a changed version.
        return False

    if int(alarm.get("version", "0")) > 1 + int(previous_version):
        # This is an absurd thing to check, but it solves many, many edge cases.
        # Experimentally, when an alarm is dismissed, the version always increases by 1
        # When an alarm is edited either via app or voice, its version always increases by 2+
        return False

    # It seems obvious that a check involving time should be necessary. It is not.
    # We know there was a change and that it wasn't an edit.
    # We also know the alarm's status rules out a snooze.
    # The only remaining possibility is that this alarm was just dismissed.
    return True
