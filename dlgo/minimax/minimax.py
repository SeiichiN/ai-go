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
        if game_state.winner() == game_state.next_player and max_depth == 2:
            return MAX_SCORE + 10
        elif game_state.winner() == game_state.next_player:
            return MAX_SCORE
        elif game_state.winner() == game_state.next_player.other and max_depth == 3:
            return MIN_SCORE - 10
        elif game_state.winner() == game_state.next_player.other:
            return MIN_SCORE
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
        high_moves = []
        best_moves = []
        better_moves = []
        other_moves = []
        low_moves = []
        for possible_move in game_state.legal_moves():
            print('possible_move %s %s' % (possible_move.point, game_state.next_player))
            next_state = game_state.apply_move(possible_move)        # <1>
            opponent_best_outcome = best_result(next_state, DEPTH, eval_situation)   # <2>
            our_best_outcome = -1 * opponent_best_outcome            # <3>
            print('our_best_outcome', our_best_outcome)
            if our_best_outcome > MAX_SCORE:                        # <4>
                high_moves.append(possible_move)
            elif our_best_outcome == MAX_SCORE:
                best_moves.append(possible_move)
            elif our_best_outcome == 0:
                better_moves.append(possible_move)
            elif our_best_outcome == MIN_SCORE:
                other_moves.append(possible_move)
            elif our_best_outcome < MIN_SCORE:
                low_moves.append(possible_move)
            else:
                print('=================!')                          # <5>
        if high_moves:
            print_best_moves('high', high_moves)
            return random.choice(high_moves)
        if best_moves:
            print_best_moves('best', best_moves)
            return random.choice(best_moves)
        if better_moves:
            print_best_moves('better', better_moves)
            return random.choice(better_moves)
        if other_moves:
            print_best_moves('other', other_moves)
            return random.choice(other_moves)
        if low_moves:
            print_best_moves('low', low_moves)
            return random.choice(low_moves)
    # <1> game_state.apply_move は、next_state を 相手側とする。
    #     つまり、possible_moveを適用した盤状況で、player は相手側であ
    #     る。
    # <2> 探索の深さを 2 としてみた。
    #     opponent_best_outcome -- 相手側が最善手を打った場合の値。
    #                              MAX_SCORE, 0, MIN_SCORE のいずれか。
    # <3> 相手が MAX_SCORE なら、こちら側は MIN_SCORE である。
    # <4> our_best_outcome が MAX_SCORE, 0, MIN_SCORE で処理を分ける。
    #     MAX_SCOREの場合 -- best_moves のリストに着手を加える。
    #     0               -- better_moves         〃
    #     MIN_SCORE       -- other_moves          〃
    # <5> それ以外は無いはずだけど。
    
# -----------------------------------
# 修正時刻： Sat Mar  7 08:03:16 2020
