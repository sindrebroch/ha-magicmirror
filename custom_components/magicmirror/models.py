"""Models for MagicMirror."""

from enum import Enum
from typing import Any, Dict, List

import attr

from custom_components.magicmirror.const import LOGGER


class Entity(Enum):
    """Enum for storing Entity."""

    MONITOR_STATUS = "monitor_status"
    UPDATE_AVAILABLE = "update_available"
    BRIGHTNESS = "brightness"
    MODULES = "modules"

    REBOOT = "reboot"
    RESTART = "restart"
    REFRESH = "refresh"
    SHUTDOWN = "shutdown"


class Services(Enum):
    """Enum for storing services."""

    MINIMIZE = "minimize"
    FULLSCREEN_TOGGLE = "toggle_fullscreen"
    DEVTOOLS = "devtools"
    MODULE = "module"
    MODULE_ACTION = "module_action"
    MODULE_INSTALLED = "module_installed"  # Create entity based on installed?
    MODULE_AVAILABLE = "module_available"
    MODULE_UPDATE = "module_update"
    MODULE_INSTALL = "module_install"


class ActionsDict:
    """Class representing Actions."""

    notification: str
    guessed: bool


@attr.s(auto_attribs=True)
class ModuleDataResponse:
    """Class representing Module Data Response."""

    index: int
    identifier: str
    name: str
    path: str
    file: str
    configDeepMerge: bool
    # config: str # dict
    classes: str
    hidden: bool
    # lockStrings: str # List
    # actions: Dict[str, ActionsDict]  # optional

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ModuleDataResponse":
        """Transform data to dict."""

        LOGGER.debug("ModuleDataResponse=%s", data)

        return ModuleDataResponse(
            index=data.get("index"),
            identifier=data.get("identifier"),
            name=data.get("name"),
            path=data.get("path"),
            file=data.get("file"),
            configDeepMerge=bool(data.get("configDeepMerge")),
            classes=data.get("classes"),
            hidden=bool(data.get("hidden")),
        )


@attr.s(auto_attribs=True)
class MagicMirrorData:
    """Class representing MagicMirrorData."""

    monitor_status: str
    update_available: bool
    brightness: int
    modules: List[ModuleDataResponse]


@attr.s(auto_attribs=True)
class ModuleResponse:
    """Class representing Module Response."""

    success: bool
    data: List[ModuleDataResponse]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ModuleResponse":
        """Transform data to dict."""

        LOGGER.debug("ModuleResponse=%s", data)

        modules: List[ModuleDataResponse] = []
        for module in data.get("data"):
            modules.append(ModuleDataResponse.from_dict(module))

        return ModuleResponse(
            success=bool(data.get("success")),
            data=modules,
        )


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
