# minimax.py
# 3目並べを解く：ミニマックスの例 p94
# Copyright (c) 2020 by Seiichi Nukayama

import enum
import random

from dlgo.agent import Agent

MAX_SCORE = 10
MIN_SCORE = -10

class GameResult(enum.Enum):
    loss = -1
    draw = 0
    win = 1


def reverse_game_result(game_result):
    if game_result == MAX_SCORE:    # GameResult.loss:
        return MIN_SCORE            # game_result.win
    if game_result == MIN_SCORE:    # GameResult.win:
        return MAX_SCORE            # game_result.loss
    return 0                        # GameResult.draw

def eval_situation(game_state):
    # opponent = game_state.next_player.other
    # if game_state._has_3_in_a_row(opponent):
    #     print('%s が3つそろった' % opponent)
    #     return MIN_SCORE
    # elif game_state._has_3_in_a_row(game_state.next_player):
    #     print('%s が3つそろった' % game_state.next_player)
    #     return MAX_SCORE
    # else:
    #     print('3つそろったのは無し')
        return 1

# 深さで枝刈りされたミニマックス検索    
def best_result(game_state, max_depth, eval_fn):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            # print('OVER! %s' % game_state.next_player )
            return MAX_SCORE
        elif game_state.winner() == game_state.next_player.other:
            return MIN_SCORE
        else:
            # print('OVER! %s' %  game_state.next_player.other)
            return 0

    if max_depth == 0:
        return eval_fn(game_state)

    best_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves():
        # print('%s: candidate_move %s %s' % (max_depth, candidate_move.point, game_state.next_player))
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = best_result(next_state, max_depth - 1, eval_fn)
        our_result =  -1 * opponent_best_result
        if our_result > best_so_far:
            best_so_far = our_result
    print('best_so_far %s %s' % (game_state.next_player, best_so_far))
    return best_so_far
# best_so_far -- これまでの最高

class MinimaxAgent(Agent):
    def select_move(self, game_state):
        winning_moves = []
        draw_moves = []
        losing_moves = []
        for possible_move in game_state.legal_moves():              # <1>
            print('possible_move %s %s' % (possible_move.point, game_state.next_player))
            next_state = game_state.apply_move(possible_move)        # <2>
            opponent_best_outcome = best_result(next_state, 3, eval_situation)          # <3>
            # <4>
            print('opponent_best_outcome ', opponent_best_outcome)
            our_best_outcome = reverse_game_result(opponent_best_outcome)
            print('our_best_outcome', our_best_outcome)
            if our_best_outcome > 0:                   # == GameResult.win:
                winning_moves.append(possible_move)
            elif our_best_outcome == 0:                # == GameResult.draw:
                draw_moves.append(possible_move)
            else:
                losing_moves.append(possible_move)
        if winning_moves:
            return random.choice(winning_moves)
        if draw_moves:
            return random.choice(draw_moves)
        return random.choice(losing_moves)
    # <1> GameStateクラスに legal_moves メソッドを作らねばならない
    # <2> possible_move を適用したあとの GameState が next_state である。
    #     仮にこの手を打ってみたとして、その結果を next_state に出力する
    # <3> best_result -- ゲームの状態から最善の手をみつける
    #     こちら側の仮の手に対して、相手の最善の手を予想してみる
    #     opponent_best_outcome -- 相手の最善の予想手
    # <4> reverse_game_result -- 相手の手に対するこちら側の最善の手
    #     相手 win   <--> 自分 loss
    #          draw  <-->      draw
    #          loss  <-->      win
    
# -----------------------------------
# 修正時刻： Fri Mar  6 15:03:12 2020
