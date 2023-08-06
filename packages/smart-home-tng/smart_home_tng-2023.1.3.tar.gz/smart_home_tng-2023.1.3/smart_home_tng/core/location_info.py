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

import asyncio
import collections.abc
import logging
import math
import typing

import aiohttp

from .const import Const
from .state import State


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


_WHOAMI_URL: typing.Final = "https://services.home-assistant.io/whoami/v1"
_WHOAMI_URL_DEV: typing.Final = (
    "https://services-dev.home-assistant.workers.dev/whoami/v1"
)

# Constants from https://github.com/maurycyp/vincenty
# Earth ellipsoid according to WGS 84
# Axis a of the ellipsoid (Radius of the earth in meters)
_AXIS_A: typing.Final = 6378137
# Flattening f = (a-b) / a
_FLATTENING: typing.Final = 1 / 298.257223563
# Axis b of the ellipsoid in meters.
_AXIS_B: typing.Final = 6356752.314245

_MILES_PER_KILOMETER: typing.Final = 0.621371
_MAX_ITERATIONS: typing.Final = 200
_CONVERGENCE_THRESHOLD: typing.Final = 1e-12

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable
class LocationInfo(typing.NamedTuple):
    """Tuple with location information."""

    ip: str
    country_code: str
    currency: str
    region_code: str
    region_name: str
    city: str
    zip_code: str
    time_zone: str
    latitude: float
    longitude: float
    use_metric: bool

    @staticmethod
    async def async_detect_location_info(
        session: aiohttp.ClientSession,
    ):
        """Detect location information."""
        if (data := await LocationInfo._get_whoami(session)) is None:
            return None

        data["use_metric"] = data["country_code"] not in ("US", "MM", "LR")

        return LocationInfo(**data)

    @staticmethod
    def distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate the distance in meters between two points.

        Async friendly.
        """
        if lat1 is None or lon1 is None:
            return None
        result = LocationInfo.vincenty((lat1, lon1), (lat2, lon2))
        if result is None:
            return None
        return result * 1000

    # Author: https://github.com/maurycyp
    # Source: https://github.com/maurycyp/vincenty
    # License: https://github.com/maurycyp/vincenty/blob/master/LICENSE
    @staticmethod
    def vincenty(
        point1: tuple[float, float], point2: tuple[float, float], miles: bool = False
    ) -> float:
        """
        Vincenty formula (inverse method) to calculate the distance.

        Result in kilometers or miles between two points on the surface of a
        spheroid.

        Async friendly.
        """
        # short-circuit coincident points
        if point1[0] == point2[0] and point1[1] == point2[1]:
            return 0.0

        # pylint: disable=invalid-name
        U1 = math.atan((1 - _FLATTENING) * math.tan(math.radians(point1[0])))
        U2 = math.atan((1 - _FLATTENING) * math.tan(math.radians(point2[0])))
        L = math.radians(point2[1] - point1[1])
        Lambda = L

        sinU1 = math.sin(U1)
        cosU1 = math.cos(U1)
        sinU2 = math.sin(U2)
        cosU2 = math.cos(U2)

        for _ in range(_MAX_ITERATIONS):
            sinLambda = math.sin(Lambda)
            cosLambda = math.cos(Lambda)
            sinSigma = math.sqrt(
                (cosU2 * sinLambda) ** 2
                + (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2
            )
            if sinSigma == 0.0:
                return 0.0  # coincident points
            cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
            sigma = math.atan2(sinSigma, cosSigma)
            sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
            cosSqAlpha = 1 - sinAlpha**2
            try:
                cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
            except ZeroDivisionError:
                cos2SigmaM = 0
            C = _FLATTENING / 16 * cosSqAlpha * (4 + _FLATTENING * (4 - 3 * cosSqAlpha))
            LambdaPrev = Lambda
            Lambda = L + (1 - C) * _FLATTENING * sinAlpha * (
                sigma
                + C
                * sinSigma
                * (cos2SigmaM + C * cosSigma * (-1 + 2 * cos2SigmaM**2))
            )
            if abs(Lambda - LambdaPrev) < _CONVERGENCE_THRESHOLD:
                break  # successful convergence
        else:
            return None  # failure to converge

        uSq = cosSqAlpha * (_AXIS_A**2 - _AXIS_B**2) / (_AXIS_B**2)
        A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
        B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
        deltaSigma = (
            B
            * sinSigma
            * (
                cos2SigmaM
                + B
                / 4
                * (
                    cosSigma * (-1 + 2 * cos2SigmaM**2)
                    - B
                    / 6
                    * cos2SigmaM
                    * (-3 + 4 * sinSigma**2)
                    * (-3 + 4 * cos2SigmaM**2)
                )
            )
        )
        s = _AXIS_B * A * (sigma - deltaSigma)

        s /= 1000  # Conversion of meters to kilometers
        if miles:
            s *= _MILES_PER_KILOMETER  # kilometers to miles

        return round(s, 6)

    @staticmethod
    async def _get_whoami(
        session: aiohttp.ClientSession,
    ) -> dict[str, typing.Any]:
        """Query whoami.home-assistant.io for location data."""
        try:
            resp = await session.get(
                _WHOAMI_URL_DEV
                if Const.__version__.endswith("0.dev0")
                else _WHOAMI_URL,
                timeout=30,
            )
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return None

        try:
            raw_info = await resp.json()
        except (aiohttp.ClientError, ValueError):
            return None

        return {
            "ip": raw_info.get("ip"),
            "country_code": raw_info.get("country"),
            "currency": raw_info.get("currency"),
            "region_code": raw_info.get("region_code"),
            "region_name": raw_info.get("region"),
            "city": raw_info.get("city"),
            "zip_code": raw_info.get("postal_code"),
            "time_zone": raw_info.get("timezone"),
            "latitude": float(raw_info.get("latitude")),
            "longitude": float(raw_info.get("longitude")),
        }

    @staticmethod
    def has_location(state: State) -> bool:
        """Test if state contains a valid location.

        Async friendly.
        """
        return (
            isinstance(state, State)
            and isinstance(state.attributes.get(Const.ATTR_LATITUDE), float)
            and isinstance(state.attributes.get(Const.ATTR_LONGITUDE), float)
        )

    @staticmethod
    def closest(
        latitude: float, longitude: float, states: collections.abc.Iterable[State]
    ) -> State:
        """Return closest state to point.

        Async friendly.
        """
        with_location = [state for state in states if LocationInfo.has_location(state)]

        if not with_location:
            return None

        return min(
            with_location,
            key=lambda state: LocationInfo.distance(
                state.attributes.get(Const.ATTR_LATITUDE),
                state.attributes.get(Const.ATTR_LONGITUDE),
                latitude,
                longitude,
            )
            or 0,
        )

    @staticmethod
    def find_coordinates(
        shc: SmartHomeController, name: str, recursion_history: list = None
    ) -> str:
        """Try to resolve the a location from a supplied name or entity_id.

        Will recursively resolve an entity if pointed to by the state of the
        supplied entity.
        Returns coordinates in the form of '90.000,180.000', an address or
        the state of the last resolved entity.
        """
        # Check if a friendly name of a zone was supplied
        if (zone_coords := LocationInfo.resolve_zone(shc, name)) is not None:
            return zone_coords

        # Check if an entity_id was supplied.
        if (entity_state := shc.states.get(name)) is None:
            _LOGGER.debug(f"Unable to find entity {name}")
            return name

        # Check if the entity_state has location attributes
        if LocationInfo.has_location(entity_state):
            return LocationInfo._get_location_from_attributes(entity_state)

        # Check if entity_state is a zone
        zone_entity = shc.states.get(f"zone.{entity_state.state}")
        if LocationInfo.has_location(zone_entity):  # type: ignore[arg-type]
            _LOGGER.debug(
                f"{name} is in {zone_entity.entity_id}, getting zone location"
            )
            return LocationInfo._get_location_from_attributes(zone_entity)  # type: ignore[arg-type]

        # Check if entity_state is a friendly name of a zone
        if (
            zone_coords := LocationInfo.resolve_zone(shc, entity_state.state)
        ) is not None:
            return zone_coords

        # Check if entity_state is an entity_id
        if recursion_history is None:
            recursion_history = []
        recursion_history.append(name)
        if entity_state.state in recursion_history:
            _LOGGER.error(
                "Circular reference detected while trying to find coordinates of an entity. "
                + f"The state of {entity_state.state} has already been checked"
            )
            return None
        _LOGGER.debug(f"Getting nested entity for state: {entity_state.state}")
        nested_entity = shc.states.get(entity_state.state)
        if nested_entity is not None:
            _LOGGER.debug(
                f"Resolving nested entity_id: {entity_state.state}", entity_state.state
            )
            return LocationInfo.find_coordinates(
                shc, entity_state.state, recursion_history
            )

        # Might be an address, coordinates or anything else. This has to be checked by the caller.
        return entity_state.state

    @staticmethod
    def resolve_zone(shc: SmartHomeController, zone_name: str) -> str:
        """
        Get a lat/long from a zones friendly_name or None
        if no zone is found by that friendly_name.
        """
        states = shc.states.async_all("zone")
        for state in states:
            if state.name == zone_name:
                return LocationInfo._get_location_from_attributes(state)

        return None

    @staticmethod
    def _get_location_from_attributes(entity_state: State) -> str:
        """Get the lat/long string from an entities attributes."""
        attr = entity_state.attributes
        return f"{attr.get(Const.ATTR_LATITUDE)},{attr.get(Const.ATTR_LONGITUDE)}"

    @staticmethod
    def in_zone(
        zone: State, latitude: float, longitude: float, radius: float = 0
    ) -> bool:
        """Test if given latitude, longitude is in given zone.

        Async friendly.
        """
        if zone.state == Const.STATE_UNAVAILABLE:
            return False

        zone_dist = LocationInfo.distance(
            latitude,
            longitude,
            zone.attributes[Const.ATTR_LATITUDE],
            zone.attributes[Const.ATTR_LONGITUDE],
        )

        if zone_dist is None or zone.attributes[Const.ATTR_RADIUS] is None:
            return False
        return zone_dist - radius < typing.cast(
            float, zone.attributes[Const.ATTR_RADIUS]
        )
