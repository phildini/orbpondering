"""Tests for display functionality."""

from datetime import date

import pytest

from orbpondering.cards import Card
from orbpondering.constants import Arcana, HouseSystem, Suit
from orbpondering.models import CardPosition, TarotReading
from orbpondering.spreads import Spread


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_reading() -> TarotReading:
    spread = Spread(name="Three Card Spread", positions=("Past", "Present", "Future"))
    cards = [
        Card(name="The Tower", arcana=Arcana.MAJOR, keywords=("sudden_change", "upheaval")),
        Card(name="Five of Cups", arcana=Arcana.MINOR, suit=Suit.CUPS, number=5, keywords=("regret", "loss")),
        Card(name="The Sun", arcana=Arcana.MAJOR, keywords=("positivity", "fun")),
    ]
    positions = [
        CardPosition(position_label=label, card=card)
        for label, card in zip(spread.positions, cards, strict=True)
    ]
    return TarotReading(
        date=date(2025, 1, 15),
        house_system=HouseSystem.WHOLE_SIGN,
        spread=spread,
        seed=123456789,
        positions=positions,
        chart=None,
    )


# ---------------------------------------------------------------------------
# display_reading
# ---------------------------------------------------------------------------


class TestDisplayReading:
    def test_display_importable(self) -> None:
        from orbpondering.display import display_reading

        assert callable(display_reading)

    def test_display_reading_runs_with_rich(self, sample_reading) -> None:
        from orbpondering.display import display_reading

        # When Rich is installed this should not raise
        display_reading(sample_reading)


class TestRichModuleImport:
    def test_displays_when_rich_installed(self, sample_reading) -> None:
        import importlib

        from orbpondering import display as display_mod

        importlib.reload(display_mod)

        from rich import console as rich_console

        # Rich is available, no exception expected
        display_mod.display_reading(sample_reading)


# ---------------------------------------------------------------------------
# Arcana enum comparisons
# ---------------------------------------------------------------------------


class TestArcanaEnumComparison:
    def test_arcana_major_is_enum_not_string(self) -> None:
        card = Card(name="The Fool", arcana=Arcana.MAJOR, keywords=("beginnings",))
        assert card.arcana == Arcana.MAJOR
        assert card.arcana != "major"

    def test_arcana_minor_is_enum_not_string(self) -> None:
        card = Card(name="Ace of Wands", arcana=Arcana.MINOR, suit=Suit.WANDS, number=1)
        assert card.arcana == Arcana.MINOR
        assert card.arcana != "minor"

    def test_arcana_membership(self) -> None:
        assert Arcana.MAJOR in Arcana
        assert Arcana.MINOR in Arcana


# ---------------------------------------------------------------------------
# Suit symbols
# ---------------------------------------------------------------------------


class TestSuitSymbols:
    def test_wands_symbol(self) -> None:
        assert Suit.WANDS.symbol == "\u26a1"

    def test_cups_symbol(self) -> None:
        assert Suit.CUPS.symbol == "\u2617"

    def test_swords_symbol(self) -> None:
        assert Suit.SWORDS.symbol == "\u2694"

    def test_pentacles_symbol(self) -> None:
        assert Suit.PENTACLES.symbol == "\u2b50"

    def test_suit_symbols_not_empty(self) -> None:
        for suit in Suit:
            assert len(suit.symbol) > 0
            assert isinstance(suit.symbol, str)

    def test_display_uses_suit_symbols(self) -> None:
        from orbpondering.display import _get_suit_symbol

        for suit in Suit:
            symbol = _get_suit_symbol(suit)
            assert symbol == suit.symbol

    def test_get_suit_symbol_none_returns_empty(self) -> None:
        from orbpondering.display import _get_suit_symbol

        assert _get_suit_symbol(None) == ""


# ---------------------------------------------------------------------------
# House system symbols in display
# ---------------------------------------------------------------------------


class TestHouseSystemSymbols:
    def test_get_house_symbol_all_systems(self) -> None:
        from orbpondering.display import _get_house_symbol

        for hs in HouseSystem:
            symbol = _get_house_symbol(hs)
            assert isinstance(symbol, str)
            assert len(symbol) > 0

    def test_get_house_symbol_unknown_fallback(self) -> None:
        from orbpondering.display import _get_house_symbol

        # Should not raise; falls back to default
        symbol = _get_house_symbol("invalid")  # type: ignore[arg-type]
        assert isinstance(symbol, str)
