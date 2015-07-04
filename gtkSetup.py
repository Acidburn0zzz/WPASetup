__author__ = 'ryanvade'

from Tkinter import * # Python 3.x: from tkinter import *

def advance():
    lb['text'] = str(int(lb['text']) + 1)
    root.after(1000, advance)

root = Tk()
lb = Label(root, text='0')
lb.pack()
root.after(1000, advance)
root.mainloop()