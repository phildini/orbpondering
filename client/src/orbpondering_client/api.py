"""HTTP client for the remote Orbpondering API."""

import httpx

API_URL = "http://localhost:8099/api"
API_KEY = "dev-key"


def create_reading(date=None, lat=0.0, lon=0.0, house_system="whole_sign", spread="daily", reversed=False):
    """Fetch a standard reading from the API."""
    payload = {
        "lat": lat,
        "lon": lon,
        "house_system": house_system,
        "spread": spread,
        "reversed": reversed,
    }
    if date:
        payload["date"] = date

    resp = httpx.post(
        f"{API_URL}/reading/",
        json=payload,
        headers={"X-API-Key": API_KEY},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["reading"]
