"""Light entity for MagicMirror."""

from math import ceil
from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ColorMode,
    LightEntity,
    LightEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.magicmirror.const import DOMAIN
from custom_components.magicmirror.coordinator import MagicMirrorDataUpdateCoordinator
from custom_components.magicmirror.models import Entity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add MagicMirror entities from a config_entry."""
    coordinator: MagicMirrorDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            MagicMirrorLight(
                coordinator,
                LightEntityDescription(
                    key=Entity.MONITOR_STATUS.value,
                    name="MagicMirror Monitor",
                ),
            )
        ]
    )


class MagicMirrorLight(CoordinatorEntity, LightEntity):
    """Define a MagicMirror."""

    monitor_state: bool
    brightness_state: int
    coordinator: MagicMirrorDataUpdateCoordinator

    def __init__(
        self,
        coordinator: MagicMirrorDataUpdateCoordinator,
        description: LightEntityDescription,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

        self.color_mode = ColorMode.BRIGHTNESS
        self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}

        self.update_from_data()

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return self.monitor_state

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return (
            "mdi:toggle-switch-outline"
            if self.is_on
            else "mdi:toggle-switch-off-outline"
        )

    def update_from_data(self) -> None:
        """Update sensor data."""
        coordinator_data = self.coordinator.data
        self.monitor_state = (
            coordinator_data.__getattribute__(Entity.MONITOR_STATUS.value) == STATE_ON
        )
        self.brightness_state = int(
            coordinator_data.__getattribute__(Entity.BRIGHTNESS.value)
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self.update_from_data()
        super()._handle_coordinator_update()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        if ATTR_BRIGHTNESS in kwargs:
            await self.coordinator.api.brightness(
                ceil(kwargs[ATTR_BRIGHTNESS] * 100 / 255.0)
            )

        await self.coordinator.api.monitor_on()
        self.monitor_state = True
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self.coordinator.api.monitor_off()
        self.monitor_state = False
        await self.coordinator.async_request_refresh()

    @property
    def brightness(self) -> int | None:
        """Return the brightness of the light."""
        return ceil(self.brightness_state * 255 / 100)
