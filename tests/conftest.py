from datetime import date

import pytest

from orbpondering.constants import HouseSystem


@pytest.fixture
def sample_date():
    return date(2025, 1, 15)


@pytest.fixture
def sample_location():
    return {"lat": 40.7128, "lon": -74.0060}


@pytest.fixture
def house_systems():
    return list(HouseSystem)
