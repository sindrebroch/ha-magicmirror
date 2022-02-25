"""BinarySensor file for MagicMirror."""

from custom_components.magicmirror.models import Entity, ModuleDataResponse
from typing import Any, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import (
    ToggleEntity,
    ToggleEntityDescription,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LOGGER
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

    modules: List[ModuleDataResponse] = coordinator.data.__getattribute__(
        Entity.MODULES.value
    )

    for module in modules:
        LOGGER.error("module %s", module)

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
            if self.coordinator.data.__getattribute__(self.entity_description.key)
            == STATE_ON
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
            if self.coordinator.data.__getattribute__(self.entity_description.key)
            == STATE_ON
            else False
        )
        super()._handle_coordinator_update()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""

        await self.coordinator.api.monitor_on()
        self.sensor_data = True
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""

        await self.coordinator.api.monitor_off()
        self.sensor_data = False
        await self.coordinator.async_request_refresh()
