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
from heuristic import hasWinnerSeq, calculateHeuristic


#|4th.| The description is below
class State(object):
    '''
    Class description:
        Game state (graph nodes).
    Attributes:
        board: numpy 2D array.
        player: next player to make a move. 1 (player one) or -1 (player two).
    Properties:
        heuristic_value: number calculated from heuristics.
        available_moves: all possible moves, given the board configuration.
    Methods:
        is_terminal: verify if the state is terminal.
        next_state: returns the next state, given the state itself and a move.
    '''
    def __init__(self, board, player):
        self.board = board
        self.player = player

    @property
    def heuristic_value(self):
        self._heuristic_value = calculateHeuristic(self.board, self.player)
        return self._heuristic_value

    @property
    def available_moves(self):
        height = self.board.shape[0]
        width = self.board.shape[1]
        proximityBoard = self.board.copy()
        radius = 3
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

        self._available_moves = []
        diffToCenterHeight = abs(np.arange(height) - int(height/2))
        centerToBorderHeight = np.argsort(diffToCenterHeight)
        diffToCenterWidth = abs(np.arange(width) - int(width/2))
        centerToBorderWidth = np.argsort(diffToCenterWidth)
        for row in centerToBorderHeight:
            for col in centerToBorderWidth:
                if (proximityBoard[row][col] % 3 == 0 and proximityBoard[row][col] > 0):
                    move = (row, col)
                    self._available_moves.append(move)

        return self._available_moves

    def is_terminal(self):
        # A board is terminal if it is won or there are no empty spaces.
        if not (0 in self.board):
            return True
        if hasWinnerSeq(self.board, self.player):
            return True
        else:
            return False

    def next_state(self, move):
        next_board = np.copy(self.board)
        next_board[move] = self.player
        next_player = -1*self.player
        return State(next_board, next_player)


