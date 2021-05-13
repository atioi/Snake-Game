import tkinter
from tkinter import *


def rgb(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'


root = Tk()

my_canva = tkinter.Canvas(root, width=500, height=500, bg=rgb(175, 215, 70))
my_canva.pack()

rect = my_canva.create_rectangle(0, 0, 100, 100, fill='black')


root.config(bg=rgb(175, 215, 70))
root.title('Snake')
root.iconbitmap('./snake.ico')
root.resizable(False, False)
root.geometry("500x500")

root.mainloop()
