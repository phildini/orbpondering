"""Tests for seed generation."""

from datetime import date

import pytest

from orbpondering.constants import HouseSystem
from orbpondering.seed import chart_seed


class TestChartSeed:
    def test_seed_is_integer(self, sample_date, sample_location) -> None:
        seed = chart_seed(
            sample_date,
            sample_location["lat"],
            sample_location["lon"],
            HouseSystem.WHOLE_SIGN,
        )
        assert isinstance(seed, int)

    def test_seed_is_non_negative(self, sample_date, sample_location) -> None:
        seed = chart_seed(
            sample_date,
            sample_location["lat"],
            sample_location["lon"],
            HouseSystem.WHOLE_SIGN,
        )
        assert seed >= 0

    def test_consistency_same_inputs(self, sample_date, sample_location) -> None:
        seed1 = chart_seed(
            sample_date,
            sample_location["lat"],
            sample_location["lon"],
            HouseSystem.WHOLE_SIGN,
        )
        seed2 = chart_seed(
            sample_date,
            sample_location["lat"],
            sample_location["lon"],
            HouseSystem.WHOLE_SIGN,
        )
        assert seed1 == seed2

    def test_different_dates_different_seeds(self, sample_location) -> None:
        seed1 = chart_seed(
            date(2025, 1, 1),
            sample_location["lat"],
            sample_location["lon"],
            HouseSystem.WHOLE_SIGN,
        )
        seed2 = chart_seed(
            date(2025, 1, 2),
            sample_location["lat"],
            sample_location["lon"],
            HouseSystem.WHOLE_SIGN,
        )
        assert seed1 != seed2

    def test_different_latitudes_different_seeds(self, sample_date) -> None:
        seed1 = chart_seed(sample_date, 40.0, -74.0, HouseSystem.WHOLE_SIGN)
        seed2 = chart_seed(sample_date, 51.0, -74.0, HouseSystem.WHOLE_SIGN)
        assert seed1 != seed2

    def test_different_longitudes_different_seeds(self, sample_date) -> None:
        seed1 = chart_seed(sample_date, 40.7, -74.0, HouseSystem.WHOLE_SIGN)
        seed2 = chart_seed(sample_date, 40.7, 0.0, HouseSystem.WHOLE_SIGN)
        assert seed1 != seed2

    def test_different_house_systems_different_seeds(self, sample_date, sample_location) -> None:
        seeds = set()
        for hs in HouseSystem:
            seed = chart_seed(
                sample_date,
                sample_location["lat"],
                sample_location["lon"],
                hs,
            )
            seeds.add(seed)
        # Placidus is simplified to Porphyry, so we expect at least 3 distinct values
        assert len(seeds) >= 3

    def test_seed_usable_with_random(self, sample_date, sample_location) -> None:
        import random

        seed = chart_seed(
            sample_date,
            sample_location["lat"],
            sample_location["lon"],
            HouseSystem.WHOLE_SIGN,
        )
        rng = random.Random(seed)
        # Should not raise; seed must be a valid integer for Random
        value = rng.random()
        assert 0.0 <= value < 1.0

    def test_seed_reproducibility_with_random(self, sample_date, sample_location) -> None:
        import random

        seed = chart_seed(
            sample_date,
            sample_location["lat"],
            sample_location["lon"],
            HouseSystem.WHOLE_SIGN,
        )
        rng1 = random.Random(seed)
        rng2 = random.Random(seed)
        nums1 = [rng1.random() for _ in range(100)]
        nums2 = [rng2.random() for _ in range(100)]
        assert nums1 == nums2
