"""The MagicMirror integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from async_timeout import timeout
from voluptuous.error import Error

from .models import PollenvarselResponse
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN as MAGICMIRROR_DOMAIN
from .magicmirror import MagicMirror

PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the MagicMirror integration."""

    hass.data[MAGICMIRROR_DOMAIN] = {}

    if MAGICMIRROR_DOMAIN in config:
        for conf in config[MAGICMIRROR_DOMAIN]:
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    MAGICMIRROR_DOMAIN, context={"source": SOURCE_IMPORT}, data=conf
                )
            )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pollenvarsel from a config entry."""

    websession = async_get_clientsession(hass)
    coordinator = MagicMirrorDataUpdateCoordinator(hass, websession)

    await coordinator.async_config_entry_first_refresh()

    entry.async_on_unload(entry.add_update_listener(update_listener))

    hass.data.setdefault(MAGICMIRROR_DOMAIN, {})[entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[MAGICMIRROR_DOMAIN].pop(entry.entry_id)

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener."""

    await hass.config_entries.async_reload(entry.entry_id)


class MagicMirrorDataUpdateCoordinator(DataUpdateCoordinator[MagicMirrorResponse]):
    """Class to manage fetching MagicMirror data."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: ClientSession,
    ) -> None:
        """Initialize."""

        update_interval = timedelta(minutes=60)

        self.magicmirror: MagicMirror = MagicMirror(session=session)

        super().__init__(
            hass,
            _LOGGER,
            name=MAGICMIRROR_DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> MagicMirrorResponse:
        """Update data via library."""

        try:
            async with timeout(10):
                magicmirror = await self.magicmirror.fetch()

        except (Error, ClientConnectorError) as error:
            _LOGGER.error("Update error %s", error)
            raise UpdateFailed(error) from error

        return magicmirror
