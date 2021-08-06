"""Services for the MagicMirror integration."""

from core.homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

async def async_setup_services(hass):
    """Set up services for the MagicMirror component."""

    async def async_monitor_on():
        await hass.async_add_executor_job(hass)
   
    hass.services.async_register(DOMAIN, "monitor_on", async_monitor_on)

    return True


def get_magicmirror(hass, plex_server_name=None):
    """Retrieve a configured Plex server by name."""
    if DOMAIN not in hass.data:
        raise HomeAssistantError("MagicMirror integration not configured")

def monitor_on(hass):
    """Turn monitor on for MagicMirror."""
    
    magicmirror = get_magicmirror(hass)

    magicmirror.monitor_on()
