# bot_v_bot.py
# p73
# Copyright (c) 2020 by Seiichi Nukayama

#from dlgo.agent import base, helpers, naive
from dlgo import agent
from dlgo import goboard_slow
from dlgo import gotypes
from dlgo.utils import print_board, print_move
from explain import explain
import time
import sys

def main():
    board_size = 9
    game = goboard_slow.GameState.new_game( board_size )
    bots = {
        gotypes.Player.black: agent.RandomBot(),
        gotypes.Player.white: agent.RandomBot(),
    }
    count = 0
    while not game.is_over():
        count += 1
        time.sleep(0.3)
        print( chr(27) + "[2J" )
        print_board( game.board )                       # <1>
        bot_move = bots[ game.next_player ].select_move( game )
        print_move( game.next_player, bot_move )
        game = game.apply_move( bot_move )
        # if count is 50:
        #     sys.exit(0)
    # <1> botが着手する前の盤面を描く。
        
if __name__ == '__main__':                             # <2>
    main()
# <2> このファイルがimportされた場合、「import bot_v_bot」
#     __name__には、「bot_v_bot」がはいる。
#     もし、「python3 bot_v_bot.py」として起動した場合、
#     __name__ には、「__main__」がはいる。

