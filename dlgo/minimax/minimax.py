# minimax.py
# 3目並べを解く：ミニマックスの例 p102
# 深さで枝刈りされたミニマックス検索    
# Copyright (c) 2020 by Seiichi Nukayama

import enum
import random

from dlgo.agent import Agent

MAX_SCORE = 10
MIN_SCORE = -10
DEPTH = 3

def eval_situation(game_state):
    return 0

# 深さで枝刈りされたミニマックス検索    
def best_result(game_state, max_depth, eval_fn):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE + max_depth
        elif game_state.winner() == game_state.next_player.other:
            return MIN_SCORE - max_depth
        else:
            return 0

    if max_depth == 0:
        return eval_fn(game_state)

    best_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = best_result(next_state, max_depth - 1, eval_fn)
        our_result =  -1 * opponent_best_result
        if our_result > best_so_far:
            best_so_far = our_result
    return best_so_far
# best_so_far -- これまでの最高

def print_best_moves(str, best_moves):
    for move in best_moves:
        print(str, move.point)

class MinimaxAgent(Agent):
    def select_move(self, game_state):
        best_moves = []
        our_best_outcome = None
        for possible_move in game_state.legal_moves():
            print('possible_move %s %s' % (possible_move.point, game_state.next_player))
            next_state = game_state.apply_move(possible_move)        # <1>
            opponent_best_outcome = best_result(next_state, DEPTH, eval_situation)   # <2>
            our_better_outcome = -1 * opponent_best_outcome          # <3>
            if our_best_outcome is None:                             # <4>
                our_best_outcome = our_better_outcome
                best_moves.append(possible_move)
            elif our_best_outcome == our_better_outcome:               # <5>
                best_moves.append(possible_move)
            elif our_best_outcome < our_better_outcome:                # <6>
                our_best_outcome = our_better_outcome
                best_moves.clear()
                best_moves.append(possible_move)
            else:
                print('負ける手なので、考慮の対象外')
            print('our_better_outcome:%d  our_best_outcome:%d' % (our_better_outcome, our_best_outcome))

        if best_moves:
            print_best_moves('best', best_moves)
            return random.choice(best_moves)
        else:
            print('best_movesがないなんて、あり得ない...')
            
    # <1> game_state.apply_move は、next_state を 相手側とする。
    #     つまり、possible_moveを適用した盤状況で、player は相手側であ
    #     る。
    # <2> DEPTH -- 定数とした。
    # <3> 相手が MAX_SCORE なら、こちら側は MIN_SCORE である。
    # <4> our_best_outcome が None ならば、our_better_outcome の値を
    #     our_best_outcome に入れて、best_moves にその着手を入れる。
    # <5> our_best_outcome と our_better_outcome が同じなら
    #     best_moves にその着手を追加する。
    # <6> our_best_outcome よりも our_better_outcome の方が大きければ
    #     best_moves を空にして、その着手をリストに入れる。

    
# -----------------------------------
# 修正時刻： Mon Mar  9 11:23:42 2020
