from Players import Player
from random import choice


class Table:

    def __init__(self, players: int):
        self.list_players = [Player() for _ in range(players)]  # Генерирует список игроков за столом
        self.turn = []
        self.river = []
        self.flop = []

    @staticmethod
    def gen_deck_of_cards():
        '''Генерация колоды карт'''
        return [[mast, nominal] for mast in range(4)
                for nominal in range(2, 15)]

    def card_draw(self, list_deck):
        '''Добавляет две случайные карты в атрибут card экземпляра класса Player
        и удаляет их из колоды(list_deck)'''
        for player in self.list_players:
            for i in range(2):
                card = choice(list_deck)
                player.hand.append(card)
                list_deck.remove(card)

    def flop_draw(self, deck: list):
        for _ in range(3):
            card = choice(deck)
            self.flop.append(card)
            deck.remove(card)

    def turn_draw(self, deck: list):
        card = choice(deck)
        self.turn.append(card)
        self.turn.extend(self.flop)
        deck.remove(card)

    def river_draw(self, deck: list):
        card = choice(deck)
        self.river.append(card)
        self.river.extend(self.turn)
        deck.remove(card)


