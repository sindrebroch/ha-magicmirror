from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory, UpdateEntity, UpdateEntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from custom_components.magicmirror.const import DOMAIN
from custom_components.magicmirror.coordinator import MagicMirrorDataUpdateCoordinator
from custom_components.magicmirror.models import Entity

UPDATES: tuple[UpdateEntityDescription, ...] = (
    UpdateEntityDescription(
        key=Entity.UPDATE_AVAILABLE.value,
        name="MagicMirror Update Available",
        entity_category=EntityCategory.DIAGNOSTIC,
    )
)

async def async_setup_entry(
    hass: HomeAssistant, 
    entry: ConfigEntry, 
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Pi-hole update entities."""
    
    coordinator: MagicMirrorDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        MagicMirrorUpdate(coordinator, description)
        for description in UPDATES
    )

class MagicMirrorUpdate(CoordinatorEntity, UpdateEntity):

    coordinator: MagicMirrorDataUpdateCoordinator

    def __init__(
        self,
        coordinator: MagicMirrorDataUpdateCoordinator,
        name: str,
        description: UpdateEntityDescription,
    ) -> None:
        """Initialize update entity."""

        super().__init__(coordinator)

        self.coordinator = coordinator
        self.entity_description = description
        
        self._attr_unique_id = f"{description.name}"
        self._attr_device_info = coordinator._attr_device_info

        self._attr_title = description.name
        self._attr_release_url = "https://github.com/MichMich/MagicMirror/releases/latest"
