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
from minimax import decideMove, reset
from heuristic import hasFinished, calculateHeuristic

#|2nd.| The main class! This have all the attibutes and methods to the game works!
class Game:
    def __init__(self, master):
        self.masterParameter = master
        self.createButtons(master) #|3rd.|

        self.difficulty = 0
        self.state = np.zeros((15, 15)) # Structure of state: all 0

        # Graphic Interface
        self.bottomFrame = tk.Frame(root)
        self.bottomFrame.grid(row=15, columnspan=155)
        self.printCredits = tk.Text(self.bottomFrame, width=117, height=7, bg='#D9D9D9')
        self.printCredits.grid(row=21, columnspan=2)
        self.printCredits.insert('end', 'Authors: \n\t - Luis Felipe Pelison\
                                \n\t - Ígor Yamamoto \n\t - Andrei Donati\
                                \n \nUFSC - INE5430 - 2017 - Professor Elder Rizzon')
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
        self.player = self.choosePlayer() #|4th.|
        self.pc = -1

        #|5th.| If pc starts, pc is the player 1, he does the next movement his color is BLUE.
        if(self.player == -1):
            self.pc = 1
            self.nextMove() #|6th.|
            self.buttons[self.findBt()][0].config(bg='blue')
            self.buttons[self.findBt()][0].config(state='disabled',
                                                  relief=tk.SUNKEN)
            self.state[self.buttons
                       [self.findBt()][2]][self.buttons[self.findBt()][3]] = 1
            print('----')
            print('Wating a move')

    #|3rd.| This method creates the graphic interface
    def createButtons(self, parent):

        self.buttons = {} # A dictionary that will contain:
                          # {number from 0 to 15*15: list of [button object, id:'row-col', row, col]}
        row = 0
        col = 0
        for x in range(0, 15*15):
            id = str(row) + '-' + str(col)
            self.buttons[x] = [tk.Button(parent,
                                         bg='#8a8a8a',
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
        return lambda Button: self.leftClick(x) #|19th.|


    #|19th.| This method is executed when a button is clicked by mouse left click.
    # Depending on wich player is, this method set the color for the button,
    # put the value of the state, update the interface and verify the end game
    def leftClick(self, btn):
        # This if clause verifies wich player is and if his move is possible
        # Remember: buttons structure is:
        # {number from 0 to 15*15: list of [button object, id:'row-col', row, col]}
        if (self.player == 1 and self.state[self.buttons
                                            [btn][2]][self.buttons
                                                      [btn][3]] == 0):
            self.buttons[btn][0].config(bg='blue')
            self.buttons[btn][0].config(state='disabled', relief=tk.SUNKEN)
            self.state[self.buttons[btn][2]][self.buttons[btn][3]] = 1
            root.update()
            if (self.is_gameover_pc()): #|20th.|
                if (self.playAgainPlayer() == 1): #|22th.|
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

    #|4th.| If human wants to start, he is the player 1. Else, he will be the player -1.
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

    #|22th.|
    def playAgainPC(self):
        msg = ':-( You lose!\nDo you want to play again?'
        answer = messagebox.askquestion('Play again', msg)
        if answer == 'yes':
            return 1
        else:
            return -1

    #|20th.|
    def is_gameover_pc(self):
        # A board is terminal if it is won or there are no empty spaces.
        if (0 in self.state and hasFinished(self.state, self.player)): #|21th.|
            return False
        else:
            return True

    def is_gameover_player(self):
        # A board is terminal if it is won or there are no empty spaces.
        if (0 in self.state and hasFinished(self.state, self.pc)):
            return False
        else:
            return True

    #|17th.|
    # Search for the buttons{}'s key that match the row value (2) AND column (3).
    # E.g: key:1 is row 0 and column 1 > buttons[0][2] == 0 and buttons[0][3] == 1
    def findBt(self):
        for b in self.buttons.keys():
            if (self.buttons[b][2] == self.nextMovement[0] and
               self.buttons[b][3] == self.nextMovement[1]):
                return b

    #|6th.| Changes the interface's buttons by your nextMovement (row and column)
    def nextMove(self):
        # Remember: buttons > {number from 0 to 15*15: list of [button object, id:'row-col', row, col]}
        self.nextMovement = decideMove(self.state, self.pc, self.player) #|7th.| This function is at minimax.py
        if (self.player == 1):
            self.buttons[self.findBt()][0].config(bg='red') #|17th.| #Changes color
            self.buttons[self.findBt()][0].config(state='disabled',
                                                  relief=tk.SUNKEN)
            self.state[ self.buttons[self.findBt()][2] ][ self.buttons[self.findBt()][3] ] = -1 #Changes state
        else: #plater == -1
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


#|1st.| Here is where all happens.
def main():
    global root
    root = tk.Tk() #This creates a toplevel widget of Tk / the main window.
    root.geometry('840x680+250+0')
    root.title('Gomoku Game')
    img = tk.PhotoImage(file='../img/favicon.png')
    root.tk.call('wm', 'iconphoto', root._w, img)
    game = Game(root) #Call the class Game
    root.mainloop() #Start the game!


if __name__ == '__main__':
    main()
