class CheckRules:
    rules = {'старшая карта': 1,
             'пара': 2,
             '2 пары': 3,
             'сет': 4,
             'стрит': 5,
             'флэш': 6,
             'фулл-хаус': 7,
             'карэ': 8,
             'стрит-флэш': 9
             }

    @staticmethod
    def quads(pl_cards: list):
        count_item = {key: 0 for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]] += 1
        for key in count_item:
            if count_item[key] == 4:
                return True
        return False

