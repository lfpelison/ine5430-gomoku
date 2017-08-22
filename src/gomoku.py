'''
Universidade Federal de Santa Catarina
INE5430 - Inteligencia Artificial
Authors: Andrei Donati, Igor Yamamoto, Luis Felipe Pelison
'''

import numpy as np
import matplotlib.pyplot as plt


class State(object):
    '''
    Game state (graph nodes)
    state: numpy 2D array
    '''
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.heuristic_val = self.compute_heuristic()
        
    def get_available_moves(self):
        # get the empty positions of the board
        pass
    
    def is_valid_move(self, move):
        moves = self.get_available_moves()
        return move in moves
    
    def is_gameover(self):
        # A board is terminal if it is won or there are no empty spaces.
        pass
    
    def compute_heuristic(self):
        # from board calculate heuristic value
        pass
    
    def next_state(self, move):
        next_board = np.copy(self.board)
        next_board[move] = self.player
        next_player = -1*self.player
        return State(next_board, next_player)
    
class Gomoku(object):
    '''
    Game controller
    height x width board
    current_board: current state of the game, it is a matrix of 1's (player one), 0's (empty) or -1's (player two)
    player: 1 (player one) or -1 (player two)
    
    '''
    
    def __init__(self, height=15, width=15, player=1):
        self.height = height
        self.width = width
        initial_board = np.zeros((height, width))
        self.current_state = State(initial_board, player)
    
    def make_move(self, move):
        # aplly move to the game
        self.current_state = self.current_state.next_state(move)
    
    def display(self):
        plt.imshow(game.current_state.board, 
                   interpolation='nearest', 
                   cmap=plt.cm.cubehelix,
                   vmin=-1,
                   vmax=1)
        plt.xticks(range(self.width), range(1, self.width+1))
        plt.yticks(range(self.height), range(1, self.height+1))
        plt.grid(True)
        plt.show()
        
    def __bool__(self):
        # return True if is not gameover, otherwise return false
        return not self.current_state.is_gameover()
    
    def __repr__(self):
        # print current state of the game
        return '{}'.format(self.current_state.board)


if __name__ == '__main__':
    # Game play code
    print("------------------------------------------Gomoku!------------------------------------------")
    game = Gomoku()
    game.display()    
    while game:
        #player_move = ask for human move
        player_move = input('your turn! move: ').split(',')
        player_move = tuple(map(lambda x: int(x)-1, player_move))
        game.make_move(player_move)
        game.display()
        
        # computer move = aplly minimax
        computer_move = input('thinking... move: ').split(',')
        computer_move = tuple(map(lambda x: int(x)-1, computer_move))
        game.make_move(computer_move)
        game.display()
    print('\nGame Over!!!')