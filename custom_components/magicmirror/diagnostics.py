"""Diagnostics support for MagicMirror."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from custom_components.magicmirror.api import MagicMirrorApiClient
from custom_components.magicmirror.const import DOMAIN, LOGGER
from custom_components.magicmirror.coordinator import MagicMirrorDataUpdateCoordinator


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    LOGGER.debug("diagnostics entry %s", entry.as_dict())

    coordinator: MagicMirrorDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    api: MagicMirrorApiClient = coordinator.api
    data = coordinator.data
    LOGGER.debug("diagnostics data %s", data)

    return {
        "host": api.host,
        "port": api.port,
        "brightness": data.brightness,
        "monitor_status": data.monitor_status,
        "update_available": data.update_available,
        "module_updates": data.module_updates,
        "modules": str(data.modules),
    }

    # todo
    # TO_REDACT = [
    #    CONF_API_KEY,
    #    APPLIANCE_CODE
    # ]
    # return {
    #    "entry_data": async_redact_data(entry.data, TO_REDACT),
    #    "data": entry.runtime_data.data,
    # }


async def async_get_device_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry, device: DeviceEntry
) -> dict[str, Any]:
    """Return diagnostics for a device."""
    LOGGER.debug("diagnostics device %s", device)
    LOGGER.debug("diagnostics entry %s", entry.as_dict())
    coordinator: MagicMirrorDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    api: MagicMirrorApiClient = coordinator.api
    data = coordinator.data
    return {
        "host": api.host,
        "port": api.port,
        "brightness": data.brightness,
        "monitor_status": data.monitor_status,
        "update_available": data.update_available,
        "module_updates": data.module_updates,
        "modules": str(data.modules),
    }
