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
import logging
import collections
import typing

from . import helpers
from .callback import callback
from .const import Const
from .integration import Integration


_LOGGER: typing.Final = logging.getLogger(__name__)
_LOCALE_EN: typing.Final = "en"


if not typing.TYPE_CHECKING:

    class SmartHomeController:
        ...


if typing.TYPE_CHECKING:
    from .smart_home_controller import SmartHomeController


# pylint: disable=unused-variable
class Translations:
    """Translation string lookup helpers."""

    def __init__(self, shc: SmartHomeController) -> None:
        self._shc = shc
        self._cache = None
        self._load_lock = asyncio.Lock()

    async def async_get_translations(
        self,
        language: str,
        category: str,
        integrations: typing.Iterable[str] = None,
        config_flow: bool = False,
    ) -> dict[str, typing.Any]:
        """Return all backend translations.

        If integration specified, load it for that one.
        Otherwise default to loaded intgrations combined with config flow
        integrations if config_flow is true.
        """
        lock = self._load_lock

        if integrations is not None:
            components = set(integrations)
        elif config_flow:
            components = (
                await self._shc.setup.async_get_config_flows()
            ) - self._shc.config.components
        elif category == "state":
            components = set(self._shc.config.components)
        else:
            # Only 'state' supports merging, so remove platforms from selection
            components = {
                component
                for component in self._shc.config.components
                if "." not in component
            }

        async with lock:
            if self._cache is None:
                self._cache = _TranslationCache(self._shc)
            cached = await self._cache.async_fetch(language, category, components)

        return dict(collections.ChainMap(*cached))


class _TranslationCache:
    """Cache for flattened translations."""

    def __init__(self, shc: SmartHomeController) -> None:
        """Initialize the cache."""
        self._shc = shc
        self._loaded: dict[str, set[str]] = {}
        self._cache: dict[str, dict[str, dict[str, typing.Any]]] = {}

    async def async_fetch(
        self,
        language: str,
        category: str,
        components: set[str],
    ) -> list[dict[str, dict[str, typing.Any]]]:
        """Load resources into the cache."""
        components_to_load = components - self._loaded.setdefault(language, set())

        if components_to_load:
            await self._async_load(language, components_to_load)

        cached = self._cache.get(language, {})

        return [cached.get(component, {}).get(category, {}) for component in components]

    async def _async_load(self, language: str, components: set[str]) -> None:
        """Populate the cache for a given set of components."""
        _LOGGER.debug(
            f"Cache miss for {language}: {', '.join(components)}",
        )
        # Fetch the English resources, as a fallback for missing keys
        languages = [_LOCALE_EN] if language == _LOCALE_EN else [_LOCALE_EN, language]
        for translation_strings in await asyncio.gather(
            *(self._async_get_component_strings(lang, components) for lang in languages)
        ):
            self._build_category_cache(language, components, translation_strings)

        self._loaded[language].update(components)

    @callback
    def _build_category_cache(
        self,
        language: str,
        components: set[str],
        translation_strings: dict[str, dict[str, typing.Any]],
    ) -> None:
        """Extract resources into the cache."""
        resource: dict[str, typing.Any] | str
        cached = self._cache.setdefault(language, {})
        categories: set[str] = set()
        for resource in translation_strings.values():
            categories.update(resource)

        for category in categories:
            resource_func = (
                _merge_resources if category == "state" else _build_resources
            )
            new_resources: typing.Mapping[str, dict[str, typing.Any] | str]
            new_resources = resource_func(translation_strings, components, category)

            for component, resource in new_resources.items():
                category_cache: dict[str, typing.Any] = cached.setdefault(
                    component, {}
                ).setdefault(category, {})

                if isinstance(resource, dict):
                    category_cache.update(
                        _recursive_flatten(
                            f"component.{component}.{category}.",
                            resource,
                        )
                    )
                else:
                    category_cache[f"component.{component}.{category}"] = resource

    async def _async_get_component_strings(
        self, language: str, components: set[str]
    ) -> dict[str, typing.Any]:
        """Load translations."""
        domains = list({loaded.split(".")[-1] for loaded in components})
        integrations = dict(
            zip(
                domains,
                await helpers.gather_with_concurrency(
                    Const.MAX_LOAD_CONCURRENTLY,
                    *(
                        self._shc.setup.async_get_integration(domain)
                        for domain in domains
                    ),
                ),
            )
        )

        translations: dict[str, typing.Any] = {}

        # Determine paths of missing components/platforms
        files_to_load = {}
        for loaded in components:
            parts = loaded.split(".")
            domain = parts[-1]
            integration = integrations[domain]

            path = self._component_translation_path(loaded, language, integration)
            # No translation available
            if path is None:
                translations[loaded] = {}
            else:
                files_to_load[loaded] = path

        if not files_to_load:
            return translations

        # Load files
        load_translations_job = self._shc.async_add_executor_job(
            self._load_translations_files, files_to_load
        )
        assert load_translations_job is not None
        loaded_translations = await load_translations_job

        # Translations that miss "title" will get integration put in.
        for loaded, loaded_translation in loaded_translations.items():
            if "." in loaded:
                continue

            if "title" not in loaded_translation:
                loaded_translation["title"] = integrations[loaded].name

        translations.update(loaded_translations)

        return translations

    @callback
    def _component_translation_path(
        self, component: str, language: str, integration: Integration
    ) -> str:
        """Return the translation json file location for a component.

        For component:
        - components/hue/translations/nl.json

        For platform:
        - components/hue/translations/light.nl.json

        If component is just a single file, will return None.
        """
        parts = component.split(".")
        domain = parts[-1]
        is_platform = len(parts) == 2

        # If it's a component that is just one file, we don't support translations
        # Example custom_components/my_component.py
        if integration.file_path.name != domain:
            return None

        if is_platform:
            filename = f"{parts[0]}.{language}.json"
        else:
            filename = f"{language}.json"

        translation_path = integration.file_path / "translations"

        return str(translation_path / filename)

    def _load_translations_files(
        self, translation_files: dict[str, str]
    ) -> dict[str, dict[str, typing.Any]]:
        """Load and parse translation.json files."""
        loaded = {}
        for component, translation_file in translation_files.items():
            loaded_json = helpers.load_json(translation_file)

            if not isinstance(loaded_json, dict):
                _LOGGER.warning(
                    f"Translation file is unexpected type {type(loaded_json)}. "
                    + f"Expected dict for {translation_file}",
                )
                continue

            loaded[component] = loaded_json

        return loaded


