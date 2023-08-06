"""
Logger Component for Smart Home - The Next Generation.

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

from ... import core
from .smart_home_controller_logger import SmartHomeControllerLogger

_cv: typing.TypeAlias = core.ConfigValidation


_SERVICE_SET_DEFAULT_LEVEL: typing.Final = "set_default_level"
_SERVICE_SET_LEVEL: typing.Final = "set_level"

_DEFAULT_LOGSEVERITY: typing.Final = "DEBUG"

_LOGGER_DEFAULT: typing.Final = "default"
_LOGGER_LOGS: typing.Final = "logs"
_LOGGER_FILTERS: typing.Final = "filters"

_ATTR_LEVEL: typing.Final = "level"

_VALID_LOG_LEVEL: typing.Final = vol.All(vol.Upper, vol.In(core.Const.LOGSEVERITY))

_SERVICE_SET_DEFAULT_LEVEL_SCHEMA: typing.Final = vol.Schema(
    {_ATTR_LEVEL: _VALID_LOG_LEVEL}
)
_SERVICE_SET_LEVEL_SCHEMA = vol.Schema({_cv.string: _VALID_LOG_LEVEL})


# pylint: disable=unused-variable
class LoggerComponent(core.SmartHomeControllerComponent):
    """Support for setting the level of logging for components."""

    def __init__(self, path: typing.Iterable[str]):
        super().__init__(path)
        self._overrides = dict[str, SmartHomeControllerLogger]()
        # pylint: disable=protected-access
        SmartHomeControllerLogger._overrides = self._overrides

    async def async_validate_config(self, config: core.ConfigType) -> core.ConfigType:
        """Validate configuration."""
        schema = vol.Schema(
            {
                self.domain: vol.Schema(
                    {
                        vol.Optional(_LOGGER_DEFAULT): _VALID_LOG_LEVEL,
                        vol.Optional(_LOGGER_LOGS): vol.Schema(
                            {_cv.string: _VALID_LOG_LEVEL}
                        ),
                        vol.Optional(_LOGGER_FILTERS): vol.Schema(
                            {_cv.string: [_cv.is_regex]}
                        ),
                    }
                )
            },
            extra=vol.ALLOW_EXTRA,
        )
        return schema(config)

    async def async_setup(self, config: core.ConfigType) -> bool:
        """Set up the logger component."""
        if not await super().async_setup(config):
            return False

        logging.setLoggerClass(SmartHomeControllerLogger)

        # Set default log severity
        conf = config[self.domain]
        self._set_default_log_level(conf.get(_LOGGER_DEFAULT, _DEFAULT_LOGSEVERITY))

        if _LOGGER_LOGS in conf:
            self._set_log_levels(conf[_LOGGER_LOGS])

        if _LOGGER_FILTERS in conf:
            for key, value in conf[_LOGGER_FILTERS].items():
                logger = logging.getLogger(key)
                _add_log_filter(logger, value)

        self._shc.services.async_register(
            self.domain,
            _SERVICE_SET_DEFAULT_LEVEL,
            self._service_handler,
            schema=_SERVICE_SET_DEFAULT_LEVEL_SCHEMA,
        )

        self._shc.services.async_register(
            self.domain,
            _SERVICE_SET_LEVEL,
            self._service_handler,
            schema=_SERVICE_SET_LEVEL_SCHEMA,
        )

        return True

    @core.callback
    def _service_handler(self, service: core.ServiceCall) -> None:
        """Handle logger services."""
        if service.service == _SERVICE_SET_DEFAULT_LEVEL:
            self._set_default_log_level(service.data.get(_ATTR_LEVEL))
        else:
            self._set_log_levels(service.data)

    @core.callback
    def _set_default_log_level(self, level):
        """Set the default log level for components."""
        _set_log_level(logging.getLogger(""), level)

    @core.callback
    def _set_log_levels(self, logpoints):
        """Set the specified log levels."""
        self._overrides.update(logpoints)
        for key, value in logpoints.items():
            _set_log_level(logging.getLogger(key), value)


def _set_log_level(logger, level):
    """Set the log level.

    Any logger fetched before this integration is loaded will use old class.
    """
    getattr(logger, "orig_setLevel", logger.setLevel)(core.Const.LOGSEVERITY[level])


def _add_log_filter(logger, patterns):
    """Add a Filter to the logger based on a regexp of the filter_str."""

    def filter_func(logrecord):
        return not any(p.search(logrecord.getMessage()) for p in patterns)

    logger.addFilter(filter_func)
