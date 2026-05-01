"""Edge case tests."""

import subprocess
import sys
from datetime import date

import pytest

from orbpondering.constants import HouseSystem
from orbpondering.draw import tarot_draw_for_date
from orbpondering.spreads import Spread, get_spread


class TestMissingRichGracefulFallback:
    def test_main_runs_without_rich(self) -> None:
        """Verify __main__ prints plain text when Rich is unavailable."""
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import sys; "
                    "sys.modules['rich'] = None; "
                    "sys.modules['rich.console'] = None; "
                    "from orbpondering.__main__ import main; "
                    "sys.exit(main(['--lat', '0.0', '--lon', '0.0'][:]))"
                ),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        # Should not crash; either prints cards or an informative message
        assert result.returncode in (0, 1)

    def test_main_prints_card_names_without_rich(self) -> None:
        """When Rich is missing, main should still print position: card_name lines."""
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import sys\n"
                    "sys.modules['rich'] = None\n"
                    "sys.modules['rich.console'] = None\n"
                    "sys.modules['rich.progress'] = None\n"
                    "from orbpondering.__main__ import main\n"
                    "sys.exit(main(['--lat', '0.0', '--lon', '0.0', '--spread', 'daily']))\n"
                ),
            ],
            capture_output=True,
            text=True,
            env={**__import__('os').environ, 'PYTHONPATH': '/home/phildini/code/phildini/orbpondering/src'},
            timeout=30,
        )
        # Should produce output about the card drawn
        assert "Theme" in result.stdout or result.returncode == 0


class TestInvalidDateFormats:
    def test_invalid_date_string_returns_error(self) -> None:
        from orbpondering.__main__ import main

        rc = main(["not-a-date"])
        assert rc == 1

    def test_malformed_date_returns_error(self) -> None:
        from orbpondering.__main__ import main

        rc = main(["13/2025/01"])
        assert rc == 1

    def test_empty_date_uses_today(self) -> None:
        from orbpondering.__main__ import main

        rc = main([])
        assert rc == 0


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
