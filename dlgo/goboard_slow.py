# goboard_slow.py
# Copyright (c) 2020 by Seiichi Nukayama

# class Move():
# class GoString():
# class Board():
# class GameState():

from explain import explain

import sys

# p56
import copy
from dlgo.gotypes import Player

# Move(着手)
#   Move.play(point) -- そのポイントをポイントとする
#   Move.pass_turn -- パスする (self.is_pass が true になる)
#   Move.resign -- 投了する (self.is_resign が true になる)
class Move():
    def __init__( self, point=None, is_pass=False, is_resign=False ):
        assert (point is not None) ^ is_pass ^ is_resign    # <1>
        self.point = point                                  # <2>
        self.is_play = (self.point is not None)             # <3>
        self.is_pass = is_pass
        self.is_resign = is_resign
        # <1> 排他的論理和 -- すべてが1だと0になる
        # <2> self -- インスタンス自身のこと。
        # <3> is_play -- その点は空ではない
        #     is_play, is_pass, is_resign は、True / False の値をとる

    # クラスメソッド -- インスタンス化せずにクラスから直接呼び出すことができる
    # cls -- クラスのこと。呼び出すときの引数は point から。
    # play(打つ) -- プロパティself.point に 引数point をセット。
    @classmethod                    
    def play( cls, point ):         
        return Move( point=point )

    # pass(パス)
    @classmethod
    def pass_turn( cls ):
        return Move( is_pass=True )

    # resign(投了)
    @classmethod
    def resign( cls ):
        return Move( is_resign=True )


# p58    
# 石の連 GoString
#   color -- 石の色
#   stones -- 石の集合 setを使っている。集合をあらわすデータ型だそうだ。
#   liberties -- 呼吸点の集合
# (例)
#   ren1 = GoString(white, 3, 8) -- ren1は白で、3つの石があり、呼吸点は8個である。
#   ren1.remove_liberty(point) -- 呼吸点を1つ削除する。
class GoString():
    def __init__( self, color, stones, liberties ):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    # 呼吸点を削除
    # removeは集合型のメソッド。要素を削除する。
    def remove_liberty( self, point ):
        self.liberties.remove( point )

    # 呼吸点を追加
    # add -- 集合に要素を追加する
    def add_liberty( self, point ):
        self.liberties.add( point )

    # 2つの連を合体
    def merged_with( self, go_string ):
        assert go_string.color == self.color               # <1>
        combined_stones = self.stones | go_string.stones   # <2>
        return GoString(                                   # <3>
            self.color,
            combined_stones,
            ( self.liberties | go_string.liberties ) - combined_stones )
    # <1> 石の色が同じかをチェック
    # <2> | -- 論理和  combined_stones は、石の集合の論理和である。
    # <3> 新しくクラスをインタンス化して、それを返している
    #     第3引数 -- 両方の呼吸点の集合の論理和をとって、石の集合との差集合を求めている。
    #     論理和をとる場合、重複したものは1つとみなされる。
    #     差集合をとる場合、a - b なら、a集合のなかに b集合と重複するものがある場合、
    #     それは削除される。
    #     (参考) -- https://uxmilk.jp/14834

    # インスタンス.num_liberties -- 集合のlen(要素数)を返す
    @property
    def num_liberties( self ):
        return len( self.liberties )

    # 2つのインスタンスを比較できる -- a.__eq__(b)
    # isinstance( object, class) -- 第1引数のオブジェクトが、
    #                               第2引数の型のインスタンスであれば true を返す
    def __eq__( self, other ):
        return isinstance( other, GoString ) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties

