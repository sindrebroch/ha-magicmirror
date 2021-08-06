"""Sensor file for MagicMirror."""

from core.homeassistant.const import CONF_HOST, CONF_NAME
import logging
from typing import Final, List, Optional, Tuple, cast

from .const import DOMAIN as MAGICMIRROR_DOMAIN

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

_LOGGER = logging.getLogger(__name__)

SENSORS: Final[Tuple[SensorEntityDescription, ...]] = ()


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add MagicMirror entities from a config_entry."""

    coordinator: DataUpdateCoordinator = hass.data[MAGICMIRROR_DOMAIN][entry.entry_id]

    name: str = entry.data[CONF_NAME]  #
    host: str = entry.data[CONF_HOST]  #

    sensors: List[MagicMirrorSensor] = []

    for sensor_description in SENSORS:
        sensors.append(
            MagicMirrorSensor(coordinator,sensor_description),
        )

    async_add_entities(sensors)


class MagicMirrorSensor(CoordinatorEntity, SensorEntity):
    """Define a MagicMirror entity."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)

        self.entity_description = description

        self.sensor_data: str = _get_sensor_data(coordinator.data, description.key)

        self._attr_unique_id = f"{self.area.name}_{description.key}"
        self._attr_name = f"{self.area.name.title()} {description.key}"

    @property
    def state(self) -> StateType:
        """Return the state."""

        return cast(StateType, self.sensor_data)

    @property
    def device_info(self) -> Optional[DeviceInfo]:
        """Return the device info."""

        return {
            "identifiers": {(MAGICMIRROR_DOMAIN, self.area.name)},
            "name": f"MagicMirror {self.area.name.title()}",
            "model": "MagicMirror",
            "manufacturer": f"{self.area.name.title()}",
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = _get_sensor_data(
            self.coordinator.data, self.entity_description.key
        )
        self.async_write_ha_state()


def _get_sensor_data(sensors: MagicMirrorResponse, sensor_name: str) -> str:
    """Get sensor data."""

    return sensors[sensor_name]
