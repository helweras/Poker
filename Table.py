from Players import Player
from random import choice

class TableRabbit:
    """Класс в котором происходит полная симуляция игры
    1) Раздача флопа (3 карты)
    2) Раздача тюрна (1 карта)
    3) Раздача ривера (1 карта)
    4) Раздача карт на руки игрокам
    5) Определение победителя"""

    def __init__(self, players, hand=None, turn=None, flop=None, river=None):
        self.list_players = [Player() for _ in range(players)]  # Генерирует список игроков за столом
        self.players = players  # Колличество игроков за столом
        self.deck = [(mast, nominal) for mast in range(4)
                     for nominal in range(2, 15)]  # Генерация колоды карт
        self.turn = turn
        self.flop = flop
        self.river = river
        self.hand_fp = False
        self.canvas = [] # Список с картами выложенными на стол
        self.winner_list = []
        if hand:
            self.hand_fp = hand
            self.set_hand_first_player(hand)  # Раздача карт на руки 0-му игроку

    def set_hand_first_player(self, hand):
        """Добавляет hand в атрибут 0 - ого игрока в списке и удаляет hand из колоды"""
        for card in hand:
            self.deck.remove(card)
        self.list_players[0].hand = hand

    def card_draw(self):
        """Добавляет две случайные карты в атрибут card экземпляра класса Player
        и удаляет их из колоды(deck)"""
        flag_hand = int(bool(self.hand_fp))
        for player in self.list_players[flag_hand:]:
            player.hand = []
            for i in range(2):
                card = choice(self.deck)
                player.hand.append(card)
                self.deck.remove(card)
        self.get_players_cards()

    def flop_draw(self):
        """Раздает флоп если он задан или генерирует его случайно
        и добавляет эти карты в canvas, удаляет их из колоды"""
        if self.flop:
            for card in self.flop:
                self.deck.remove(card)
        else:
            self.flop = []
            for _ in range(3):
                card = choice(self.deck)
                self.flop.append(card)
                self.deck.remove(card)
        self.canvas.extend(self.flop)

    def turn_draw(self):
        """Раздает тюрн если он задаи или генерирует его случайно, добавляет его в canvas и удаляет из колоды"""
        if self.turn:
            for card in self.turn:
                self.deck.remove(card)
        else:
            self.turn = []
            card = choice(self.deck)
            self.turn.append(card)
            self.deck.remove(card)
        self.canvas.extend(self.turn)

    def river_draw(self):
        """Раздает ривер если он задаи или генерирует его случайно, добавляет его в canvas и удаляет из колоды"""
        if self.river:
            for card in self.river:
                self.deck.remove(card)
        else:
            self.river = []
            card = choice(self.deck)
            self.river.append(card)
            self.deck.remove(card)
        self.canvas.extend(self.river)

    def get_players_cards(self):
        """Вызывает метод get_cards у игроков в списке get_cards"""
        for pl in self.list_players:
            pl.get_cards(self.canvas)

    def determ_winner(self):
        """Функция определяет победителя
        Возвращает список с объектами класса Player с наибольшим коэфициентом"""
        compare_player = self.list_players[0]
        winner_list = [compare_player]
        for player in self.list_players[1:]:
            if player.cf_comb > winner_list[-1].cf_comb:
                winner_list = [player]
            elif player.cf_comb == winner_list[-1].cf_comb:
                winner_list.append(player)
        if len(winner_list) > 1:
            return self.final_win(winner_list)
        self.winner_list = winner_list
        return winner_list

    def final_win(self, winner_list):
        """Метод сравнивает игроков в списке winner_list и возвращает список с победителями"""
        winner_list_final = [winner_list[0]]  # Добавляем первого игрока в список для сравнения его с остальными
        check = [card[-1] for card in
                 winner_list[0].play_card]  # создаем отсортированный список из номиналов карт для для первого игрока
        for pl in winner_list[1:]:  # Начинаем сравнение со второго игрока в списке
            play_card = [card[-1] for card in pl.play_card]  # создаем отсортированный список из номиналов карт
            if play_card > check:  # Если список из номиналов карт другого игрока логически больше
                check = play_card  # Заменяем сравниваемый список на другой наибольший
                winner_list_final = [pl]  # Новый игрок в списке с наибольшим списком
            elif play_card == check:
                winner_list_final.append(pl)  # Добавляем игрока в список не удаляя предыдущего
        self.winner_list = winner_list_final
        return winner_list_final

    def full_play(self):
        """Метод симулирут полный цикл игры
        Вызовы метоов строго определены"""
        self.flop_draw()
        self.turn_draw()
        self.river_draw()
        self.card_draw()
        self.determ_winner()

    def get_winner_determ_player(self):
        """Возвращает True если 0-й игрок в списке победителей"""
        self.full_play()
        determ_pl = self.list_players[0]
        return determ_pl in self.winner_list


