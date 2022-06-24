"""Support for MagicMirror notifications."""
import asyncio
import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.notify import (
    ATTR_TITLE,
    BaseNotificationService,
    PLATFORM_SCHEMA,
)
from custom_components.magicmirror.coordinator import MagicMirrorDataUpdateCoordinator
from custom_components.magicmirror.const import ATTR_CONFIG_ENTRY_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_TIMER = "timer"
CONF_DROPDOWN = "dropdown"

DEFAULT_TIMER = 5000
DEFAULT_DROPDOWN = False

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_TIMER): vol.Coerce(int), vol.Required(CONF_DROPDOWN): str}
)


async def async_get_service(hass, _, discovery_info=None):
    """Get the MagicMirror notification service."""

    entry_id = discovery_info[ATTR_CONFIG_ENTRY_ID]
    coordinator: MagicMirrorDataUpdateCoordinator = hass.data[DOMAIN][entry_id]
    return MagicMirrorNotificationService(coordinator.api)


class MagicMirrorNotificationService(BaseNotificationService):
    """Implement the notification service for MagicMirror."""

    def __init__(self, notify):
        """Initialize the service."""
        self._notify = notify

    async def async_send_message(self, message: str, **kwargs: Any) -> None:
        """Send a message to MagicMirror devices."""

        title = kwargs.get(ATTR_TITLE, "")

        data = kwargs["data"]

        if data is None:
            timer = DEFAULT_TIMER
            alert_type = DEFAULT_DROPDOWN
        else:
            timer = data.get(CONF_TIMER, DEFAULT_TIMER)
            alert_type = data.get(CONF_DROPDOWN, DEFAULT_DROPDOWN)

        try:
            await self._notify.alert(
                title=title,
                msg=message,
                timer=timer,
                dropdown=bool(alert_type),
            )
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout sending message with MagicMirror")
