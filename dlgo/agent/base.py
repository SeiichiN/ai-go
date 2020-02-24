# base.py
# p71
# Copyright (c) 2020 by Seiichi Nukayama

# 対局ボットのためのインターフェース
class Agent():
    def __init__( self ):
        pass

    # この基底クラスをもとに派生クラスを作る場合
    # この抽象メソッドが派生クラスでオーバーライドされることを
    # 要求している。
    # その場合、この例外を記述しておくことが求められる。
    def select_move( self, game_state ):
        raise NotImplementedError()

    
