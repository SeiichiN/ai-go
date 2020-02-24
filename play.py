# play.py
# とりあえず、本に載っているコードがどう動くかをみるためのコード
# Copyright (c) 2020 by Seiichi Nukayama

from explain import explain
from dlgo.gotypes import Player
from dlgo.gotypes import Point
from dlgo.goboard_slow import *
# from dlgo.goboard_slow import GoString

print(Player.black)
print(Player.white.name)
print(Player.white.value)

COLS = "ABCDEFGHJ"

board = Board(9, 9)


board = GameState(board, Player.black, None, None )
print("board>", board)
explain(board)

D16 = Point(16, 4)
E4 = Point(4, 5)

print(D16)
print(E4)


E16 = Point(row=16, col=5)
P3 = Point(row=3, col=15)

print(E16)
print(P3)

print( D16.neighbors() )

board = Board(19, 19)
board.place_stone(taro, D16)
D15 = Point(15, 4)
board.place_stone(jiro, D15)

board.get(D15)

#--------------------------------------------
# 修正時刻： Sat Feb 22 23:05:09 2020
