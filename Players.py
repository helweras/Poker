class Player:
    """Класс описывающий игрока за столом который сам определяет какая у него комбинация
    Все методы определяющие комбинации добавляют в атрибут play_card 5 карт учавствующих в комбинации"""

    def __init__(self):
        self.hand = []
        self.cards = []  # 7 карт 5 общих и рука
        self.play_card = []  # 5 карт участвующие в комбинации появляются после выполнения одного из метода определения комбинаций
        self.cf_comb = 1

    def get_cards(self, table_river: list):
        """Добавляет в атрибут cards 7 карт стол + руку"""
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

    def check_comb_new(self, cards: list):
        for comb in self.get_comb():
            cf = comb(self.cards)
            if cf:
                self.cf_comb = cf
                return cf

    def quads(self, pl_cards: list):
        """Функция ищет карэ и возвращает его коэф"""
        count_item = {key: [] for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]].append(card)
        for key in count_item:
            if len(count_item[key]) == 4:
                pl_card = []
                for c in self.cards:
                    if c not in count_item[key]:
                        pl_card.append(c)
                pl_card = sorted(pl_card, key=lambda cards: cards[-1])
                self.play_card = count_item[key]
                self.play_card.append(pl_card[-1])
                return 25
        return False

    def triple(self, pl_cards: list):
        """Метод опредялющий наличия сета"""
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
        """Метод опредялющий наличия пары"""
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
        """Метод опредялющий наличия фулл-хауса"""
        cond_classic = self.double(pl_cards) * self.triple(pl_cards)
        cond_isk = self.triple_or_triple(pl_cards)
        if cond_classic or cond_isk:
            if cond_classic:
                self.play_card = self.triple_full(pl_cards) + self.double_full(pl_cards)
            else:
                self.play_card = self.triple_or_triple_full(pl_cards)
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
                sort_list = sorted(count_mast[key], key=lambda x: x[-1], reverse=True)
                for ind in range(5):
                    self.play_card.append(sort_list[ind])
                return count_mast[key]
        return False

    def double_or_double(self, pl_cards: list):
        """Метод опредялющий наличия двух пар"""
        double = 0
        self.play_card = []
        sort_pl_cards = sorted(pl_cards, key=lambda x: x[-1], reverse=True)
        count_item = {key: [] for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]].append(card)
        for key in list(count_item.keys())[::-1]:
            if len(count_item[key]) == 2:
                double += 5
                self.play_card += count_item[key]
                if double == 10:
                    for c in sort_pl_cards:
                        if c not in self.play_card:
                            self.play_card.append(c)
                    self.play_card = self.play_card[:-2]
                    return 10
        return False

    def triple_or_triple(self, pl_cards: list):
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

    def street(self, pl_cards: list):
        """Метод опредялющий наличия стрита
        Учавствует в методе определения стрит-флэша"""
        count_item = {key: [] for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]].append(card)
        check = []
        check_isk = []
        isk = (5, 4, 3, 2, 14)
        for card in list(count_item.keys())[::-1]:
            if count_item[card]:
                check.append(count_item[card][0])
                if len(check) == 5:
                    self.play_card = check
                    return 16
                    # return check
            else:
                check = []
        for key in isk:
            if count_item[key]:
                check_isk.append(count_item[key][0])

        if len(check_isk) == 5:
            self.play_card = check_isk
            return 16
            # return sorted(list(chain.from_iterable(check_isk)), key=lambda x: x[-1])[::-1]
        else:
            return False

    def street_flash(self, pl_cards: list):
        """Возвращает коэф. стрит - флэша если он найден
        Возвращает коэф. флеша если найден флэш и не найден стрит"""
        found_flash = self.flash(pl_cards)
        if type(found_flash) is list:  # Если найден флэш
            if self.street(found_flash):  # Если во флэше найден стрит
                return 33
            else:
                return 17
        else:
            return False

    def higher_card(self, pl_cards: list):
        """Метод опредялющий наличия старшей карты"""
        self.play_card = sorted(pl_cards, key=lambda c: c[-1], reverse=True)[:-2]
        return 1
        # return sorted(pl_card, key=lambda c: c[-1])[2:]

    def get_comb(self):
        return (
            self.quads, self.street_flash, self.full_house, self.street, self.triple, self.double_or_double,
            self.double, self.higher_card)

    def triple_full(self, pl_cards):
        """Метод опредялющий наличия сета и возвращающий список с картами для сета
        Только для метода full_house"""
        count_item = {key: [] for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]].append(card)
        for key in list(count_item.keys())[::-1]:
            if len(count_item[key]) == 3:
                return count_item[key]

    def double_full(self, pl_cards: list):
        """Метод опредялющий наличия сета и возвращающий список с картами для пары
        Только для метода full_house"""
        count_item = {key: [] for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]].append(card)
        for key in list(count_item.keys())[::-1]:
            if len(count_item[key]) == 2:
                return count_item[key]

    def triple_or_triple_full(self, pl_cards):
        resp_list = []
        count_item = {key: [] for key in range(2, 15)}
        for card in pl_cards:
            count_item[card[-1]].append(card)
        for key in list(count_item.keys())[::-1]:
            if len(count_item[key]) == 3:
                resp_list += count_item[key]
        resp_list.sort(key=lambda x: x[-1], reverse=True)
        return resp_list[:-1]
