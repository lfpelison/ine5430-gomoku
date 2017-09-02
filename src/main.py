'''
Universidade Federal de Santa Catarina
INE5430 - Inteligencia Artificial
Authors:
    Andrei Donati
    Igor Yamamoto
    Luis Felipe Pelison
'''
#Other libs
import tkinter as tk
from tkinter import messagebox
import numpy as np
from functools import partial
#Our libs
from minimax import decideMove, reset
from heuristic import hasFinished, calculateHeuristic


class Game:
    #The main class! This have all the attibutes and methods to the game works!
    def __init__(self, master):
        self.masterParameter = master
        self.createButtons(master)
        self.difficulty = 0
        self.currentHeuristic = [0, 0]
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
            print('Heuristica PC: ' + str(self.currentHeuristic[0]))
            self.buttons[self.findBt()][0].config(bg='blue')
            self.buttons[self.findBt()][0].config(state='disabled',
                                                  relief=tk.SUNKEN)
            self.state[self.buttons
                       [self.findBt()][2]][self.buttons[self.findBt()][3]] = 1

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
            self.calculate_heuristic_player()
            print('Player Heuristics: ' + str(self.currentHeuristic[1]))
            root.update()
            if (self.is_gameover_pc()):
                if (self.playAgainPlayer() == 1):
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1
            self.nextMove()
            print('PC Heuristics: ' + str(self.currentHeuristic[0]))
            if (self.is_gameover_player()):
                if (self.playAgainPC() == 1):
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1
        elif (self.player == -1 and self.state[self.buttons
                                               [btn][2]][self.buttons
                                                         [btn][3]] == 0):
            self.buttons[btn][0].config(bg='red')
            self.buttons[btn][0].config(state='disabled', relief=tk.SUNKEN)
            self.state[self.buttons[btn][2]][self.buttons[btn][3]] = -1
            self.calculate_heuristic_player()
            print('Player Heuristics: ' + str(self.currentHeuristic[1]))
            if (self.is_gameover_pc()):
                if (self.playAgainPlayer() == 1):
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1
            self.nextMove()
            print('PC Heuristics: ' + str(self.currentHeuristic[0]))
            if (self.is_gameover_player()):
                if (self.playAgainPC() == 1):
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1

    def choosePlayer(self):
        msg = 'Do you want to play first?'
        answer = messagebox.askquestion('Play First', msg)
        if answer == 'yes':
            return 1
        else:
            return -1

    def playAgainPlayer(self):
        msg = 'Congratulations! You won!\n Do you want to play again?'
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

    def calculate_heuristic_pc(self):
        self.currentHeuristic[0] = calculateHeuristic(self.state, self.pc)
        pass

    def calculate_heuristic_player(self):
        self.currentHeuristic[1] = calculateHeuristic(self.state,
                                                           self.player)
        pass

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
        self.calculate_heuristic_pc()
        return True

    def is_valid_move(self):
        if self.state[self.nextMovement[0]][self.nextMovement[1]] == 0:
            return True
        else:
            return False

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
            print('Heuristica PC: ' + str(self.currentHeuristic[0]))
            self.buttons[self.findBt()][0].config(bg='blue')
            self.buttons[self.findBt()][0].config(state='disabled',
                                                  relief=tk.SUNKEN)
            self.state[self.buttons
                       [self.findBt()][2]][self.buttons[self.findBt()][3]] = 1


def main():
    global root
    root = tk.Tk()
    root.geometry('840x660+250+0')
    root.title('Gomoku Game')
    #root.iconbitmap("../img/favicon.ico")
    game = Game(root) #Call the class Game
    root.mainloop() #Start the game!


if __name__ == '__main__':
    main()
