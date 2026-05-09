from datetime import date

import pytest

from orbpondering.constants import HouseSystem
from orbpondering.houses import (
    equal_cusps,
    house_cusps,
    porphyry_cusps,
    whole_sign_cusps,
)


def test_whole_sign_12_cusps() -> None:
    cusps = whole_sign_cusps(15.0)
    assert len(cusps) == 12
    assert all(0 <= c < 360 for c in cusps)


def test_equal_12_cusps() -> None:
    cusps = equal_cusps(15.0)
    assert len(cusps) == 12
    assert all(0 <= c < 360 for c in cusps)


def test_porphyry_12_cusps() -> None:
    cusps = porphyry_cusps(15.0, 200.0)
    assert len(cusps) == 12
    assert all(0 <= c < 360 for c in cusps)


@pytest.mark.parametrize("hs", list(HouseSystem))
def test_all_house_systems_return_12_cusps(hs: HouseSystem) -> None:
    d = date(2025, 1, 15)
    cusps = house_cusps(d, 40.7, -74.0, hs)
    assert len(cusps) == 12
    assert all(0 <= c < 360 for c in cusps)


def test_whole_sign_cusp_order() -> None:
    cusps = whole_sign_cusps(157.5)
    assert cusps[0] == 150
    assert cusps[1] == 180
