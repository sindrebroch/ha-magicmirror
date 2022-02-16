"""BinarySensor file for MagicMirror."""

from custom_components.magicmirror.models import Entity
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import (
    ToggleEntity,
    ToggleEntityDescription,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MagicMirrorDataUpdateCoordinator

SWITCHES: tuple[ToggleEntityDescription, ...] = (
    ToggleEntityDescription(
        key=Entity.MONITOR_STATUS.value,
        name="MagicMirror Monitor",
        icon="mdi:mirror",
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
        MagicMirrorSwitch(coordinator, description) for description in SWITCHES
    )


class MagicMirrorSwitch(CoordinatorEntity, ToggleEntity):
    """Define a MagicMirror entity."""

    coordinator: MagicMirrorDataUpdateCoordinator

    def __init__(
        self,
        coordinator: MagicMirrorDataUpdateCoordinator,
        description: ToggleEntityDescription,
    ) -> None:
        """Initialize."""

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
    def is_on(self) -> bool:
        """Return true if the switch is on."""

        return self.sensor_data

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = (
            True
            if self.coordinator.data[self.entity_description.key] == STATE_ON
            else False
        )
        super()._handle_coordinator_update()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""

        await self.coordinator.api.monitor_on()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""

        await self.coordinator.api.monitor_off()
        await self.coordinator.async_request_refresh()
