from Table import TableRabbit


class Room:
    """Класс который симулирует необходимое колличество игр и считает вероятность 0-го игрока не проиграть
    table - экземпляр класса стола TableRabbit
    count_games - колличество игр для симуляции"""
    def __init__(self, table: TableRabbit, count_games=6500):

        self.table = table
        self.count_win = 0
        self.count_games = count_games
        self.players = 8
        self.hand = None
        self.flop = None
        self.turn = None
        self.river = None

    def up_count(self):
        """Метод увеличивает значение count_win на 1 если 0-й игрок оказался в списке победителей"""
        for i in range(self.count_games):
            table = self.reset_table()
            self.count_win += table.get_winner_determ_player()



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



