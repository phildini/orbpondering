"""Tests for aspect detection and analysis."""

from __future__ import annotations

from orbpondering.aspects import _angular_separation, _classify_aspect, find_aspects
from orbpondering.constants import AspectType
from orbpondering.models import BirthData, NatalChart


class TestAngularSeparation:
    def test_separation_0(self) -> None:
        assert _angular_separation(0.0, 0.0) == 0.0

    def test_separation_90(self) -> None:
        assert _angular_separation(0.0, 90.0) == 90.0

    def test_separation_180(self) -> None:
        assert _angular_separation(0.0, 180.0) == 180.0

    def test_separation_270(self) -> None:
        assert _angular_separation(0.0, 270.0) == 90.0

    def test_separation_commutative(self) -> None:
        assert (
            _angular_separation(30.0, 60.0) == _angular_separation(60.0, 30.0) == 30.0
        )

    def test_separation_wraps(self) -> None:
        assert _angular_separation(350.0, 10.0) == 20.0


class TestClassifyAspect:
    def test_conjunction(self) -> None:
        result = _classify_aspect(0.0)
        assert result == (AspectType.CONJUNCTION, 0.0)

    def test_conjunction_with_orb(self) -> None:
        result = _classify_aspect(7.5)
        assert result == (AspectType.CONJUNCTION, 7.5)

    def test_conjunction_outside_orb(self) -> None:
        result = _classify_aspect(9.0)
        assert result == (None, 0.0)

    def test_sextile(self) -> None:
        result = _classify_aspect(60.0)
        assert result == (AspectType.SEXTILE, 0.0)

    def test_sextile_with_orb(self) -> None:
        result = _classify_aspect(65.0)
        assert result == (AspectType.SEXTILE, 5.0)

    def test_square(self) -> None:
        result = _classify_aspect(90.0)
        assert result == (AspectType.SQUARE, 0.0)

    def test_trine(self) -> None:
        result = _classify_aspect(120.0)
        assert result == (AspectType.TRINE, 0.0)

    def test_opposition(self) -> None:
        result = _classify_aspect(180.0)
        assert result == (AspectType.OPPOSITION, 0.0)


class TestFindAspects:
    def test_no_aspects(self) -> None:
        # Test case where no planets are close enough to form aspects
        natal_positions = {
            "sun": 0.0,
            "moon": 100.0,
        }
        transit_positions = {
            "sun": 30.0,
            "moon": 200.0,
        }
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
        # All separations (30°, 160°, 70°, 100°) are outside aspect orbs
        assert result == ()

    def test_one_aspect(self) -> None:
        # Test case where sun and moon form a conjunction
        natal_positions = {
            "sun": 0.0,
            "moon": 100.0,
        }
        transit_positions = {
            "sun": 2.0,  # close to natal sun
            "moon": 100.0,  # same as natal moon
        }
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
        # Should detect 3 aspects from the combinations:
        # sun-sun: 2° difference, conjunction
        # moon-moon: 0° difference, conjunction
        # moon-sun: 100° difference, square (90°)
        assert len(result) == 3
        # Check that they are ordered by orb (tightest first)
        # moon-moon: 0° difference, conjunction (orb = 0.0) - should come first
        assert result[0].natal_body == "moon"
        assert result[0].transit_body == "moon"
        assert result[0].aspect_type == AspectType.CONJUNCTION
        assert result[0].orb == 0.0
        # sun-sun: 2° difference, conjunction (orb = 2.0) - should come second
        assert result[1].natal_body == "sun"
        assert result[1].transit_body == "sun"
        assert result[1].aspect_type == AspectType.CONJUNCTION
        assert result[1].orb == 2.0
        # moon-sun: 98° difference, square (orb = 8.0) - should come third
        assert result[2].natal_body == "moon"
        assert result[2].transit_body == "sun"
        assert result[2].aspect_type == AspectType.SQUARE
        assert result[2].orb == 8.0

    def test_multiple_aspects(self) -> None:
        # Test case where multiple aspects form
        natal_positions = {
            "sun": 0.0,
            "moon": 180.0,
            "mercury": 90.0,
        }
        transit_positions = {
            "sun": 5.0,  # conjunction
            "moon": 175.0,  # opposition
            "mercury": 95.0,  # square
        }
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
        # Should detect 9 aspects total from combinations
        assert len(result) == 9
        # Check a few specific ones (sorted by orb, stable sort preserves insertion order)
        # All have orb=5.0, ordered by insertion: sun first (first key in dict)
        assert result[0].natal_body == "sun"
        assert result[0].transit_body == "sun"
        assert result[0].aspect_type == AspectType.CONJUNCTION
        assert result[0].orb == 5.0
        assert result[1].natal_body == "sun"
        assert result[1].transit_body == "moon"
        assert result[1].aspect_type == AspectType.OPPOSITION
        assert result[1].orb == 5.0
        assert result[2].natal_body == "sun"
        assert result[2].transit_body == "mercury"
        assert result[2].aspect_type == AspectType.SQUARE
        assert result[2].orb == 5.0
