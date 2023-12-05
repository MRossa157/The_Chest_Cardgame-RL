from models import Deck
import pytest


def test_deck_fill_deck():
    deck = Deck()
    unique_cards = set(deck.cards)
    assert len(unique_cards) == 52
    


if __name__ == '__main__':
    pytest.main()