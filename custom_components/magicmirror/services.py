"""The MagicMirror integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .api import MagicMirrorApiClient
from .const import DOMAIN as MAGICMIRROR_DOMAIN
from .models import Services

async def async_register_services(
    hass: HomeAssistant, api: MagicMirrorApiClient
) -> bool:
    """Register services."""

    async def async_monitor_on(_):
        """Turn monitor on for MagicMirror."""
        await api.monitor_on()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        Services.MONITOR_ON.value,
        async_monitor_on,
    )

    async def async_monitor_off(_):
        """Turn monitor off for MagicMirror."""
        await api.monitor_off()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        Services.MONITOR_OFF.value,
        async_monitor_off,
    )

    async def async_monitor_toggle(_):
        """Toggle monitor for MagicMirror."""
        await api.monitor_toggle()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        Services.MONITOR_TOGGLE.value,
        async_monitor_toggle,
    )

    async def async_shutdown(_):
        """Shutdown MagicMirror."""
        await api.shutdown()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        Services.SHUTDOWN.value,
        async_shutdown,
    )

    async def async_reboot(_):
        """Reboot MagicMirror."""
        await api.reboot()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        Services.REBOOT.value,
        async_reboot,
    )

    async def async_restart(_):
        """Restart MagicMirror."""
        await api.restart()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        Services.RESTART.value,
        async_restart,
    )

    async def async_notification(service: ServiceCall):
        """Notification MagicMirror."""
        await api.alert(
            service.data.get("title", ""),
            service.data.get("message", ""),
            service.data.get("timer", "1000"),
            True,
        )

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        Services.NOTIFICATION.value,
        async_notification,
        schema=vol.Schema(
            {
                vol.Required("title"): cv.string,
                vol.Required("message"): cv.string,
                vol.Required("timer"): cv.positive_int,
            },
        ),
    )

    async def async_alert(service: ServiceCall):
        """Alert MagicMirror."""
        await api.alert(
            service.data.get("title", ""),
            service.data.get("message", ""),
            service.data.get("timer", "1000"),
            False,
        )

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        Services.ALERT.value,
        async_alert,
        schema=vol.Schema(
            {
                vol.Required("title"): cv.string,
                vol.Required("message"): cv.string,
                vol.Required("timer"): cv.positive_int,
            },
        ),
    )

    async def async_brightness(service: ServiceCall):
        """Change brightness of MagicMirror."""
        await api.brightness(service.data["brightness"])

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        Services.BRIGHTNESS.value,
        async_brightness,
        schema=vol.Schema({vol.Required("brightness"): cv.positive_int}),
    )

    async def async_refresh(_):
        """Refresh MagicMirror."""
        await api.refresh()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        Services.REFRESH.value,
        async_refresh,
    )

    return True

async def async_unload_services(hass: HomeAssistant) -> bool:
    """Unload services."""

    hass.services.async_remove(MAGICMIRROR_DOMAIN, Services.MONITOR_ON.value)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, Services.MONITOR_OFF.value)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, Services.MONITOR_TOGGLE.value)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, Services.SHUTDOWN.value)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, Services.REBOOT.value)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, Services.RESTART.value)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, Services.REFRESH.value)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, Services.BRIGHTNESS.value)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, Services.NOTIFICATION.value)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, Services.ALERT.value)

    return True