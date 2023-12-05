import pytest
from models import GameBoard, Deck, Player, Card, Rank, Suit

def test_ask_for_card():
    deck = Deck()
    player1 = Player()
    player2 = Player()
    game = GameBoard(deck, [player1, player2])
    
    game.start_game()
    
    current_player = game.current_player
    
    player1.cards_on_hand = [Card(rank=Rank.TEN, suit=Suit.HEARTS)]
    player2.cards_on_hand = [Card(rank=Rank.TEN, suit=Suit.CLUBS)]
    
    game.ask_for_card(player1, player2, Rank.TEN)
    
    assert Card(rank=Rank.TEN, suit=Suit.CLUBS) in player1.cards_on_hand
    assert Card(rank=Rank.TEN, suit=Suit.CLUBS) not in player2.cards_on_hand
    
    assert len(player1.cards_on_hand) == 2
    assert len(player2.cards_on_hand) == 0

    # Т.к. мы забрали карту, то ход не должен передаваться
    assert game.current_player == current_player
    
def test_update_board():
    deck = Deck()

    player1 = Player(name='Егорка')
    player2 = Player()

    game = GameBoard(deck, [player1, player2])
    game.start_game()

    player1.chests = 3
    player2.chests = 2

    game.deck.cards = []
            
    game.update_board()
    
    assert isinstance(game.winner, Player) == True
    assert game.winner == player1
    
if __name__ == '__main__':
    pytest.main()
