#!/usr/bin/python3.4
from tkinter import *
import time
from tkinter.messagebox import *
import random
import numpy as np

class Game:

    def __init__(self, master,player):

#        self.flags = 60
        self.createButtons(master)

        self.bottomFrame = Frame(root)
        self.bottomFrame.grid(row=15, columnspan=155)

        self.quitBtn = Button(self.bottomFrame, text='Quit', command=self.quit)
        self.quitBtn.grid(row=18, columnspan=2)
        
        self.player = []
        self.player.append(player)
        
        self.state= np.zeros((15,15))
    

    def createButtons(self, parent):
        self.buttons = {}
        row = 0
        col = 0
        for x in range(0, 15*15):
            status = 'danger'
            self.buttons[x] = [
            Button(parent, bg='#8a8a8a',height = 2, width = 4),
            [], #player
            row,
            col]
            

            self.buttons[x][0].bind('<Button-1>', self.leftClick_w(x))
            self.buttons[x][0].bind('<Button-3>', self.rightClick_w(x))
            
            #self.buttons[x][0].config( height = 10, width = 10 )
            col += 1
            if col == 15:
                col = 0
                row += 1
            for k in self.buttons:
                self.buttons[k][0].grid(row= self.buttons[k][2], column= self.buttons[k][3])

    #i don't know why but you'll get error if you remove these two functions
    def leftClick_w(self, x):
        return lambda Button: self.leftClick(x)

    def rightClick_w(self, x):
        pass
#       return lambda Button: self.rightClick(x)

    def leftClick(self, btn):
        
        if ( self.player[-1]==1  and self.state[self.buttons[btn][2]][self.buttons[btn][3]]== 0) :
            self.buttons[btn][0].config(bg='blue')
            self.buttons[btn][0].config(state='disabled', relief=SUNKEN)
            self.player.append(2)
            self.state[self.buttons[btn][2]][self.buttons[btn][3]] =1

        elif (self.player[-1] == 2 and self.state[self.buttons[btn][2]][self.buttons[btn][3]]== 0):
            self.buttons[btn][0].config(bg='red')
            self.buttons[btn][0].config(state='disabled', relief=SUNKEN)
            self.player.append(1)
            self.state[self.buttons[btn][2]][self.buttons[btn][3]] = 2
            
        
    
           

    def quit(self):
        global root
        root.quit()


def main():
    global root
    root = Tk()
    root.geometry('580x650+0+0')
    root.title('Gomoku Game')
    game = Game(root,1)
    root.mainloop()


if __name__ == '__main__':
    main()
