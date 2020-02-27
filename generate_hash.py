# generate_hash.py
# ゾブリストハッシュの生成 p77
# Copyright (c) 2020 by Seiichi Nukayama

import random

from dlgo.gotypes import Player, Point

def to_python( state ):
    if state is None:
        return 'None'
    if state == Player.black:
        return Player.black
    return Player.white

MAX63 = 0x7fffffffffffffff                                # <1>

table = {}
empty_board = 0
for row in range(1, 20):
    for col in range(1, 20):
        for state in ( Player.black, Player.white ):      # <2>
            code = random.randint( 0, MAX63 )             # <3>
            table[ Point( row, col ), state ] = code      # <4>

print('from .gotypes import Player, Point')
print('')
print("__all__ = [ 'HASH_CODE', 'EMPTY_BOARD' ]")
print('')
print ('HASH_CODE = {')
for ( pt, state ), hash_code in table.items():
    print('    (%r, %s): %r,' % (pt, to_python(state), hash_code))
print('}')
print('')
print('EMPTY_BOARD = %d' % (empty_board,))

# <1> ハッシュ値を生成する大きさ -- 2の4乗の15乗 x 7
# <2> 黒の場合と白の場合の2通りでハッシュ値を作る
# <3> ランダムな整数を作っている
# <4> ハッシュ値を値とするリストを作成している。
#     キーとなるのは、点と黒あるいは点と白である。
