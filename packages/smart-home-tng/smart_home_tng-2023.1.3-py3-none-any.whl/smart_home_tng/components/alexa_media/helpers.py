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

import hashlib
import logging
import typing

import alexapy
import wrapt

from ... import core
from .const import Const

_const: typing.TypeAlias = core.Const
_LOGGER: typing.Final = logging.getLogger(__name__)

# pylint: disable=unused-variable


@wrapt.decorator
async def _catch_login_errors(func, instance, args, kwargs) -> typing.Any:
    """Detect AlexapyLoginError and attempt relogin."""

    # pylint: disable=logging-too-many-args, protected-access

    result = None
    if instance is None and args:
        instance = args[0]
    if hasattr(instance, "check_login_changes"):
        # _LOGGER.debug(
        #     "%s checking for login changes", instance,
        # )
        instance.check_login_changes()
    try:
        result = await func(*args, **kwargs)
    except alexapy.AlexapyLoginCloseRequested:
        _LOGGER.debug(
            "%s.%s: Ignoring attempt to access Alexa after HA shutdown",
            func.__module__[func.__module__.find(".") + 1 :],
            func.__name__,
        )
        return None
    except alexapy.AlexapyLoginError as ex:
        login = None
        email = None
        controller = None
        all_args = list(args) + list(kwargs.values())
        # _LOGGER.debug("Func %s instance %s %s %s", func, instance, args, kwargs)
        if instance:
            if hasattr(instance, "_login"):
                login = instance._login
                controller = instance.controller
        else:
            for arg in all_args:
                _LOGGER.debug("Checking %s", arg)

                if isinstance(arg, alexapy.AlexaLogin):
                    login = arg
                    break
                if hasattr(arg, "_login"):
                    login = instance._login
                    controller = instance.controller
                    break

        if login:
            email = login.email
            _LOGGER.debug(
                "%s.%s: detected bad login for %s: %s",
                func.__module__[func.__module__.find(".") + 1 :],
                func.__name__,
                alexapy.hide_email(email),
                Const.EXCEPTION_TEMPLATE.format(type(ex).__name__, ex.args),
            )
        try:
            controller
        except NameError:
            controller = None
        _report_relogin_required(controller, login, email)
        return None
    return result


def _report_relogin_required(
    controller: core.SmartHomeController, login: alexapy.AlexaLogin, email: str
) -> bool:
    """Send message for relogin required."""
    if controller and login and email:
        if login.status:
            _LOGGER.debug(
                f"Reporting need to relogin to {login.url} with {alexapy.hide_email(email)} "
                + f"stats: {login.stats}",
            )
            controller.bus.async_fire(
                "alexa_media.relogin_required",
                event_data={
                    "email": alexapy.hide_email(email),
                    "url": login.url,
                    "stats": login.stats,
                },
            )
            return True
    return False


async def _calculate_uuid(
    component: core.SmartHomeControllerComponent, email: str, url: str
) -> tuple[str, int]:
    """Return uuid and index of email/url.

    Args
        hass (bool): Hass entity
        url (Text): url for account
        email (Text): email for account

    Returns
        dict: dictionary with uuid and index

    """
    return_index = 0
    entries = component.controller.config_entries.async_entries(component.domain)
    for index, entry in enumerate(entries):
        if (
            entry.data.get(_const.CONF_EMAIL) == email
            and entry.data.get(_const.CONF_URL) == url
        ):
            return_index = index
            break
    uuid = await component.controller.async_get_instance_id()
    return_uuid = hex(
        int(uuid, 16)
        # increment uuid for second accounts
        + return_index
        # hash email/url in case HA uuid duplicated
        + int(  # nosec
            hashlib.md5(
                (email.lower() + url.lower()).encode(), usedforsecurity=False
            ).hexdigest(),
            16,
        )
    )[-32:]
    return return_uuid, return_index


async def add_devices(
    account: str,
    devices: list[core.Entity],
    add_devices_callback: core.AddEntitiesCallback,
    include_filter: list[str] = None,
    exclude_filter: list[str] = None,
) -> bool:
    """Add devices using add_devices_callback."""
    include_filter = include_filter or []
    exclude_filter = exclude_filter or []
    new_devices = []
    for device in devices:
        if (
            include_filter
            and device.name not in include_filter
            or exclude_filter
            and device.name in exclude_filter
        ):
            _LOGGER.debug(f"{account}: Excluding device: {device}", account, device)
            continue
        new_devices.append(device)
    devices = new_devices
    if devices:
        _LOGGER.debug(f"{account}: Adding {devices}", account, devices)
        try:
            add_devices_callback(devices, False)
            return True
        except core.SmartHomeControllerError as exception_:
            message = str(exception_)  # type: str
            if message.startswith("Entity id already exists"):
                _LOGGER.debug(f"{account}: Device already added: {message}")
            else:
                _LOGGER.debug(
                    f"{account}: Unable to add devices: {devices} : {message}"
                )
        except BaseException as ex:  # pylint: disable=broad-except
            tmp = Const.EXCEPTION_TEMPLATE.format(type(ex).__name__, ex.args)
            _LOGGER.debug(
                f"{alexapy.hide_email(account)}: Unable to add devices: " + f"{tmp}",
            )
    else:
        return True
    return False
