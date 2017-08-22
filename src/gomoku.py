'''
Universidade Federal de Santa Catarina
INE5430 - Inteligencia Artificial
Autores: Andrei Donati, Igor Yamamoto, Luis Felipe Pelison
'''

import numpy as np

class Board(object):
    '''
    Game board
    state: numpy 2D array
    '''
    def __init__(self, state):
        self.state = state
    
    def get_available_moves(self, move):
        # get the empty positions of the board
        pass
    
    def is_gameover(self):
        # A board is terminal if it is won or there are no empty spaces.
        pass
    
    def compute_heuristic(self, board):
        # from board calculate heuristic value
        pass
    
    def next_state(self, move):
        pass
    
class Gomoku(object):
    '''
    Game controller
    height x width board
    current_board: current state of the game, it is a matrix of 1's (player one), 0's (empty) or -1's (player two)
    player: True (player one) or False (player two)
    
    '''
    
    def __init__(self, height=15, width=15, player=True):
        self.height = height
        self.width = width
        initial_state = np.zeros((height, width))
        self.current_board = Board(initial_state)
        self.player = player
    
    def make_move(self, move):
        # aplly move to the game
        # current_board = current_board.next_state(move)
        pass
    
    def __bool__(self):
        # return True if is not gameover, otherwise return false
        return not self.current_board.is_gameover()
    
    def __repr__(self):
        # print current state of the game
        return '{}'.format(self.current_board)


if __name__ == '__main__':
    # Game play code
    print("Gomoku!\n")
    game = Gomoku()
    while game:
        # player_move = ask for human move
        # make_move(player_move)
        # computer move = aplly minimax
        # make_move(computer move)
        print(game)
    print('\nGame Over!!!')