"""Constants for MagicMirror."""

from logging import Logger, getLogger

from homeassistant.const import Platform

LOGGER: Logger = getLogger(__package__)

DOMAIN = "magicmirror"
PLATFORMS = [
    Platform.BINARY_SENSOR, 
    Platform.BUTTON, 
    Platform.NUMBER, 
    Platform.SWITCH, 
    Platform.UPDATE,
]
DATA_HASS_CONFIG = "mm_hass_config"
ATTR_CONFIG_ENTRY_ID = "entry_id"