"""Update coordinator for Starea Vremii."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import async_get_station_weather
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class StareaVremiiCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator to fetch Starea Vremii data."""

    def __init__(self, hass: HomeAssistant, session, station: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}-{station}",
            update_interval=UPDATE_INTERVAL,
        )
        self._session = session
        self._station = station

    async def _async_update_data(self) -> dict:
        try:
            return await async_get_station_weather(self._session, self._station)
        except Exception as err:
            raise UpdateFailed(str(err)) from err
