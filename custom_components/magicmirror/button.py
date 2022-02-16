"""Button for MagicMirror."""

from custom_components.magicmirror.models import Entity

from homeassistant.components.button import (
    ButtonEntity,
    ButtonEntityDescription,
    ButtonDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MagicMirrorDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add MagicMirror entities from a config_entry."""

    coordinator: MagicMirrorDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        MagicMirrorShutdownButton(
            coordinator,
            ButtonEntityDescription(
                key=Entity.SHUTDOWN.value,
                name="Magic Mirror Shutdown",
                icon="mdi:power",
            ),
        ),
        MagicMirrorRestartButton(
            coordinator,
            ButtonEntityDescription(
                key=Entity.RESTART.value,
                name="Magic Mirror Restart",
                icon="mdi:restart",
                device_class=ButtonDeviceClass.RESTART,
            ),
        ),
        MagicMirrorRebootButton(
            coordinator,
            ButtonEntityDescription(
                key=Entity.REBOOT.value,
                name="Magic Mirror Reboot",
                icon="mdi:restart",
                device_class=ButtonDeviceClass.RESTART,
            ),
        ),
        MagicMirrorRefreshButton(
            coordinator,
            ButtonEntityDescription(
                key=Entity.REFRESH.value,
                name="Magic Mirror Refresh",
                icon="mdi:refresh",
            ),
        ),
    )


class MagicMirrorButton(CoordinatorEntity, ButtonEntity):
    """Define a MagicMirror entity."""

    coordinator: MagicMirrorDataUpdateCoordinator

    def __init__(
        self,
        coordinator: MagicMirrorDataUpdateCoordinator,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description

        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

    async def async_press(self) -> None:
        """Handle the button press."""


class MagicMirrorShutdownButton(MagicMirrorButton):
    async def async_press(self) -> None:
        """Shut down magicmirror."""
        await self.coordinator.api.shutdown()


class MagicMirrorRestartButton(MagicMirrorButton):
    async def async_press(self) -> None:
        """Restart magicmirror."""
        await self.coordinator.api.restart()


class MagicMirrorRebootButton(MagicMirrorButton):
    async def async_press(self) -> None:
        """Reboot magicmirror."""
        await self.coordinator.api.reboot()


class MagicMirrorRefreshButton(MagicMirrorButton):
    async def async_press(self) -> None:
        """Refresh magicmirror."""
        await self.coordinator.api.refresh()
