# utils.py
# p72
# Copyright (c) 2020 by Seiichi Nukayama

from dlgo import gotypes

COLS = 'ABCDEFGHJKLMNOPQRST'

STONE_TO_CHAR = {
    None: '.',
    gotypes.Player.black: 'x',
    gotypes.Player.white: 'o',
}

def print_move( player, move ):
    if move.is_pass:
        move_str = 'passes'
    elif move.is_resign:
        move_str = 'resigns'
    else:
        move_str = '%s%d' % ( COLS[move.point.col - 1], move.point.row )
    print( '%s %s' % ( player, move_str ))

def print_board( board ):
    for row in range( board.num_rows, 0, -1 ):
        bump = " " if row <= 9 else ""
        line = []
        for col in range( 1, board.num_cols + 1 ):
            stone = board.get( gotypes.Point( row=row, col=col ))    # <1>
            line.append( STONE_TO_CHAR[stone] )
        print( '%s%d %s' % (bump, row, ''.join(line)) )
    print( '   ' + ''.join(COLS[ :board.num_cols ]))
    # <1> board.get -- 盤上の格子に石があれば、その色を返す。なければ None
    
# 人間の入力をBoardのための座標に変換する
# coords -- C3 とか E7 などの文字列
def point_from_coords( coords ):
    col = COLS.index( coords[0] ) + 1
    row = int( coords[ 1: ])
    return gotypes.Point( row=row, col=col )


# 修正時刻： Mon Apr 20 09:17:43 2020
