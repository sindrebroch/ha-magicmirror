"""The MagicMirror integration."""

from __future__ import annotations

from datetime import timedelta

from aiohttp.client_exceptions import ClientConnectorError
from async_timeout import timeout
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from voluptuous.error import Error

from custom_components.magicmirror.api import MagicMirrorApiClient
from custom_components.magicmirror.const import DOMAIN, LOGGER
from custom_components.magicmirror.models import (
    MagicMirrorData,
    ModuleResponse,
    ModuleUpdateResponses,
    MonitorResponse,
    QueryResponse,
)


class MagicMirrorDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching MagicMirror data."""

    data: MagicMirrorData

    def __init__(
        self, hass: HomeAssistant, api: MagicMirrorApiClient, name: str
    ) -> None:
        """Initialize."""
        self.api = api
        self.name = name

        self._attr_device_info = DeviceInfo(
            name=name,
            model="MagicMirror",
            manufacturer="MagicMirror",
            identifiers={(DOMAIN, "MagicMirror")},
            configuration_url=f"{api.base_url}/remote.html",
        )

        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )

    async def _async_update_data(self) -> MagicMirrorData:
        """Update data via library."""
        try:
            async with timeout(20):
                update: QueryResponse = await self.api.mm_update_available()
                module_updates: ModuleUpdateResponses = (
                    await self.api.update_available()
                )
                monitor: MonitorResponse = await self.api.monitor_status()
                brightness: QueryResponse = await self.api.get_brightness()
                modules: ModuleResponse = await self.api.get_modules()

                if not monitor.success:
                    LOGGER.warning("Failed to fetch monitor-status for MagicMirror")
                if not update.success:
                    LOGGER.warning("Failed to fetch update-status for MagicMirror")
                if not brightness.success:
                    LOGGER.warning("Failed to fetch brightness for MagicMirror")
                if not modules.success:
                    LOGGER.warning("Failed to fetch modules for MagicMirror")
                if not module_updates.success:
                    LOGGER.warning("Failed to fetch module updates for MagicMirror")

                return MagicMirrorData(
                    monitor_status=monitor.monitor,
                    update_available=update.result,
                    module_updates=module_updates.result,
                    brightness=int(brightness.result),
                    modules=modules.data,
                )

        except (Error, ClientConnectorError) as error:
            LOGGER.error("Update error %s", error)
            raise UpdateFailed(error) from error
