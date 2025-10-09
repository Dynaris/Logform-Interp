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
            print("About to call parse.") #Debug
            parsed = parse_file(path, extension) # Run parsing, since all checks came back valid.
            return parsed
        else:
            return gui.errors_box.insert("end", "Error: File extension from selected file is not valid. \n")

# engine core mechanics (parsing files after validation)
def parse_file(path, extension):
    print("Parse file command has been reached.") #Debug
    text_based_ext = {".txt", ".log"}
    text_based_special = {".nfo"}
    binary_based_ext = {".dmp"}
    encodings_list = ["utf-8", "latin-1", "cp1252", "cp437"]
    Github_Issues = "https://github.com/Dynaris/Logform-Interp/issues"

    # .TXT, .LOG, .CEF3 (text)
    print("Detect encoding needed.") #Debug
    for encoding in encodings_list:
        try:
            if extension in text_based_ext:
                with open(path, "r", encoding=encoding) as text:
                    print("Parsing lines... ")
                    lines = text.readlines()
                    result = decoded_text_validation("".join(lines))
                    if result:
                        gui.errors_box.insert("end", f"The following lines were found: {lines}.")  # Needs to be moved to a new window
                        return lines
                    else:
                        continue
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Exception while parsing with {encoding}: {e}")
            continue

    #If no encoding works from the list
    gui.errors_box.insert("end", "Unable to parse file. \n")
    gui.errors_box.insert("end", f"Please report the issue via Github at {Github_Issues}\n. DISCLAIMER: I may not be able to provide the expected response rate, or return with a solution. I ask for your understanding as this is an experimental project to showcase my personal skills.")
    return "Unable to parse file"

    #.NFO (convert to text) - This removes any possible existent incompatibilities due to OS versions - NOT TO BE INCLUDED IN DEMO
    #.DMP (binary) - NOT TO BE INCLUDED IN DEMO

def decoded_text_validation(text): #check for a ratio of printable characters, check for line breaks, return boolean as a result and an error if Invalid
    """
    When taking in a document, independent of the extension and encoder chosen, the file may still open, despite all of its contents not be readable.
    This is a false-positive that can take place, and needs measures of evaluation to address (i.e. requirements).

    The requirements for the decoded text to be accepted are:
    - Printable characters (ratio) - At least 70% of the file's characters.
    - Min. Line breaks - 10
    - Min. char. limit - 50
    """

    print(f"Type of text is: {type(text)}.") #Debug

    #Replaces any Windows Return + Newline, into a universal newline for all Operating Systems
    text = text.replace("\r\n", "\n")

    #Removes any encoding noise that may be interpreted as a bad character and unfairly contribute to a file being invalid.
    text = text.lstrip("\ufeff")

    special_chars = ["\n", "\r", "\t"]
    bad_char_count = 0
    line_break_count = text.count("\n")

    #check character limit
    gui.errors_box.insert("end", "Checking file character limit... \n")
    total_characters = len(text)
    print(f"The total character count found is: {total_characters}.") #Debug
    if total_characters <= 50:
        gui.errors_box.insert("end", "File is not valid. \n")
        return False

    #check for printable characters (readability) (i.e. "NULL", "\x00", etc)
    gui.errors_box.insert("end", "Checking file character validity... \n")
    for char in text:
        if not (char.isprintable() or char in special_chars):
            bad_char_count +=1

    char_ratio = bad_char_count / len(text)
    print(f"The percentage of bad characters is: {char_ratio}. ") #Debug
    if char_ratio >= 0.3:
        gui.errors_box.insert("end", "File is not valid. \n ")
        return False

    #check for line breaks
    gui.errors_box.insert("end", "Checking line break count... \n")
    print(f"The number of line breaks found, is: {line_break_count}.")
    if line_break_count <= 10:
        gui.errors_box.insert("end", "File is not valid. \n")
        return False

    #if all requirements are valid, return True
    print("True was returned") #Debug
    return True