# helpers.py
# p69
# Copyright (c) 2020 by Seiichi Nukayama

from dlgo.gotypes import Point

# 盤上の指定された点は、眼か？
def is_point_an_eye( board, point, color ):
    if board.get( point ) is not None:               # <1>
        return False
    for neighbor in point.neighbors():
        if board.is_on_grid( neighbor ):
            neighbor_color = board.get( neighbor )
            if neighbor_color != color:              # <2>
                return False

    friendly_corners = 0
    off_board_corners = 0
    corners = [                                      # <3>
        Point( point.row - 1, point.col - 1),
        Point( point.row - 1, point.col + 1),
        Point( point.row + 1, point.col - 1),
        Point( point.row + 1, point.col + 1),
    ]
    for corner in corners:
        if board.is_on_grid( corner ):
            corner_color = board.get( corner )
            if corner_color == color:                 # <4>
                friendly_corners += 1
        else:
            off_board_corners += 1                    # <5>
    if off_board_corners > 0:                         # <6>
        return off_board_corners + friendly_corners == 4
    return friendly_corners >= 3                      # <7>
# <1> 眼は空の点
# <2> 隣接するすべての点の色は、味方の色であること
# <3> corners -- その点の四隅の点
# <4> そのコーナーの色が味方の色であれば、friendly_corners をプラス1
# <5> そのコーナーが盤上の点ではなかったら、off_board_corners をプラス1
# <6> off_board_cornersが1つでもあれば、off_board_corners と
#     friendly_corners の合計が 4 ならば True,そうじゃなければ False を返す
# <7> friendly_corners が 3 以上なら True を返す
