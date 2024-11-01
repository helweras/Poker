from Rules import CheckRules


class Player:

    def __init__(self):
        self.hand = []
        self.cards = []  # 7 карт 5 общих и рука
        self.play_card = None

    def get_cards(self, table_river: list):
        self.cards = self.hand + table_river
        self.play_card = sorted(self.cards, key=lambda cards: cards[-1])

    @staticmethod
    def check_comb(pl_card):
        if CheckRules.quads(pl_card):
            return CheckRules.quads(pl_card)
        elif CheckRules.street_flash(pl_card):
            return CheckRules.street_flash(pl_card)
        elif CheckRules.full_house(pl_card):
            return CheckRules.full_house(pl_card)
        elif CheckRules.flash(pl_card):
            return CheckRules.flash(pl_card)
        elif CheckRules.street(pl_card):
            return CheckRules.street(pl_card)
        elif CheckRules.triple(pl_card):
            return CheckRules.triple(pl_card)
        elif CheckRules.double_or_double(pl_card):
            return CheckRules.double_or_double(pl_card)
        elif CheckRules.double(pl_card):
            return CheckRules.double(pl_card)
        else:
            return CheckRules.higher_card(pl_card)

    @staticmethod
    def check_comb_new(pl_card):
        for comb in CheckRules.get_comb():
            cf = comb(pl_card)
            if cf:
                return cf
        #  CheckRules.triple(self.play_card)
        # return CheckRules.double(self.play_card)
        # return CheckRules.full_house(self.play_card)
        # return CheckRules.flash(self.play_card)
        # return CheckRules.double_or_double(self.play_card)
        # return CheckRules.street(self.play_card)
        # return CheckRules.street_flash(self.play_card)
        # return CheckRules.higher_card(self.play_card)
