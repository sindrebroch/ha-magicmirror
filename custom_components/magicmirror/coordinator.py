"""The MagicMirror integration."""
from __future__ import annotations

from datetime import timedelta

from aiohttp.client_exceptions import ClientConnectorError
from async_timeout import timeout
from voluptuous.error import Error

from homeassistant.core import HomeAssistant

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MagicMirrorApiClient
from .const import DOMAIN as MAGICMIRROR_DOMAIN, LOGGER
from .models import MagicMirrorResponse


class MagicMirrorDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching MagicMirror data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: MagicMirrorApiClient,
    ) -> None:
        """Initialize."""

        self.api = api

        update_interval = timedelta(minutes=1)

        self._attr_device_info: DeviceInfo = {
            "name": "MagicMirror",
            "model": "MagicMirror",
            "manufacturer": "MagicMirror",
            "identifiers": {(MAGICMIRROR_DOMAIN, "MagicMirror")},
        }

        super().__init__(
            hass,
            LOGGER,
            name=MAGICMIRROR_DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict[str, str]:
        """Update data via library."""

        LOGGER.debug("Updating coordinator")

        try:
            async with timeout(10):
                magicmirror: MagicMirrorResponse = (
                    await self.magicmirror.monitor_status()
                )

                if not magicmirror.success:
                    LOGGER.warning("Magicmirror failed update %s", magicmirror)

        except (Error, ClientConnectorError) as error:
            LOGGER.error("Update error %s", error)
            raise UpdateFailed(error) from error

        return {"monitor_status": magicmirror.monitor}
