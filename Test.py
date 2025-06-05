from math import sqrt
import time
import numpy as np
from tqdm import tqdm


class StudentTest:
    def __init__(self, param1, param2):
        self.param_list = (param1, param2)
        self.data = [[], []]
        self.m_list = []
        self.sd_list = []
        self.n = None

    def get_sd(self, param: list):
        m = sum(param) / len(param)
        # print(m, '---- математическое ожидание')
        self.m_list.append(m)
        dis = sum(list(map(lambda x: pow((x - m), 2), param))) / (len(param) - 1)
        sd = sqrt(dis)
        # print(sd, '--- стандартное отклонение')
        # print()
        self.sd_list.append(sd)
        return sd

    def get_se(self):
        se = sqrt((self.sd_list[0] * self.sd_list[0]) / self.n + (self.sd_list[1] * self.sd_list[1]) / self.n)
        return se

    def get_t(self):
        s_m = sorted(self.m_list)
        t = (s_m[1] - s_m[0]) / self.get_se()
        return t

    def test(self, fun_list, param, out_iter, it):
        try:
            start = time.perf_counter()
            for _ in range(it):
                fun_list[0](param)
            stop = time.perf_counter()
            # print(f"Первая функция {out_iter + 1}) {round(stop - start, 3)}")
            # print()
            self.data[0].append(stop - start)
        except TypeError:
            start = time.perf_counter()
            for _ in range(it):
                fun_list[0]()
            stop = time.perf_counter()
            # print(f"Первая функция {it + 1}) {round(stop - start, 3)}")
            # print()
            self.data[0].append(stop - start)
        try:
            start = time.perf_counter()
            for _ in range(it):
                fun_list[1](param)
            stop = time.perf_counter()
            # print(f"Вторая функция {it + 1}) {round(stop - start, 3)}")
            # print()
            self.data[1].append(stop - start)
        except TypeError:
            start = time.perf_counter()
            for _ in range(it):
                fun_list[1]()
            stop = time.perf_counter()
            # print(f"Вторая функция {it + 1}) {round(stop - start, 3)}")
            # print()
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

    def start_test(self, include_iter, itr=5, param=False):
        self.n = itr
        for it in tqdm(range(itr)):
            self.test(self.param_list, param, it, it=include_iter)
        for data in self.data:
            self.get_sd(data)
        print(f"Среднее время работы 1 и 2 функции при {include_iter} итерациях")
        print(*[round(count, 3) for count in self.m_list], sep=' Секунд\n', end=' Секунд\n')
        self.get_se()
        print(round(self.m_list[0] - self.m_list[1], 3), '--- Разница среднего времени работы')
        print("T-value = ", round(self.get_t(), 3))


d1 = [10, 15, 25]
d2 = [20, 10, 20]



# if any(x) and all(x):
#     print(True)
# else:
#     print(False)
class X2:
    def __init__(self, data_1, data_2):
        self.data_1 = np.array(data_1)
        self.data_2 = np.array(data_2)
        self.sum_1 = sum(data_1)
        self.sum_2 = sum(data_2)
        self.expected = []

    def get_x2(self):
        sum_row = self.data_1 + self.data_2
        expected_1 = sum_row * self.sum_1 / (self.sum_1 + self.sum_1)
        expected_2 = sum_row * self.sum_2 / (self.sum_1 + self.sum_1)

        x2 = np.sum(((self.data_1 - expected_1) ** 2) / expected_1 + ((self.data_2 - expected_2) ** 2) / expected_2)

        print(x2)
        return x2
