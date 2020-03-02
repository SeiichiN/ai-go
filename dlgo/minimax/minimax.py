# minimax.py
# 3目並べを解く：ミニマックスの例 p94
# Copyright (c) 2020 by Seiichi Nukayama

import enum
import random

from dlgo.agent import Agent

class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3


def reverse_game_result(game_result):
    if game_result == GameResult.loss:
        return game_result.win
    if game_result == GameResult.win:
        return game_result.loss
    return GameResult.draw

    
def best_result(game_state):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return GameResult.win
        elif game_state.winner() is None:
            return GameResult.draw
        else:
            return GameResult.loss

    best_result_so_far = GameResult.loss
    opponent = game_state.next_player.other
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_result = best_result(next_state)
        our_result = reverse_game_result(opponent_best_result)
        if our_result.value > best_result_so_far.value:
            best_result_so_far = our_result
    return best_result_so_far
# best_result_so_far -- これまでの最高の結果



class MinimaxAgent(Agent):
    def select_move(self, game_state):
        winning_moves = []
        draw_moves = []
        losing_moves = []
        for possible_move in game_state.legal_moves():              # <1>
            next_state = game_state.apply_move(possible_move)        # <2>
            opponent_best_outcome = best_result(next_state)          # <3>
            # <4>
            our_best_outcome = reverse_game_result(opponent_best_outcome)
            if our_best_outcome == GameResult.win:
                winning_moves.append(possible_move)
            elif our_best_outcome == GameResult.draw:
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
    
