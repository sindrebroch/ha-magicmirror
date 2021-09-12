"""Binary sensor file for MagicMirror."""

from typing import Optional

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN as MAGICMIRROR_DOMAIN
from .coordinator import MagicMirrorDataUpdateCoordinator

BINARY_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="monitor_status",
        name="Monitor status",
        icon="mdi:mirror",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add MagicMirror entities from a config_entry."""

    coordinator: DataUpdateCoordinator = hass.data[MAGICMIRROR_DOMAIN][entry.entry_id]

    for binary_sensor_description in BINARY_SENSORS:
        async_add_entities([MagicMirrorSensor(coordinator, binary_sensor_description)])

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

        self.sensor_data = (
            True
            if self.coordinator.data[self.entity_description.key] == STATE_ON
            else False
        )

        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info
    
    @property
    def is_on(self) -> Optional[bool]:
        """Return true if the binary sensor is on."""

        return self.sensor_data

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = (
            True
            if self.coordinator.data[self.entity_description.key] == STATE_ON
            else False
        )
        self.async_write_ha_state()
