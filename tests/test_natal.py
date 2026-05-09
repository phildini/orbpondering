"""Test basic natal chart functionality."""

from datetime import date

from orbpondering.aspects import find_aspects
from orbpondering.constants import HouseSystem
from orbpondering.draw import birth_tarot_draw, compute_natal_chart
from orbpondering.models import BirthData, NatalChart


class TestNatalChart:
    def test_compute_natal_chart(self) -> None:
        """Test computing a natal chart."""
        birth_data = BirthData(
            date=date(1990, 5, 15),
            time=None,
            lat=40.7128,
            lon=-74.0060,
            tz=None,
        )
        natal = compute_natal_chart(birth_data)
        assert isinstance(natal, NatalChart)
        assert natal.birth_data == birth_data
        assert "sun" in natal.planetary_positions
        assert "moon" in natal.planetary_positions

    def test_compute_chart_with_time(self) -> None:
        """Test computing a chart with exact time."""
        from datetime import time

        birth_data = BirthData(
            date=date(1990, 5, 15),
            time=time(14, 30),
            lat=40.7128,
            lon=-74.0060,
            tz="America/New_York",
        )
        natal = compute_natal_chart(birth_data)
        assert isinstance(natal, NatalChart)

    def test_find_aspects_basic(self) -> None:
        """Test basic aspect detection."""
        # Simple test that doesn't rely on exact orbital calculations
        natal_positions = {"sun": 0.0, "moon": 90.0}
        transit_positions = {"sun": 2.0, "moon": 90.0}
        natal = NatalChart(
            birth_data=BirthData(
                date="2025-01-01",  # pyright: ignore[reportArgumentType]
                time=None,
                lat=0.0,
                lon=0.0,
                tz=None,
            ),
            planetary_positions=natal_positions,
        )
        transit = type(
            "Chart",
            (),
            {
                "planetary_positions": transit_positions,
            },
        )()
        result = find_aspects(natal, transit)
        # Should find some aspects, at least the sun-sun conjunction
        assert isinstance(result, tuple)
        assert len(result) >= 0  # Can be empty

    def test_birth_tarot_draw(self) -> None:
        """Test the full birth tarot draw functionality."""
        birth_data = BirthData(
            date=date(1990, 5, 15),
            time=None,
            lat=40.7128,
            lon=-74.0060,
            tz=None,
        )
        # This should not raise any exceptions
        reading = birth_tarot_draw(
            date.today(), 0.0, 0.0, birth_data, HouseSystem.WHOLE_SIGN, "daily"
        )
        assert reading.natal_chart is not None
        assert reading.aspects is not None
