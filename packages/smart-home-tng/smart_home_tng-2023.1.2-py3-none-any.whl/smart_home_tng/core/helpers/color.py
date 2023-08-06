"""
Helpers for Components of Smart Home - The Next Generation.

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

import colorsys
import math
import typing

import attr


@attr.s()
class _XYPoint:
    """Represents a CIE 1931 XY coordinate pair."""

    x: float = attr.ib()  # pylint: disable=invalid-name
    y: float = attr.ib()  # pylint: disable=invalid-name


# pylint: disable=unused-variable
class Color:
    """Color util methods."""

    # pylint: disable=invalid-name
    class RGB(typing.NamedTuple):
        """RGB hex values."""

        r: int
        g: int
        b: int

    XYPoint: typing.TypeAlias = _XYPoint

    # Official CSS3 colors from w3.org:
    # https://www.w3.org/TR/2010/PR-css3-color-20101028/#html4
    # names do not have spaces in them so that we can compare against
    # requests more easily (by removing spaces from the requests as well).
    # This lets "dark seagreen" and "dark sea green" both match the same
    # color "darkseagreen".
    COLORS: typing.Final = {
        "aliceblue": RGB(240, 248, 255),
        "antiquewhite": RGB(250, 235, 215),
        "aqua": RGB(0, 255, 255),
        "aquamarine": RGB(127, 255, 212),
        "azure": RGB(240, 255, 255),
        "beige": RGB(245, 245, 220),
        "bisque": RGB(255, 228, 196),
        "black": RGB(0, 0, 0),
        "blanchedalmond": RGB(255, 235, 205),
        "blue": RGB(0, 0, 255),
        "blueviolet": RGB(138, 43, 226),
        "brown": RGB(165, 42, 42),
        "burlywood": RGB(222, 184, 135),
        "cadetblue": RGB(95, 158, 160),
        "chartreuse": RGB(127, 255, 0),
        "chocolate": RGB(210, 105, 30),
        "coral": RGB(255, 127, 80),
        "cornflowerblue": RGB(100, 149, 237),
        "cornsilk": RGB(255, 248, 220),
        "crimson": RGB(220, 20, 60),
        "cyan": RGB(0, 255, 255),
        "darkblue": RGB(0, 0, 139),
        "darkcyan": RGB(0, 139, 139),
        "darkgoldenrod": RGB(184, 134, 11),
        "darkgray": RGB(169, 169, 169),
        "darkgreen": RGB(0, 100, 0),
        "darkgrey": RGB(169, 169, 169),
        "darkkhaki": RGB(189, 183, 107),
        "darkmagenta": RGB(139, 0, 139),
        "darkolivegreen": RGB(85, 107, 47),
        "darkorange": RGB(255, 140, 0),
        "darkorchid": RGB(153, 50, 204),
        "darkred": RGB(139, 0, 0),
        "darksalmon": RGB(233, 150, 122),
        "darkseagreen": RGB(143, 188, 143),
        "darkslateblue": RGB(72, 61, 139),
        "darkslategray": RGB(47, 79, 79),
        "darkslategrey": RGB(47, 79, 79),
        "darkturquoise": RGB(0, 206, 209),
        "darkviolet": RGB(148, 0, 211),
        "deeppink": RGB(255, 20, 147),
        "deepskyblue": RGB(0, 191, 255),
        "dimgray": RGB(105, 105, 105),
        "dimgrey": RGB(105, 105, 105),
        "dodgerblue": RGB(30, 144, 255),
        "firebrick": RGB(178, 34, 34),
        "floralwhite": RGB(255, 250, 240),
        "forestgreen": RGB(34, 139, 34),
        "fuchsia": RGB(255, 0, 255),
        "gainsboro": RGB(220, 220, 220),
        "ghostwhite": RGB(248, 248, 255),
        "gold": RGB(255, 215, 0),
        "goldenrod": RGB(218, 165, 32),
        "gray": RGB(128, 128, 128),
        "green": RGB(0, 128, 0),
        "greenyellow": RGB(173, 255, 47),
        "grey": RGB(128, 128, 128),
        "honeydew": RGB(240, 255, 240),
        "hotpink": RGB(255, 105, 180),
        "indianred": RGB(205, 92, 92),
        "indigo": RGB(75, 0, 130),
        "ivory": RGB(255, 255, 240),
        "khaki": RGB(240, 230, 140),
        "lavender": RGB(230, 230, 250),
        "lavenderblush": RGB(255, 240, 245),
        "lawngreen": RGB(124, 252, 0),
        "lemonchiffon": RGB(255, 250, 205),
        "lightblue": RGB(173, 216, 230),
        "lightcoral": RGB(240, 128, 128),
        "lightcyan": RGB(224, 255, 255),
        "lightgoldenrodyellow": RGB(250, 250, 210),
        "lightgray": RGB(211, 211, 211),
        "lightgreen": RGB(144, 238, 144),
        "lightgrey": RGB(211, 211, 211),
        "lightpink": RGB(255, 182, 193),
        "lightsalmon": RGB(255, 160, 122),
        "lightseagreen": RGB(32, 178, 170),
        "lightskyblue": RGB(135, 206, 250),
        "lightslategray": RGB(119, 136, 153),
        "lightslategrey": RGB(119, 136, 153),
        "lightsteelblue": RGB(176, 196, 222),
        "lightyellow": RGB(255, 255, 224),
        "lime": RGB(0, 255, 0),
        "limegreen": RGB(50, 205, 50),
        "linen": RGB(250, 240, 230),
        "magenta": RGB(255, 0, 255),
        "maroon": RGB(128, 0, 0),
        "mediumaquamarine": RGB(102, 205, 170),
        "mediumblue": RGB(0, 0, 205),
        "mediumorchid": RGB(186, 85, 211),
        "mediumpurple": RGB(147, 112, 219),
        "mediumseagreen": RGB(60, 179, 113),
        "mediumslateblue": RGB(123, 104, 238),
        "mediumspringgreen": RGB(0, 250, 154),
        "mediumturquoise": RGB(72, 209, 204),
        "mediumvioletred": RGB(199, 21, 133),
        "midnightblue": RGB(25, 25, 112),
        "mintcream": RGB(245, 255, 250),
        "mistyrose": RGB(255, 228, 225),
        "moccasin": RGB(255, 228, 181),
        "navajowhite": RGB(255, 222, 173),
        "navy": RGB(0, 0, 128),
        "navyblue": RGB(0, 0, 128),
        "oldlace": RGB(253, 245, 230),
        "olive": RGB(128, 128, 0),
        "olivedrab": RGB(107, 142, 35),
        "orange": RGB(255, 165, 0),
        "orangered": RGB(255, 69, 0),
        "orchid": RGB(218, 112, 214),
        "palegoldenrod": RGB(238, 232, 170),
        "palegreen": RGB(152, 251, 152),
        "paleturquoise": RGB(175, 238, 238),
        "palevioletred": RGB(219, 112, 147),
        "papayawhip": RGB(255, 239, 213),
        "peachpuff": RGB(255, 218, 185),
        "peru": RGB(205, 133, 63),
        "pink": RGB(255, 192, 203),
        "plum": RGB(221, 160, 221),
        "powderblue": RGB(176, 224, 230),
        "purple": RGB(128, 0, 128),
        "red": RGB(255, 0, 0),
        "rosybrown": RGB(188, 143, 143),
        "royalblue": RGB(65, 105, 225),
        "saddlebrown": RGB(139, 69, 19),
        "salmon": RGB(250, 128, 114),
        "sandybrown": RGB(244, 164, 96),
        "seagreen": RGB(46, 139, 87),
        "seashell": RGB(255, 245, 238),
        "sienna": RGB(160, 82, 45),
        "silver": RGB(192, 192, 192),
        "skyblue": RGB(135, 206, 235),
        "slateblue": RGB(106, 90, 205),
        "slategray": RGB(112, 128, 144),
        "slategrey": RGB(112, 128, 144),
        "snow": RGB(255, 250, 250),
        "springgreen": RGB(0, 255, 127),
        "steelblue": RGB(70, 130, 180),
        "tan": RGB(210, 180, 140),
        "teal": RGB(0, 128, 128),
        "thistle": RGB(216, 191, 216),
        "tomato": RGB(255, 99, 71),
        "turquoise": RGB(64, 224, 208),
        "violet": RGB(238, 130, 238),
        "wheat": RGB(245, 222, 179),
        "white": RGB(255, 255, 255),
        "whitesmoke": RGB(245, 245, 245),
        "yellow": RGB(255, 255, 0),
        "yellowgreen": RGB(154, 205, 50),
        # And...
        "homeassistant": RGB(3, 169, 244),
    }

    @attr.s()
    class GamutType:
        """Represents the Gamut of a light."""

        # ColorGamut = gamut(xypoint(xR,yR),xypoint(xG,yG),xypoint(xB,yB))
        red: _XYPoint = attr.ib()
        green: _XYPoint = attr.ib()
        blue: _XYPoint = attr.ib()

    @staticmethod
    def name_to_rgb(color_name: str) -> RGB:
        """Convert color name to RGB hex value."""
        # COLORS map has no spaces in it, so make the color_name have no
        # spaces in it as well for matching purposes
        hex_value = Color.COLORS.get(color_name.replace(" ", "").lower())
        if not hex_value:
            raise ValueError("Unknown color")

        return hex_value

    # pylint: disable=invalid-name

    @staticmethod
    def RGB_to_xy(
        iR: int, iG: int, iB: int, Gamut: GamutType = None
    ) -> tuple[float, float]:
        """Convert from RGB color to XY color."""
        return Color.RGB_to_xy_brightness(iR, iG, iB, Gamut)[:2]

    # Taken from:
    # https://github.com/PhilipsHue/PhilipsHueSDK-iOS-OSX/blob/00187a3/ApplicationDesignNotes/RGB%20to%20xy%20Color%20conversion.md
    # License: Code is given as is. Use at your own risk and discretion.
    @staticmethod
    def RGB_to_xy_brightness(
        iR: int, iG: int, iB: int, Gamut: GamutType = None
    ) -> tuple[float, float, int]:
        """Convert from RGB color to XY color."""
        if iR + iG + iB == 0:
            return 0.0, 0.0, 0

        R = iR / 255
        B = iB / 255
        G = iG / 255

        # Gamma correction
        R = pow((R + 0.055) / (1.0 + 0.055), 2.4) if (R > 0.04045) else (R / 12.92)
        G = pow((G + 0.055) / (1.0 + 0.055), 2.4) if (G > 0.04045) else (G / 12.92)
        B = pow((B + 0.055) / (1.0 + 0.055), 2.4) if (B > 0.04045) else (B / 12.92)

        # Wide RGB D65 conversion formula
        X = R * 0.664511 + G * 0.154324 + B * 0.162028
        Y = R * 0.283881 + G * 0.668433 + B * 0.047685
        Z = R * 0.000088 + G * 0.072310 + B * 0.986039

        # Convert XYZ to xy
        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)

        # Brightness
        Y = 1 if Y > 1 else Y
        brightness = round(Y * 255)

        # Check if the given xy value is within the color-reach of the lamp.
        if Gamut:
            in_reach = Color.check_point_in_lamps_reach((x, y), Gamut)
            if not in_reach:
                xy_closest = Color.get_closest_point_to_point((x, y), Gamut)
                x = xy_closest[0]
                y = xy_closest[1]

        return round(x, 3), round(y, 3), brightness

    @staticmethod
    def xy_to_RGB(
        vX: float, vY: float, Gamut: GamutType | None = None
    ) -> tuple[int, int, int]:
        """Convert from XY to a normalized RGB."""
        return Color.xy_brightness_to_RGB(vX, vY, 255, Gamut)

    # Converted to Python from Obj-C, original source from:
    # https://github.com/PhilipsHue/PhilipsHueSDK-iOS-OSX/blob/00187a3/ApplicationDesignNotes/RGB%20to%20xy%20Color%20conversion.md
    @staticmethod
    def xy_brightness_to_RGB(
        vX: float, vY: float, ibrightness: int, Gamut: GamutType | None = None
    ) -> tuple[int, int, int]:
        """Convert from XYZ to RGB."""
        if Gamut and not Color.check_point_in_lamps_reach((vX, vY), Gamut):
            xy_closest = Color.get_closest_point_to_point((vX, vY), Gamut)
            vX = xy_closest[0]
            vY = xy_closest[1]

        brightness = ibrightness / 255.0
        if brightness == 0.0:
            return (0, 0, 0)

        Y = brightness

        if vY == 0.0:
            vY += 0.00000000001

        X = (Y / vY) * vX
        Z = (Y / vY) * (1 - vX - vY)

        # Convert to RGB using Wide RGB D65 conversion.
        r = X * 1.656492 - Y * 0.354851 - Z * 0.255038
        g = -X * 0.707196 + Y * 1.655397 + Z * 0.036152
        b = X * 0.051713 - Y * 0.121364 + Z * 1.011530

        # Apply reverse gamma correction.
        r, g, b = (
            12.92 * x
            if (x <= 0.0031308)
            else ((1.0 + 0.055) * pow(x, (1.0 / 2.4)) - 0.055)
            for x in (r, g, b)
        )

        # Bring all negative components to zero.
        r, g, b = (max(0, x) for x in (r, g, b))

        # If one component is greater than 1, weight components by that value.
        max_component = max(r, g, b)
        if max_component > 1:
            r, g, b = (x / max_component for x in (r, g, b))

        ir, ig, ib = (int(x * 255) for x in (r, g, b))

        return (ir, ig, ib)

    @staticmethod
    def hsb_to_RGB(fH: float, fS: float, fB: float) -> tuple[int, int, int]:
        """Convert a hsb into its rgb representation."""
        if fS == 0.0:
            fV = int(fB * 255)
            return fV, fV, fV

        r = g = b = 0
        h = fH / 60
        f = h - float(math.floor(h))
        p = fB * (1 - fS)
        q = fB * (1 - fS * f)
        t = fB * (1 - (fS * (1 - f)))

        if int(h) == 0:
            r = int(fB * 255)
            g = int(t * 255)
            b = int(p * 255)
        elif int(h) == 1:
            r = int(q * 255)
            g = int(fB * 255)
            b = int(p * 255)
        elif int(h) == 2:
            r = int(p * 255)
            g = int(fB * 255)
            b = int(t * 255)
        elif int(h) == 3:
            r = int(p * 255)
            g = int(q * 255)
            b = int(fB * 255)
        elif int(h) == 4:
            r = int(t * 255)
            g = int(p * 255)
            b = int(fB * 255)
        elif int(h) == 5:
            r = int(fB * 255)
            g = int(p * 255)
            b = int(q * 255)

        return (r, g, b)

    @staticmethod
    def RGB_to_hsv(iR: float, iG: float, iB: float) -> tuple[float, float, float]:
        """Convert an rgb color to its hsv representation.

        Hue is scaled 0-360
        Sat is scaled 0-100
        Val is scaled 0-100
        """
        fHSV = colorsys.rgb_to_hsv(iR / 255.0, iG / 255.0, iB / 255.0)
        return round(fHSV[0] * 360, 3), round(fHSV[1] * 100, 3), round(fHSV[2] * 100, 3)

    @staticmethod
    def RGB_to_hs(iR: float, iG: float, iB: float) -> tuple[float, float]:
        """Convert an rgb color to its hs representation."""
        return Color.RGB_to_hsv(iR, iG, iB)[:2]

    @staticmethod
    def hsv_to_RGB(iH: float, iS: float, iV: float) -> tuple[int, int, int]:
        """Convert an hsv color into its rgb representation.

        Hue is scaled 0-360
        Sat is scaled 0-100
        Val is scaled 0-100
        """
        fRGB = colorsys.hsv_to_rgb(iH / 360, iS / 100, iV / 100)
        return (int(fRGB[0] * 255), int(fRGB[1] * 255), int(fRGB[2] * 255))

    @staticmethod
    def hs_to_RGB(iH: float, iS: float) -> tuple[int, int, int]:
        """Convert an hsv color into its rgb representation."""
        return Color.hsv_to_RGB(iH, iS, 100)

    @staticmethod
    def xy_to_hs(
        vX: float, vY: float, Gamut: GamutType | None = None
    ) -> tuple[float, float]:
        """Convert an xy color to its hs representation."""
        h, s, _ = Color.RGB_to_hsv(*Color.xy_to_RGB(vX, vY, Gamut))
        return h, s

    @staticmethod
    def hs_to_xy(
        iH: float, iS: float, Gamut: GamutType | None = None
    ) -> tuple[float, float]:
        """Convert an hs color to its xy representation."""
        return Color.RGB_to_xy(*Color.hs_to_RGB(iH, iS), Gamut)

    @staticmethod
    def match_max_scale(
        input_colors: tuple[int, ...], output_colors: tuple[float, ...]
    ) -> tuple[int, ...]:
        """Match the maximum value of the output to the input."""
        max_in = max(input_colors)
        max_out = max(output_colors)
        if max_out == 0:
            factor = 0.0
        else:
            factor = max_in / max_out
        return tuple(int(round(i * factor)) for i in output_colors)

    @staticmethod
    def rgb_to_rgbw(r: int, g: int, b: int) -> tuple[int, int, int, int]:
        """Convert an rgb color to an rgbw representation."""
        # Calculate the white channel as the minimum of input rgb channels.
        # Subtract the white portion from the remaining rgb channels.
        w = min(r, g, b)
        rgbw = (r - w, g - w, b - w, w)

        # Match the output maximum value to the input. This ensures the full
        # channel range is used.
        return Color.match_max_scale((r, g, b), rgbw)  # type: ignore[return-value]

    @staticmethod
    def rgbw_to_rgb(r: int, g: int, b: int, w: int) -> tuple[int, int, int]:
        """Convert an rgbw color to an rgb representation."""
        # Add the white channel to the rgb channels.
        rgb = (r + w, g + w, b + w)

        # Match the output maximum value to the input. This ensures the
        # output doesn't overflow.
        return Color.match_max_scale((r, g, b, w), rgb)  # type: ignore[return-value]

    @staticmethod
    def rgb_to_rgbww(
        r: int, g: int, b: int, min_mireds: int, max_mireds: int
    ) -> tuple[int, int, int, int, int]:
        """Convert an rgb color to an rgbww representation."""
        # Find the color temperature when both white channels have equal brightness
        mired_range = max_mireds - min_mireds
        mired_midpoint = min_mireds + mired_range / 2
        temp_kelvin = Color.temperature_mired_to_kelvin(mired_midpoint)
        w_r, w_g, w_b = Color.temperature_to_rgb(temp_kelvin)

        # Find the ratio of the midpoint white in the input rgb channels
        white_level = min(
            r / w_r if w_r else 0, g / w_g if w_g else 0, b / w_b if w_b else 0
        )

        # Subtract the white portion from the rgb channels.
        rgb = (r - w_r * white_level, g - w_g * white_level, b - w_b * white_level)
        rgbww = (*rgb, round(white_level * 255), round(white_level * 255))

        # Match the output maximum value to the input. This ensures the full
        # channel range is used.
        return Color.match_max_scale((r, g, b), rgbww)  # type: ignore[return-value]

    @staticmethod
    def rgbww_to_rgb(
        r: int, g: int, b: int, cw: int, ww: int, min_mireds: int, max_mireds: int
    ) -> tuple[int, int, int]:
        """Convert an rgbww color to an rgb representation."""
        # Calculate color temperature of the white channels
        mired_range = max_mireds - min_mireds
        try:
            ct_ratio = ww / (cw + ww)
        except ZeroDivisionError:
            ct_ratio = 0.5
        temp_mired = min_mireds + ct_ratio * mired_range
        if temp_mired:
            temp_kelvin = Color.temperature_mired_to_kelvin(temp_mired)
        else:
            temp_kelvin = 0
        w_r, w_g, w_b = Color.temperature_to_rgb(temp_kelvin)
        white_level = max(cw, ww) / 255

        # Add the white channels to the rgb channels.
        rgb = (r + w_r * white_level, g + w_g * white_level, b + w_b * white_level)

        # Match the output maximum value to the input. This ensures the
        # output doesn't overflow.
        return Color.match_max_scale((r, g, b, cw, ww), rgb)  # type: ignore[return-value]

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Return a RGB color from a hex color string."""
        return f"{round(r):02x}{round(g):02x}{round(b):02x}"

    @staticmethod
    def rgb_hex_to_rgb_list(hex_string: str) -> list[int]:
        """Return an RGB color value list from a hex color string."""
        return [
            int(hex_string[i : i + len(hex_string) // 3], 16)
            for i in range(0, len(hex_string), len(hex_string) // 3)
        ]

    @staticmethod
    def temperature_to_hs(color_temperature_kelvin: float) -> tuple[float, float]:
        """Return an hs color from a color temperature in Kelvin."""
        return Color.RGB_to_hs(*Color.temperature_to_rgb(color_temperature_kelvin))

    @staticmethod
    def temperature_to_rgb(
        color_temperature_kelvin: float,
    ) -> tuple[float, float, float]:
        """
        Return an RGB color from a color temperature in Kelvin.

        This is a rough approximation based on the formula provided by T. Helland
        http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
        """
        # range check
        if color_temperature_kelvin < 1000:
            color_temperature_kelvin = 1000
        elif color_temperature_kelvin > 40000:
            color_temperature_kelvin = 40000

        tmp_internal = color_temperature_kelvin / 100.0

        red = Color._get_red(tmp_internal)

        green = Color._get_green(tmp_internal)

        blue = Color._get_blue(tmp_internal)

        return red, green, blue

    @staticmethod
    def temperature_to_rgbww(
        temperature: int, brightness: int, min_mireds: int, max_mireds: int
    ) -> tuple[int, int, int, int, int]:
        """Convert color temperature in mireds to rgbcw."""
        mired_range = max_mireds - min_mireds
        cold = ((max_mireds - temperature) / mired_range) * brightness
        warm = brightness - cold
        return (0, 0, 0, round(cold), round(warm))

    @staticmethod
    def rgbww_to_temperature(
        rgbww: tuple[int, int, int, int, int], min_mireds: int, max_mireds: int
    ) -> tuple[int, int]:
        """Convert rgbcw to color temperature in mireds."""
        _, _, _, cold, warm = rgbww
        return Color.white_levels_to_temperature(cold, warm, min_mireds, max_mireds)

    @staticmethod
    def white_levels_to_temperature(
        cold: int, warm: int, min_mireds: int, max_mireds: int
    ) -> tuple[int, int]:
        """Convert whites to color temperature in mireds."""
        brightness = warm / 255 + cold / 255
        if brightness == 0:
            return (max_mireds, 0)
        return round(
            ((cold / 255 / brightness) * (min_mireds - max_mireds)) + max_mireds
        ), min(255, round(brightness * 255))

    @staticmethod
    def _clamp(
        color_component: float, minimum: float = 0, maximum: float = 255
    ) -> float:
        """
        Clamp the given color component value between the given min and max values.

        The range defined by the minimum and maximum values is inclusive, i.e. given a
        color_component of 0 and a minimum of 10, the returned value is 10.
        """
        color_component_out = max(color_component, minimum)
        return min(color_component_out, maximum)

    @staticmethod
    def _get_red(temperature: float) -> float:
        """Get the red component of the temperature in RGB space."""
        if temperature <= 66:
            return 255
        tmp_red = 329.698727446 * math.pow(temperature - 60, -0.1332047592)
        return Color._clamp(tmp_red)

    @staticmethod
    def _get_green(temperature: float) -> float:
        """Get the green component of the given color temp in RGB space."""
        if temperature <= 66:
            green = 99.4708025861 * math.log(temperature) - 161.1195681661
        else:
            green = 288.1221695283 * math.pow(temperature - 60, -0.0755148492)
        return Color._clamp(green)

    @staticmethod
    def _get_blue(temperature: float) -> float:
        """Get the blue component of the given color temperature in RGB space."""
        if temperature >= 66:
            return 255
        if temperature <= 19:
            return 0
        blue = 138.5177312231 * math.log(temperature - 10) - 305.0447927307
        return Color._clamp(blue)

    @staticmethod
    def temperature_mired_to_kelvin(mired_temperature: float) -> int:
        """Convert absolute mired shift to degrees kelvin."""
        return math.floor(1000000 / mired_temperature)

    @staticmethod
    def temperature_kelvin_to_mired(kelvin_temperature: float) -> int:
        """Convert degrees kelvin to mired shift."""
        return math.floor(1000000 / kelvin_temperature)

    # The following 5 functions are adapted from rgbxy provided by Benjamin Knight
    # License: The MIT License (MIT), 2014.
    # https://github.com/benknight/hue-python-rgb-converter
    @staticmethod
    def cross_product(p1: XYPoint, p2: XYPoint) -> float:
        """Calculate the cross product of two XYPoints."""
        return float(p1.x * p2.y - p1.y * p2.x)

    @staticmethod
    def get_distance_between_two_points(one: XYPoint, two: XYPoint) -> float:
        """Calculate the distance between two XYPoints."""
        dx = one.x - two.x
        dy = one.y - two.y
        return math.sqrt(dx * dx + dy * dy)

    @staticmethod
    def get_closest_point_to_line(A: XYPoint, B: XYPoint, P: XYPoint) -> XYPoint:
        """
        Find the closest point from P to a line defined by A and B.

        This point will be reproducible by the lamp
        as it is on the edge of the gamut.
        """
        AP = Color.XYPoint(P.x - A.x, P.y - A.y)
        AB = Color.XYPoint(B.x - A.x, B.y - A.y)
        ab2 = AB.x * AB.x + AB.y * AB.y
        ap_ab = AP.x * AB.x + AP.y * AB.y
        t = ap_ab / ab2

        if t < 0.0:
            t = 0.0
        elif t > 1.0:
            t = 1.0

        return Color.XYPoint(A.x + AB.x * t, A.y + AB.y * t)

    @staticmethod
    def get_closest_point_to_point(
        xy_tuple: tuple[float, float], Gamut: GamutType
    ) -> tuple[float, float]:
        """
        Get the closest matching color within the gamut of the light.

        Should only be used if the supplied color is outside of the color gamut.
        """
        xy_point = Color.XYPoint(xy_tuple[0], xy_tuple[1])

        # find the closest point on each line in the CIE 1931 'triangle'.
        pAB = Color.get_closest_point_to_line(Gamut.red, Gamut.green, xy_point)
        pAC = Color.get_closest_point_to_line(Gamut.blue, Gamut.red, xy_point)
        pBC = Color.get_closest_point_to_line(Gamut.green, Gamut.blue, xy_point)

        # Get the distances per point and see which point is closer to our Point.
        dAB = Color.get_distance_between_two_points(xy_point, pAB)
        dAC = Color.get_distance_between_two_points(xy_point, pAC)
        dBC = Color.get_distance_between_two_points(xy_point, pBC)

        lowest = dAB
        closest_point = pAB

        if dAC < lowest:
            lowest = dAC
            closest_point = pAC

        if dBC < lowest:
            lowest = dBC
            closest_point = pBC

        # Change the xy value to a value which is within the reach of the lamp.
        cx = closest_point.x
        cy = closest_point.y

        return (cx, cy)

    @staticmethod
    def check_point_in_lamps_reach(p: tuple[float, float], Gamut: GamutType) -> bool:
        """Check if the provided XYPoint can be recreated by a Hue lamp."""
        v1 = Color.XYPoint(Gamut.green.x - Gamut.red.x, Gamut.green.y - Gamut.red.y)
        v2 = Color.XYPoint(Gamut.blue.x - Gamut.red.x, Gamut.blue.y - Gamut.red.y)

        q = Color.XYPoint(p[0] - Gamut.red.x, p[1] - Gamut.red.y)
        s = Color.cross_product(q, v2) / Color.cross_product(v1, v2)
        t = Color.cross_product(v1, q) / Color.cross_product(v1, v2)

        return (s >= 0.0) and (t >= 0.0) and (s + t <= 1.0)

    @staticmethod
    def check_valid_gamut(Gamut: GamutType) -> bool:
        """Check if the supplied gamut is valid."""
        # Check if the three points of the supplied gamut are not on the same line.
        v1 = Color.XYPoint(Gamut.green.x - Gamut.red.x, Gamut.green.y - Gamut.red.y)
        v2 = Color.XYPoint(Gamut.blue.x - Gamut.red.x, Gamut.blue.y - Gamut.red.y)
        not_on_line = Color.cross_product(v1, v2) > 0.0001

        # Check if all six coordinates of the gamut lie between 0 and 1.
        red_valid = (
            Gamut.red.x >= 0
            and Gamut.red.x <= 1
            and Gamut.red.y >= 0
            and Gamut.red.y <= 1
        )
        green_valid = (
            Gamut.green.x >= 0
            and Gamut.green.x <= 1
            and Gamut.green.y >= 0
            and Gamut.green.y <= 1
        )
        blue_valid = (
            Gamut.blue.x >= 0
            and Gamut.blue.x <= 1
            and Gamut.blue.y >= 0
            and Gamut.blue.y <= 1
        )

        return not_on_line and red_valid and green_valid and blue_valid
