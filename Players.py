

class Player:

    def __init__(self):
        self.hand = []
        self.cards = []  # 7 карт 5 общих и рука
        self.play_card = []
        self.cf_comb = 1

    def get_cards(self, table_river: list):
        self.cards = self.hand + table_river

    # @staticmethod
    # def check_comb(pl_card):
    #     if CheckRules.quads(pl_card):
    #         return CheckRules.quads(pl_card)
    #     elif CheckRules.street_flash(pl_card):
    #         return CheckRules.street_flash(pl_card)
    #     elif CheckRules.full_house(pl_card):
    #         return CheckRules.full_house(pl_card)
    #     elif CheckRules.flash(pl_card):
    #         return CheckRules.flash(pl_card)
    #     elif CheckRules.street(pl_card):
    #         return CheckRules.street(pl_card)
    #     elif CheckRules.triple(pl_card):
    #         return CheckRules.triple(pl_card)
    #     elif CheckRules.double_or_double(pl_card):
    #         return CheckRules.double_or_double(pl_card)
    #     elif CheckRules.double(pl_card):
    #         return CheckRules.double(pl_card)
    #     else:
    #         return CheckRules.higher_card(pl_card)

    def check_comb_new(self, pl_cards:list):
        for comb in self.get_comb():
            cf = comb(pl_cards)
            if cf:
                self.cf_comb = cf
                return cf

    def get_play_card(self):
        pass

    def quads(self, pl_cards: list):
        count_item = {key: [] for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]].append(card)
        for key in count_item:
            if len(count_item[key]) == 4:
                pl_card = []
                for c in self.cards:
                    if c not in count_item[key]:
                        pl_card.append(c)
                pl_card =  sorted(pl_card, key=lambda cards: cards[-1])
                self.play_card = count_item[key]
                self.play_card.append(pl_card[-1])
                return 25
        return False

    def triple(self, pl_cards: list):
        count_item = {key: [] for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]].append(card)
        for key in list(count_item.keys())[::-1]:
            if len(count_item[key]) == 3:
                pl_card = []
                for c in self.cards:
                    if c not in count_item[key]:
                        pl_card.append(c)
                pl_card = sorted(pl_card, key=lambda cards: cards[-1], reverse=True)
                self.play_card = count_item[key]
                self.play_card.extend(pl_card[:2])
                return 15
        return False

    def double(self, pl_cards: list):
        count_item = {key: [] for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]].append(card)
        for key in list(count_item.keys())[::-1]:
            if len(count_item[key]) == 2:
                pl_card = []
                for c in self.cards:
                    if c not in count_item[key]:
                        pl_card.append(c)
                pl_card = sorted(pl_card, key=lambda cards: cards[-1], reverse=True)
                self.play_card = count_item[key]
                self.play_card.extend(pl_card[:3])
                return 5
        return False

    def full_house(self, pl_cards: list):
        if self.double(pl_cards) * self.triple(pl_cards) + self.triple_or_triple(pl_cards):
            self.play_card = []
            return 20
        else:
            return False

    def flash(self, pl_cards: list):
        """Возвращает список какрт одной масти если найден флэш
        Используется в функции street_flash"""
        count_mast = {key: [] for key in range(4)}
        for card in pl_cards:
            count_mast[card[0]].append(card)
        for key in count_mast:
            if len(count_mast[key]) >= 5:
                return count_mast[key]
        return False

    def double_or_double(self, pl_cards:list):
        double = 0
        count_item = {key: 0 for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]] += 1
        for key in list(count_item.keys())[::-1]:
            if count_item[key] == 2:
                double += 5
                if double == 10:
                    return double
        return False

    def triple_or_triple(self, pl_cards:list):
        """Определяет кобимнацию Сет и исключает два Сета
        Возвращает весовой коэф Сета если он найден и False если обнаружено два Сета"""
        triple = 0
        count_item = {key: 0 for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]] += 1
        for key in list(count_item.keys())[::-1]:
            if count_item[key] == 3:
                triple += 5
        if triple == 10:
            return triple
        else:
            return False

    def street(self, pl_cards:list):
        count_item = {key: [] for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]].append(card)
        check = []
        check_isk = []
        isk = (2, 3, 4, 5, 14)
        for card in list(count_item.keys())[::-1]:
            if count_item[card]:
                check.append(count_item[card])
                if len(check) == 5:
                    return 16
                    # return check
            else:
                check = []
        for key in isk:
            if count_item[key]:
                check_isk.append(count_item[key])

        if len(check_isk) == 5:
            return 16
            # return sorted(list(chain.from_iterable(check_isk)), key=lambda x: x[-1])[::-1]
        else:
            return False

    def street_flash(self, pl_cards:list):
        """Возвращает коэф. стрит - флэша если он найден
        Возвращает коэф. флеша если найден флэш и не найден стрит"""
        if type(self.flash(pl_cards)) is list:  # Если найден флэш
            if self.street(self.flash(pl_cards)):  # Если во флэше найден стрит
                return 33
            else:
                return 17
        else:
            return False

    def higher_card(self, pl_cards:list):
        return 1
        # return sorted(pl_card, key=lambda c: c[-1])[2:]

    def get_comb(self):
        return (
            self.quads, self.street_flash, self.full_house, self.street, self.triple, self.double_or_double,
            self.double, self.higher_card)
