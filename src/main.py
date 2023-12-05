from models import *


if __name__ == "__main__":  
    deck = Deck()

    player1 = Player(name='Егорка')
    player2 = Player()

    game = GameBoard(deck, [player1, player2])
    
    game.start_game()