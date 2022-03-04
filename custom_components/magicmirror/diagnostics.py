"""Diagnostics support for MagicMirror."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from custom_components.magicmirror.api import MagicMirrorApiClient

from custom_components.magicmirror.coordinator import MagicMirrorDataUpdateCoordinator
from custom_components.magicmirror.const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""

    coordinator: MagicMirrorDataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    api: MagicMirrorApiClient = coordinator.api
    data = coordinator.data

    return {
        "host": api.host,
        "port": api.port,
        "brightness": data.brightness,
        "monitor_status": data.monitor_status,
        "update_available": data.update_available,
        "modules": str(data.modules),
    }
