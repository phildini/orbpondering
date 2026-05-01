"""Tests for the draw pipeline."""

import random
from datetime import date

import pytest

from orbpondering.cards import DECK, Arcana
from orbpondering.constants import HouseSystem
from orbpondering.draw import daily_tarot_draw, tarot_draw_for_date, tarot_draw_from_seed
from orbpondering.models import CardPosition, TarotReading
from orbpondering.spreads import SPREADS, Spread


class TestTarotDrawForDate:
    def test_returns_tarot_reading(self, sample_date) -> None:
        reading = tarot_draw_for_date(d=sample_date)
        assert isinstance(reading, TarotReading)

    def test_reading_has_correct_structure(self, sample_date) -> None:
        reading = tarot_draw_for_date(d=sample_date)
        assert reading.date == sample_date
        assert reading.house_system is not None
        assert reading.spread is not None
        assert isinstance(reading.seed, int)
        assert isinstance(reading.positions, list)
        assert reading.chart is not None

    def test_default_spread_is_daily(self, sample_date) -> None:
        reading = tarot_draw_for_date(d=sample_date)
        assert reading.spread.name == SPREADS["daily"].name

    def test_spread_name_selects_correct_spread(self, sample_date) -> None:
        reading = tarot_draw_for_date(
            d=sample_date,
            spread_name="three_card",
        )
        assert reading.spread.name == SPREADS["three_card"].name

    def test_house_system_applied(self, sample_date) -> None:
        reading = tarot_draw_for_date(
            d=sample_date,
            house_system=HouseSystem.PLACIDUS,
        )
        assert reading.house_system == HouseSystem.PLACIDUS

    def test_position_count_matches_spread(self, sample_date) -> None:
        spread = SPREADS["celtic_cross"]
        reading = tarot_draw_for_date(
            d=sample_date,
            spread_name="celtic_cross",
        )
        assert len(reading.positions) == len(spread.positions)

    def test_positions_are_CardPosition_instances(self, sample_date) -> None:
        reading = tarot_draw_for_date(d=sample_date)
        for pos in reading.positions:
            assert isinstance(pos, CardPosition)

    def test_all_positions_have_labels(self, sample_date) -> None:
        reading = tarot_draw_for_date(d=sample_date)
        for pos in reading.positions:
            assert pos.position_label is not None
            assert len(pos.position_label) > 0


class TestDailyTarotDraw:
    @pytest.mark.parametrize("house_system", list(HouseSystem))
    def test_all_house_systems(self, sample_date, sample_location, house_system: HouseSystem) -> None:
        spread = SPREADS["three_card"]
        reading = daily_tarot_draw(
            d=sample_date,
            lat=sample_location["lat"],
            lon=sample_location["lon"],
            house_system=house_system,
            spread=spread,
        )
        assert isinstance(reading, TarotReading)
        assert reading.house_system == house_system
        assert len(reading.positions) == len(spread.positions)

    def test_chart_is_attached(self, sample_date, sample_location) -> None:
        spread = SPREADS["daily"]
        reading = daily_tarot_draw(
            d=sample_date,
            lat=sample_location["lat"],
            lon=sample_location["lon"],
            house_system=HouseSystem.WHOLE_SIGN,
            spread=spread,
        )
        assert reading.chart is not None
        assert reading.chart.date == sample_date

    def test_seed_matches_chart_seed(self, sample_date, sample_location) -> None:
        from orbpondering.seed import chart_seed

        spread = SPREADS["daily"]
        reading = daily_tarot_draw(
            d=sample_date,
            lat=sample_location["lat"],
            lon=sample_location["lon"],
            house_system=HouseSystem.WHOLE_SIGN,
            spread=spread,
        )
        expected_seed = chart_seed(
            sample_date, sample_location["lat"], sample_location["lon"], HouseSystem.WHOLE_SIGN
        )
        assert reading.seed == expected_seed


class TestTarotDrawFromSeed:
    def test_returns_tarot_reading(self) -> None:
        reading = tarot_draw_from_seed(seed=42, spread_name="daily")
        assert isinstance(reading, TarotReading)

    def test_same_seed_same_result(self) -> None:
        r1 = tarot_draw_from_seed(seed=12345, spread_name="three_card")
        r2 = tarot_draw_from_seed(seed=12345, spread_name="three_card")
        assert r1.seed == r2.seed
        assert len(r1.positions) == len(r2.positions)
        for pos1, pos2 in zip(r1.positions, r2.positions, strict=True):
            assert pos1.position_label == pos2.position_label
            assert pos1.card == pos2.card

    def test_different_seeds_different_results(self) -> None:
        r1 = tarot_draw_from_seed(seed=11111, spread_name="three_card")
        r2 = tarot_draw_from_seed(seed=99999, spread_name="three_card")
        cards1 = [pos.card for pos in r1.positions]
        cards2 = [pos.card for pos in r2.positions]
        # Very unlikely but possible that all cards match; check at least the first
        assert cards1[0] != cards2[0] or cards1[1] != cards2[1]

    def test_chart_is_none_when_seeded_manually(self) -> None:
        reading = tarot_draw_from_seed(seed=42, spread_name="daily")
        assert reading.chart is None

    def test_position_count_matches_spread(self) -> None:
        reading = tarot_draw_from_seed(seed=42, spread_name="celtic_cross")
        assert len(reading.positions) == 10

    def test_invalid_spread_raises_keyerror(self) -> None:
        with pytest.raises(KeyError):
            tarot_draw_from_seed(seed=42, spread_name="nonexistent")


class TestDeterministicBehavior:
    def test_repeated_draw_same_result(self, sample_date, sample_location) -> None:
        r1 = tarot_draw_for_date(
            d=sample_date,
            lat=sample_location["lat"],
            lon=sample_location["lon"],
            house_system=HouseSystem.WHOLE_SIGN,
            spread_name="daily",
        )
        r2 = tarot_draw_for_date(
            d=sample_date,
            lat=sample_location["lat"],
            lon=sample_location["lon"],
            house_system=HouseSystem.WHOLE_SIGN,
            spread_name="daily",
        )
        assert r1.seed == r2.seed
        assert r1.positions[0].card == r2.positions[0].card

    def test_shuffle_is_deterministic(self) -> None:
        spread = Spread(name="test", positions=("A", "B", "C"))
        rng1 = random.Random(999)
        cards1 = list(DECK)
        rng1.shuffle(cards1)
        dealt1 = cards1[:3]

        rng2 = random.Random(999)
        cards2 = list(DECK)
        rng2.shuffle(cards2)
        dealt2 = cards2[:3]

        assert dealt1 == dealt2
