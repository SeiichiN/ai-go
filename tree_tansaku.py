# tree_tansaku.py
#

# p90
# すぐにゲームに勝つ手を見つける関数
def find_winning_move( game_state, next_player ):
    for candidate_move in game_state.legal_moves( next_player ):       # <1>
        next_state = game_state.apply_move( candidate_move )
        if next_state.is_over() and next_state.winner == next_player:  # <2>
            return candidate_move
    return None
# <1> legal -- 妥当な
#     GameState に legal_move というメソッドを作成する
#        -- 妥当な手を調べるメソッド
# <2> next_state は GameState のインスタンスなので、
#     winner は GameState のメソッド。これも作成する。



# p92
# 相手に勝つ手を与えないようにする関数
# 全ての候補手について、相手が勝つ手があるか検討し、もしその手が
# 相手の勝つ手ではなかったら、possible_movesリストに加える。
# 引数 -- game_state -- GameStateのインスタンス。ゲーム状況
#         next_player -- 次のプレーヤー
# 返り値 -- possible_moves -- next_player にとっての可能な手。
#           next_player の相手が勝つ手を排除する。
def eliminate_losing_moves( game_state, next_player ):            # <1>
    opponent = next_player.other()
    possible_moves = []
    for candidate_move in game_state.legal_moves( next_player ):  # <2>
        next_state = game_state.apply_move( candidate_move )
        opponent_winning_move = find_winning_move(next_state, oppnent)
        if opponent_winning_move is None:
            possible_moves.append( candidate_move )
    return possible_moves
# <1> eliminate -- 除外する
#     losing -- 負ける
# <2> GameState に legal_move というメソッドを作る。
# <3> find_winning_move というメソッドを作る。おそらくGameStateに。


# p93
# 勝ちを保証する2手の手順を見つける関数
def find_two_step_win( game_state, next_player ):
    oppnent = next_player.other()
    # 複数の妥当な手を一つずつ調べる
    for candidate_move in game_state.legal_moves( next_player ):
        next_state = game_state.apply_move( candidate_move )     # <2>        
        good_responses = eliminate_losing_moves( next_state, oppnent )  # <3>
        if not good_responses:
            return candidate_move                                # <4>
    return None
# <2> その一つの手を適用した局面を next_state とする。
# <3> 相手は、敵が勝つ手以外の手を打ってくるはず。それを
#     good_responsesとする。
# <4> good_responses でなければ、それを候補手とする。
# 疑問点
#   candidate_move は複数あるだろうに、一つの候補手を返している。
#   それでもいいのだろうか。
