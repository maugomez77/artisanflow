"""ArtisanFlow real-time data — DuckDuckGo search + Open-Meteo weather."""

from __future__ import annotations

import httpx


def search_market(query: str, max_results: int = 5) -> list[dict]:
    """Search for Oaxacan craft market data via DuckDuckGo."""
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(f"Oaxacan artisan craft {query}", max_results=max_results))
            return [{"title": r.get("title", ""), "body": r.get("body", ""), "href": r.get("href", "")} for r in results]
    except Exception as e:
        return [{"error": str(e)}]


def get_oaxaca_weather() -> dict:
    """Get current Oaxaca weather — humidity matters for pottery/textile packaging."""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 17.0732,
            "longitude": -96.7266,
            "current_weather": True,
            "hourly": "relativehumidity_2m",
            "timezone": "America/Mexico_City",
            "forecast_days": 1,
        }
        resp = httpx.get(url, params=params, timeout=10)
        data = resp.json()
        current = data.get("current_weather", {})
        humidity_values = data.get("hourly", {}).get("relativehumidity_2m", [])
        avg_humidity = sum(humidity_values) / len(humidity_values) if humidity_values else 0

        return {
            "temperature_c": current.get("temperature"),
            "windspeed_kmh": current.get("windspeed"),
            "weather_code": current.get("weathercode"),
            "avg_humidity_pct": round(avg_humidity, 1),
            "packaging_advisory": (
                "HIGH HUMIDITY - Use extra moisture barriers for pottery and textiles"
                if avg_humidity > 70
                else "Normal conditions - Standard packaging OK"
            ),
        }
    except Exception as e:
        return {"error": str(e)}


def search_shipping_rates(destination: str) -> list[dict]:
    """Search current shipping rates from Mexico."""
    return search_market(f"shipping rates Mexico to {destination} fragile art 2026")


def search_artisan_fairs() -> list[dict]:
    """Search upcoming Oaxacan artisan fairs and events."""
    return search_market("Oaxaca artisan fair event 2026 schedule")


def search_craft_prices(craft_type: str) -> list[dict]:
    """Search current market prices for a craft type."""
    return search_market(f"{craft_type} price market value 2026")
