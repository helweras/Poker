from StatRoom import Room
from Table import Table, TableRabbit
from Test import StudentTest
import matplotlib.pyplot as plt
import time
from tqdm import tqdm


rules = {1: 'старшая карта',
         5: 'пара',
         10: '2 пары',
         15: 'сет',
         16: 'стрит',
         17: 'флэш',
         20: 'фулл-хаус',
         25: 'карэ',
         33: 'стрит-флэш'
         }

count_comb = {}
for key in rules.values():
    count_comb[key] = 1


def test_quads(it: int):
    count_qads = 0
    for i in range(it):
        table = Table(players=1)
        table.card_draw()
        table.flop_draw()
        table.turn_draw()
        table.river_draw()

        # for pl in table.list_players:
        #     pl.get_cards(table.river)
        #     pl.check_comb_new(pl.cards)
        # winner = table.determ_winner()
        # print(table.river, '---stol')
        # print()
        # for x in table.list_players:
        #     print(x.hand, '---hand', x.cf_comb)
        # print()
        # for b in winner:
        #     print(b.cf_comb)
        #     print(b.hand, '---winner')

        for pl in table.list_players:
            pl.get_cards(table.river)
            cf = pl.check_comb_new(pl.cards)
            if cf == 33:
                count_qads += 1
                # print(pl.hand)
                # print(f'играющие  {pl.play_card}')
                # print(f'все карты  {pl.cards}')
                # print(f'{table.river} стол')
                # print()
    return count_qads


def test_win(it):
    for i in range(it):
        table = TableRabbit(players=4)
        table.full_play()

        for pl in table.list_players:
            pl.get_cards(table.river)
            pl.check_comb_new(pl.cards)

        print(table.river)
        winners = table.determ_winner()
        print('--------winner---------')
        for pl in winners:
            print(pl.play_card)
            print(pl.hand)
            print(f'{pl.cf_comb} ---- {rules[pl.cf_comb]}')


def r_true_hand():
    table = TableRabbit(players=1, hand=[(1, 7), (1, 14)])
    print(len(table.deck))


def test_check_comb(it):
    stat_table_orig = count_comb.copy()
    stat_table_rabbit = count_comb.copy()
    for i in range(it):
        table_original = Table(players=1)

        table_original.card_draw()
        table_original.flop_draw()
        table_original.turn_draw()
        table_original.river_draw()

        for pl in table_original.list_players:
            pl.check_comb_new(pl.cards)
            name = rules[pl.cf_comb]
            stat_table_orig[name] = stat_table_orig.get(name, 0) + 1
    print(stat_table_orig)

    for i in range(it):
        table_r = TableRabbit(players=1)

        # table_r.full_play()
        table_r.flop_draw()
        table_r.turn_draw()
        table_r.river_draw()
        table_r.card_draw()

        for pl in table_r.list_players:
            pl.check_comb_new(pl.cards)
            name = rules[pl.cf_comb]
            stat_table_rabbit[name] = stat_table_rabbit.get(name, 0) + 1
    print(stat_table_rabbit)
    return list(stat_table_rabbit.values()), list(stat_table_orig.values())


c = 0

# for i in range(10000):
#     table = TableRabbit(players=8,
#                         hand=[(0, 14), (0, 13)],
#                         flop=[(1,3),(2,7),(2,8)],
#                         turn=[(3,9)],
#                         river=[])
#
#     if table.play():
#         c += 1
#     print('--------hands----------')
#     for k in table.list_players:
#         print(k.hand)
#     print()
#
#     print(table.river)
#     print('--------winner---------')
#     for pl in table.winner_list:
#         print(pl.play_card)
#         print(pl.hand)
#         print(f'{pl.cf_comb} ---- {rules[pl.cf_comb]}')
#     print(c)
table = TableRabbit(players=2,
                    hand=[],
                    flop=[],
                    turn=[],
                    river=[])
room = Room(table)
room.up_count()
print(room.chans())
# for iteration in tqdm(range(5)):
#     d =[]
#     start = time.perf_counter()
#     for j in range(10):
#         room = Room(table, iter=3500)
#         room.up_count()
#         d.append(room.chans())
#     stop = time.perf_counter()
#     time_check.append(stop-start)
#     sd_3500.append(st.get_sd(d))
#
#     for k in range(10):
#         room = Room(table, iter=6500)
#         room.up_count()
#         d.append(room.chans())
#     stop = time.perf_counter()
#     time_check.append(stop-start)
#     sd_6500.append(st.get_sd(d))

