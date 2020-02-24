# naive.py
# p71
# Copyright (c) 2020 by Seiichi Nukayama

import random
from dlgo.agent.base import Agent
from dlgo.agent.helpers import is_point_an_eye
from dlgo.goboard_slow import Move
from dlgo.gotypes import Point

# candidates -- 有効な着手ができる候補リスト
# もし、candidatesが無ければ、パスする
# ボットは、candidatesリストの中からランダムに手を選ぶ
class RandomBot( Agent ):
    def select_move( self, game_state ):
        """Choose a random valid move that preserves our own eyes.
        自分の眼を維持するランダムな有効な着手を選択する"""
        candidates = []              # 候補
        for r in range( 1, game_state.board.num_rows + 1 ):
            for c in range( 1, game_state.board.num_cols + 1 ):
                candidate = Point( row=r, col=c )
                if game_state.is_valie_move( Move.play( candidate ) ) and \
                   not is_point_an_eye( game_state.board,            # <1>
                                        candidate,
                                        game_state.next_player ):
                    candidates.append( candidate )                   # <2>
        if not candidates:                                           # <3>
            return Move.pass_turn()
        return Move.play( random.choice( candidates ))               # <4>
    # <1> 要するに、候補点が着手可能な点であるか
    #     not is_point_an_eye つまり、眼には打てないということ。
    # <2> 盤上のすべての着手可能な点を「候補点」として candidates リストに入れている。
    # <3> もしも、候補点が無ければ、パスせざるを得ん。
    # <4> 候補点のリストの中から、ランダムに選んで、「指し手」としている。
