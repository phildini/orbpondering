"""HTTP client for the Orbpondering remote API."""

import os

import httpx

API_URL = os.environ.get("ORBPONDERING_API_URL", "https://orbpondering.fly.dev/api")
API_KEY = os.environ.get("ORBPONDERING_API_KEY", "dev-key")


class APIError(Exception):
    """Raised when the API returns an error or is unreachable."""


def create_reading(
    date: str | None = None,
    lat: float = 0.0,
    lon: float = 0.0,
    house_system: str = "whole_sign",
    spread: str = "daily",
    reversed: bool = False,
) -> dict:
    """Fetch a standard tarot reading from the API."""
    payload: dict = {
        "lat": lat,
        "lon": lon,
        "house_system": house_system,
        "spread": spread,
        "reversed": reversed,
    }
    if date:
        payload["date"] = date

    try:
        resp = httpx.post(
            f"{API_URL}/reading/",
            json=payload,
            headers={"X-API-Key": API_KEY},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["reading"]
    except httpx.HTTPStatusError as e:
        detail = ""
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        raise APIError(f"API error ({e.response.status_code}): {detail}") from e
    except httpx.RequestError as e:
        raise APIError(f"Could not reach server: {e}") from e


def create_natal_reading(
    date: str | None = None,
    lat: float = 0.0,
    lon: float = 0.0,
    house_system: str = "whole_sign",
    spread: str = "daily",
    reversed: bool = False,
    birth_date: str | None = None,
    birth_time: str | None = None,
    birth_lat: float = 0.0,
    birth_lon: float = 0.0,
    birth_tz: str | None = None,
) -> dict:
    """Fetch a natal-chart-based tarot reading from the API."""
    payload: dict = {
        "lat": lat,
        "lon": lon,
        "house_system": house_system,
        "spread": spread,
        "reversed": reversed,
        "birth_date": birth_date,
        "birth_time": birth_time,
        "birth_lat": birth_lat,
        "birth_lon": birth_lon,
        "birth_tz": birth_tz,
    }
    if date:
        payload["date"] = date

    try:
        resp = httpx.post(
            f"{API_URL}/reading/natal/",
            json=payload,
            headers={"X-API-Key": API_KEY},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["reading"]
    except httpx.HTTPStatusError as e:
        detail = ""
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        raise APIError(f"API error ({e.response.status_code}): {detail}") from e
    except httpx.RequestError as e:
        raise APIError(f"Could not reach server: {e}") from e
