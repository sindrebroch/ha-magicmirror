"""Models for MagicMirror."""

from enum import Enum
from typing import Any, Dict

import attr

from .const import LOGGER

class Services(Enum):
    """Enum for storing services."""

    MONITOR_ON = "monitor_on"
    MONITOR_OFF = "monitor_off"
    MONITOR_TOGGLE = "monitor_toggle"
    SHUTDOWN = "shutdown"
    REBOOT = "reboot"
    RESTART = "restart"
    MINIMIZE = "minimize"
    FULLSCREEN_TOGGLE = "toggle_fullscreen"
    NOTIFICATION = "notification"
    ALERT = "alert"
    BRIGHTNESS = "brightness"
    REFRESH = "refresh"
    DEVTOOLS = "devtools"
    MODULE = "module"
    MODULE_ACTION = "module_action"
    MODULE_INSTALLED = "module_installed"  # Create entity based on installed?
    MODULE_AVAILABLE = "module_available"
    MODULE_UPDATE = "module_update"
    MODULE_INSTALL = "module_install"

@attr.s(auto_attribs=True)
class MagicMirrorResponse:
    """Class representing MagicMirror."""

    success: bool
    monitor: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MagicMirrorResponse":
        """Transform data to dict."""

        LOGGER.debug("MagicMirrorResponse=%s", data)

        return MagicMirrorResponse(
            success=bool(data.get("success")),
            monitor=data.get("monitor", ""),
        )
