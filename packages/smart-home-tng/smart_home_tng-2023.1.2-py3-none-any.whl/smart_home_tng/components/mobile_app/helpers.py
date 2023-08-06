"""
Mobile App Component for Smart Home - The Next Generation.

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

import http
import json
import logging
import typing


from aiohttp import web
from nacl import encoding, secret

from ... import core
from .const import Const

try:
    import nacl
except OSError:
    nacl = False  # pylint: disable=invalid-name

_LOGGER: typing.Final = logging.getLogger(__name__)


# pylint: disable=unused-variable


def _registration_context(registration: dict) -> core.Context:
    """Generate a context from a request."""
    return core.Context(user_id=registration[Const.CONF_USER_ID])


def _supports_encryption() -> bool:
    """Test if we support encryption."""
    return bool(nacl)


def _empty_okay_response(
    headers: dict = None, status: http.HTTPStatus = http.HTTPStatus.OK
) -> web.Response:
    """Return a Response with empty JSON object and a 200."""
    return web.Response(
        text="{}",
        status=status,
        content_type=core.Const.CONTENT_TYPE_JSON,
        headers=headers,
    )


def _error_response(
    code: str,
    message: str,
    status: http.HTTPStatus = http.HTTPStatus.BAD_REQUEST,
    headers: dict = None,
) -> web.Response:
    """Return an error Response."""
    return web.json_response(
        {"success": False, "error": {"code": code, "message": message}},
        status=status,
        headers=headers,
    )


def _decrypt_payload(key: str, ciphertext: str) -> dict[str, str]:
    """Decrypt encrypted payload."""

    # pylint: disable=unused-argument
    def get_key_bytes(key: str, keylen: int) -> str:
        return key

    return _decrypt_payload_helper(key, ciphertext, get_key_bytes, encoding.HexEncoder)


def _decrypt_payload_helper(
    key: str,
    ciphertext: str,
    get_key_bytes: typing.Callable[[str, int], str | bytes],
    key_encoder,
) -> dict[str, str] | None:
    """Decrypt encrypted payload."""
    try:
        keylen, decrypt = _setup_decrypt(key_encoder)
    except OSError:
        _LOGGER.warning("Ignoring encrypted payload because libsodium not installed")
        return None

    if key is None:
        _LOGGER.warning("Ignoring encrypted payload because no decryption key known")
        return None

    key_bytes = get_key_bytes(key, keylen)

    msg_bytes = decrypt(ciphertext, key_bytes)
    message = core.helpers.json_loads(msg_bytes)
    _LOGGER.debug("Successfully decrypted mobile_app payload")
    return message


def _setup_decrypt(key_encoder) -> tuple[int, typing.Callable]:
    """Return decryption function and length of key.

    Async friendly.
    """

    def decrypt(ciphertext, key):
        """Decrypt ciphertext using key."""
        return secret.SecretBox(key, encoder=key_encoder).decrypt(
            ciphertext, encoder=encoding.Base64Encoder
        )

    return (secret.SecretBox.KEY_SIZE, decrypt)


def _decrypt_payload_legacy(key: str, ciphertext: str) -> dict[str, str]:
    """Decrypt encrypted payload."""

    def get_key_bytes(key: str, keylen: int) -> bytes:
        key_bytes = key.encode("utf-8")
        key_bytes = key_bytes[:keylen]
        key_bytes = key_bytes.ljust(keylen, b"\0")
        return key_bytes

    return _decrypt_payload_helper(key, ciphertext, get_key_bytes, encoding.RawEncoder)


def _webhook_response(
    data,
    *,
    registration: dict,
    status: http.HTTPStatus = http.HTTPStatus.OK,
    headers: dict = None,
) -> web.Response:
    """Return a encrypted response if registration supports it."""
    data = json.dumps(data, cls=core.JsonEncoder)

    if registration[Const.ATTR_SUPPORTS_ENCRYPTION]:
        keylen, encrypt = _setup_encrypt(
            encoding.HexEncoder
            if Const.ATTR_NO_LEGACY_ENCRYPTION in registration
            else encoding.RawEncoder
        )

        if Const.ATTR_NO_LEGACY_ENCRYPTION in registration:
            key = registration[Const.CONF_SECRET]
        else:
            key = registration[Const.CONF_SECRET].encode("utf-8")
            key = key[:keylen]
            key = key.ljust(keylen, b"\0")

        enc_data = encrypt(data.encode("utf-8"), key).decode("utf-8")
        data = json.dumps({"encrypted": True, "encrypted_data": enc_data})

    return web.Response(
        text=data,
        status=status,
        content_type=core.Const.CONTENT_TYPE_JSON,
        headers=headers,
    )


def _setup_encrypt(key_encoder) -> tuple[int, typing.Callable]:
    """Return encryption function and length of key.

    Async friendly.
    """

    def encrypt(ciphertext, key):
        """Encrypt ciphertext using key."""
        return secret.SecretBox(key, encoder=key_encoder).encrypt(
            ciphertext, encoder=encoding.Base64Encoder
        )

    return (secret.SecretBox.KEY_SIZE, encrypt)


def _safe_registration(registration: dict) -> dict:
    """Return a registration without sensitive values."""
    # Sensitive values: webhook_id, secret, cloudhook_url
    return {
        Const.ATTR_APP_DATA: registration[Const.ATTR_APP_DATA],
        Const.ATTR_APP_ID: registration[Const.ATTR_APP_ID],
        Const.ATTR_APP_NAME: registration[Const.ATTR_APP_NAME],
        Const.ATTR_APP_VERSION: registration[Const.ATTR_APP_VERSION],
        Const.ATTR_DEVICE_NAME: registration[Const.ATTR_DEVICE_NAME],
        Const.ATTR_MANUFACTURER: registration[Const.ATTR_MANUFACTURER],
        Const.ATTR_MODEL: registration[Const.ATTR_MODEL],
        Const.ATTR_OS_VERSION: registration[Const.ATTR_OS_VERSION],
        Const.ATTR_SUPPORTS_ENCRYPTION: registration[Const.ATTR_SUPPORTS_ENCRYPTION],
    }
