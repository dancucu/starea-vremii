"""API client for Starea Vremii."""

from __future__ import annotations

import html
from typing import Any

import aiohttp

from .const import API_URL


def _normalize(text: str) -> str:
    return text.strip().upper()


def _safe_float(value: Any) -> float | None:
    if value in (None, "", "indisponibil"):
        return None
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return None


def _safe_int(value: Any) -> int | None:
    if value in (None, "", "indisponibil"):
        return None
    try:
        return int(float(str(value).replace(",", ".")))
    except ValueError:
        return None


def _matches_station(name: str, query: str) -> bool:
    if not name:
        return False
    name_norm = _normalize(name)
    query_norm = _normalize(query)
    return name_norm == query_norm or query_norm in name_norm


def _clean_updated(value: Any) -> str | None:
    if not value:
        return None
    return html.unescape(str(value)).replace("\u00a0", " ").strip()


def _extract_properties(properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "station": properties.get("nume"),
        "temperature": _safe_float(properties.get("tempe")),
        "humidity": _safe_int(properties.get("umezeala")),
        "phenomenon": properties.get("fenomen_e"),
        "clouds": properties.get("nebulozitate"),
        "pressure": properties.get("presiunetext"),
        "wind": properties.get("vant"),
        "snow": properties.get("zapada"),
        "icon": properties.get("icon"),
        "updated": _clean_updated(properties.get("actualizat")),
    }


async def async_get_station_weather(
    session: aiohttp.ClientSession, station: str
) -> dict[str, Any]:
    if not station:
        raise ValueError("Station is required")
    query = station

    async with session.get(API_URL, timeout=30) as response:
        response.raise_for_status()
        payload = await response.json()

    if not payload.get("success"):
        raise ValueError("API returned success=false")

    features = payload.get("features") or []
    for feature in features:
        properties = feature.get("properties") or {}
        name = properties.get("nume")
        if name and _matches_station(name, query):
            return _extract_properties(properties)

    raise ValueError(f"Station not found for county: {county}")
