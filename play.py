# play.py
# とりあえず、本に載っているコードがどう動くかをみるためのコード
# Copyright (c) 2020 by Seiichi Nukayama

from dlgo import zobrist
from dlgo.gotypes import Point, Player

_hash = zobrist.EMPTY_BOARD
print(_hash)

_hash ^= zobrist.HASH_CODE[ Point(row=1, col=3), Player.black ]
print(" 1:", _hash)

_hash ^= zobrist.HASH_CODE[ Point(row=1, col=4), Player.white ]
print(" 2:", _hash)

_hash ^= zobrist.HASH_CODE[ Point(row=1, col=4), Player.white ]
print("2B:", _hash)

# _hash ^= zobrist.HASH_CODE[ Point(row=2, col=4), Player.black ]
# print(" 3:", _hash)
# 
# _hash ^= zobrist.HASH_CODE[ Point(row=3, col=6), Player.white ]
# print(" 4:", _hash)
# 
# _hash ^= zobrist.HASH_CODE[ Point(row=3, col=5), Player.black ]
# print(" 5:", _hash)
# 
# _hash ^= zobrist.HASH_CODE[ Point(row=4, col=5), Player.white ]
# print(" 6:", _hash)
# 
# _hash ^= zobrist.HASH_CODE[ Point(row=4, col=4), Player.black ]
# print(" 7:", _hash)
# 
# _hash ^= zobrist.HASH_CODE[ Point(row=3, col=4), Player.white ]
# print(" 8:", _hash)
# 
# _hash ^= zobrist.HASH_CODE[ Point(row=2, col=5), Player.white ]
# print(" 9:", _hash)
# 
# _hash ^= zobrist.HASH_CODE[ Point(row=7, col=3), Player.black ]
# print("10:", _hash)
# 
# _hash ^= zobrist.HASH_CODE[ Point(row=3, col=4), Player.white ]
# print("11:", _hash)
# 
# _hash ^= zobrist.HASH_CODE[ Point(row=3, col=5), Player.black ]
# print("12:", _hash)
# 
# _hash ^= zobrist.HASH_CODE[ Point(row=3, col=5), Player.black ]
# print("13:", _hash)
# 
# _hash ^= zobrist.HASH_CODE[ Point(row=3, col=4), Player.white ]
# print("14:", _hash)
# 
# _hash ^= zobrist.HASH_CODE[ Point(row=7, col=3), Player.black ]
# print("15:", _hash)
# 

#--------------------------------------------
# 修正時刻： Sat Feb 22 23:05:09 2020
