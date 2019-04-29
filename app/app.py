"""
Driver file
"""
import tkinter as tk
from tkinter import *
import gui

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)


root = tk.Tk()
root.geometry("400x300")
app = gui.DeepTopoWindow(root)
app.place(x=10,y=10) 
canvas = Canvas(app)
frame=Frame(canvas)
myscrollbar=Scrollbar(app,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)

root.mainloop()

