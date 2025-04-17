from Players import Player
from random import choice


class Table:

    def __init__(self, players: int):
        self.list_players = [Player() for _ in range(players)]  # Генерирует список игроков за столом
        self.turn = []
        self.river = []
        self.flop = []
        self.deck = [[mast, nominal] for mast in range(4)
                     for nominal in range(2, 15)]

    def set_turn(self, turn):
        self.turn = turn

    def set_flop(self, flop):
        self.flop = flop

    def set_river(self, river):
        self.river = river

    def card_draw(self):
        """Добавляет две случайные карты в атрибут card экземпляра класса Player
        и удаляет их из колоды(list_deck)"""
        for player in self.list_players:
            for i in range(2):
                card = choice(self.deck)
                player.hand.append(card)
                self.deck.remove(card)

    def flop_draw(self):
        for _ in range(3):
            card = choice(self.deck)
            self.flop.append(card)
            self.deck.remove(card)

    def turn_draw(self):
        card = choice(self.deck)
        self.turn.append(card)
        self.turn.extend(self.flop)
        self.deck.remove(card)

    def river_draw(self):
        card = choice(self.deck)
        self.river.append(card)
        self.river.extend(self.turn)
        self.deck.remove(card)
        self.get_players_cards()

    def get_players_cards(self):
        for pl in self.list_players:
            pl.get_cards(self.river)

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
        return winner_list

    @staticmethod
    def final_win(winner_list):
        winner_list_final = [winner_list[0]]
        check = [i[-1] for i in winner_list[0].play_card]
        for pl in winner_list[1:]:
            play_card = [i[-1] for i in pl.play_card]
            if play_card > check:
                check = play_card
                winner_list_final = [pl]
            elif play_card == check:
                winner_list_final.append(pl)
        return winner_list_final


class TableRabbit(Table):
    """Тестовый стол наследванный от предыдущего"""

    def __init__(self, players, hand=None, turn=None, flop=None, river=None):
        super().__init__(players)
        self.deck = [(mast, nominal) for mast in range(4)
                     for nominal in range(2, 15)]
        self.turn = turn
        self.flop = flop
        self.river = river
        self.hand_fp = False
        if hand:
            self.hand_fp = hand
            self.set_hand_first_player(hand)

    def set_hand_first_player(self, hand):
        """Добавляет hand в атрибут первого игрока в списке и удаляет hand из колоды"""
        for card in hand:
            self.deck.remove(card)
        self.list_players[0].hand = hand

    # def gen_deck_of_cards(self):
    #     self.deck = [[mast, nominal] for mast in range(4)
    #             for nominal in range(2, 15)]

    def card_draw(self):
        """Добавляет две случайные карты в атрибут card экземпляра класса Player
        и удаляет их из колоды(list_deck)"""
        flag_hand = int(bool(self.hand_fp))
        for player in self.list_players[flag_hand:]:
            for i in range(2):
                card = choice(self.deck)
                player.hand.append(card)
                self.deck.remove(card)

    def flop_draw(self):
        if self.flop:
            for card in self.flop:
                self.deck.remove(card)
        else:
            self.flop = []
            for _ in range(3):
                card = choice(self.deck)
                self.flop.append(card)
                self.deck.remove(card)

    def turn_draw(self):
        if self.turn:
            for card in self.turn:
                self.deck.remove(card)
        else:
            self.turn = []
            card = choice(self.deck)
            self.turn.append(card)
            self.deck.remove(card)
        self.turn.extend(self.flop)

    def river_draw(self):
        if self.river:
            for card in self.river:
                self.deck.remove(card)
        else:
            self.river = []
            card = choice(self.deck)
            self.river.append(card)
            self.deck.remove(card)
        self.river.extend(self.turn)
        self.get_players_cards()

    def get_players_cards(self):
        for pl in self.list_players:
            pl.get_cards(self.river)

    def full_play(self):
        self.flop_draw()
        print(len(self.deck))
        self.turn_draw()
        print(len(self.deck))
        self.river_draw()
        print(len(self.deck))
        self.card_draw()
        print(len(self.deck))
