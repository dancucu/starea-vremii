"""Starea Vremii integration."""

import unicodedata

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_COUNTY,
    CONF_MODE,
    CONF_STATION,
    COUNTY_STATION_MAP,
    DOMAIN,
    MODE_COUNTY,
)
from .coordinator import StareaVremiiCoordinator

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Starea Vremii from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    session = async_get_clientsession(hass)
    data = {**entry.data, **entry.options}
    mode = data.get(CONF_MODE, MODE_COUNTY)
    if mode == MODE_COUNTY:
        county = data.get(CONF_COUNTY)
        station = _resolve_station_from_county(county)
    else:
        station = data.get(CONF_STATION)

    coordinator = StareaVremiiCoordinator(hass, session, station)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok


def _normalize_county(name: str) -> str:
    normalized = unicodedata.normalize("NFD", name)
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn").lower()


def _resolve_station_from_county(county: str | None) -> str | None:
    if not county:
        return None
    station = COUNTY_STATION_MAP.get(county)
    if station:
        return station
    county_normalized = _normalize_county(county)
    for key, value in COUNTY_STATION_MAP.items():
        if _normalize_county(key) == county_normalized:
            return value
    return None
