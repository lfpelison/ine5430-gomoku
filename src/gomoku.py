'''
Universidade Federal de Santa Catarina
INE5430 - Inteligencia Artificial
Authors: 
    Andrei Donati
    Igor Yamamoto
    Luis Felipe Pelison
File description:
    Main file to play the game.
'''

import numpy as np
import matplotlib.pyplot as plt


class State(object):
    '''
    Class description: 
        Game state (graph nodes).
    Attributes:
        board: numpy 2D array.
        player: 1 (player one) or -1 (player two).
        heuristic_val: number calculated from heuristics.
    Methods:
        get_available_moves: returns all possible moves, given a board configuration.
        is_valid_move: verify if the move is valid.
        is_gameover: verify if the state is terminal.
        calculate_heuristic: returns a numeric value from heuristic function.
        next_state: returns the next state, from the state itself and a move.
    '''
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.heuristic_val = self.calculate_heuristic()
        
    def get_available_moves(self):
        # get the empty positions of the board
        pass
    
    def is_valid_move(self, move):
        try:
            if self.board[move] == 0:
                return True
            else:
                print('\nThis position of the board is already taken...\n')
                return False
        except IndexError:
            print('\nBoard dimension is {}\n'.format(self.board.shape))
            return False
    
    def is_gameover(self):
        # A board is terminal if it is won or there are no empty spaces.
        if 0 in self.board:
            return False
        else:
            return True
    
    def calculate_heuristic(self):
        pass
    
    def next_state(self, move):
        next_board = np.copy(self.board)
        next_board[move] = self.player
        next_player = -1*self.player
        return State(next_board, next_player)
    
class Gomoku(object):
    '''
    Class description: 
        Game controller. It stores the current state of the game and displays the
        board and contains the game actions to play.
    Attributes:
        height: board height
        width: board width
        current_state: current state of the game
    Methods:
        make_move: changes the state of the game from a move.
        player_move: asks for a human player to play.
        display: shows the board in a colored graphic.
    '''
    
    def __init__(self, height=15, width=15, player=1):
        self.height = height
        self.width = width
        initial_board = np.zeros((height, width))
        self.current_state = State(initial_board, player)
    
    def make_move(self, move):
        self.current_state = self.current_state.next_state(move)
    
    def player_move(self):
        while True:
            try:
                move = input('your turn! move: ').split(',')
                move = tuple(map(lambda x: int(x)-1, move))
            except ValueError:
                print('\nProvide the coordinates separated by comma, e.g.: 1,1\n')
            if self.current_state.is_valid_move(move):
                self.make_move(move)
                break
            print('\nInvalid move!\n')
        
    def display(self):
        plt.imshow(game.current_state.board, 
                   interpolation='nearest', 
                   cmap=plt.cm.cubehelix,
                   vmin=-1,
                   vmax=1)
        plt.xticks(range(self.width), ['']*self.width)
        plt.yticks(range(self.height), ['']*self.height)
        plt.grid(True)
        plt.show()
        
    def __bool__(self):
        # return True if is not gameover, otherwise return false
        return not self.current_state.is_gameover()
    
    def __repr__(self):
        # print current board of the game
        return '{}'.format(self.current_state.board)


if __name__ == '__main__':
    # Game play code
    print("------------------Gomoku!------------------")
    game = Gomoku()
    game.display()    
    while game:
        #player_move = ask for human move
        game.player_move()
        game.display()
        
        # computer move = aplly minimax
        game.player_move()
        game.display()
    print('\nGame Over!!!')