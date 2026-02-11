"""Config flow for Starea Vremii."""

from __future__ import annotations

import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig

from .const import (
    API_URL,
    CONF_COUNTY,
    CONF_MODE,
    CONF_STATION,
    COUNTIES,
    DOMAIN,
    MODE_COUNTY,
    MODE_STATION,
    NAME,
)


class StareaVremiiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Starea Vremii."""

    VERSION = 1

    def __init__(self) -> None:
        self._mode: str | None = None

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            self._mode = user_input[CONF_MODE]
            if self._mode == MODE_STATION:
                return await self.async_step_station()
            return await self.async_step_county()

        return self.async_show_form(step_id="user", data_schema=_mode_schema())

    async def async_step_county(self, user_input=None):
        if user_input is not None:
            county = user_input[CONF_COUNTY]
            await self.async_set_unique_id(f"{MODE_COUNTY}:{county}")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=county,
                data={CONF_MODE: MODE_COUNTY, CONF_COUNTY: county},
            )

        return self.async_show_form(step_id="county", data_schema=_county_schema())

    async def async_step_station(self, user_input=None):
        options = await _fetch_station_options(self.hass)
        if user_input is not None:
            station = user_input[CONF_STATION]
            await self.async_set_unique_id(f"{MODE_STATION}:{station}")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=station,
                data={CONF_MODE: MODE_STATION, CONF_STATION: station},
            )

        return self.async_show_form(
            step_id="station", data_schema=_station_schema(options)
        )

    async def async_step_reauth(self, user_input=None):
        return await self.async_step_user(user_input)

    @staticmethod
    def async_get_options_flow(config_entry):
        return StareaVremiiOptionsFlow(config_entry)


class StareaVremiiOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Starea Vremii."""

    def __init__(self, config_entry):
        self._entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            mode = user_input[CONF_MODE]
            if mode == MODE_STATION:
                return await self.async_step_station()
            return await self.async_step_county()

        current = self._entry.options.get(
            CONF_MODE, self._entry.data.get(CONF_MODE, MODE_COUNTY)
        )
        return self.async_show_form(
            step_id="init", data_schema=_mode_schema(current)
        )

    async def async_step_county(self, user_input=None):
        if user_input is not None:
            county = user_input[CONF_COUNTY]
            return self.async_create_entry(
                title=NAME,
                data={CONF_MODE: MODE_COUNTY, CONF_COUNTY: county},
            )

        current = self._entry.options.get(CONF_COUNTY, self._entry.data.get(CONF_COUNTY))
        return self.async_show_form(
            step_id="county", data_schema=_county_schema(current)
        )

    async def async_step_station(self, user_input=None):
        options = await _fetch_station_options(self.hass)
        if user_input is not None:
            station = user_input[CONF_STATION]
            return self.async_create_entry(
                title=NAME,
                data={CONF_MODE: MODE_STATION, CONF_STATION: station},
            )

        current = self._entry.options.get(
            CONF_STATION, self._entry.data.get(CONF_STATION)
        )
        return self.async_show_form(
            step_id="station", data_schema=_station_schema(options, current)
        )


def _mode_schema(current=None):
    return vol.Schema(
        {
            vol.Required(CONF_MODE, default=current or MODE_COUNTY): SelectSelector(
                SelectSelectorConfig(
                    options=[
                        {"label": "Județ", "value": MODE_COUNTY},
                        {"label": "Stație", "value": MODE_STATION},
                    ],
                    mode="dropdown",
                )
            )
        }
    )


def _county_schema(current=None):
    return vol.Schema(
        {
            vol.Required(CONF_COUNTY, default=current): SelectSelector(
                SelectSelectorConfig(options=COUNTIES, mode="dropdown")
            )
        }
    )


def _station_schema(options, current=None):
    if options:
        return vol.Schema(
            {
                vol.Required(CONF_STATION, default=current): SelectSelector(
                    SelectSelectorConfig(options=options, mode="dropdown")
                )
            }
        )
    return vol.Schema({vol.Required(CONF_STATION, default=current): str})


async def _fetch_station_options(hass) -> list[str]:
    session = async_get_clientsession(hass)
    try:
        async with async_timeout.timeout(30):
            async with session.get(API_URL) as response:
                response.raise_for_status()
                payload = await response.json()
    except Exception:
        return []

    if not payload.get("success"):
        return []

    features = payload.get("features") or []
    names = []
    for feature in features:
        properties = feature.get("properties") or {}
        name = properties.get("nume")
        if name:
            names.append(str(name).strip())
    return sorted(set(names))
