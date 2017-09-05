'''
Universidade Federal de Santa Catarina
INE5430 - Inteligencia Artificial
Authors:
    Andrei Donati
    Igor Yamamoto
    Luis Felipe Pelison
'''
# Other libs
import tkinter as tk
from tkinter import messagebox
import numpy as np
from functools import partial
# Our libs
from minimax import minimax
from heuristic import hasFinished, calculateHeuristic


def decideMove(state, pcNumber, playerNumber):
        nextMove = [0, 0]
        print("I'm deciding  the move. It may take a while! ")    
        nextMove = minimax(state)
        return nextMove
    
def reset():
    return np.zeros((15, 15))


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
    
    @property
    def heuristic_value(self):
        self._heuristic_value = calculateHeuristic(self.board, self.player)
        return self._heuristic_value
    
    def get_available_moves(self):
        height = self.board.shape[0]
        width = self.board.shape[1]
        proximityBoard = self.board.copy()
        radius = 5
        proximityMatrix = np.ones((radius, radius))*3
        temp = np.count_nonzero(proximityBoard)
        if (temp > 1):
            for row in range(height - radius + 1):
                for col in range(width - radius + 1):
                    if np.any(self.board[row:row + radius, col:col + radius]):
                        proximityBoard[row:row + radius, col:col + radius] += proximityMatrix
        elif temp == 1 and self.board[int(height/2), int(width/2)] == 0: 
            proximityBoard[int(height/2), int(width/2)] = 3
        elif temp == 1 and self.board[int(height/2), int(width/2)] != 0: 
            proximityBoard[int(height/2) - 1, int(width/2) - 1] = 3
        elif temp == 0: 
            proximityBoard[int(height/2), int(width/2)] = 3
            
        availableMoves = []
        diffToCenterHeight = abs(np.arange(height) - int(height/2))
        centerToBorderHeight = np.argsort(diffToCenterHeight)
        diffToCenterWidth = abs(np.arange(width) - int(width/2))
        centerToBorderWidth = np.argsort(diffToCenterWidth)
        for row in centerToBorderHeight:
            for col in centerToBorderWidth:
                if (proximityBoard[row][col] % 3 == 0 and proximityBoard[row][col] > 0):
                    move = (row, col)
                    availableMoves.append(move)
        return availableMoves
    
    def is_terminal(self):
        # A board is terminal if it is won or there are no empty spaces.
        return hasFinished(self.board, self.player)
    
    def next_state(self, move):
        next_board = np.copy(self.board)
        next_board[move] = self.player
        next_player = -1*self.player
        return State(next_board, next_player)
    
   
