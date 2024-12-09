"""Models for MagicMirror."""

from enum import Enum
from typing import Any

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
    header: str  # optional
    config: str  # dict
    classes: str
    hidden: bool
    lockStrings: str  # List
    actions: str  # optional # Dict[str, ActionsDict]

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "ModuleDataResponse":
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
            header=data.get("header"),
            config=data.get("config"),
            lockStrings=data.get("lockStrings"),
            actions=data.get("actions"),
        )


@attr.s(auto_attribs=True)
class ModuleUpdateResponse:
    """Class representing ModuleUpdateResponse."""

    module: str
    result: bool
    remote: str
    lsremote: str
    behind: int

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "ModuleUpdateResponse":
        """Transform data to dict."""
        LOGGER.debug("ModuleUpdateResponse=%s", data)

        return ModuleUpdateResponse(
            module=data.get("module"),
            result=bool(data.get("result", False)),
            remote=data.get("remote") or "",
            lsremote=data.get("lsremote") or "",
            behind=int(data.get("behind", 0)),
        )


@attr.s(auto_attribs=True)
class MagicMirrorData:
    """Class representing MagicMirrorData."""

    monitor_status: str
    update_available: bool
    module_updates: list[ModuleUpdateResponse]
    brightness: int
    modules: list[ModuleDataResponse]


@attr.s(auto_attribs=True)
class ModuleResponse:
    """Class representing Module Response."""

    success: bool
    data: list[ModuleDataResponse]

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "ModuleResponse":
        """Transform data to dict."""
        LOGGER.debug("ModuleResponse=%s", data)

        modules: list[ModuleDataResponse] = []
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
    def from_dict(data: dict[str, Any]) -> "MonitorResponse":
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
    def from_dict(query: dict[str, Any]) -> "Query":
        """Transform data to dict."""
        LOGGER.debug("Query=%s", query)
        return Query(data=query.get("data"))


@attr.s(auto_attribs=True)
class ModuleUpdateResponses:
    """Class representing Module Response."""

    success: bool
    result: list[ModuleUpdateResponse]

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "ModuleUpdateResponses":
        """Transform data to dict."""
        LOGGER.debug("ModuleUpdateResponses=%s", data)

        module_update: list[ModuleUpdateResponse] = []
        for module in data.get("result"):
            module_update.append(ModuleUpdateResponse.from_dict(module))

        return ModuleUpdateResponses(
            success=bool(data.get("success")),
            result=module_update,
        )


@attr.s(auto_attribs=True)
class QueryResponse:
    """Class representing MagicMirror."""

    success: bool
    result: Any
    query: Query

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "QueryResponse":
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
    def from_dict(data: dict[str, Any]) -> "GenericResponse":
        """Transform data to dict."""
        LOGGER.debug("GenericResponse=%s", data)

        return GenericResponse(
            success=bool(data.get("success")),
        )
