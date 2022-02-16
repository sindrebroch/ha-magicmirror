"""Constants for MagicMirror."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "magicmirror"
PLATFORMS = ["binary_sensor", "button", "switch", "number"]
DATA_HASS_CONFIG = "mm_hass_config"
ATTR_CONFIG_ENTRY_ID = "entry_id"