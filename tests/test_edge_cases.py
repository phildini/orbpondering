"""Edge case tests."""

import io
import subprocess
import sys
from datetime import date
from unittest.mock import patch

import pytest

from orbpondering.constants import HouseSystem
from orbpondering.display import display_reading
from orbpondering.draw import tarot_draw_for_date
from orbpondering.spreads import Spread, get_spread


class TestMissingRichGracefulFallback:
    def test_display_falls_back_to_plain_text_when_rich_missing(self) -> None:
        """When Rich is missing, display_reading should print plain text."""
        reading = tarot_draw_for_date(
            d=date(2025, 6, 21),
            lat=0.0,
            lon=0.0,
            house_system=HouseSystem.WHOLE_SIGN,
            spread_name="daily",
        )

        with patch.dict(sys.modules, {"rich": None}):
            # Force reimport to trigger ImportError path
            import importlib

            import orbpondering.display

            importlib.reload(orbpondering.display)

            captured = io.StringIO()
            with patch("sys.stdout", captured):
                orbpondering.display.display_reading(reading)

            output = captured.getvalue()
            assert reading.spread.name in output
            assert str(reading.date) in output


class TestBoundaryConditions:
    def test_lat_0_lon_0(self) -> None:
        reading = tarot_draw_for_date(
            d=date(2025, 6, 21),  # solstice
            lat=0.0,
            lon=0.0,
            house_system=HouseSystem.WHOLE_SIGN,
        )
        assert reading.chart is not None

    def test_extreme_latitude(self) -> None:
        reading = tarot_draw_for_date(
            d=date(2025, 3, 20),
            lat=89.0,
            lon=0.0,
            house_system=HouseSystem.WHOLE_SIGN,
        )
        assert reading.chart is not None

    def test_extreme_negative_latitude(self) -> None:
        reading = tarot_draw_for_date(
            d=date(2025, 3, 20),
            lat=-89.0,
            lon=0.0,
            house_system=HouseSystem.WHOLE_SIGN,
        )
        assert reading.chart is not None

    @pytest.mark.parametrize("house_system", list(HouseSystem))
    def test_all_house_systems_at_equinox(self, house_system: HouseSystem) -> None:
        reading = tarot_draw_for_date(
            d=date(2025, 3, 20),
            lat=0.0,
            lon=0.0,
            house_system=house_system,
        )
        assert reading.chart is not None
        assert reading.house_system == house_system


class TestEmptySpreadHandling:
    def test_spread_with_zero_positions(self) -> None:
        """A spread with no positions should return an empty positions list."""
        from orbpondering.draw import daily_tarot_draw

        empty_spread = Spread(name="empty", positions=())
        reading = daily_tarot_draw(
            d=date(2025, 1, 1),
            lat=0.0,
            lon=0.0,
            house_system=HouseSystem.WHOLE_SIGN,
            spread=empty_spread,
        )
        assert isinstance(reading.positions, list)
        assert len(reading.positions) == 0

    def test_get_spread_empty_name(self) -> None:
        with pytest.raises(KeyError):
            get_spread("")
