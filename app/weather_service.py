"""
Weather API service: geocode zipcode -> lat/lon, then fetch forecast (min/max temp, humidity).
Uses Open-Meteo (free, no API key).
"""

import httpx
from typing import Optional

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def geocode_zipcode(zipcode: str, country: str = "US") -> Optional[dict]:
    """Resolve zipcode to latitude, longitude, and display name."""
    params = {
        "name": zipcode.strip(),
        "count": 1,
        "language": "en",
        "format": "json",
    }
    if country:
        params["country"] = country
    with httpx.Client(timeout=10.0) as client:
        r = client.get(GEOCODE_URL, params=params)
        r.raise_for_status()
        data = r.json()
    results = data.get("results") or []
    if not results:
        return None
    loc = results[0]
    return {
        "name": loc.get("name", zipcode),
        "latitude": loc["latitude"],
        "longitude": loc["longitude"],
        "timezone": loc.get("timezone", "auto"),
        "country_code": loc.get("country_code", ""),
    }


def get_forecast(latitude: float, longitude: float, timezone: str = "auto") -> Optional[dict]:
    """Fetch daily forecast: min/max temperature and relative humidity (daily aggregates)."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "daily": ["temperature_2m_min", "temperature_2m_max", "relative_humidity_mean"],
        "forecast_days": 7,
    }
    with httpx.Client(timeout=10.0) as client:
        r = client.get(WEATHER_URL, params=params)
        r.raise_for_status()
        data = r.json()
    daily = data.get("daily") or {}
    if not daily or "temperature_2m_min" not in daily:
        return None
    return {
        "time": daily.get("time", []),
        "temperature_min": daily.get("temperature_2m_min", []),
        "temperature_max": daily.get("temperature_2m_max", []),
        "relative_humidity_mean": daily.get("relative_humidity_mean", []),
    }


def get_weather_for_zipcode(zipcode: str, country: str = "US") -> dict:
    """
    Get location and 7-day forecast (min/max temp, mean RH) for a zipcode.
    Returns dict with 'location', 'forecast', and optional 'error'.
    """
    loc = geocode_zipcode(zipcode, country)
    if not loc:
        return {"error": f"Could not find location for zipcode: {zipcode}", "location": None, "forecast": None}
    tz = loc.get("timezone") or "auto"
    forecast = get_forecast(loc["latitude"], loc["longitude"], tz)
    if not forecast:
        return {"error": "Could not fetch forecast for this location", "location": loc, "forecast": None}
    return {"location": loc, "forecast": forecast, "error": None}