def _merge_resources(
    translation_strings: dict[str, dict[str, typing.Any]],
    components: set[str],
    category: str,
) -> dict[str, dict[str, typing.Any]]:
    """Build and merge the resources response for the given components and platforms."""
    # Build response
    resources: dict[str, dict[str, typing.Any]] = {}
    for component in components:
        if "." not in component:
            domain = component
        else:
            domain = component.split(".", 1)[0]

        domain_resources = resources.setdefault(domain, {})

        # Integrations are able to provide translations for their entities under other
        # integrations if they don't have an existing device class. This is done by
        # using a custom device class prefixed with their domain and two underscores.
        # These files are in platform specific files in the integration folder with
        # names like `strings.sensor.json`.
        # We are going to merge the translations for the custom device classes into
        # the translations of sensor.

        new_value = translation_strings[component].get(category)

        if new_value is None:
            continue

        if isinstance(new_value, dict):
            domain_resources.update(new_value)
        else:
            _LOGGER.error(
                f"An integration providing translations for {domain} provided "
                + f"invalid data: {new_value}",
            )

    return resources


def _build_resources(
    translation_strings: dict[str, dict[str, typing.Any]],
    components: set[str],
    category: str,
) -> dict[str, dict[str, typing.Any] | str]:
    """Build the resources response for the given components."""
    # Build response
    return {
        component: translation_strings[component][category]
        for component in components
        if category in translation_strings[component]
        and translation_strings[component][category] is not None
    }


def _recursive_flatten(
    prefix: typing.Any, data: dict[str, typing.Any]
) -> dict[str, typing.Any]:
    """Return a flattened representation of dict data."""
    output = {}
    for key, value in data.items():
        if isinstance(value, dict):
            output.update(_recursive_flatten(f"{prefix}{key}.", value))
        else:
            output[f"{prefix}{key}"] = value
    return output
