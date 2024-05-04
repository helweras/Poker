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
        if CheckRules.quads(self.play_card):
            return CheckRules.quads(self.play_card), 'kare'
        elif CheckRules.street_flash(self.play_card):
            return CheckRules.street_flash(self.play_card), 'street-flash'
        elif CheckRules.full_house(self.play_card):
            return CheckRules.full_house(self.play_card), 'full-house'
        elif CheckRules.flash(self.play_card):
            return CheckRules.flash(self.play_card), 'flash'
        elif CheckRules.street(self.play_card):
            return CheckRules.street(self.play_card), 'street'
        elif CheckRules.triple(self.play_card):
            return CheckRules.triple(self.play_card), 'set'
        elif CheckRules.double_or_double(self.play_card):
            return CheckRules.double_or_double(self.play_card), '2 double'
        elif CheckRules.double(self.play_card):
            return CheckRules.double(self.play_card), 'double'
        else:
            return CheckRules.higher_card(self.play_card), 'хуй'
        #  CheckRules.triple(self.play_card)
        # return CheckRules.double(self.play_card)
        # return CheckRules.full_house(self.play_card)
        # return CheckRules.flash(self.play_card)
        # return CheckRules.double_or_double(self.play_card)
        # return CheckRules.street(self.play_card)
        # return CheckRules.street_flash(self.play_card)
        # return CheckRules.higher_card(self.play_card)