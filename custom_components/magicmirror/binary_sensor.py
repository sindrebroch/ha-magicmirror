"""Binary sensor file for MagicMirror."""

import logging
from typing import Final, List, Optional, Tuple

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .__init__ import MagicMirrorDataUpdateCoordinator
from .const import DOMAIN as MAGICMIRROR_DOMAIN

BINARY_SENSORS: Final[Tuple[BinarySensorEntityDescription, ...]] = (
    BinarySensorEntityDescription(
        key="monitor_status",
        name="Monitor status",
        icon="mdi:mirror",
    ),
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add MagicMirror entities from a config_entry."""

    coordinator: DataUpdateCoordinator = hass.data[MAGICMIRROR_DOMAIN][entry.entry_id]

    binary_sensors: List[MagicMirrorSensor] = []

    for binary_sensor_description in BINARY_SENSORS:
        binary_sensors.append(
            MagicMirrorSensor(coordinator, binary_sensor_description),
        )

    async_add_entities(binary_sensors)


class MagicMirrorSensor(CoordinatorEntity, BinarySensorEntity):
    """Define a MagicMirror entity."""

    coordinator: MagicMirrorDataUpdateCoordinator

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{description.key}"

    @property
    def is_on(self) -> Optional[bool]:
        """Return true if the binary sensor is on."""

        return (
            True
            if self.coordinator.data[self.entity_description.key] == STATE_ON
            else False
        )

    @property
    def device_info(self) -> Optional[DeviceInfo]:
        """Return the device info."""

        return {
            "identifiers": {(MAGICMIRROR_DOMAIN, "MagicMirror")},
            "name": "MagicMirror",
            "model": "MagicMirror",
            "manufacturer": "",
        }
