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

_SUPPORTED_SCALING_FACTORS: typing.Final = [
    (7, 8),
    (3, 4),
    (5, 8),
    (1, 2),
    (3, 8),
    (1, 4),
    (1, 8),
]

_JPEG_QUALITY: typing.Final = 75


def _find_supported_scaling_factor(
    current_width: int, current_height: int, target_width: int, target_height: int
) -> tuple[int, int]:
    """Find a supported scaling factor to scale the image.

    If there is no exact match, we use one size up to ensure
    the image remains crisp.
    """
    for idx, supported_sf in enumerate(_SUPPORTED_SCALING_FACTORS):
        ratio = supported_sf[0] / supported_sf[1]
        width_after_scale = current_width * ratio
        height_after_scale = current_height * ratio
        if width_after_scale == target_width and height_after_scale == target_height:
            return supported_sf
        if width_after_scale < target_width or height_after_scale < target_height:
            return None if idx == 0 else _SUPPORTED_SCALING_FACTORS[idx - 1]

    # Giant image, the most we can reduce by is 1/8
    return _SUPPORTED_SCALING_FACTORS[-1]


# pylint: disable=unused-variable
def _scale_jpeg_camera_image(cam_image: core.Image, width: int, height: int) -> bytes:
    """Scale a camera image as close as possible to one of the supported scaling factors."""
    turbo_jpeg = core.TurboJPEGSingleton.instance()
    if not turbo_jpeg:
        return cam_image.content

    try:
        (current_width, current_height, _, _) = turbo_jpeg.decode_header(
            cam_image.content
        )
    except OSError:
        return cam_image.content

    scaling_factor = _find_supported_scaling_factor(
        current_width, current_height, width, height
    )
    if scaling_factor is None:
        return cam_image.content

    return typing.cast(
        bytes,
        turbo_jpeg.scale_with_quality(
            cam_image.content,
            scaling_factor=scaling_factor,
            quality=_JPEG_QUALITY,
        ),
    )
