from orbpondering.cards import DECK, MAJOR_ARCANA, MINOR_ARCANA
from orbpondering.constants import Arcana, Suit


def test_deck_size() -> None:
    assert len(DECK) == 78


def test_major_arcana_count() -> None:
    assert len(MAJOR_ARCANA) == 22


def test_minor_arcana_count() -> None:
    assert len(MINOR_ARCANA) == 56


def test_all_cards_unique() -> None:
    names = [card.name for card in DECK]
    assert len(names) == len(set(names))


def test_minor_arcana_has_suit() -> None:
    for card in MINOR_ARCANA:
        assert card.suit is not None
        assert card.number is not None


def test_major_arcana_has_no_suit() -> None:
    for card in MAJOR_ARCANA:
        assert card.suit is None
        assert card.arcana == Arcana.MAJOR


def test_four_suits() -> None:
    suits_in_deck = {
        card.suit for card in MINOR_ARCANA if card.suit is not None
    }
    assert suits_in_deck == set(Suit)


def test_card_keywords() -> None:
    for card in DECK:
        assert len(card.keywords) > 0