# 盤面
# num_rows, num_cols -- 格子線の数
# _grid -- 盤面の情報を辞書リストでもっている。
#          keyは、Point(row=2, col=3)などのPoint。
#          値は、オブジェクトで、GoString情報をもっている
class Board():
    def __init__( self, num_rows, num_cols ):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}                    # 辞書 -- {キー: 値, ...}
    # _grid -- Pointをkeyとした辞書である。
    #          value には、GoStringが入っている。

    # 呼吸点のために隣接する点をチェック
    # player -- (ex) Player.black
    # point -- (ex) Point(row=1, col=1)
    def place_stone( self, player, point ):
        assert self.is_on_grid(point)         # pointが盤上にあるかどうか
        assert self._grid.get(point) is None  # pointがまだ打たれていないかどうか
        adjacent_same_color = []              # 同じ色のリスト
        adjacent_opposite_color = []          # 相手の色のリスト
        liberties = []                        # 呼吸点のリスト
        # print( Point(3, 5).neighbors() )
        # [ Point(row=15, col=6), Point(row=17, col=6), Point(row=16, col=5), Point(row=16, col=7) ]
        for neighbor in point.neighbors():
            if not self.is_on_grid( neighbor ):                # <1>
                continue
            neighbor_string = self._grid.get( neighbor )       # <2>
            if neighbor_string is None:                        # <3>
                liberties.append( neighbor )
            elif neighbor_string.color == player:               # <4>
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append( neighbor_string )
                else:
                    if neighbor_string not in adjacent_opposite_color:
                        adjacent_opposite_color.append( neighbor_string )
        new_string = GoString( player, [point], liberties )      # <5>
        # <1> neighborが盤上の点ではなかったら、パス
        # <2> _grid.get( key ) -- 指定されたkeyがあれば、その連情報を返す。
        #                         なければ、Noneを返す。
        #       値は、GoStringである。
        # <3> もしneighbor_stringがNoneであれば、呼吸点のリストに追加
        # <4> もしneighbor_stringの色がプレイヤーと同じであれば
        #     adjacent_sama_color, adjacent_oppsite_colorにいれる
        # <5> 新しい連をつくる
        #
        for same_color_string in adjacent_same_color:                  # <6>
            new_string = new_string.merged_with( same_color_string )
        for new_string_point in new_string.stones:                     # <7>
            self._grid[ new_string_point ] = new_string
        for other_color_string in adjacent_opposite_color:             # <8>
            other_color_string.remove_liberty( point )
        for other_color_string in adjacent_opposite_color:             # <9>
            if other_color_string.num_liberties == 0:
                self._remove_string( other_color_string )
        # <6> 同じ色の隣接する連をマージする
        # <7> 新しくできた連のそれぞれのポイントに、連の情報をそれぞれセットする。
        # <8> 敵の色の隣接する連の呼吸点を減らす
        # <9> 敵の色の連の呼吸点が 0 になっている場合は、それを取り除く

    def is_on_grid( self, point ):
        return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols

    # 盤上の点の連情報をかえす
    # その点に石がある場合はPlayerの色、それ以外はNoneを返す
    def get( self, point ):
        string = self._grid.get( point )
        if string is None:
            return None
        return string.color

    # ある点における石の連全体を返す。
    # その点に石がある場合はGoString、なければNoneを返す
    def get_go_string( self, point ):
        string = self._grid.get( point )
        if string is None:
            return None
        return string

    # 連を取り除く
    # 連を取り除くと、相手の石が呼吸点を得ることができる
    # string -- 取られる連
    def _remove_string( self, string ):
        for point in string.stones:                             # <1>
            for neighbor in point.neighbors():                  # <2>
                neighbor_string = self._grid.get( neighbor )    # <3>
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:               # <4>
                    neighbor_string.add_liberty( point )
            self._grid[ point ] = None                          # <5>
# <1> string.stones --- stonesはpointの集合
# <2> point.neighbors() --- 隣の点のリスト
# <3> neighbor_string -- 隣の連の情報
# <4> neighbor_string が 取られる連でなかったら、相手の連の呼吸点の集合に追加する。
# <5> 石を取り除いたので、そのポイントは None になる

