"""The MagicMirror integration."""
from __future__ import annotations

from datetime import timedelta

from aiohttp.client_exceptions import ClientConnectorError
from async_timeout import timeout
import voluptuous as vol
from voluptuous.error import Error

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN as MAGICMIRROR_DOMAIN, LOGGER
from .magicmirror import MagicMirror
from .models import MagicMirrorResponse

PLATFORMS = ["binary_sensor", "switch"]

SERVICE_MONITOR_ON = "monitor_on"
SERVICE_MONITOR_OFF = "monitor_off"
SERVICE_MONITOR_TOGGLE = "monitor_toggle"
SERVICE_SHUTDOWN = "shutdown"
SERVICE_REBOOT = "reboot"
SERVICE_RESTART = "restart"
SERVICE_MINIMIZE = "minimize"
SERVICE_FULLSCREEN_TOGGLE = "toggle_fullscreen"
SERVICE_NOTIFICATION = "notification"
SERVICE_ALERT = "alert"
SERVICE_BRIGHTNESS = "brightness"
SERVICE_REFRESH = "refresh"
SERVICE_DEVTOOLS = "devtools"
SERVICE_MODULE = "module"
SERVICE_MODULE_ACTION = "module_action"
SERVICE_MODULE_INSTALLED = "module_installed"  # Create entity based on installed?
SERVICE_MODULE_AVAILABLE = "module_available"
SERVICE_MODULE_UPDATE = "module_update"
SERVICE_MODULE_INSTALL = "module_install"


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
    """Set up MagicMirror from a config entry."""

    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    api_key = entry.data[CONF_API_KEY]
    session = async_get_clientsession(hass)

    magicmirror: MagicMirror = MagicMirror(
        host=host,
        port=port,
        api_key=api_key,
        session=session,
    )

    coordinator = MagicMirrorDataUpdateCoordinator(hass, magicmirror)

    await coordinator.async_config_entry_first_refresh()

    entry.async_on_unload(entry.add_update_listener(update_listener))

    hass.data.setdefault(MAGICMIRROR_DOMAIN, {})[entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    await async_register_services(hass, magicmirror)

    return True


async def async_register_services(
    hass: HomeAssistant, magicmirror: MagicMirror
) -> bool:
    """Register services."""

    async def async_monitor_on(_):
        """Turn monitor on for MagicMirror."""
        await magicmirror.monitor_on()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        SERVICE_MONITOR_ON,
        async_monitor_on,
    )

    async def async_monitor_off(_):
        """Turn monitor off for MagicMirror."""
        await magicmirror.monitor_off()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        SERVICE_MONITOR_OFF,
        async_monitor_off,
    )

    async def async_monitor_toggle(_):
        """Toggle monitor for MagicMirror."""
        await magicmirror.monitor_toggle()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        SERVICE_MONITOR_TOGGLE,
        async_monitor_toggle,
    )

    async def async_shutdown(_):
        """Shutdown MagicMirror."""
        await magicmirror.shutdown()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        SERVICE_SHUTDOWN,
        async_shutdown,
    )

    async def async_reboot(_):
        """Reboot MagicMirror."""
        await magicmirror.reboot()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        SERVICE_REBOOT,
        async_reboot,
    )

    async def async_restart(_):
        """Restart MagicMirror."""
        await magicmirror.restart()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        SERVICE_RESTART,
        async_restart,
    )

    async def async_notification(service: ServiceCall):
        """Notification MagicMirror."""
        await magicmirror.alert(
            service.data.get("title", ""),
            service.data.get("message", ""),
            service.data.get("timer", "1000"),
            True,
        )

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        SERVICE_NOTIFICATION,
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
        await magicmirror.alert(
            service.data.get("title", ""),
            service.data.get("message", ""),
            service.data.get("timer", "1000"),
            False,
        )

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        SERVICE_ALERT,
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
        await magicmirror.brightness(service.data["brightness"])

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        SERVICE_BRIGHTNESS,
        async_brightness,
        schema=vol.Schema({vol.Required("brightness"): cv.positive_int}),
    )

    async def async_refresh(_):
        """Refresh MagicMirror."""
        await magicmirror.refresh()

    hass.services.async_register(
        MAGICMIRROR_DOMAIN,
        SERVICE_REFRESH,
        async_refresh,
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[MAGICMIRROR_DOMAIN].pop(entry.entry_id)

    await async_unload_services(hass)

    return unload_ok


async def async_unload_services(hass: HomeAssistant) -> bool:
    """Unload services."""

    hass.services.async_remove(MAGICMIRROR_DOMAIN, SERVICE_MONITOR_ON)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, SERVICE_MONITOR_OFF)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, SERVICE_MONITOR_TOGGLE)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, SERVICE_SHUTDOWN)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, SERVICE_REBOOT)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, SERVICE_RESTART)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, SERVICE_REFRESH)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, SERVICE_BRIGHTNESS)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, SERVICE_NOTIFICATION)
    hass.services.async_remove(MAGICMIRROR_DOMAIN, SERVICE_ALERT)

    return True


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener."""

    await hass.config_entries.async_reload(entry.entry_id)


class MagicMirrorDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching MagicMirror data."""

    def __init__(
        self,
        hass: HomeAssistant,
        magicmirror: MagicMirror,
    ) -> None:
        """Initialize."""

        update_interval = timedelta(minutes=1)

        self.magicmirror: MagicMirror = magicmirror

        super().__init__(
            hass,
            LOGGER,
            name=MAGICMIRROR_DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict[str, str]:
        """Update data via library."""

        LOGGER.warning("Updating coordinator")

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
