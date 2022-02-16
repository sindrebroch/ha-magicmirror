"""Diagnostics support for MagicMirror."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from custom_components.magicmirror.api import MagicMirrorApiClient

from custom_components.magicmirror.coordinator import MagicMirrorDataUpdateCoordinator
from custom_components.magicmirror.models import Entity

from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""

    coordinator: MagicMirrorDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    api: MagicMirrorApiClient = coordinator.api
    data = coordinator.data

    diagnostics_data = {
        "host": api.host,
        "port": api.port,
        "brightness": data[Entity.BRIGHTNESS.value],
        "monitor_status": data[Entity.MONITOR_STATUS.value],
        "update_available": data[Entity.UPDATE_AVAILABLE.value],
    }

    return diagnostics_data