class GameState():
    def __init__( self, board, next_player, previous, move ):
        self.board = board                      # 盤面の情報
        self.next_player = next_player          # 次のプレーヤー
        self.previous_state = previous          # 前のゲーム状態        
        self.last_move = move                   # 最後に行われた着手

    # 着手を適用したあと、新しい GameState を返す
    def apply_move( self, move ):
        if move.is_play:                                       # <1>
            next_board = copy.deepcopy( self.board )
            next_board.place_stone( self.next_player, move.point )
        else:
            next_board = self.board
        return GameState( next_board, self.next_player.other, self, move )
    # <1> 着手が is_play、つまり Move.play(point)で指し手をした場合、
    #     pointはNoneではなくなるので、is_play は True となる。

    # board_size -- 9 / 19 などの数値
    @classmethod
    def new_game( cls, board_size ):
        if isinstance( board_size, int ):                      # <1>
            board_size = ( board_size, board_size )
        board = Board( *board_size )                           # <2>
        return GameState( board, Player.black, None, None )
    # <1> board_sizeオブジェクトが int型のインスタンスであれば True
    # <2> *board_size -- 9 9 どうもタプルやリストの中の値だけをとりだしてくれるみたい

    # 終局しているか判定
    def is_over( self ):
        if self.last_move is None:                             # <1>
            return False
        if self.last_move.is_resign:                           # <2>
            return True
        second_last_move = self.previous_state.last_move       # <3>
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass  # <4>
    # <1> 最後の着手がまだの場合は False
    # <2> 最後の着手が「投了」の場合は True
    # <3> 前回の盤面の最後の着手を second_last_move とする
    # <4> last_move と second_last_move がともに パス なら True を
    #     そうでなければ False を返す

    # 自殺手のルールを強制する
    def is_move_self_capture( self, player, move ):
        if not move.is_play:                                   # <1>
            return False
        next_board = copy.deepcopy( self.board )
        next_board.place_stone( player, move.point )
        new_string = next_board.get_go_string( move.point )
        return new_string.num_liberties == 0
    # <1> Move.play(point)であれば is_play は True になっている。

    # 現在のゲーム状態はコウのルールに違反しているか？
    @property
    def situation( self ):
        return ( self.next_player, self.board )

    # player -- Player.black / Player.white
    # move -- Move.play(row, col)
    def does_move_violate_ko( self, player, move ):
        if not move.is_play:
            return False
        next_board = copy.deepcopy( self.board )           # <1>
        next_board.place_stone( player, move.point )       # <2>
        next_situation = ( player.other, next_board )      # <3>
        past_state = self.previous_state                   # <4>
        while past_state is not None:                      # <5>
            if past_state.situation == next_situation:     # <6>
                return True
            past_state = past_state.previous_state         # <7>
        return False                                       # <8>
    # <1> 現在の盤をdeepcopyして、next_boardとする。
    # <2> next_boardに次の指し手を実行（石を置く）。
    # <3> next_board と player.other をタプルにして next_situation とする。
    # <4> 前回の盤を past_state とする。
    # <5> 前回の盤が None でない限り実行。
    # <6> past_sitate.situation と next_situation が同じであれば、
    #     つまり、「コウ」であれば、True を返す。
    # <7> past_stateを past_stateの更に前の盤(previous_state)とする。
    #     それで、もう一度、past_state.situation と next_situation を比べる。
    # <8> 同じゲーム状況が無ければ、「コウ」ではないので、False を返す。

    # この着手は指定されたゲーム状態に対して有効か？
    def is_valid_move( self, move ):
        if self.is_over():                                     # <1>
            return False
        if move.is_pass or move.is_resign:                     # <2>
            return True
        return (                                               
            self.board.get( move.point ) is None and                        # <3>
            not self.is_move_self_capture( self.next_player, move ) and     # <4>
            not self.does_move_violate_ko( self.next_player, move ))        # <5>
    # <1> 終局の場合 False（無効）
    # <2> 着手がパスあるいは投了の場合 True（有効）
    # <3> 指し手の点に石（連）が無い場合
    # <4> 指し手が自殺手である場合
    # <5> 指し手がコウである場合
    #     <3><4><5>がともに成立することって、あるのかな？


#--------------------------------------
# 修正時刻： Sun Feb 23 10:17:14 2020
