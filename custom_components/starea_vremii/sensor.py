"""Sensor platform for Starea Vremii."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import CONF_COUNTY, CONF_MODE, CONF_STATION, DOMAIN, MODE_COUNTY, NAME
from .coordinator import StareaVremiiCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    coordinator: StareaVremiiCoordinator = hass.data[DOMAIN][entry.entry_id]
    data = {**entry.data, **entry.options}
    mode = data.get(CONF_MODE, MODE_COUNTY)
    if mode == MODE_COUNTY:
        label = data.get(CONF_COUNTY)
    else:
        label = data.get(CONF_STATION)
    async_add_entities([StareaVremiiSensor(coordinator, label, mode)])


class StareaVremiiSensor(CoordinatorEntity[StareaVremiiCoordinator], SensorEntity):
    """Representation of a Starea Vremii sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = "°C"

    def __init__(
        self, coordinator: StareaVremiiCoordinator, label: str, mode: str
    ) -> None:
        super().__init__(coordinator)
        self._label = label
        self._mode = mode
        display_label = label if mode == MODE_COUNTY else f"Statie {label}"
        self._attr_name = f"{NAME} {display_label}"
        self._attr_unique_id = f"{DOMAIN}_{slugify(mode)}_{slugify(label)}"

    @property
    def native_value(self):
        return (self.coordinator.data or {}).get("temperature")

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        return {
            "station": data.get("station"),
            "updated": data.get("updated"),
            "humidity": data.get("humidity"),
            "phenomenon": data.get("phenomenon"),
            "clouds": data.get("clouds"),
            "pressure": data.get("pressure"),
            "wind": data.get("wind"),
            "snow": data.get("snow"),
            "icon": data.get("icon"),
        }
