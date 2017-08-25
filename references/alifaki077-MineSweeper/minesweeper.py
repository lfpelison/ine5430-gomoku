#!/usr/bin/python3.4
from tkinter import *
import time
from tkinter.messagebox import *
import random

class Game:

    def __init__(self, master):

        self.flags = 60
        self.createButtons(master)

        self.bottomFrame = Frame(root)
        self.bottomFrame.grid(row=11, columnspan=10)

        self.flagRemainning = Label(self.bottomFrame, text='Flag Remaining : '+str(self.flags))
        self.flagRemainning.grid(row=12)

        self.quitBtn = Button(self.bottomFrame, text='Quit', command=self.quit)
        self.quitBtn.grid(row=13, columnspan=2)

        self.total = 0
        self.count = 0
        for i in self.buttons:
            if self.buttons[i][4][0] == 1:
                self.total += 1

    def createButtons(self, parent):
        self.buttons = {}
        row = 0
        col = 0
        for x in range(0, 200):
            status = random.choice(['safe', 'danger'])
            self.buttons[x] = [
            Button(parent, bg='#8a8a8a'),
            status,
            row,
            col,
            [0 if status == 'danger' else 1]
            ]

            self.buttons[x][0].bind('<Button-1>', self.leftClick_w(x))
            self.buttons[x][0].bind('<Button-3>', self.rightClick_w(x))
            col += 1
            if col == 20:
                col = 0
                row += 1
            for k in self.buttons:
                self.buttons[k][0].grid(row= self.buttons[k][2], column= self.buttons[k][3])

    #i don't know why but you'll get error if you remove these two functions
    def leftClick_w(self, x):
        return lambda Button: self.leftClick(x)

    def rightClick_w(self, x):
        return lambda Button: self.rightClick(x)

    def leftClick(self, btn):
        check = self.buttons[btn][1]
        if check == 'safe':

            self.buttons[btn][0].config(bg='green')
            self.buttons[btn][0].config(state='disabled', relief=SUNKEN)
            self.count += 1
            self.nearbyMines(btn)
            self.showNearby(btn)
            win = self.checkWin()
            if win:
                self.victory()

        if check == 'danger':
            self.buttons[btn][0].config(bg='red')
            self.buttons[btn][0].config(state='disabled', relief=SUNKEN)
            self.lost()

    def rightClick(self, btn):
        if self.flags > 0:
            self.buttons[btn][0].config(bg='blue')
            self.buttons[btn][0].config(state='disabled', relief=SUNKEN)
            self.flags -= 1
            self.flagRemainning.config(text= 'Flag Remaining : '+str(self.flags))
            if self.buttons[btn][1] == 'safe':
                self.count += 1

        else:
            showinfo('no flags', 'you run out of flags')

    def showNearby(self, btn):
        if btn > 20 and btn < 190:
            self.possible = [btn-21,btn+21, btn-20, btn+20,btn-19, btn+19,btn+1, btn-1]
            for i in self.possible:
                try:
                    if self.buttons[i][1] == 'safe':
                        if self.buttons[i][0]['bg'] == 'green':
                            continue
                        else:
                            self.buttons[i][0].config(bg='green')
                            self.buttons[i][0].config(state='disabled', relief=SUNKEN)
                            self.count += 1
                            self.buttons[i][4][0] == 0
                            self.nearbyMines(i)
                except KeyError:
                    pass

            if self.checkWin():
                self.victory()

    def nearbyMines(self, btn):
        self.near = 0
        if btn > 20 and btn < 190:
            self.pos = [btn-21,btn+21, btn-20, btn+20,btn-19, btn+19,btn+1, btn-1]
            for i in self.pos:
                try:
                    if self.buttons[i][1] == 'danger':
                        self.near += 1
                except KeyError:
                    pass
        if btn < 20:
            self.pos2 = [btn+21,btn+20, btn+19,btn+1]
            for i in self.pos:
                try:
                    if self.buttons[i][1] == 'danger':
                        self.near += 1
                except KeyError:
                    pass
        if btn > 190:
            self.pos3 = [btn-21,btn-20, btn-19,btn-1]
            for i in self.pos:
                try:
                    if self.buttons[i][1] == 'danger':
                        self.near += 1
                except KeyError:
                    pass
        self.buttons[btn][0].config(text=str(self.near), font=('Helvetica', 7))

    def lost(self):
        global root
        for i in self.buttons:
            if self.buttons[i][1] == 'danger':
                self.buttons[i][0].config(bg='red')
        time.sleep(1.5)
        msg = 'you lose ! do you want to play again?'
        answer = askquestion('play again',msg)
        if answer == 'yes':
            self.reset()
        else:
            self.quit()

    def victory(self):
        global root
        msg = 'congratulations you won ! do you want to play again?'
        answer = askquestion('play again',msg)
        if answer == 'yes':
            self.reset()
        else:
            self.quit()

    def reset(self):
        self.flags = 50
        self.flagRemainning.config(text= 'Flag Remaining : '+str(self.flags))
        for i in self.buttons:
            self.buttons[i][0].config(bg='#8a8a8a', text='')
            self.buttons[i][0].config(state='normal', relief=RAISED)
            self.buttons[i][1] = random.choice(['safe', 'danger'])
        self.count = 0
        self.total = 0
        for i in self.buttons:
            if self.buttons[i][4][0] == 1:
                self.total += 1

    def checkWin(self):
        return self.count == self.total

    def quit(self):
        global root
        root.quit()


def main():
    global root
    root = Tk()
    root.title('MiNeSwEePeR')
    game = Game(root)
    root.mainloop()

if __name__ == '__main__':
    main()
