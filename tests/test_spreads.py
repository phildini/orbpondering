import pytest

from orbpondering.spreads import SPREADS, get_spread


def test_spreads_available() -> None:
    assert "daily" in SPREADS
    assert "three_card" in SPREADS
    assert "celtic_cross" in SPREADS


def test_daily_spread_size() -> None:
    spread = get_spread("daily")
    assert len(spread.positions) == 1


def test_three_card_spread_size() -> None:
    spread = get_spread("three_card")
    assert len(spread.positions) == 3


def test_celtic_cross_spread_size() -> None:
    spread = get_spread("celtic_cross")
    assert len(spread.positions) == 10


def test_get_spread_unknown() -> None:
    with pytest.raises(KeyError):
        get_spread("nonexistent_spread")
