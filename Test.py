from math import sqrt
from random import choice
from Players import Player
import time

fun_new = Player.check_comb_new
fun_old = Player.check_comb


def dec():
    return [[mast, nominal] for mast in range(4)
            for nominal in range(2, 15)]


def gen_7_card(deck_t):
    cards = []
    for i in range(7):
        card = choice(deck_t)
        cards.append(card)
        deck_t.remove(card)
    return cards


class StudentTest:
    def __init__(self, param1, param2):
        self.param_list = (param1, param2)
        self.data = [[], []]
        self.m_list = []
        self.sd_list = []
        self.n = None

    def get_sd(self, param: list):
        m = sum(param) / len(param)
        print(m)
        self.m_list.append(m)
        dis = sum(list(map(lambda x: pow((x - m), 2), param))) / (len(param) - 1)
        sd = sqrt(dis)
        print(sd)
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

    def test(self, fun_list, cards: list, it):
        try:
            start = time.perf_counter()
            for pl_cards in cards:
                fun_list[0](pl_cards)
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
            for pl_cards in cards:
                fun_list[1](pl_cards)
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
            seven_cards = []
            for _ in range(100000):
                deck = [[mast, nominal] for mast in range(4)
                        for nominal in range(2, 15)]
                cards = []
                for _ in range(7):
                    card = choice(deck)
                    cards.append(card)
                    deck.remove(card)
                seven_cards.append(cards)

            self.test(self.param_list, seven_cards, it)
        for data in self.data:
            self.get_sd(data)
        print("Среднее время работы 1 и 2 функции")
        print(*self.m_list)
        self.get_se()
        print(self.m_list[0] - self.m_list[1])
        print("T-value = ", self.get_t())


t_test = StudentTest(fun_old, fun_new)
t_test.start_test(20)
