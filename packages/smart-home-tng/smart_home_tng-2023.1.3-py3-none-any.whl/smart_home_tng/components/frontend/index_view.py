"""
Frontend Component for Smart Home - The Next Generation.

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
import functools
import pathlib
import typing

import jinja2
import yarl
from aiohttp import hdrs, web, web_urldispatcher

from ... import core
from .const import Const
from .panel import Panel


# pylint: disable=unused-variable
class IndexView(web_urldispatcher.AbstractResource):
    """Serve the frontend."""

    def __init__(self, repo_path: str, owner: core.FrontendComponent) -> None:
        """Initialize the frontend view."""
        super().__init__(name="frontend:index")
        self._repo_path = repo_path
        self._owner = owner
        self._template_cache: jinja2.Template = None

    @property
    def repo_path(self) -> str:
        return self._repo_path

    @property
    def canonical(self) -> str:
        """Return resource's canonical path."""
        return "/"

    @property
    def _route(self) -> web_urldispatcher.ResourceRoute:
        """Return the index route."""
        return web_urldispatcher.ResourceRoute("GET", self.get, self)

    def url_for(self, **kwargs: str) -> yarl.URL:
        """Construct url for resource with additional params."""
        return yarl.URL("/")

    async def resolve(
        self, request: web.Request
    ) -> tuple[web_urldispatcher.UrlMappingMatchInfo, set[str]]:
        """Resolve resource.

        Return (UrlMappingMatchInfo, allowed_methods) pair.
        """
        if (
            request.path != "/"
            and len(request.url.parts) > 1
            and Panel.get_panel(request.url.parts[1]) is None
        ):
            return None, set()

        if request.method != hdrs.METH_GET:
            return None, {"GET"}

        return web_urldispatcher.UrlMappingMatchInfo({}, self._route), {"GET"}

    def add_prefix(self, prefix: str) -> None:
        """Add a prefix to processed URLs.

        Required for subapplications support.
        """

    def get_info(self) -> dict[str, list[str]]:
        """Return a dict with additional info useful for introspection."""
        return {"panels": Panel.get_info()}

    def freeze(self) -> None:
        """Freeze the resource."""

    def raw_match(self, _path: str) -> bool:
        """Perform a raw match against path."""

    def get_template(self) -> jinja2.Template:
        """Get template."""
        if (tpl := self._template_cache) is None:
            with (_frontend_root(self.repo_path) / "index.html").open(
                encoding="utf8"
            ) as file:
                tpl = jinja2.Template(file.read())

            # Cache template if not running from repository
            if self.repo_path is None:
                self._template_cache = tpl

        return tpl

    async def get(self, request: web.Request) -> web.Response:
        """Serve the index page for panel pages."""
        shc: core.SmartHomeController = request.app[core.Const.KEY_SHC]

        comp = shc.components.onboarding
        if (
            not isinstance(comp, core.OnboardingComponent)
            or not comp.async_is_onboarded()
        ):
            return web.Response(status=302, headers={"location": "/onboarding.html"})

        template = self._template_cache or await shc.async_add_executor_job(
            self.get_template
        )

        return web.Response(
            text=_async_render_index_cached(
                template,
                theme_color=Const.MANIFEST_JSON["theme_color"],
                extra_modules=self._owner.extra_modules.urls,
                extra_js_es5=self._owner.extra_js_es5.urls,
            ),
            content_type="text/html",
        )

    def __len__(self) -> int:
        """Return length of resource."""
        return 1

    def __iter__(self) -> collections.abc.Iterator[web_urldispatcher.ResourceRoute]:
        """Iterate over routes."""
        return iter([self._route])


def _frontend_root(dev_repo_path: str) -> pathlib.Path:
    """Return root path to the frontend files."""
    if dev_repo_path is not None:
        return pathlib.Path(dev_repo_path) / "hass_frontend"
    # Keep import here so that we can import frontend without installing reqs
    # pylint: disable=import-outside-toplevel
    from ... import frontend

    return frontend.where()


@core.callback
@functools.lru_cache(maxsize=1)
def _async_render_index_cached(template: jinja2.Template, **kwargs: typing.Any) -> str:
    return template.render(**kwargs)
