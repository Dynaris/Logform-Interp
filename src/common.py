#Common module to talk between libraries, to avoid circular library import.

errors_box = None
local_llm_ready_flag = False

#Prints messages to Tkinter GUI through the usage of "log_message" function.
def log_message(message):
    print(f"Updated user with message '{message}'.\n") #Debug
    if errors_box is not None:
        try:
            errors_box.insert("end", message +"\n")
            errors_box.see("end")
        except:
            print("GUI is not ready...\n")