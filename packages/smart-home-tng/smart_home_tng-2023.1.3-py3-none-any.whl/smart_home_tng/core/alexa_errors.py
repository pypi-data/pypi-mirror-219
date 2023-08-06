"""

Core components of Smart Home - The Next Generation.

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

from .const import Const
from .smart_home_controller_error import SmartHomeControllerError

if not typing.TYPE_CHECKING:

    class SmartHomeController:
        pass


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController

_const: typing.TypeAlias = Const
_API_TEMP_UNITS: typing.Final = {
    _const.UnitOfTemperature.FAHRENHEIT: "FAHRENHEIT",
    _const.UnitOfTemperature.CELSIUS: "CELSIUS",
}

# pylint: disable=unused-variable


class NoTokenAvailable(SmartHomeControllerError):
    """There is no access token available."""


class RequireRelink(Exception):
    """The skill needs to be relinked."""


class UnsupportedInterface(SmartHomeControllerError):
    """This entity does not support the requested Smart Home API interface."""


class UnsupportedProperty(SmartHomeControllerError):
    """This entity does not support the requested Smart Home API property."""


class AlexaError(Exception):
    """Base class for errors that can be serialized for the Alexa API.

    A handler can raise subclasses of this to return an error to the request.
    """

    namespace: str = None
    error_type: str = None

    def __init__(self, error_message, payload=None):
        """Initialize an alexa error."""
        Exception.__init__(self)
        self.error_message = error_message
        self.payload = payload


class AlexaInvalidEndpointError(AlexaError):
    """The endpoint in the request does not exist."""

    namespace = "Alexa"
    error_type = "NO_SUCH_ENDPOINT"

    def __init__(self, endpoint_id):
        """Initialize invalid endpoint error."""
        msg = f"The endpoint {endpoint_id} does not exist"
        AlexaError.__init__(self, msg)
        self.endpoint_id = endpoint_id


class AlexaInvalidValueError(AlexaError):
    """Class to represent InvalidValue errors."""

    namespace = "Alexa"
    error_type = "INVALID_VALUE"


class AlexaInternalError(AlexaError):
    """Class to represent internal errors."""

    namespace = "Alexa"
    error_type = "INTERNAL_ERROR"


class AlexaNotSupportedInCurrentMode(AlexaError):
    """The device is not in the correct mode to support this command."""

    namespace = "Alexa"
    error_type = "NOT_SUPPORTED_IN_CURRENT_MODE"

    def __init__(
        self,
        endpoint_id: str,
        current_mode: typing.Literal["COLOR", "ASLEEP", "NOT_PROVISIONED", "OTHER"],
    ) -> None:
        """Initialize invalid endpoint error."""
        msg = f"Not supported while in {current_mode} mode"
        AlexaError.__init__(self, msg, {"currentDeviceMode": current_mode})
        self.endpoint_id = endpoint_id


class AlexaUnsupportedThermostatModeError(AlexaError):
    """Class to represent UnsupportedThermostatMode errors."""

    namespace = "Alexa.ThermostatController"
    error_type = "UNSUPPORTED_THERMOSTAT_MODE"


class AlexaTempRangeError(AlexaError):
    """Class to represent TempRange errors."""

    namespace = "Alexa"
    error_type = "TEMPERATURE_VALUE_OUT_OF_RANGE"

    def __init__(
        self, shc: SmartHomeController, temp: float, min_temp: float, max_temp: float
    ):
        """Initialize TempRange error."""
        unit = shc.config.units.temperature_unit
        temp_range = {
            "minimumValue": {"value": min_temp, "scale": _API_TEMP_UNITS[unit]},
            "maximumValue": {"value": max_temp, "scale": _API_TEMP_UNITS[unit]},
        }
        payload = {"validRange": temp_range}
        msg = f"The requested temperature {temp} is out of range"

        AlexaError.__init__(self, msg, payload)


class AlexaBridgeUnreachableError(AlexaError):
    """Class to represent BridgeUnreachable errors."""

    namespace = "Alexa"
    error_type = "BRIDGE_UNREACHABLE"


class AlexaSecurityPanelUnauthorizedError(AlexaError):
    """Class to represent SecurityPanelController Unauthorized errors."""

    namespace = "Alexa.SecurityPanelController"
    error_type = "UNAUTHORIZED"


class AlexaSecurityPanelAuthorizationRequired(AlexaError):
    """Class to represent SecurityPanelController AuthorizationRequired errors."""

    namespace = "Alexa.SecurityPanelController"
    error_type = "AUTHORIZATION_REQUIRED"


class AlexaAlreadyInOperationError(AlexaError):
    """Class to represent AlreadyInOperation errors."""

    namespace = "Alexa"
    error_type = "ALREADY_IN_OPERATION"


class AlexaInvalidDirectiveError(AlexaError):
    """Class to represent InvalidDirective errors."""

    namespace = "Alexa"
    error_type = "INVALID_DIRECTIVE"


class AlexaVideoActionNotPermittedForContentError(AlexaError):
    """Class to represent action not permitted for content errors."""

    namespace = "Alexa.Video"
    error_type = "ACTION_NOT_PERMITTED_FOR_CONTENT"
