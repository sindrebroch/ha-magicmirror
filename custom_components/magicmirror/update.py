"""Update for MagicMirror."""

from typing import Any
from homeassistant.components.update import UpdateEntity, UpdateEntityFeature

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo, EntityCategory, EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.magicmirror.const import DOMAIN, LOGGER
from custom_components.magicmirror.coordinator import MagicMirrorDataUpdateCoordinator
from custom_components.magicmirror.models import (
    Entity,
    ModuleDataResponse,
)

OLD_VERSION = "outdated"
LATEST_VERSION = "latest"


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the MagicMirror update entities."""

    coordinator: MagicMirrorDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            MagicMirrorUpdate(
                coordinator,
                EntityDescription(
                    key=Entity.UPDATE_AVAILABLE.value,
                    name="MagicMirror update",
                ),
            )
        ]
    )

    coordinator: MagicMirrorDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    modules = list(coordinator.data.modules)
    updates = list(coordinator.data.module_updates)

    for module in modules:
        for update in updates:
            if module.name == update.module:
                async_add_entities([MagicMirrorModuleUpdate(coordinator, module)])


class MagicMirrorUpdate(CoordinatorEntity, UpdateEntity):
    """MagicMirror Update class."""

    coordinator: MagicMirrorDataUpdateCoordinator

    def __init__(
        self,
        coordinator: MagicMirrorDataUpdateCoordinator,
        description: EntityDescription,
    ) -> None:
        """Initialize update entity."""

        super().__init__(coordinator)

        self.coordinator = coordinator
        self.entity_description = description

        self.sensor_data = self.get_sensor_data()

        self._attr_unique_id = f"{description.name}"
        self._attr_device_info = coordinator._attr_device_info
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

        self._attr_title = description.name
        self._attr_release_url = (
            "https://github.com/MichMich/MagicMirror/releases/latest"
        )

        self._attr_latest_version = LATEST_VERSION

    def get_sensor_data(self) -> bool:
        """Get sensor data."""
        state = self.coordinator.data.__getattribute__(self.entity_description.key)
        return True if state == STATE_ON else False

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self.sensor_data = self.get_sensor_data()
        super()._handle_coordinator_update()

    @property
    def installed_version(self) -> str:
        """Version installed and in use."""
        return OLD_VERSION if self.sensor_data else LATEST_VERSION


class MagicMirrorModuleUpdate(MagicMirrorUpdate):
    """MagicMirror Module Update class."""

    coordinator: MagicMirrorDataUpdateCoordinator

    def __init__(
        self,
        coordinator: MagicMirrorDataUpdateCoordinator,
        module: ModuleDataResponse,
    ) -> None:
        """Initialize update entity."""

        super().__init__(coordinator, EntityDescription(key=module.name))
        self.module = module

        self.coordinator = coordinator

        self._attr_name = f"{module.name} update"
        self._attr_unique_id = module.identifier
        self._attr_title = module.name
        self._attr_release_url = None
        self._attr_latest_version = LATEST_VERSION

        self._attr_supported_features = (
            UpdateEntityFeature.INSTALL | UpdateEntityFeature.PROGRESS
        )

        self.sensor_data = self.get_sensor_data()
        self.entity_id = f"update.{module.name}"

    def get_sensor_data(self) -> bool:
        """Get sensor data."""
        for module in self.coordinator.data.module_updates:
            if self.module.name == module.module:
                return module.result
        return False

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self.sensor_data = self.get_sensor_data()
        super()._handle_coordinator_update()

    @property
    def device_info(self) -> DeviceInfo or None:
        return DeviceInfo(
            name=self.entity_description.key,
            model=self.entity_description.key,
            manufacturer="MagicMirror",
            identifiers={(DOMAIN, self.entity_description.key)},
            configuration_url=f"{self.coordinator.api.base_url}/remote.html",
        )

    @property
    def installed_version(self) -> str:
        """Version installed and in use."""
        return OLD_VERSION if self.sensor_data else LATEST_VERSION

    async def async_install(
        self, version: str or None, backup: bool, **kwargs: Any
    ) -> None:
        """Install update."""

        self._attr_in_progress = True
        await self.coordinator.api.module_update(self.module.name)
        self._attr_in_progress = False
