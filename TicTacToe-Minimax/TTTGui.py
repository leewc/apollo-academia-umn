#!/usr/bin/python3

from tkinter import Frame, Canvas, Label, Button, LEFT,RIGHT, ALL, Tk
from tkinter.font import Font

class TTTGui:
    def __init__(self, controller, dimension):
        self.controller = controller

        self.root = Tk()  # put this here removes Tkinter dep in the Controller
        self.root.title('TicTacToe')
        self.root.resizable(width=False, height=False)

        self.font = Font(family="Helvetica", size=32)
        self.buttons = {}

        self.dimension = dimension
        self.draw_grids()
        self.load_restart_button()
        
    def draw_grids(self):
        for x in range (0, self.dimension):
            for y in range(0, self.dimension):
                handler = lambda x=x,y=y: self.playerMoved(x, y)
                button = Button(self.root, command=handler  , width=20, height=10)
                button.grid(row=y, column=x)
                self.buttons[x,y] = button

    def load_restart_button(self):
        handler = lambda: self.restart()
        button = Button(self.root, text='Restart',font=self.font, command=handler)
        button.grid(row=self.dimension + 1, column=0, columnspan=self.dimension, sticky="WE")
        self.root.update()


    def playerMoved(self, x, y):
        print('Got object click', x,y)
        self.controller.updateModel(x, y)            

    def start(self):
        self.root.mainloop()