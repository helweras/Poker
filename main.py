from Table import Table, TableRabbit
import matplotlib

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
    table = TableRabbit(players=1, hand=[[1, 7], [1, 14]])
    print(len(table.deck))

def test_check_comb():
    stat_table_orig = {}
    stat_table_rabbit = {}
    for i in range(100):
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


    for i in range(100):
        table_original = TableRabbit(players=1)

        table_original.card_draw()
        table_original.flop_draw()
        table_original.turn_draw()
        table_original.river_draw()

        for pl in table_original.list_players:
            pl.check_comb_new(pl.cards)
            name = rules[pl.cf_comb]
            stat_table_rabbit[name] = stat_table_rabbit.get(name, 0) + 1
    print(stat_table_rabbit)


test_check_comb()
