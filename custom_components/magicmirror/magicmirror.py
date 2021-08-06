"""MagicMirror library."""

import json
import logging
from typing import Optional

import aiohttp
from voluptuous.error import Error

from .models import MagicMirrorResponse
from homeassistant.const import HTTP_OK, HTTP_UNAUTHORIZED

SCHEME = "https"
BASE_URL = "/api/"

_LOGGER = logging.getLogger(__name__)


class MagicMirror:
    """Main class for handling connection with."""

    def __init__(
        self,
        session: Optional[aiohttp.client.ClientSession] = None,
    ) -> None:
        """Initialize connection with MagicMirror."""

        self._session = session

    async def fetch(self) -> MagicMirrorResponse:
        """Fetch data from MagicMirror."""

        if self._session is None:
            raise RuntimeError("Session required")

        URL = f"{SCHEME}://{BASE_URL}"

        async with self._session.get(url=URL) as resp:
            if resp.status == HTTP_UNAUTHORIZED:
                raise Error(f"Unauthorized. {resp.status}")
            if resp.status != HTTP_OK:
                error_text = json.loads(await resp.text())
                raise Error(f"Not OK {resp.status} {error_text}")

            data = await resp.json()

        return MagicMirrorResponse.from_dict(data)
