"""
Camera Component for Smart Home - The Next Generation.

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

from ... import core


# pylint: disable=unused-variable
class CameraMediaSource(core.MediaSource):
    """Provide camera feeds as media sources."""

    _name: str = "Camera"

    def __init__(self, owner: core.Camera.Component) -> None:
        """Initialize CameraMediaSource."""
        super().__init__(owner.domain)
        self._owner = owner

    async def async_resolve_media(self, item: core.MediaSourceItem) -> core.PlayMedia:
        """Resolve media to a url."""
        component = self._owner.entity_component
        camera = typing.cast(
            typing.Optional[core.Camera], component.get_entity(item.identifier)
        )

        if not camera:
            raise core.Unresolvable(f"Could not resolve media item: {item.identifier}")

        if (stream_type := camera.frontend_stream_type) is None:
            return core.PlayMedia(
                f"/api/camera_proxy_stream/{camera.entity_id}", camera.content_type
            )

        if stream_type != core.StreamType.HLS:
            raise core.Unresolvable("Camera does not support MJPEG or HLS streaming.")

        if "stream" not in self._owner.controller.config.components:
            raise core.Unresolvable("Stream integration not loaded")

        try:
            # pylint: disable=protected-access
            url = await self._owner._async_stream_endpoint_url(
                camera, core.StreamComponent.Const.HLS_PROVIDER
            )
        except core.SmartHomeControllerError as err:
            raise core.Unresolvable(str(err)) from err

        return core.PlayMedia(
            url,
            core.StreamComponent.Const.FORMAT_CONTENT_TYPE[
                core.StreamComponent.Const.HLS_PROVIDER
            ],
        )

    async def async_browse_media(
        self,
        item: core.MediaSourceItem,
    ) -> core.BrowseMediaSource:
        """Return media."""
        if item.identifier:
            raise core.MediaPlayer.BrowseError("Unknown item")

        can_stream_hls = "stream" in self._owner.controller.config.components

        # Root. List cameras.
        component = self._owner.entity_component
        children = []
        not_shown = 0
        for camera in component.entities:
            camera = typing.cast(core.Camera, camera)
            stream_type = camera.frontend_stream_type

            if stream_type is None:
                content_type = camera.content_type

            elif can_stream_hls and stream_type == core.StreamType.HLS:
                content_type = core.StreamComponent.Const.FORMAT_CONTENT_TYPE[
                    core.StreamComponent.Const.HLS_PROVIDER
                ]

            else:
                not_shown += 1
                continue

            children.append(
                core.BrowseMediaSource(
                    domain=self._owner.domain,
                    identifier=camera.entity_id,
                    media_class=core.MediaPlayer.MediaClass.VIDEO,
                    media_content_type=content_type,
                    title=camera.name,
                    thumbnail=f"/api/camera_proxy/{camera.entity_id}",
                    can_play=True,
                    can_expand=False,
                )
            )

        return core.BrowseMediaSource(
            domain=self._owner.domain,
            identifier=None,
            media_class=core.MediaPlayer.MediaClass.APP,
            media_content_type="",
            title="Camera",
            can_play=False,
            can_expand=True,
            children_media_class=core.MediaPlayer.MediaClass.VIDEO,
            children=children,
            not_shown=not_shown,
        )
