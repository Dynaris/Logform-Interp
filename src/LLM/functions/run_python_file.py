import os
import subprocess

run_python_file_schema = {
      "type": "function",
      "function": {
        "name": "run_python_file",
        "description": "Runs files in a specified directory relative to the working directory.",
        "parameters": {
          "type": "object",
          "required": ["path"],
          "properties": {
            "path": {"type": "string", "description": "File path to list files from, relative to the working directory (default is the working directory itself)"}}}}}

def run_python_file(working_directory, path, args=None):

    #get the absolute path for both work directory and file path
    target_file_path = os.path.normpath(os.path.join(working_directory, path))
    abs_file_path = os.path.abspath(target_file_path)
    abs_working_directory = os.path.abspath(working_directory)

    #combine both paths
    dir_list = [abs_working_directory, abs_file_path]
    final_absolute_dir = os.path.commonpath(dir_list)

    ### set configurations for different outcomes ###
    if abs_working_directory != final_absolute_dir:
        return f'Error: Cannot execute "{path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: "{path}" does not exist or is not a regular file'

    if not path.endswith(".py"):
        return f'Error: "{path}" is not a Python file'
    
    ###

    # create a way to add more arguments into the function via args with .extend()
    command = ["python", abs_file_path]

    if args is not None:
        command.extend(args)
    
    # try to run using subprocess
    try:
        result = subprocess.run(command, cwd= final_absolute_dir, capture_output= True, text= True, timeout=30)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    # create output messaging with variable outcomes
    output_messages = ""
    
    if result.returncode != 0:
        output_messages += f"Process exited with code {result.returncode}"

    if not result.stdout and not result.stderr:
        output_messages += "No output produced"
    
    if result.stdout:
        output_messages += f"STDOUT:{result.stdout}\n"
    
    if result.stderr:
        output_messages += f"STDERR:{result.stderr}\n"

    return output_messages