"""Binary sensor for MagicMirror."""

from typing import Optional

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
    BinarySensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.magicmirror.const import DOMAIN
from custom_components.magicmirror.coordinator import MagicMirrorDataUpdateCoordinator
from custom_components.magicmirror.models import Entity

BINARY_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key=Entity.UPDATE_AVAILABLE.value,
        name="MagicMirror Update Available",
        icon="mdi:arrow-up-box",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=BinarySensorDeviceClass.UPDATE,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add MagicMirror entities from a config_entry."""

    coordinator: MagicMirrorDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        MagicMirrorBinarySensor(coordinator, description)
        for description in BINARY_SENSORS
    )


class MagicMirrorBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Define a MagicMirror entity."""

    coordinator: MagicMirrorDataUpdateCoordinator

    def __init__(
        self,
        coordinator: MagicMirrorDataUpdateCoordinator,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description

        self.sensor_data = self.get_sensor_data()

        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

    @property
    def is_on(self) -> Optional[bool]:
        """Return true if the binary sensor is on."""
        return self.sensor_data

    def get_sensor_data(self) -> bool:
        """Get sensor data."""
        state = self.coordinator.data.__getattribute__(self.entity_description.key)
        return True if state == STATE_ON else False

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = self.get_sensor_data()
        super()._handle_coordinator_update()
