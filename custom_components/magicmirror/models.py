"""Models for MagicMirror."""

from enum import Enum
from typing import Any, Dict

import attr

from .const import LOGGER


class Entity(Enum):
    """Enum for storing Entity."""

    MONITOR_STATUS = "monitor_status"
    UPDATE_AVAILABLE = "update_available"
    BRIGHTNESS = "brightness"

    REBOOT = "reboot"
    RESTART = "restart"
    REFRESH = "refresh"
    SHUTDOWN = "shutdown"


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
class MonitorResponse:
    """Class representing MagicMirror."""

    success: bool
    monitor: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MonitorResponse":
        """Transform data to dict."""

        LOGGER.debug("MonitorResponse=%s", data)

        return MonitorResponse(
            success=bool(data.get("success")),
            monitor=data.get("monitor"),
        )


@attr.s(auto_attribs=True)
class Query:
    """Class representing Query"""

    data: str

    @staticmethod
    def from_dict(query: Dict[str, Any]) -> "Query":
        """Transform data to dict."""

        LOGGER.debug("Query=%s", query)

        return Query(data=query.get("data"))


@attr.s(auto_attribs=True)
class QueryResponse:
    """Class representing MagicMirror."""

    success: bool
    result: Any
    query: Query

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "QueryResponse":
        """Transform data to dict."""

        LOGGER.debug("QueryResponse=%s", data)

        return QueryResponse(
            success=bool(data.get("success")),
            result=data.get("result"),
            query=Query.from_dict(data.get("query")),
        )


@attr.s(auto_attribs=True)
class GenericResponse:
    """Class representing MagicMirror."""

    success: bool

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "GenericResponse":
        """Transform data to dict."""

        LOGGER.debug("GenericResponse=%s", data)

        return GenericResponse(
            success=bool(data.get("success")),
        )
