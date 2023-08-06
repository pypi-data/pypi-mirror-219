from tkinter import *
def enterbox(title):
    windows = Tk()
    windows.geometry("350x200")
    windows.title(title)
    enter = Text(windows,width=20,height=20)
    enter.grid(column=0,row=0)
    windows.mainloop()
    out = enter.get()
    return out
