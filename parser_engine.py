import os
import gui

#engine core mechanics (validate file selection and return feedback to user based on selection)
def validate_input_path(path):
    allowed_extensions = {".txt", ".log", ".dmp", ".nfo"}  # List of accepted file extensions

    if not os.path.exists(path): #Check if a path exists
        return gui.errors_box.insert("end", "Error: File does not exist, or was not selected. \n")
    elif not os.path.isfile(path): #Check if path is a file
        return gui.errors_box.insert("end", "Error: Selected item is not expected file type. Ensure only eligible files (i.e. '.txt' '.log' '.dmp' '.nfo' ) are selected. Note that DEMO version only encompasses '.txt' '.log'. \n")
    else:
        filename, extension = os.path.splitext(path) #If a valid file, split the text into filename, and extension.
        extension = extension.lower().strip() #Convert all casing to lower and remove white spacing

        #Check if extension is valid and parse, if it is
        if extension in allowed_extensions:
            gui.errors_box.insert("end", f"Extension '{extension}' found. File is valid and will now be parsed. \n")
            parsed = parse_file(path, extension) # Run parsing, since all checks came back valid.
            print("About to call parse. ")
            return parsed
        else:
            return gui.errors_box.insert("end", "Error: File extension from selected file is not valid. \n")

# engine core mechanics (parsing files after validation)
def parse_file(path, extension):
    print("Parse file command has been reached. ")
    text_based_ext = {".txt", ".log"}
    text_based_special = {".nfo"}
    binary_based_ext = {".dmp"}

    # .TXT, .LOG (text)
    try:
        if extension in text_based_ext: #attempt encoding utf-8
            print("Extension set check.")
            with open(path, "r", encoding="utf-8") as text:
                print("Parsing lines")
                lines = text.readlines()
            print(lines)
            gui.errors_box.insert("end", f"The following lines were found: {lines}") #Needs to be moved to a new window.
        else:
            return gui.errors_box.insert("end", "There was an error parsing file's extension.")
    except UnicodeDecodeError:
        try:
            if extension in text_based_ext: #attempt encoding latin-1
                print("Unicode error found, retrying.")
                with open(path, "r", encoding="latin-1") as text:
                    print("Parsing lines")
                    lines = text.readlines()
                print(lines)
                gui.errors_box.insert("end", f"The following lines were found: {lines}")
        except UnicodeDecodeError:
            if extension in text_based_ext: #attempt encoding cp1252
                print("Unicode error found, retrying.")
                with open(path, "r", encoding="cp1252") as text:
                    print("Parsing lines")
                    lines = text.readlines()
                print(lines)
                gui.errors_box.insert("end", f"The following lines were found: {lines}")
    except Exception as e:
        gui.errors_box.insert("end", f"Parsing failed: {e}.\n")
        print("Unreadable file. ")
        Github_Issues = "https://github.com/ByterMasterX/Logform-Interp/issues"
        return (f"Please report the issue via Github at {Github_Issues}\n. DISCLAIMER: I may not be able to provide the expected response rate, or return with a solution. I ask for your understanding as this is an experimental project to showcase my personal skills.")

        #.NFO (convert to text) - This removes any possible existent incompatibilities due to OS versions

        #.DMP (binary)