"""Number for MagicMirror."""

from custom_components.magicmirror.models import Entity
from typing import cast

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LOGGER
from .coordinator import MagicMirrorDataUpdateCoordinator

NUMBERS: tuple[NumberEntityDescription, ...] = (
    NumberEntityDescription(
        key=Entity.BRIGHTNESS.value,
        name="Magic Mirror Brightness",
        icon="mdi:television-ambient-light",
        unit_of_measurement=PERCENTAGE,
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
        MagicMirrorNumber(coordinator, description) for description in NUMBERS
    )


class MagicMirrorNumber(CoordinatorEntity, NumberEntity):
    """Define a MagicMirror entity."""

    coordinator: MagicMirrorDataUpdateCoordinator

    def __init__(
        self,
        coordinator: MagicMirrorDataUpdateCoordinator,
        description: NumberEntityDescription,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description

        self.sensor_data = self.get_sensor_data()

        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

    @property
    def value(self) -> float:
        return self.sensor_data

    def get_sensor_data(self) -> float:
        return self.coordinator.data.__getattribute__(self.entity_description.key)

    async def async_set_value(self, value: float) -> None:
        """Update the current value."""

        await self.coordinator.api.brightness(int(value))
        await self.coordinator.async_request_refresh()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = self.get_sensor_data()
        super()._handle_coordinator_update()