class Game:
    #The main class! This have all the attibutes and methods to the game works!
    def __init__(self, master):
        self.masterParameter = master
        self.createButtons(master)
        self.difficulty = 0
        self.state = np.zeros((15, 15))
        self.bottomFrame = tk.Frame(root)
        self.bottomFrame.grid(row=15, columnspan=155)
        self.quitBtn = tk.Button(self.bottomFrame,
                                 text='Quit',
                                 command=self.quit)
        self.quitBtn.grid(row=18, columnspan=5)
        reset_with_arg = partial(self.reset, master)
        self.Reset = tk.Button(self.bottomFrame,
                               text='Reset Game',
                               command=reset_with_arg)
        self.Reset.grid(row=19, columnspan=5)
        self.btn = tk.Button(self.bottomFrame, text='My text')
        self.btn.config(state='disabled', relief=tk.SUNKEN)
        self.heuristic_val = 0
        self.nextMovement = [0, 0]
        self.player = self.choosePlayer()
        self.pc = -1
        if(self.player == -1):
            self.pc = 1
            self.nextMove()
            self.buttons[self.findBt()][0].config(bg='blue')
            self.buttons[self.findBt()][0].config(state='disabled',
                                                  relief=tk.SUNKEN)
            self.state[self.buttons
                       [self.findBt()][2]][self.buttons[self.findBt()][3]] = 1
            print('----')
            print('Wating a move')


    def createButtons(self, parent):
        ##This method creates the graphic interface
        self.buttons = {}
        row = 0
        col = 0
        for x in range(0, 15*15):
            id = str(row) + '-' + str(col)
            self.buttons[x] = [tk.Button(parent,
                                         bg='#8a8a8a',
                                         height=2,
                                         width=4),
                               id,  # player
                               row,
                               col]
            self.buttons[x][0].bind('<Button-1>', self.leftClick_w(x))
            col += 1
            if col == 15:
                col = 0
                row += 1
            for k in self.buttons:
                self.buttons[k][0].grid(row=self.buttons[k][2],
                                        column=self.buttons[k][3])

    def leftClick_w(self, x):
        return lambda Button: self.leftClick(x)

    def leftClick(self, btn):
        if (self.player == 1 and self.state[self.buttons
                                            [btn][2]][self.buttons
                                                      [btn][3]] == 0):
            self.buttons[btn][0].config(bg='blue')
            self.buttons[btn][0].config(state='disabled', relief=tk.SUNKEN)
            self.state[self.buttons[btn][2]][self.buttons[btn][3]] = 1
            root.update()
            if (self.is_gameover_pc()):
                if (self.playAgainPlayer() == 1):
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1
            self.nextMove()
            if (self.is_gameover_player()):
                if (self.playAgainPC() == 1):
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1
            print('----')
            print('Waiting a move')
        
        elif (self.player == -1 and self.state[self.buttons
                                               [btn][2]][self.buttons
                                                         [btn][3]] == 0):
            self.buttons[btn][0].config(bg='red')
            self.buttons[btn][0].config(state='disabled', relief=tk.SUNKEN)
            self.state[self.buttons[btn][2]][self.buttons[btn][3]] = -1
            root.update()
            if (self.is_gameover_pc()):
                if (self.playAgainPlayer() == 1):
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1
            self.nextMove()
            if (self.is_gameover_player()):
                if (self.playAgainPC() == 1):
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1
            print('----')
            print('Waiting a move')

    def choosePlayer(self):
        '''
            Function to choose who play first (PC or Player).
        '''
        msg = 'Do you want to play first?'
        answer = messagebox.askquestion('Play First', msg)
        if answer == 'yes':
            return 1
        else:
            return -1

    def playAgainPlayer(self):
        msg = 'Congratulations! You won! Do you want to play again?'
        answer = messagebox.askquestion('Play again', msg)
        if answer == 'yes':
            return 1
        else:
            return -1

    def playAgainPC(self):
        msg = ':-( You lose!\nDo you want to play again?'
        answer = messagebox.askquestion('Play again', msg)
        if answer == 'yes':
            return 1
        else:
            return -1

    def is_gameover_pc(self):
        # A board is terminal if it is won or there are no empty spaces.
        if (0 in self.state and hasFinished(self.state, self.player)):
            return False
        else:
            return True

    def is_gameover_player(self):
        # A board is terminal if it is won or there are no empty spaces.
        if (0 in self.state and hasFinished(self.state, self.pc)):
            return False
        else:
            return True

    def findBt(self):
        for b in self.buttons.keys():
            if (self.buttons[b][2] == self.nextMovement[0] and
               self.buttons[b][3] == self.nextMovement[1]):
                return b

    def nextMove(self):

        self.nextMovement = decideMove(self.state, self.pc, self.player)
        if (self.player == 1):
            self.buttons[self.findBt()][0].config(bg='red')
            self.buttons[self.findBt()][0].config(state='disabled',
                                                  relief=tk.SUNKEN)
            self.state[self.buttons
                       [self.findBt()][2]][self.buttons[self.findBt()][3]] = -1
        else:
            self.buttons[self.findBt()][0].config(bg='blue')
            self.buttons[self.findBt()][0].config(state='disabled',
                                                  relief=tk.SUNKEN)
            self.state[self.buttons
                       [self.findBt()][2]][self.buttons[self.findBt()][3]] = 1
       
        return True

    def quit(self):
        global root
        root.destroy()

    def reset(self, master):
        print('--------------------')
        self.nextMovement = [0, 0]
        self.state = reset()
        for btn in self.buttons.keys():
            self.buttons[btn][0].destroy()
        self.createButtons(master)
        self.player = self.choosePlayer()
        if(self.player == -1):
            self.nextMove()
            self.buttons[self.findBt()][0].config(bg='blue')
            self.buttons[self.findBt()][0].config(state='disabled',
                                                  relief=tk.SUNKEN)
            self.state[self.buttons
                       [self.findBt()][2]][self.buttons[self.findBt()][3]] = 1
            print('----')
            print('Wating a move')


def main():
    global root
    root = tk.Tk()
    root.geometry('700x680+250+0')
    root.title('Gomoku Game')
    img = tk.PhotoImage(file='../img/favicon.png')
    root.tk.call('wm', 'iconphoto', root._w, img)
    game = Game(root) #Call the class Game
    root.mainloop() #Start the game!


if __name__ == '__main__':
    main()
