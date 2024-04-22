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
                player.card.append(card)
                list_deck.remove(card)
