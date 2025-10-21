#GUI to attach files for parsing by parser_engine
from tkinter import ttk, filedialog
from tkinter import *
from src import common
from src import parser_engine

#GUI setup
root = Tk()
root.title("Welcome to Logform Interp")
root.geometry("500x500")
root.resizable(width=True,height=True)
root.configure(background="lightgray")

disclaimer = (
    "\n⚠️ DISCLAIMER:\n"
    "These troubleshooting steps are provided for informational purposes only.\n"
    "If you are unsure about any recommendation, consult a qualified technician.\n"
    "The developer assumes no liability for any damage or data loss resulting from\n"
    "actions taken based on this analysis.\n\n"
)

#Get file path depending on what user selects with OS Explorer
def getfile_path():
    path = filedialog.askopenfilename(title="Select a file to upload", filetypes=[("Text Files", ".txt"),("Log Files", ".log"),("DMP Files", ".dmp"),("NFO Files", ".nfo")])
    if not path:
        errors_box.insert("end", "No file selected. \n")
    else:
        #Debug - prints user selected path.
        errors_box.insert("end", f"Path {path} was selected. \n")
        parser_engine.validate_input_path(path)
        return

#File attach button
#attach_button = ttk.Button(root, text="Choose a file", command=getfile_path)
#ttk.Button.pack(attach_button, side="bottom", pady="100")

attach_button = ttk.Button(root, text="Choose a file", command=getfile_path, state="disabled")
attach_button.pack(side="bottom", pady=100)

#Disables attach button until all requirements are met
def on_startup_config(retry=False):
    from app_requirements import local_llm_ready

    if local_llm_ready():
        print("LLM flag value:", common.local_llm_ready_flag) #Debug
        print("Program meets all prerequisites.\n ") #Debug
        errors_box.insert("end", "Program meets all prerequisites.\n")
        common.local_llm_ready_flag = True
        attach_button.config(state="normal")
        return True
    else:
        print("LLM flag value:", common.local_llm_ready_flag) #Debug
        print("Program does not meet prerequisites to run.\n ") #Debug
        errors_box.insert("end", "Program does not meet all prerequisites.\n")
        common.local_llm_ready_flag = False
        attach_button.config(state="disabled")
        if not retry:
            return on_startup_config(retry=True)
        else:
            common.local_llm_ready_flag = False
            print("LLM flag value:", common.local_llm_ready_flag) #Debug
            print("Recursive attempt also failed to meet prerequisites.\n ") #Debug
            errors_box.insert("end", "Program continues to not meet all prerequisites.\n")
            return False

#Error feedback for user
errors_box = Text(root, height= 10, width=50)
errors_box.pack(side="top", pady=100, anchor="center", expand=True, fill="both")
errors_box.see("end")

#Print disclaimer
errors_box.insert("end", disclaimer)

#Common libraries module details
common.errors_box = errors_box

#Application start
root.after(200, on_startup_config)
root.mainloop()