from math import sqrt
from random import choice
from Players import Player
from Table import Table
import time

def test_quads(it: int):
    for i in range(it):
        table = Table(players=8)
        original_deck = table.gen_deck_of_cards()
        table.card_draw(original_deck)
        table.flop_draw(original_deck)
        table.turn_draw(original_deck)
        table.river_draw(original_deck)

def test_quads_new(it: int):
    for i in range(it):
        table = Table(players=4)
        original_deck = table.gen_deck_of_cards()
        table.card_draw(original_deck)
        table.flop_draw(original_deck)
        table.turn_draw(original_deck)
        table.river_draw(original_deck)

    return




class StudentTest:
    def __init__(self, param1, param2):
        self.param_list = (param1, param2)
        self.data = [[], []]
        self.m_list = []
        self.sd_list = []
        self.n = None

    def get_sd(self, param: list):
        m = sum(param) / len(param)
        print(m, '---- математическое ожидание')
        self.m_list.append(m)
        dis = sum(list(map(lambda x: pow((x - m), 2), param))) / (len(param) - 1)
        sd = sqrt(dis)
        print(sd, '--- стандартное отклонение')
        print()
        self.sd_list.append(sd)
        return sd

    def get_se(self):
        se = sqrt((self.sd_list[0] * self.sd_list[0]) / self.n + (self.sd_list[1] * self.sd_list[1]) / self.n)
        return se

    def get_t(self):
        s_m = sorted(self.m_list)
        t = (s_m[1] - s_m[0]) / self.get_se()
        return t

    def test(self, fun_list, param, it):
        try:
            start = time.perf_counter()
            fun_list[0](param)
            stop = time.perf_counter()
            print(f"Первая функция {it + 1}) {stop - start}")
            print()
            self.data[0].append(stop - start)
        except TypeError:
            start = time.perf_counter()
            fun_list[0]()
            stop = time.perf_counter()
            self.data[0].append(stop - start)
        try:
            start = time.perf_counter()
            fun_list[1](param)
            stop = time.perf_counter()
            print(f"Вторая функция {it + 1}) {stop - start}")
            print()
            self.data[1].append(stop - start)
        except TypeError:
            start = time.perf_counter()
            fun_list[1]()
            stop = time.perf_counter()
            self.data[1].append(stop - start)

        # start = time.perf_counter()
        #
        # for fun in range(len(fun_list)):
        #     try:
        #         for i in range(it):
        #             fun_list[fun](param)
        #     except TypeError:
        #         for i in range(it):
        #             fun_list[fun]()
        # stop = time.perf_counter()
        # return stop - start

    def start_test(self, itr=5):
        self.n = itr
        for it in range(itr):

            self.test(self.param_list, 10000, it)
        for data in self.data:
            self.get_sd(data)
        print("Среднее время работы 1 и 2 функции")
        print(*self.m_list)
        self.get_se()
        print(self.m_list[0] - self.m_list[1] ,'--- Разница среднего времени работы')
        print("T-value = ", self.get_t())


t_test = StudentTest(test_quads, test_quads_new)
t_test.start_test(20)
