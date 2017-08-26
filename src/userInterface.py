#!/usr/bin/python3.4
from tkinter import *
import time
from tkinter.messagebox import *
import random
import numpy as np
from functools import partial
from heuristic import *
from decideMove import *


class Game:

    def __init__(self, master,utility, heuristic, finalState):

#        self.flags = 60
        
        self.masterParameter = master
        
        self.createButtons(master)
        self.difficulty = 0
        
        self.utility = utility
        self.heuristic = heuristic
        
        self.actualHeuristic = [0,0]
        
        self.finalState = finalState
        
        self.state= np.zeros((15,15))
        
        self.bottomFrame = Frame(root)
        self.bottomFrame.grid(row=15, columnspan=155)

        self.quitBtn = Button(self.bottomFrame, text='Quit', command=self.quit)
        self.quitBtn.grid(row=18, columnspan=5)
        
        reset_with_arg = partial(self.reset, master)   
        
        self.Reset = Button(self.bottomFrame, text='Reset Game', command=reset_with_arg )
        self.Reset.grid(row=19, columnspan=5)
        
        self.btn = Button(self.bottomFrame, text='My text' )
        self.btn.config(state='disabled', relief=SUNKEN)
        
        self.heuristic_val = 0
        
        self.nextMovement = [0,0]
               
        self.player = self.choosePlayer()
        self.pc = -1
        
        if(self.player==-1):
            self.pc = 1
            self.nextMove()
            print('Heuristica PC: ' + str( self.actualHeuristic[0]) )
            
            self.buttons[self.findBt()][0].config(bg='blue')
            self.buttons[self.findBt()][0].config(state='disabled', relief=SUNKEN)
            self.state[self.buttons[self.findBt()][2]][self.buttons[self.findBt()][3]] =1
       
    

    def createButtons(self, parent):
        self.buttons = {}
        row = 0
        col = 0
        for x in range(0, 15*15):
            
            id=str(row) + '-' + str(col)
            self.buttons[x] = [
            Button(parent, bg='#8a8a8a',height = 2, width = 4),
            id, #player
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

    def leftClick_w(self, x):
        return lambda Button: self.leftClick(x)

    def rightClick_w(self, x):
        pass
#       return lambda Button: self.rightClick(x)
        
    def leftClick(self, btn):
        
        if ( self.player==1  and self.state[self.buttons[btn][2]][self.buttons[btn][3]]== 0) :
            self.buttons[btn][0].config(bg='blue')
            self.buttons[btn][0].config(state='disabled', relief=SUNKEN)
            self.state[self.buttons[btn][2]][self.buttons[btn][3]] =1
            self.calculate_heuristic_player()
            print('Heuristica Player: ' + str( self.actualHeuristic[1]) )
            if (self.is_gameover_pc()):
                if (self.playAgainPlayer()==1):
                    print('--------------------')
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1
                
            
            
            self.nextMove()
            print('Heuristica PC: ' + str( self.actualHeuristic[0]) )                                    
            
            
            if (self.is_gameover_player()):
                if (self.playAgainPC()==1):
                    print('--------------------')
                    self.Reset.invoke()
                    return 1
                    
                else:
                    self.quitBtn.invoke()
                    return 1
            
            

        elif (self.player == -1 and self.state[self.buttons[btn][2]][self.buttons[btn][3]]== 0):
            self.buttons[btn][0].config(bg='red')
            self.buttons[btn][0].config(state='disabled', relief=SUNKEN)
            self.state[self.buttons[btn][2]][self.buttons[btn][3]] = -1
            self.calculate_heuristic_player()
            print('Heuristica Player: ' + str( self.actualHeuristic[1]) )
            if (self.is_gameover_pc()):
                if (self.playAgainPlayer()==1):
                    print('--------------------')
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1
            
            
            self.nextMove()
            print('Heuristica PC: ' + str( self.actualHeuristic[0]) )           
            
            
            if (self.is_gameover_player()):
                if (self.playAgainPC()==1):
                    print('--------------------')
                    self.Reset.invoke()
                    return 1
                else:
                    self.quitBtn.invoke()
                    return 1
        
    def choosePlayer(self):
        msg = 'Do you want to play first?'
        answer = askquestion('PLay First',msg)
        if answer == 'yes':
            return 1
        else:
            return -1
    
    def playAgainPlayer(self):
        msg = 'Congratulations! You win! Do you want to play again?'
        answer = askquestion('play again',msg)
        if answer == 'yes':
            return 1
        else:
            return -1
    
    def playAgainPC(self):
        msg = ':-( You lose!  Do you want to play again?'
        answer = askquestion('play again',msg)
        if answer == 'yes':
            return 1
        else:
            return -1
        
    def is_gameover_pc(self):
        # A board is terminal if it is won or there are no empty spaces.
        if (0 in self.state and finished(self.state, self.finalState,self.player)):
            return False
        else:
            
            return True
    
    def is_gameover_player(self):
        # A board is terminal if it is won or there are no empty spaces.
        if ( 0 in self.state  and finished(self.state, self.finalState,self.pc) ):
            
            return False
        else:
            
            return True
        
    
    def findBt(self):
        for b in self.buttons.keys():
            if (self.buttons[b][2]==self.nextMovement[0] and self.buttons[b][3]==self.nextMovement[1]):
                return b
        
    def calculate_heuristic_pc(self):
        self.actualHeuristic[0]= calculateHeuristic(self.state, self.utility, self.heuristic, self.pc)
               
        pass
    
    def calculate_heuristic_player(self):
        self.actualHeuristic[1] = calculateHeuristic(self.state, self.utility, self.heuristic, self.player)
              
        pass
    
    def nextMove(self):
             
       self.nextMovement =  decideMove()
       
  
       if (self.player ==1):
            self.buttons[self.findBt()][0].config(bg='red')
            self.buttons[self.findBt()][0].config(state='disabled', relief=SUNKEN)
            self.state[self.buttons[self.findBt()][2]][self.buttons[self.findBt()][3]] =-1
       else:
            self.buttons[self.findBt()][0].config(bg='blue')
            self.buttons[self.findBt()][0].config(state='disabled', relief=SUNKEN)
            self.state[self.buttons[self.findBt()][2]][self.buttons[self.findBt()][3]] =1
            
       self.calculate_heuristic_pc()
       
       
       return True
   
    
    
        
    def is_valid_move(self):
       if self.state[self.nextMovement[0]][self.nextMovement[1]]== 0:
          return True
       else:
         return False    
           

    def quit(self):
        global root
        root.destroy()
        
    def reset(self,master):
        print('--------------------')
        self.nextMovement = [0,0]
        self.state= np.zeros((15,15))
        for btn in self.buttons.keys():
            self.buttons[btn][0].destroy()
        self.createButtons(master)
        self.player = self.choosePlayer()
        if(self.player==-1):
            
            self.nextMove()
            print('Heuristica PC: ' + str( self.actualHeuristic[0]) )
            
            self.buttons[self.findBt()][0].config(bg='blue')
            self.buttons[self.findBt()][0].config(state='disabled', relief=SUNKEN)
            self.state[self.buttons[self.findBt()][2]][self.buttons[self.findBt()][3]] =1


def main():
    global root
    root = Tk()
    root.geometry('580x680+250+0')
    root.title('Gomoku Game')
    game = Game(root,Utility, Heuristic, Finished)
    root.iconbitmap("C:/Andrei/ine5430-gomoku/img/favicon.ico")
    root.mainloop()


if __name__ == '__main__':
    main()
