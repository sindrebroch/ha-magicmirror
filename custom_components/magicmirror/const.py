"""Constants for MagicMirror."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "magicmirror"
PLATFORMS = ["binary_sensor", "switch", "number"]
