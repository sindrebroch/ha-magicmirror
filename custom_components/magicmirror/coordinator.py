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
from .models import Entity, MonitorResponse, QueryResponse


class MagicMirrorDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching MagicMirror data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: MagicMirrorApiClient,
    ) -> None:
        """Initialize."""

        self.api = api
        self._attr_device_info = DeviceInfo(
            name="MagicMirror",
            model="MagicMirror",
            manufacturer="MagicMirror",
            identifiers={(MAGICMIRROR_DOMAIN, "MagicMirror")},
            configuration_url=f"{api.base_url}/remote.html",
        )

        super().__init__(
            hass,
            LOGGER,
            name=MAGICMIRROR_DOMAIN,
            update_interval=timedelta(minutes=1),
        )

    async def _async_update_data(self) -> dict[str, str]:
        """Update data via library."""

        try:
            async with timeout(10):
                monitor: MonitorResponse = await self.api.monitor_status()
                update: QueryResponse = await self.api.update_available()
                brightness: QueryResponse = await self.api.get_brightness()

                if not monitor.success:
                    LOGGER.warning("Failed to fetch monitor-status for MagicMirror")
                if not update.success:
                    LOGGER.warning("Failed to fetch update-status for MagicMirror")
                if not brightness.success:
                    LOGGER.warning("Failed to fetch brightness for MagicMirror")

                return {
                    Entity.MONITOR_STATUS.value: monitor.monitor,
                    Entity.UPDATE_AVAILABLE.value: bool(update.result),
                    Entity.BRIGHTNESS.value: int(brightness.result),
                }

        except (Error, ClientConnectorError) as error:
            LOGGER.error("Update error %s", error)
            raise UpdateFailed(error) from error
