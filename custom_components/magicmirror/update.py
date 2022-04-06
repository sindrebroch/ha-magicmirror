"""Update for MagicMirror."""

from homeassistant.components.update import UpdateEntity

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory, EntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.magicmirror.const import DOMAIN
from custom_components.magicmirror.coordinator import MagicMirrorDataUpdateCoordinator
from custom_components.magicmirror.models import Entity

OLD_VERSION = "outdated"
LATEST_VERSION = "latest"

async def async_setup_entry(
    hass: HomeAssistant, 
    entry: ConfigEntry, 
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the MagicMirror update entities."""
    
    coordinator: MagicMirrorDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        MagicMirrorUpdate(
            coordinator,     
            EntityDescription(
                key=Entity.UPDATE_AVAILABLE.value,
                name="MagicMirror Update Available",
                entity_category=EntityCategory.DIAGNOSTIC,
            )
        ) 
    ])

class MagicMirrorUpdate(CoordinatorEntity, UpdateEntity):

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

        self._attr_title = description.name
        self._attr_release_url = "https://github.com/MichMich/MagicMirror/releases/latest"
        
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
