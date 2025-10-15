import os
import gui
import re

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
                    text_content = "".join(lines)
                    if decoded_text_validation(text_content):
                        #gui.errors_box.insert("end", f"The following lines were found: {lines}.")  # Needs to be moved to a new window
                        print("Keyword hunt is running...") #Debug
                        return keyword_id(text_content)
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

def decoded_text_validation(text_content): #check for a ratio of printable characters, check for line breaks, return boolean as a result and an error if Invalid
    """
    When taking in a document, independent of the extension and encoder chosen, the file may still open, despite all of its contents not be readable.
    This is a false-positive that can take place, and needs measures of evaluation to address (i.e. requirements).

    The requirements for the decoded text to be accepted are:
    - Printable characters (ratio) - At least 70% of the file's characters.
    - Min. Line breaks - 10
    - Min. char. limit - 50
    """

    print(f"Type of text is: {type(text_content)}.") #Debug

    #Replaces any Windows Return + Newline, into a universal newline for all Operating Systems
    text_content = text_content.replace("\r\n", "\n")

    #Removes any encoding noise that may be interpreted as a bad character and unfairly contribute to a file being invalid.
    text_content = text_content.lstrip("\ufeff")

    special_chars = ["\n", "\r", "\t"]
    bad_char_count = 0
    line_break_count = text_content.count("\n")

    #check character limit
    gui.errors_box.insert("end", "Checking file character limit... \n")
    total_characters = len(text_content)
    print(f"The total character count found is: {total_characters}.") #Debug
    if total_characters <= 50:
        gui.errors_box.insert("end", "File is not valid. \n")
        return False

    #check for printable characters (readability) (i.e. "NULL", "\x00", etc)
    gui.errors_box.insert("end", "Checking file character validity... \n")
    for char in text_content:
        if not (char.isprintable() or char in special_chars):
            bad_char_count +=1

    char_ratio = bad_char_count / len(text_content)
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

def keyword_id(text_content):

    text_content_lower = text_content.lower()
    lines = text_content_lower.splitlines()

    #Keyword dictionary last update date: 15-Oct-25
    #Works as a temporary database of keywords, when parsing through attached files.
    keyword_dictionary = {
        "Errors": {"error", "failed", "fail", "failure", "fatal", "exception", "critical","crash", "abort", "terminate", "stacktrace", "traceback", "panic", "bugcheck", "core dump", "segfault", "access violation"},
        "Warnings": {"warning", "slow", "timeout", "lag", "retry", "deprecated", "unstable","overload", "bottleneck", "delayed", "throttled", "resource limit"},
        "Hardware": {"cpu", "processor", "core", "thread", "gpu", "graphics", "nvidia", "amd","ram", "memory", "disk", "hdd", "ssd", "drive", "storage", "io", "network","ethernet", "wifi", "bluetooth", "usb", "device", "bios", "firmware"},
        "Performance": {"performance", "utilization", "usage", "cpu load", "memory leak","out of memory", "cache", "latency", "benchmark", "optimize"},
        "Software": {"driver", "service", "module", "dependency", "dll", "library","process", "task", "daemon", "kernel", "system32", "executable","registry", "config", "settings", "permission", "access denied"},
        "Network": {"network", "socket", "connection", "connected", "disconnected","timeout", "unreachable", "dns", "ip", "http", "https", "port", "proxy", "server", "client", "handshake", "authentication", "ssl", "ftp"},
        "Security": {"security", "auth", "authentication", "unauthorized", "forbidden","access denied", "invalid credentials", "token", "certificate","encryption", "decryption", "ssl", "tls", "firewall", "virus", "malware"},
        "Storage": {"file", "read", "write", "save", "open", "close", "corrupted","missing", "not found", "ioerror", "permission denied", "path","directory", "mount", "unmount", "volume", "partition"},
        "Windows Known Errors": {"0x000000", "0x0000001a", "0x0000003b", "0x0000007e", "0x00000050","0x0000007b", "0x0000009f", "0x000000ef", "0x00000124", "0x00000133","0xc0000005", "0xc000021a", "0xc0000001", "0xc0000142", "0xc0000409","0xc000041d", "0xc000007b", "0x80070005", "0x80004005",},
        "BSOD": {"blue screen", "bsod", "stop code", "bugcheck", "system service exception","critical process died", "driver irql not less or equal","page fault in nonpaged area", "inaccessible boot device","dpc watchdog violation", "unexpected store exception","kernel security check failure", "memory management", "bad pool header","bad system config info", "irql not less or equal", "critical structure corruption",},
        "Module/DLL Errors": {"ntdll.dll", "kernel32.dll", "user32.dll", "win32k.sys","dxgmms2.sys", "hal.dll", "system32", "appcrash","application error", "runtime error", "fatal application exit","microsoft visual c++ runtime library",},
        "Windows Event Log": {"event id", "faulting module", "faulting application","windows error reporting", "wer", "bucket id", "fault bucket"}
    }

    #Create empty dictionary that mimics the categories (only) of the original one, to act as output storage.
    keyword_dictionary_output = { cat: [] for cat in keyword_dictionary}

    #Defining the matching level for words when outputting.
    keyword_parsing_requirements = {
        "Errors":"partial",
        "Warnings":"partial",
        "Hardware":"whole", #Prevent overlaps like “ram” in “program”.
        "Performance":"partial",
        "Software":"partial",
        "Network":"partial",
        "Security":"whole",
        "Storage":"whole", #“file” and “path” often appear inside longer words.
        "Windows Known Errors":"partial",
        "BSOD":"partial",
        "Module/DLL Errors":"partial",
        "Windows Event Log":"whole" #Match full terms like “Event ID 41” exactly.
    }

    #Keyword hunting logic - all case has been set to lowercase by text_lower variable, to avoid case-sensitive errors
    for line_number, line in enumerate(lines, start=1):
        line_lower = line.lower()
        for category, keywords in keyword_dictionary.items():
            #Default all keyword searching to partial.
            matching_mode = keyword_parsing_requirements.get(category,"partial")
            for kw in keywords:
                if matching_mode == "whole":
                    if re.search(rf"\b{re.escape(kw)}\b", line_lower):
                        print(f"Found a full match keyword: {kw} in category {category}.")
                        keyword_dictionary_output[category].append({
                            "line_number": line_number,
                            "contents": line.strip()
                        })
                elif matching_mode != "whole":
                    if kw in line_lower:
                        print(f"Found a matching keyword: {kw} in category {category}.")
                        keyword_dictionary_output[category].append({
                            "line_number": line_number,
                            "contents": line.strip()
                        })

    #Clean empty space in output dictionary
    filtered_output = {}
    for cat, entries in keyword_dictionary_output.items():
        if entries:
            filtered_output[cat] = entries

    gui.errors_box.insert("end", f"The following errors were found: {filtered_output}")
    print(filtered_output)