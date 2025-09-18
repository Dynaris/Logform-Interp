#GUI to attach files for parsing by parser_engine

from tkinter import ttk, filedialog
from tkinter import *
from tkinter.ttk import *
import os

#GUI setup
root = Tk()
root.title("Welcome to Logform Interp")
root.geometry("500x500")
root.resizable(width=True,height=True)
root.configure(background="white")

#Get file path depending on what user selects with OS Explorer
def getfile_path():
    filedialog.askopenfilename(title="Select a file to upload", filetypes=[("Text Files", ".txt"),("Log Files", ".log"),("DMP Files", ".dmp"),("NFO Files", ".nfo")])

#File attachment button
attach_button = ttk.Button(root, text="Choose a file", command=getfile_path)
ttk.Button.pack(attach_button, side="bottom", pady="100")

#Tkinter display start
root.mainloop()
