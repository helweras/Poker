from Table import Table
from Rules import CheckRules
from Players import Player


def test_random(count: int):
    iter = 0
    for i in range(count):
        table = Table(players=4)
        original_deck = table.gen_deck_of_cards()
        table.card_draw(original_deck)
        table.flop_draw(original_deck)
        table.turn_draw(original_deck)
        table.river_draw(original_deck)
        iter += 1

        table_test = Table(players=4)

        original_deck_test = table.gen_deck_of_cards()

        work = []
        na = []
        table_test.card_draw(list_deck=original_deck)

        for pl in table.list_players:
            for card in pl.hand:
                na.append(card)
        table.flop_draw(original_deck_test)

        for card_flop in table.flop:
            na.append(card_flop)

        table_test.turn_draw(original_deck_test)

        na.append(table.turn[0])

        table_test.river_draw(original_deck_test)

        na.append(table.river[0])

        for hand in na:
            if hand in work:
                print(f'итерация {iter}, повтор')
                print('for hend', na[:8])
                print('for flop', na[8:11])
                print('for turn', na[-1])
                return
            else:
                work.append(hand)

        if len(original_deck_test) != 39:
            print(f'итерация {iter} хуй карт в колоде не то колличество')
            return
    print(True)


def test_quads(it: int):
    count_qads = 0
    for i in range(it):
        table = Table(players=8)
        original_deck = table.gen_deck_of_cards()
        table.card_draw(original_deck)
        table.flop_draw(original_deck)
        table.turn_draw(original_deck)
        table.river_draw(original_deck)

        for pl in table.list_players:
            pl.get_cards(table.river)
            if pl.check_comb():
                if pl.check_comb()[-1] == 'street-flash':
                    count_qads += 1
                    print(f'рука  {pl.hand}')
                    print(f'{table.river} стол')
                    print()
    return count_qads


print(test_quads(10000))