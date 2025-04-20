from Table import TableRabbit


class Room:
    def __init__(self, table: TableRabbit, iter=6500):
        self.table = table
        self.count_win = 0
        self.iter = iter
        self.players = 8
        self.hand = None
        self.flop = None
        self.turn = None
        self.river = None

    def up_count(self):
        for i in range(self.iter):
            table = self.reset_table()
            self.count_win += table.play()

    def reset_table(self):
        self.players = self.table.players
        self.hand = self.table.hand_fp
        self.flop = self.table.flop
        if self.turn:
            self.turn = [self.table.turn[0]]
        else:
            self.turn = self.table.turn
        if self.river:
            self.river = [self.table.river[0]]
        else:
            self.river = self.table.river
        return TableRabbit(players=self.players, hand=self.hand, flop=self.flop, turn=self.turn, river=self.river)

    def chans(self):
        print(self.count_win)
        return (self.count_win / self.iter) * 100
