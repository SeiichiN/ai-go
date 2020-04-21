# human_v_bot.py
# 人間対ボットの対局プログラム(9路盤)

from dlgo import agent
from dlgo import goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move, point_from_coords
from six.moves import input
from dlgo import minimax

DEBUG_MODE = False
from explain import explain

def main():
    board_size = 9
    game = goboard.GameState.new_game( board_size )
    # bot = agent.RandomBot()
    bot = minimax.MinimaxAgent()

    while not game.is_over():
        print( chr(27) + "[2J")
        print_board( game.board )
        if game.next_player == gotypes.Player.black:
            human_move = input('-- ').upper()
            point = point_from_coords( human_move.strip() )
            move = goboard.Move.play( point )
        else:
            move = bot.select_move( game )
        if DEBUG_MODE:
            explain(move)
            print("move END --------------")
        print_move( game.next_player, move )
        game = game.apply_move( move )

if __name__ == '__main__':
    main()
    
#------------------------------------
# 修正時刻： Tue Apr 21 16:59:34 2020