#|2nd.| The main class! This have all the attibutes and methods to the game works!
class Game:
    '''
    Class description:
        Game controller. It stores the current state of the game, displays the
        board and it implements the game actions to play.
    '''
    def __init__(self, height=15, width=15):

        # Graphic Interface
        self.root = tk.Tk()
        self.root.geometry('840x680+250+0')
        self.root.title('Gomoku Game')
        #img = tk.PhotoImage(file='../img/favicon.png')
        #self.root.tk.call('wm', 'iconphoto', self.root._w, img)
        self.height = height
        self.width = width
        self.bottomFrame = tk.Frame(self.root)
        self.bottomFrame.grid(row=15, columnspan=155)
        self.btn = tk.Button(self.bottomFrame, text='My text')
        self.btn.config(state='disabled', relief=tk.SUNKEN)
        self.printCredits = tk.Text(self.bottomFrame, width=117, height=7, bg='#D9D9D9')
        self.printCredits.grid(row=21, columnspan=2)
        self.printCredits.insert('end', 'Authors: \n\t - Luis Felipe Pelison\
                                \n\t - Ígor Yamamoto \n\t - Andrei Donati\
                                \n \nUFSC - INE5430 - 2017 - Professor Elder Rizzon')
        self.quitBtn = tk.Button(self.bottomFrame,
                                 text='Quit',
                                 command=self.quit)
        self.quitBtn.grid(row=18, columnspan=5)
        reset_with_arg = partial(self.reset)
        self.Reset = tk.Button(self.bottomFrame,
                               text='Reset Game',
                               command=reset_with_arg)
        self.Reset.grid(row=19, columnspan=5)


        # Attributes more importants
        self.createButtons(self.root) #|3rd.|
        initial_board = np.zeros((height, width)) # Structure of initial state: all 0
        player_one = 1
        self.current_state = State(initial_board, player_one) #|4th.| Call the class State
        self.isPlayerOneHuman = self.isHuman('One') #|5th.| Verifies who is
        self.isPlayerTwoHuman = self.isHuman('Two')


        if (not self.isPlayerOneHuman) and self.current_state.player == 1:
            self.PCMove()


    #|6th.| Changes the interface's buttons by the PC movement (row and column)
    def PCMove(self):
        # Remember: buttons > {number from 0 to 15*15: list of [button object, id:'row-col', row, col]}
        print('The PC will play! Fasten your seats belts!')
        move = minimax(self.current_state) #|7th.| This function is at minimax.py
        print(move)
        btn = self.buttons[self.findBt(move)][0] #|17th.| #AND Changes color
        if (self.current_state.player == 1):
            btn.config(bg='black')
            btn.config(state='disabled', relief=tk.SUNKEN)
            print('Black moved.')
        else:
            btn.config(bg='white')
            btn.config(state='disabled', relief=tk.SUNKEN)
            print('White moved.')
        self.current_state = self.current_state.next_state(move) #Ver isso
        self.root.update()

        if (self.is_gameover() and self.isPlayerTwoHuman):
            if self.playAgain('One'):
                self.Reset.invoke()
                return 1
            else:
                self.quitBtn.invoke()
                return 1

        elif (self.is_gameover() and self.isPlayerOneHuman):
            if self.playAgain('Two'):
                self.Reset.invoke()
                return 1
            else:
                self.quitBtn.invoke()
                return 1

        #print('O PC Jogou, o novo estado é: {}'.format(self.current_state.player))
        #self.current_state.player = -1 * self.current_state.player
        #print('Agora trocou, o HUMANO deverá jogar. Seu novo estado é {}'.format(self.current_state.player))
        if (not self.isPlayerOneHuman) and (not self.isPlayerTwoHuman):
            self.PCMove()
        print('Waiting a move...')


    #|3rd.| This method creates the graphic interface
    def createButtons(self, parent):
        self.buttons = {} # A dictionary that will contain:
                          # {number from 0 to 15*15: list of [button object, id:'row-col', row, col]}
        row = 0
        col = 0
        for x in range(0, 15*15):
            id = str(row) + '-' + str(col)
            self.buttons[x] = [tk.Button(parent,
                                         bg='#ecab57',
                                         height=2,
                                         width=4),
                               id,  # 'row-col'
                               row,
                               col] # Populating the dictionary

            self.buttons[x][0].bind('<Button-1>', self.leftClick_w(x))
            #|18th.| WAITING A MOVE. WHEN THE EVENT <Button-1> HAPPEN: LEFTCLICK
            # Set all button objects to execute the function leftClick_w(x)
            # when the <Button-1> is clicked (button 1 means left click mouse)

            col += 1
            if col == 15:
                col = 0
                row += 1
            for k in self.buttons:
                self.buttons[k][0].grid(row=self.buttons[k][2],
                                        column=self.buttons[k][3])


    #|18th.| Just returns the leftClick function when Tkinter bind needs it.
    def leftClick_w(self, x):
        return lambda Button: self.leftClick(x)


    #|19th.| This method is executed when a button is clicked by mouse left click.
    # Depending on wich player is, this method set the color for the button,
    # put the value of the state, update the interface and verify the end game
    def leftClick(self, btn):

        # This if clause verifies wich player is and if his move is possible
        # Remember: buttons structure is:
        # {number from 0 to 15*15: list of [button object, id:'row-col', row, col]}
        if (self.current_state.player == 1 and self.current_state.board[self.buttons
                                                                        [btn][2]][self.buttons
                                                                        [btn][3]] == 0):
            self.buttons[btn][0].config(bg='black')
            self.buttons[btn][0].config(state='disabled', relief=tk.SUNKEN)
            self.current_state.board[self.buttons[btn][2]][self.buttons[btn][3]] = 1
            self.root.update()
            if (self.is_gameover()): #|20th.|
                if self.playAgain('One'): #|22th.|
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1

            print('BLACK!')
            #print('Seu estado é: {}'.format(self.current_state.player))
            self.current_state.player = -1
            #print('Agora, seu estado é: {}'.format(self.current_state.player))
            if not self.isPlayerTwoHuman:
                self.PCMove()
            print('Are you ready?')

        elif (self.current_state.player == -1 and self.current_state.board[self.buttons
                                                                        [btn][2]][self.buttons
                                                                        [btn][3]] == 0):
            self.buttons[btn][0].config(bg='white')
            self.buttons[btn][0].config(state='disabled', relief=tk.SUNKEN)
            self.current_state.board[self.buttons[btn][2]][self.buttons[btn][3]] = -1
            self.root.update()
            if (self.is_gameover()):
                if self.playAgain('Two'):
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1

            print('WHITE!')
            #print('Seu estado é: {}'.format(self.current_state.player))
            self.current_state.player = 1
            #print('Agora, seu estado é: {}'.format(self.current_state.player))
            if not self.isPlayerOneHuman:
                self.PCMove()
            print('Are you ready?')


    #|5th.| We can have 2 players: humans or PCs
    def isHuman(self, number):
        '''
            Function to choose wether the player is human or not.
        '''
        msg = 'Is Player {} a human?'.format(number)
        return messagebox.askyesno('Human or PC', msg)


    #|22th.|
    def playAgain(self, number):
        msg = 'Player {} is the winner! \nDo you want to play again?'.format(number)
        return messagebox.askyesno('Play again', msg)


    #|20th.|
    def is_gameover(self):
        # A board is terminal if it is won or there are no empty spaces.
        return self.current_state.is_terminal()


    #|17th.|
    # Search for the buttons{}'s key that match the row value (2) AND column (3).
    # E.g: key:1 is row 0 and column 1 > buttons[0][2] == 0 and buttons[0][3] == 1
    def findBt(self, move):
        for b in self.buttons.keys():
            if (self.buttons[b][2] == move[0] and
               self.buttons[b][3] == move[1]):
                return b

    def quit(self):
        self.root.destroy()

    def reset(self):
        print('--------------------')
        initial_board = np.zeros((self.height, self.width))
        player_one = 1
        self.current_state = State(initial_board, player_one)
        for btn in self.buttons.keys():
            self.buttons[btn][0].destroy()


        self.createButtons(self.root) #|3rd.|
        initial_board = np.zeros((self.height, self.width)) # Structure of initial state: all 0
        player_one = 1
        self.current_state = State(initial_board, player_one) #|4th.| Call the class State
        self.isPlayerOneHuman = self.isHuman('One') #|5th.| Verifies who is
        self.isPlayerTwoHuman = self.isHuman('Two')


        if (not self.isPlayerOneHuman) and (self.isPlayerTwoHuman) and self.current_state.player == 1:
            self.PCMove()

        '''

        self.createButtons(self.root)
        self.player = self.choosePlayer()
        if(self.player == -1):
            self.nextMove()
            self.buttons[self.findBt()][0].config(bg='blue')
            self.buttons[self.findBt()][0].config(state='disabled',
                                                  relief=tk.SUNKEN)
            self.state[self.buttons
                       [self.findBt()][2]][self.buttons[self.findBt()][3]] = 1
            print('----')
            print('Waiting a move')

        '''


    def run(self):
        self.root.mainloop()


#|1st.| Here is where all happens.
if __name__ == '__main__':
    gomoku = Game() #|2nd.| Create an instance of the main class
    gomoku.run()
