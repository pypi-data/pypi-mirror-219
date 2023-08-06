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

import collections.abc
import logging
import os
import pathlib
import typing

import yarl
from urllib3.util import url

from . import helpers
from .api_config import ApiConfig
from .callback import callback
from .config_source import ConfigSource
from .const import Const
from .location_info import LocationInfo
from .smart_home_controller_error import SmartHomeControllerError
from .store import Store
from .unit_system import UnitSystem

_CORE_STORAGE_KEY = "core.config"
_CORE_STORAGE_VERSION = 1

_LOGGER: typing.Final = logging.getLogger(__name__)


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class Config:
    """Configuration settings for Smart Home - The Next Generation."""

    def __init__(self, shc: SmartHomeController) -> None:
        """Initialize a new config object."""
        self._shc = shc
        self._latitude: float = 0
        self._longitude: float = 0
        self._elevation: int = 0
        self._location_name: str = "Home"
        self._time_zone: str = "UTC"
        self._units: UnitSystem = UnitSystem.METRIC()
        self._internal_url: str = None
        self._external_url: str = None
        self._currency: str = "EUR"

        self._config_source: ConfigSource = ConfigSource.DEFAULT

        # If True, pip install is skipped for requirements on startup
        self._skip_pip: bool = False

        # List of loaded components
        self._components: set[str] = set()

        # API (HTTP) server configuration
        self._api: ApiConfig = None

        # Directory that holds the configuration
        self._config_dir: str = None

        # List of allowed external dirs to access
        self._allowlist_external_dirs: set[str] = set()

        # List of allowed external URLs that integrations may use
        self._allowlist_external_urls: set[str] = set()

        # Dictionary of Media folders that integrations may use
        self._media_dirs: dict[str, str] = {}

        # If Home Assistant is running in safe mode
        self._safe_mode: bool = False

        # Use legacy template behavior
        self._legacy_templates: bool = False

        # Error Log Path
        self._error_log_path: str = None

    @property
    def api(self) -> ApiConfig:
        return self._api

    @api.setter
    def api(self, api: ApiConfig) -> None:
        if self._api is None:
            self._api = api

    @property
    def error_log_path(self) -> str:
        return self._error_log_path

    @error_log_path.setter
    def error_log_path(self, value: str) -> None:
        if self._error_log_path is None:
            self._error_log_path = value

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, latitude: float) -> None:
        if -90.0 <= latitude <= 90.0:
            self._latitude = latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, longitude: float) -> None:
        if -180.0 <= longitude <= 180.0:
            self._longitude = longitude

    @property
    def elevation(self) -> int:
        return self._elevation

    @elevation.setter
    def elevation(self, elevation: int) -> None:
        self._elevation = elevation

    @property
    def location_name(self) -> str:
        return self._location_name

    @location_name.setter
    def location_name(self, location_name: str) -> None:
        if location_name != "":
            self._location_name = location_name

    @property
    def time_zone(self) -> str:
        return self._time_zone

    @property
    def units(self) -> UnitSystem:
        return self._units

    @units.setter
    def units(self, units: UnitSystem) -> None:
        self._units = units

    @property
    def internal_url(self) -> str:
        return self._internal_url

    @internal_url.setter
    def internal_url(self, internal_url: str) -> None:
        if internal_url != "":
            self._internal_url = internal_url

    @property
    def external_url(self) -> str:
        return self._external_url

    @external_url.setter
    def external_url(self, external_url: str) -> None:
        if external_url != "":
            self._external_url = external_url

    @property
    def currency(self) -> str:
        return self._currency

    @currency.setter
    def currency(self, currency: str) -> None:
        if currency != "":
            self._currency = currency

    @property
    def config_source(self) -> ConfigSource:
        return self._config_source

    @config_source.setter
    def config_source(self, source: ConfigSource) -> None:
        if self._config_source is ConfigSource.DEFAULT:
            self._config_source = source

    @property
    def skip_pip(self) -> bool:
        return self._skip_pip

    @skip_pip.setter
    def skip_pip(self, skip_pip: bool) -> None:
        self._skip_pip = skip_pip

    @property
    def components(self) -> set:
        return frozenset(self._components)

    def component_loaded(self, component: str) -> None:
        self._components.add(component)

    @property
    def allowlist_external_dirs(self) -> collections.abc.Iterable[str]:
        return self._allowlist_external_dirs

    @allowlist_external_dirs.setter
    def allowlist_external_dirs(
        self, allow_list_external_dirs: collections.abc.Iterable[str]
    ) -> None:
        if allow_list_external_dirs is not None:
            self._allowlist_external_dirs = set()
            for allowed in allow_list_external_dirs:
                if allowed not in self._allowlist_external_dirs:
                    self._allowlist_external_dirs.add(allowed)

    @property
    def allowlist_external_urls(self) -> collections.abc.Iterable[str]:
        return self._allowlist_external_urls

    @allowlist_external_urls.setter
    def allowlist_external_urls(self, allowlist: collections.abc.Iterable[str]) -> None:
        if allowlist is not None:
            self._allowlist_external_urls = set()
            for allowed in self._allowlist_external_urls:
                if allowed not in self._allowlist_external_urls:
                    self._allowlist_external_urls.add(allowed)

    @property
    def media_dirs(self) -> collections.abc.Iterable[str, str]:
        return self._media_dirs

    @media_dirs.setter
    def media_dirs(self, media_dirs: collections.abc.Iterable[str, str]) -> None:
        if media_dirs is not None:
            self._media_dirs = {}
            for key, value in media_dirs.items():
                self._media_dirs[key] = value

    @property
    def safe_mode(self) -> bool:
        return self._safe_mode

    @safe_mode.setter
    def safe_mode(self, safe_mode: bool) -> None:
        self._safe_mode = safe_mode

    @property
    def legacy_templates(self) -> bool:
        return self._legacy_templates

    @legacy_templates.setter
    def legacy_templates(self, legacy_templates: bool) -> None:
        self._legacy_templates = legacy_templates

    @property
    def config_dir(self) -> str:
        return self._config_dir

    @config_dir.setter
    def config_dir(self, config_dir: str) -> None:
        if config_dir != "":
            self._config_dir = config_dir

    def distance(self, lat: float, lon: float) -> float:
        """Calculate distance from Home Assistant.

        Async friendly.
        """
        return self._units.length(
            LocationInfo.distance(self._latitude, self._longitude, lat, lon),
            Const.LENGTH_METERS,
        )

    def path(self, *path: str) -> str:
        """Generate path to the file within the configuration directory.

        Async friendly.
        """
        if self._config_dir is None:
            raise SmartHomeControllerError("config_dir is not set")
        return os.path.join(self._config_dir, *path)

    def is_allowed_external_url(self, url_to_check: str) -> bool:
        """Check if an external URL is allowed."""
        parsed_url = f"{str(yarl.URL(url_to_check))}/"

        return any(
            allowed
            for allowed in self._allowlist_external_urls
            if parsed_url.startswith(allowed)
        )

    def is_allowed_path(self, path: str) -> bool:
        """Check if the path is valid for access from outside."""
        assert path is not None

        thepath = pathlib.Path(path)
        try:
            # The file path does not have to exist (it's parent should)
            if thepath.exists():
                thepath = thepath.resolve()
            else:
                thepath = thepath.parent.resolve()
        except (FileNotFoundError, RuntimeError, PermissionError):
            return False

        for allowed_path in self._allowlist_external_dirs:
            try:
                thepath.relative_to(allowed_path)
                return True
            except ValueError:
                pass

        return False

    def as_dict(self) -> dict[str, typing.Any]:
        """Create a dictionary representation of the configuration.

        Async friendly.
        """
        return {
            Const.CONF_LATITUDE: self._latitude,
            Const.CONF_LONGITUDE: self._longitude,
            Const.CONF_ELEVATION: self._elevation,
            Const.CONF_UNIT_SYSTEM: self._units.as_dict(),
            Const.CONF_LOCATION_NAME: self._location_name,
            Const.CONF_TIME_ZONE: self._time_zone,
            Const.CONF_COMPONENTS: self._components,
            Const.CONF_CONFIG_DIR: self._config_dir,
            # legacy, backwards compat
            Const.LEGACY_CONF_WHITELIST_EXTERNAL_DIRS: self._allowlist_external_dirs,
            Const.CONF_ALLOWLIST_EXTERNAL_DIRS: self._allowlist_external_dirs,
            Const.CONF_ALLOWLIST_EXTERNAL_URLS: self._allowlist_external_urls,
            Const.CONF_VERSION: Const.__version__,
            Const.CONF_CONFIG_SOURCE: self._config_source,
            Const.CONF_SAFE_MODE: self._safe_mode,
            Const.CONF_STATE: self._shc.state.value,
            Const.CONF_EXTERNAL_URL: self._external_url,
            Const.CONF_INTERNAL_URL: self._internal_url,
            Const.CONF_CURRENCY: self._currency,
        }

    def set_time_zone(self, time_zone_str: str) -> None:
        """Help to set the time zone."""
        if time_zone := helpers.get_time_zone(time_zone_str):
            self._time_zone = time_zone_str
            helpers.set_default_time_zone(time_zone)
        else:
            raise ValueError(f"Received invalid time zone {time_zone_str}")

    @callback
    def _update(
        self,
        *,
        source: ConfigSource,
        latitude: float = None,
        longitude: float = None,
        elevation: int = None,
        unit_system: str = None,
        location_name: str = None,
        time_zone: str = None,
        external_url: str | dict[typing.Any, typing.Any] = None,
        internal_url: str | dict[typing.Any, typing.Any] = None,
        currency: str = None,
    ) -> None:
        """Update the configuration from a dictionary."""
        self._config_source = source
        if latitude is not None:
            self._latitude = latitude
        if longitude is not None:
            self._longitude = longitude
        if elevation is not None:
            self._elevation = elevation
        if unit_system is not None:
            if unit_system == Const.CONF_UNIT_SYSTEM_IMPERIAL:
                self._units = UnitSystem.IMPERIAL()
            else:
                self._units = UnitSystem.METRIC()
        if location_name is not None:
            self._location_name = location_name
        if time_zone is not None:
            self.set_time_zone(time_zone)
        if external_url is not None:
            self._external_url = typing.cast(typing.Optional[str], external_url)
        if internal_url is not None:
            self._internal_url = typing.cast(typing.Optional[str], internal_url)
        if currency is not None:
            self._currency = currency

    async def async_update(self, **kwargs: typing.Any) -> None:
        """Update the configuration from a dictionary."""
        self._update(source=ConfigSource.STORAGE, **kwargs)
        await self.async_store()
        self._shc.bus.async_fire(Const.EVENT_CORE_CONFIG_UPDATE, kwargs)

    async def async_load(self) -> None:
        """Load [TheNextGeneration] core config."""
        store = Store[dict[str, typing.Any]](
            self._shc,
            _CORE_STORAGE_VERSION,
            _CORE_STORAGE_KEY,
            private=True,
            atomic_writes=True,
        )

        if not (data := await store.async_load()):
            return

        # In 2021.9 we fixed validation to disallow a path (because that's never correct)
        # but this data still lives in storage, so we print a warning.
        if data.get("external_url") and url.parse_url(
            data["external_url"]
        ).path not in (
            "",
            "/",
        ):
            _LOGGER.warning("Invalid external_url set. It's not allowed to have a path")

        if data.get("internal_url") and url.parse_url(
            data["internal_url"]
        ).path not in (
            "",
            "/",
        ):
            _LOGGER.warning("Invalid internal_url set. It's not allowed to have a path")

        self._update(
            source=ConfigSource.STORAGE,
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            elevation=data.get("elevation"),
            unit_system=data.get("unit_system"),
            location_name=data.get("location_name"),
            time_zone=data.get("time_zone"),
            external_url=data.get("external_url", None),
            internal_url=data.get("internal_url", None),
            currency=data.get("currency"),
        )

    async def async_store(self) -> None:
        """Store [TheNextGeneration] core config."""
        data = {
            "latitude": self._latitude,
            "longitude": self._longitude,
            "elevation": self._elevation,
            "unit_system": self._units.name,
            "location_name": self._location_name,
            "time_zone": self._time_zone,
            "external_url": self._external_url,
            "internal_url": self._internal_url,
            "currency": self._currency,
        }

        store = Store[dict[str, typing.Any]](
            self._shc,
            _CORE_STORAGE_VERSION,
            _CORE_STORAGE_KEY,
            private=True,
            atomic_writes=True,
        )
        await store.async_save(data)
