"""Models for MagicMirror."""

import logging
from typing import Any, Dict

import attr

_LOGGER = logging.getLogger(__name__)

@attr.s(auto_attribs=True, frozen=True)
class MagicMirrorResponse:
    """Class representing MagicMirror."""


    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MagicMirrorResponse":
        """Transform data to dict."""

        _LOGGER.debug("MagicMirrorResponse from_dict %s", data)

        return MagicMirrorResponse()
