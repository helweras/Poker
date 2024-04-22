import numpy as np
from random import choice
from Table import Table

table = Table(players=4)

original_deck = table.gen_deck_of_cards()

table.card_draw(original_deck)


def flop(deck: list):
    for _ in range(3):
        card = choice(deck)
        table.flop.append(card)
        deck.remove(card)


def turn(deck: list):
    card = choice(deck)
    table.turn.append(card)
    table.turn.extend(table.flop)
    deck.remove(card)


for i in table.list_players:
    print(i.card)
print(len(original_deck))
# def test():
#     for i in range(1000):
#         players1 = [Players.Player() for x in range(4)]
#
#         work = []
#         work_deck = table.gen_deck_of_cards()
#         na = []
#         card_draw(list_players=players1, list_deck=work_deck)
#
#         for pl in players1:
#             for card in pl.card:
#                 na.append(card)
#         for card in na:
#             if card in work:
#                 print('xyi')
#                 return
#             else:
#                 work.append(card)
#     print(True)
