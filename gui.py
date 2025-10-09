#GUI to attach files for parsing by parser_engine

from tkinter import ttk, filedialog
from tkinter import *
from tkinter.ttk import *
import os
import parser_engine

#GUI setup
root = Tk()
root.title("Welcome to Logform Interp")
root.geometry("500x500")
root.resizable(width=True,height=True)
root.configure(background="lightgray")

#Get file path depending on what user selects with OS Explorer
def getfile_path():
    path = filedialog.askopenfilename(title="Select a file to upload", filetypes=[("Text Files", ".txt"),("Log Files", ".log"),("DMP Files", ".dmp"),("NFO Files", ".nfo")])
    if not path:
        errors_box.insert("end", "Error: No file selected. \n")
    else:
        #Debug - prints user selected path.
        errors_box.insert("end", f"Path {path} was selected. \n")
        parser_engine.validate_input_path(path)
        return

#File attach button
attach_button = ttk.Button(root, text="Choose a file", command=getfile_path)
ttk.Button.pack(attach_button, side="bottom", pady="100")

#Error feedback for user
errors_box = Text(root, height= 10, width=50)
errors_box.pack(side="top", pady="100", anchor="center", expand=True, fill="both")
errors_box.see("end")

#Tkinter display start
root.mainloop()