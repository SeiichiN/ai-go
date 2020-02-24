# gotypes.py
# Copyright (c) 2020 Seiichi Nukayama

# 55
import enum

# print(Player.black)  ==> Player.black
# print(Player.black.name) ==> black
# print(Player.black.value) ==> 1
class Player( enum.Enum ):
    black = 1
    white = 2

    # a が Player.black だとすると、a.other は Player.white となる 
    @property
    def other( self ):
        return Player.black if self == Player.white else Player.white


    
from collections import namedtuple

# クラス Point型の定義
# namedtupleを引数にもってインスタンスを作成
# namedtuple(typename, field_names, ...) -- 名前付きフィールドをもつタプルのファクトリ関数
# field_namesには、'x y'や'x, y'などの文字列をわたすことができる
# (例)
#   >>> a = Point(row=5, col=5)        # <== インスタンスの作成のしかた
#   >>> print(a)               # Point(row=5, col=5)
#   >>> print(a.row)           # 5
#   >>> b = a.neighbors()
#   >>> print(b)
#   [Point(row=4, col=5), Point(row=6, col=5), Point(row=5, col=4), Point(row=5, col=6)]
class Point( namedtuple( 'Point', 'row col')):
    def neighbors( self ):
        return [
            Point( self.row - 1, self.col ),
            Point( self.row + 1, self.col ),
            Point( self.row, self.col - 1 ),
            Point( self.row, self.col + 1 ),
        ]

#----------------------------------------
# 修正時刻： Sat Feb 22 23:04:53 2020
