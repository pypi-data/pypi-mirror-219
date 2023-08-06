"""
Blueprint Integration for Smart Home - The Next Generation.

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

import html
import re
import typing
import voluptuous as vol
import yarl

from ... import core
from .const import Const
from .blueprint import Blueprint
from .imported_blueprint import ImportedBlueprint
from .unsupported_url import UnsupportedUrl

_cv: typing.TypeAlias = core.ConfigValidation

# pylint: disable=unused-variable

_COMMUNITY_TOPIC_PATTERN: typing.Final = re.compile(
    r"^https://community.home-assistant.io/t/[a-z0-9-]+/(?P<topic>\d+)(?:/(?P<post>\d+)|)$"
)

_COMMUNITY_CODE_BLOCK: typing.Final = re.compile(
    r'<code class="lang-(?P<syntax>[a-z]+)">(?P<content>(?:.|\n)*)</code>', re.MULTILINE
)

_GITHUB_FILE_PATTERN: typing.Final = re.compile(
    r"^https://github.com/(?P<repository>.+)/blob/(?P<path>.+)$"
)

_COMMUNITY_TOPIC_SCHEMA: typing.Final = vol.Schema(
    {
        "slug": str,
        "title": str,
        "post_stream": {"posts": [{"updated_at": _cv.datetime, "cooked": str}]},
    },
    extra=vol.ALLOW_EXTRA,
)


@core.callback
def is_blueprint_config(config: typing.Any) -> bool:
    """Return if it is a blueprint config."""
    return isinstance(config, dict) and Const.CONF_BLUEPRINT in config


@core.callback
def is_blueprint_instance_config(config: typing.Any) -> bool:
    """Return if it is a blueprint instance config."""
    return isinstance(config, dict) and Const.CONF_USE_BLUEPRINT in config


def _get_github_import_url(url: str) -> str:
    """Convert a GitHub url to the raw content.

    Async friendly.
    """
    if url.startswith("https://raw.githubusercontent.com/"):
        return url

    if (match := _GITHUB_FILE_PATTERN.match(url)) is None:
        raise UnsupportedUrl("Not a GitHub file url")

    repo, path = match.groups()

    return f"https://raw.githubusercontent.com/{repo}/{path}"


def _get_community_post_import_url(url: str) -> str:
    """Convert a forum post url to an import url.

    Async friendly.
    """
    if (match := _COMMUNITY_TOPIC_PATTERN.match(url)) is None:
        raise UnsupportedUrl("Not a topic url")

    _topic, post = match.groups()

    json_url = url

    if post is not None:
        # Chop off post part, ie /2
        json_url = json_url[: -len(post) - 1]

    json_url += ".json"

    return json_url


def _extract_blueprint_from_community_topic(
    _url: str,
    topic: dict,
) -> ImportedBlueprint:
    """Extract a blueprint from a community post JSON.

    Async friendly.
    """
    block_content = None
    blueprint = None
    post = topic["post_stream"]["posts"][0]

    for match in _COMMUNITY_CODE_BLOCK.finditer(post["cooked"]):
        block_syntax, block_content = match.groups()

        if block_syntax not in ("auto", "yaml"):
            continue

        block_content = html.unescape(block_content.strip())

        try:
            data = core.YamlLoader.parse_yaml(block_content)
        except core.SmartHomeControllerError:
            if block_syntax == "yaml":
                raise

            continue

        if not is_blueprint_config(data):
            continue

        blueprint = Blueprint(data)
        break

    if blueprint is None:
        raise core.SmartHomeControllerError(
            "No valid blueprint found in the topic. Blueprint syntax blocks "
            + "need to be marked as YAML or no syntax."
        )

    return ImportedBlueprint(
        f'{post["username"]}/{topic["slug"]}', block_content, blueprint
    )


async def fetch_blueprint_from_community_post(
    shc: core.SmartHomeController, url: str
) -> ImportedBlueprint:
    """Get blueprints from a community post url.

    Method can raise aiohttp client exceptions, vol.Invalid.

    Caller needs to implement own timeout.
    """
    import_url = _get_community_post_import_url(url)
    session = core.HttpClient.async_get_clientsession(shc)

    resp = await session.get(import_url, raise_for_status=True)
    json_resp = await resp.json()
    json_resp = _COMMUNITY_TOPIC_SCHEMA(json_resp)
    return _extract_blueprint_from_community_topic(url, json_resp)


async def fetch_blueprint_from_github_url(
    shc: core.SmartHomeController, url: str
) -> ImportedBlueprint:
    """Get a blueprint from a github url."""
    import_url = _get_github_import_url(url)
    session = core.HttpClient.async_get_clientsession(shc)

    resp = await session.get(import_url, raise_for_status=True)
    raw_yaml = await resp.text()
    data = core.YamlLoader.parse_yaml(raw_yaml)
    blueprint = Blueprint(data)

    parsed_import_url = yarl.URL(import_url)
    suggested_filename = f"{parsed_import_url.parts[1]}/{parsed_import_url.parts[-1]}"
    if suggested_filename.endswith(".yaml"):
        suggested_filename = suggested_filename[:-5]

    return ImportedBlueprint(suggested_filename, raw_yaml, blueprint)


async def fetch_blueprint_from_github_gist_url(
    shc: core.SmartHomeController, url: str
) -> ImportedBlueprint:
    """Get a blueprint from a Github Gist."""
    if not url.startswith("https://gist.github.com/"):
        raise UnsupportedUrl("Not a GitHub gist url")

    parsed_url = yarl.URL(url)
    session = core.HttpClient.async_get_clientsession(shc)

    resp = await session.get(
        f"https://api.github.com/gists/{parsed_url.parts[2]}",
        headers={"Accept": "application/vnd.github.v3+json"},
        raise_for_status=True,
    )
    gist = await resp.json()

    blueprint = None
    filename = None
    content = None

    for filename, info in gist["files"].items():
        if not filename.endswith(".yaml"):
            continue

        content = info["content"]
        data = core.YamlLoader.parse_yaml(content)

        if not is_blueprint_config(data):
            continue

        blueprint = Blueprint(data)
        break

    if blueprint is None:
        raise core.SmartHomeControllerError(
            "No valid blueprint found in the gist. The blueprint file needs to end with '.yaml'"
        )

    return ImportedBlueprint(
        f"{gist['owner']['login']}/{filename[:-5]}", content, blueprint
    )


async def fetch_blueprint_from_url(
    shc: core.SmartHomeController, url: str
) -> ImportedBlueprint:
    """Get a blueprint from a url."""
    for func in (
        fetch_blueprint_from_community_post,
        fetch_blueprint_from_github_url,
        fetch_blueprint_from_github_gist_url,
    ):
        try:
            imported_bp = await func(shc, url)
            imported_bp.blueprint.update_metadata(source_url=url)
            return imported_bp
        except UnsupportedUrl:
            pass

    raise core.SmartHomeControllerError("Unsupported url")
