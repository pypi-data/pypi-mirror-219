from tkinter import *
def enterbox(title):
    windows = Tk()
    windows.geometry("350x200")
    windows.title(title)
    def clicked():
        out = enter.get()
        return out
    b1 = Button(windows,width=10,text='click',command=clicked).grid(column=0,row=1)
    enter = Entry(windows,width=30)
    enter.grid(column=0,row=0)
    windows.mainloop()
