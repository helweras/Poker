from Table import TableRabbit


class Room:
    """Класс, который симулирует необходимое количество игр и считает вероятность 0-го игрока не проиграть
    table - экземпляр класса стола TableRabbit
    count_games - количество игр для симуляции"""
    def __init__(self, table: TableRabbit, count_games=3000):

        self.table = table
        self.count_win = 0
        self.count_games = count_games
        self.players = 8
        self.hand = None
        self.flop = None
        self.turn = None
        self.river = None
        self.rules = {1: 'старшая карта',
         5: 'пара',
         10: '2 пары',
         15: 'сет',
         16: 'стрит',
         17: 'флэш',
         20: 'фулл-хаус',
         25: 'карэ',
         33: 'стрит-флэш'
         }
        self.count_comb = self.get_zero_count_comb()

    def get_zero_count_comb(self):
        count_comb = {}
        for key in self.rules.values():
            count_comb[key] = 0
        return count_comb

    def set_zero_count_comb(self):
        for key in self.count_comb:
            self.count_comb[key] = 0


    def up_count(self):
        """Метод увеличивает значение count_win на 1 если 0-й игрок оказался в списке победителей"""
        try:
            for i in range(self.count_games):
                table = self.reset_table()
                main_player = table.get_winner_determ_player()
                if main_player:
                    self.count_comb[self.rules[main_player.cf_comb]] += 1
                    self.count_win += 1
        except Exception as e:
            print(e, 'up_count')

    def get_string_count_comb(self):
        string_count = ''
        for key, val in sorted(self.count_comb.items(), key=lambda x: x[1], reverse=True):
            string_count += f'{key} ------ {round((val / self.count_games) * 100, 2)}\n'
        return string_count


    def reset_table(self):
        """Метод возвращает TableRabbit с исходными настройками"""
        self.players = self.table.players
        self.hand = self.table.hand_fp
        self.flop = self.table.flop
        self.turn = self.table.turn
        self.river = self.table.river
        return TableRabbit(players=self.players, hand=self.hand, flop=self.flop, turn=self.turn, river=self.river)

    def chans(self):
        """Метод возвращает процент побед 0-го игрока"""
        return round((self.count_win / self.count_games) * 100, 2)



