from tkinter import *

def clicked():
    lbl.configure(text="Button clicked!")

root = Tk()
root.title("Tkinter Demo")
root.geometry('300x200')

lbl = Label(root, text="Hello Tkinter")
lbl.pack(pady=10)

btn = Button(root, text="Click Me", command=clicked)
btn.pack(pady=10)

root.mainloop()
