"""BinarySensor file for MagicMirror."""

from typing import Any, Final, List, Optional, Tuple

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import (
    DeviceInfo,
    ToggleEntity,
    ToggleEntityDescription,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .__init__ import MagicMirrorDataUpdateCoordinator
from .const import DOMAIN as MAGICMIRROR_DOMAIN

SWITCHES: Final[Tuple[ToggleEntityDescription, ...]] = (
    ToggleEntityDescription(
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

    coordinator: MagicMirrorDataUpdateCoordinator = hass.data[MAGICMIRROR_DOMAIN][
        entry.entry_id
    ]

    switches: List[MagicMirrorSwitch] = []

    for switch_description in SWITCHES:
        switches.append(
            MagicMirrorSwitch(coordinator, switch_description),
        )

    async_add_entities(switches)


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
        self._attr_unique_id = f"{description.key}"

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""

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
            "manufacturer": "MagicMirror",
        }

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""

        await self.coordinator.magicmirror.monitor_on()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""

        await self.coordinator.magicmirror.monitor_off()
        await self.coordinator.async_request_refresh()
