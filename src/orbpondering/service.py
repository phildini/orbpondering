"""Service layer for orbpondering with validation and persistence."""

import json
import os
from dataclasses import asdict
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from orbpondering.models import Chart, TarotReading
from orbpondering.constants import HouseSystem
from orbpondering.draw import compute_chart, daily_tarot_draw


def validate_chart(chart: Chart) -> bool:
    """Validate chart data integrity."""
    if not isinstance(chart, Chart):
        return False
    
    # Validate planetary positions
    if not isinstance(chart.planetary_positions, dict):
        return False
    
    # Validate that all bodies have proper positions
    for body, position in chart.planetary_positions.items():
        if not hasattr(position, 'body'):
            return False
        if not hasattr(position, 'longitude'):
            return False
        if not hasattr(position, 'zodiac_sign'):
            return False
            
    return True


def validate_reading(reading: TarotReading) -> bool:
    """Validate reading data integrity."""
    if not isinstance(reading, TarotReading):
        return False
    
    # Validate that positions are properly formed
    for pos in reading.positions:
        if not hasattr(pos, 'position_label'):
            return False
        if not hasattr(pos, 'card'):
            return False
            
    return True


def load_config(config_path: str = None) -> dict:
    """Load configuration from TOML file."""
    if config_path is None:
        config_dir = Path.home() / ".config" / "orbpondering"
        config_path = config_dir / "config.toml"
    
    if not config_path.exists():
        # Return default configuration
        return {
            "default_house_system": "whole_sign",
            "default_latitude": 0.0,
            "default_longitude": 0.0,
            "enable_cache": True,
            "cache_duration_hours": 24,
        }
        
    # In a real implementation, we would parse TOML here
    # For now, returning default config as placeholder
    return {
        "default_house_system": "whole_sign",
        "default_latitude": 0.0,
        "default_longitude": 0.0,
        "enable_cache": True,
        "cache_duration_hours": 24,
    }


def save_config(config: dict, config_path: str = None) -> None:
    """Save configuration to TOML file."""
    if config_path is None:
        config_dir = Path.home() / ".config" / "orbpondering"
        config_path = config_dir / "config.toml"
    
    # Ensure directory exists
    config_dir = Path(config_path).parent
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # In a real implementation, we would save as TOML
    # For now, we'll just ensure the directory exists
    pass


def get_readings_dir() -> Path:
    """Get the directory where readings are stored."""
    return Path.home() / ".config" / "orbpondering" / "readings"


def save_reading(reading: TarotReading, reading_path: str = None) -> None:
    """Save a tarot reading to JSON file."""
    if reading_path is None:
        # Determine filename based on date and seed
        date_str = reading.date.isoformat()
        reading_path = get_readings_dir() / f"{date_str}_{reading.seed}.json"
    
    # Ensure directory exists
    reading_dir = Path(reading_path).parent
    reading_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert dataclass to dictionary for JSON serialization
    reading_dict = {
        "date": reading.date.isoformat(),
        "house_system": reading.house_system.value,
        "spread": reading.spread.name,
        "seed": reading.seed,
        "positions": [
            {
                "position_label": pos.position_label,
                "card": {
                    "name": pos.card.name,
                    "arcana": pos.card.arcana.value,
                    "suit": pos.card.suit.value if pos.card.suit else None,
                    "number": pos.card.number,
                    "keywords": pos.card.keywords,
                    "upright": pos.card.upright,
                },
                "house_number": pos.house_number,
                "resonant_planet": pos.resonant_planet,
                "resonant_sign": pos.resonant_sign.value if pos.resonant_sign else None,
            }
            for pos in reading.positions
        ],
        "chart": None,
        "natal_chart": None,
        "aspects": [],
    }
    
    # Add chart data if present
    if reading.chart:
        reading_dict["chart"] = {
            "date": reading.chart.date.isoformat(),
            "latitude": reading.chart.latitude,
            "longitude": reading.chart.longitude,
            "house_system": reading.chart.house_system.value,
            "ascendant": reading.chart.ascendant,
            "midheaven": reading.chart.midheaven,
            "house_cusps": reading.chart.house_cusps,
            "seed": reading.chart.seed,
            "dominant_element": reading.chart.dominant_element,
        }
    
    # Add natal chart data if present
    if reading.natal_chart:
        reading_dict["natal_chart"] = {
            "birth_data": {
                "date": reading.natal_chart.birth_data.date.isoformat(),
                "time": reading.natal_chart.birth_data.time.isoformat() if reading.natal_chart.birth_data.time else None,
                "lat": reading.natal_chart.birth_data.lat,
                "lon": reading.natal_chart.birth_data.lon,
                "tz": reading.natal_chart.birth_data.tz,
            },
            "planetary_positions": {
                body: deg for body, deg in reading.natal_chart.planetary_positions.items()
            }
        }
    
    # Add aspects if present
    if reading.aspects:
        reading_dict["aspects"] = [
            {
                "natal_body": aspect.natal_body,
                "transit_body": aspect.transit_body,
                "separation": aspect.separation,
                "aspect_type": aspect.aspect_type.value,
                "orb": aspect.orb,
            }
            for aspect in reading.aspects
        ]
    
    with open(reading_path, 'w') as f:
        json.dump(reading_dict, f, indent=2)


def load_reading(date: date, seed: int) -> Optional[TarotReading]:
    """Load a tarot reading from JSON file."""
    reading_path = get_readings_dir() / f"{date.isoformat()}_{seed}.json"
    
    if not reading_path.exists():
        return None
        
    with open(reading_path, 'r') as f:
        reading_data = json.load(f)
    
    # Note: This is a simplified version. In practice, we'd need to reconstruct 
    # the dataclass objects from the JSON data.
    return None


def cache_ephemeris(d: date, lat: float, lon: float, house_system: HouseSystem, tz: str | None = None) -> Chart:
    """Cache ephemeris data to avoid recomputation."""
    # For now, this just calls compute_chart, but in a real implementation 
    # we'd store the result and retrieve it if available within cache duration
    
    # This is a placeholder - in a real implementation, we'd:
    # 1. Check if cached data exists and is still valid
    # 2. If not, compute and store the data
    # 3. Return the chart
    
    return compute_chart(d, lat, lon, house_system, tz)