#GUI to attach files for parsing by parser_engine
from tkinter import ttk, filedialog
from tkinter import *
import common
import parser_engine
import threading
from app_requirements import local_llm_ready
import time

#GUI setup
def gui_launch():
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
            return parser_engine.validate_input_path(path)

    ## File attach button configuration.
    attach_button = ttk.Button(root, text="Choose a file", command=lambda: threading.Thread(target=getfile_path, daemon=True).start(), state="disabled")
    attach_button.pack(side="bottom", pady=100)



    #Disables attach button until all requirements are met, whilst checking for said requirements.
    def on_startup_config():
        
        threading.Thread(
            target=startup_validation_worker, 
            daemon=True
        ).start()

    def startup_validation_worker():

        max_attempts = 3

        for attempt in range(max_attempts):
            if local_llm_ready():

                root.after(
                    0,
                    startup_success
                )
                
                return True
            
            print(f"Startup validation failed. Attempt {attempt + 1}/{max_attempts}")
            time.sleep(2)
            
        root.after(
            0,
            startup_failure
        )
        
        return False
                
    def startup_success():
        print("LLM flag value:", common.local_llm_ready_flag) #Debug
        print("Program meets all prerequisites.\n ") #Debug
        common.local_llm_ready_flag = True
        attach_button.config(state="normal")
    
    def startup_failure():
        print("LLM flag value:", common.local_llm_ready_flag) #Debug
        print("Program does not meet prerequisites to run.\n ") #Debug
        errors_box.insert("end", "Program does not meet all prerequisites.\n")
        common.local_llm_ready_flag = False
        attach_button.config(state="disabled")

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