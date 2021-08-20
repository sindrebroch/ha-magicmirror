"""Models for MagicMirror."""

from typing import Any, Dict

import attr

from .const import LOGGER


@attr.s(auto_attribs=True, frozen=True)
class MagicMirrorResponse:
    """Class representing MagicMirror."""

    success: bool
    monitor: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MagicMirrorResponse":
        """Transform data to dict."""

        LOGGER.warning("MagicMirrorResponse from_dict %s", data)

        return MagicMirrorResponse(
            success=bool(data.get("success")),
            monitor=data.get("monitor", ""),
        )
