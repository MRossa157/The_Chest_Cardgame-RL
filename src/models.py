from enum import Enum, auto
from typing import List
import numpy as np
from constants import DEFAULT_NUMBERS_OF_CARDS_AT_START


class Suit(Enum):
    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()
    SPADES = auto()

    def __str__(self):
        return self.name


class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self):
        if self.value <= 10:
            return str(self.value)
        return self.name


class Card():
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank.name} of {self.suit.name}"
    
    def __eq__(self, other):
        if not isinstance(other, (Card)):
            raise TypeError("Операнд справа должен иметь тип Card")
        
        return self.rank == other.rank and self.suit == other.suit
    
    def __ne__(self, other):
        if not isinstance(other, (Card)):
            raise TypeError("Операнд справа должен иметь тип Card")
        
        return self.rank != other.rank and self.suit != other.suit
    
    def __hash__(self):
        return hash((self.rank, self.suit))


class Player():
    def __init__(self, name: str = '') -> None:
        self.name = name
        self.cards_on_hand: List[Card] = []
        self.chests = 0
        

class Deck():
    def __init__(self) -> None:
        self.cards: List[Card] = []

        self.__fill_deck()

    def __fill_deck(self):
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank=rank, suit=suit))

        np.random.shuffle(self.cards)


class GameBoard():
    def __init__(self, deck: Deck, players: List[Player]) -> None:
        self.deck = deck
        self.players = players
        self.current_player = self.players[np.random.randint(0, len(self.players))]
        self.is_switch_player = False

        # Именуем пользователей у которых нет имени
        for idx, player in enumerate(self.players):
            if player.name == '':
                player.name = f'Player {idx}'

    def __deal_cards_to_players(self):
        for _ in range(DEFAULT_NUMBERS_OF_CARDS_AT_START):
            for player in self.players:
                player.cards_on_hand.append(self.deck.cards.pop(0))

    def ask_for_card(self, from_player: Player, to_player: Player, asked_card_rank: Rank):
        to_player_cards_only_ranks = [card.rank for card in to_player.cards_on_hand]

        # Есть ли вообще эта карта у to_player
        if asked_card_rank in to_player_cards_only_ranks:
            
            if to_player_cards_only_ranks.count(asked_card_rank) > 1:
    
                # Передаем from_player всю пачку
                cards_idx = []
                for idx, card in enumerate(to_player_cards_only_ranks):
                    if asked_card_rank == card:
                        cards_idx.append(idx)
                        
            else:
                card_idx = to_player_cards_only_ranks.index(asked_card_rank)
                from_player.cards_on_hand.append(
                    to_player.cards_on_hand.pop(card_idx))
                
        # Если asked_card_rank нет, берём из колоды верхнюю карту и передаем ход
        else:
            from_player.cards_on_hand.append(self.deck.cards.pop(0))
            self.is_switch_player = True

        self.update_board()

    def _next_active_player(self):
        current_player_idx = self.players.index(self.current_player)
        if current_player_idx == len(self.players) - 1:
            next_player_idx = 0
        else:
            next_player_idx = current_player_idx + 1

        next_player = self.players[next_player_idx]

        print(f'Ход переходит игроку {next_player.name}!')
        self.current_player = next_player

    def announce_winner(self, player: Player):
        print(f'Победил игрок {player.name}! Он собрал {player.chests} сундучков!')

    def display_game_status(self, ):
        print(f'Текущий ход игрока: {self.current_player}')
    
    def end_game(self, ):
        winner = max(self.players, key=lambda player: player.chests)
        self.announce_winner(winner)

    def update_board(self):
        # Проверка условия окончания игры (если колода кончилась)
        if self.deck.cards == []:
            self.end_game()
            return

        # Вывод текущего состояния игры
        self.display_game_status()
        
        if self.is_switch_player:
            self.is_switch_player = False
            self._next_active_player()

    def start_game(self):
        self.__deal_cards_to_players()


if __name__ == "__main__":  
    deck = Deck()

    player1 = Player(name='Егорка')
    player2 = Player()

    game = GameBoard(deck, [player1, player2])
    game.start_game()

    player1.chests = 3
    player2.chests = 2

    game.deck.cards = []
            
    game.update_board()


