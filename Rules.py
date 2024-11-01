from itertools import chain


class CheckRules:
    rules = {'старшая карта': 1,
             'пара': 5,
             '2 пары': 10,
             'сет': 15,
             'стрит': 16,
             'флэш': 17,
             'фулл-хаус': 20,
             'карэ': 25,
             'стрит-флэш': 33
             }

    @staticmethod
    def quads(pl_cards: list):
        count_item = {key: 0 for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]] += 1
        for key in count_item:
            if count_item[key] == 4:
                return 25
        return False

    @staticmethod
    def triple(pl_cards: list):
        count_item = {key: 0 for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]] += 1
        for key in list(count_item.keys())[::-1]:
            if count_item[key] == 3:
                return 15
        return False

    @staticmethod
    def double(pl_cards: list):
        count_item = {key: 0 for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]] += 1
        for key in list(count_item.keys())[::-1]:
            if count_item[key] == 2:
                return 5
        return False

    @classmethod
    def full_house(cls, pl_cards: list):
        if cls.double(pl_cards) * cls.triple(pl_cards) + cls.triple_or_triple(pl_cards):
            return 20
        else:
            return False

    @staticmethod
    def flash(pl_cards):
        count_mast = {key: [] for key in range(4)}
        for card in pl_cards:
            count_mast[card[0]].append(card)
        for key in count_mast:
            if len(count_mast[key]) >= 5:
                return 17, count_mast[key]
        return []

    @staticmethod
    def double_or_double(pl_cards):
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

    @staticmethod
    def triple_or_triple(pl_cards):
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

    @staticmethod
    def street(pl_cards):
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
                    return check
            else:
                check = []
        for key in isk:
            if count_item[key]:
                check_isk.append(count_item[key])

        if len(check_isk) == 5:
            return sorted(list(chain.from_iterable(check_isk)), key=lambda x: x[-1])[::-1]
        else:
            return False

    @classmethod
    def street_flash(cls, pl_cards):
        if type(cls.flash(pl_cards)) is tuple:
            if cls.street(cls.flash(pl_cards)[-1]):
                return 33
            else:
                return False
        else:
            return False

    @staticmethod
    def higher_card(pl_card):
        return sorted(pl_card, key=lambda c: c[-1])[2:]

    @classmethod
    def get_comb(cls):
        return (
            cls.quads, cls.street_flash, cls.full_house, cls.flash, cls.street, cls.triple, cls.double_or_double,
            cls.double, cls.higher_card)
