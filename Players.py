import numpy as np
from Rules import CheckRules


class Player:

    def __init__(self):
        self.hand = []
        self.cards = []  # 7 карт 5 общих и рука
        self.play_card = None

    def get_cards(self, table_river: list):
        self.cards = self.hand + table_river
        self.play_card = sorted(self.cards, key=lambda cards: cards[-1])

    def check_comb(self):
        return CheckRules.quads(self.play_card)
