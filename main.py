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

        original_deck_test = table_test.gen_deck_of_cards()

        work = []
        na = []
        table_test.card_draw(list_deck=original_deck_test)

        for pl in table_test.list_players:
            for card in pl.hand:
                na.append(card)
        table_test.flop_draw(original_deck_test)

        for card_flop in table_test.flop:
            na.append(card_flop)

        table_test.turn_draw(original_deck_test)

        na.append(table_test.turn[0])

        table_test.river_draw(original_deck_test)

        na.append(table_test.river[0])

        for hand in na:
            if hand in work:
                print(work)
                print(f'итерация {iter}, повтор')
                print('for hend', na[:8])
                print('for flop', na[8:11])
                print('for turn', na[-1])
                return
            else:
                work.append(hand)

        if len(original_deck_test) != 39 or len(original_deck) != 39:
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
            if pl.check_comb(pl.play_card):
                if pl.check_comb(pl.play_card) == 33:
                    count_qads += 1
                    print(f'рука  {pl.hand}')
                    print(f'{table.river} стол')
                    print()
    return count_qads


test_quads(10000)