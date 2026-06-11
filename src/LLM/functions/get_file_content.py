import os
from config import MAX_CHARS

get_file_content_schema = {
      "type": "function",
      "function": {
        "name": "get_file_content",
        "description": "Retrieves file content in a specified directory relative to the working directory.",
        "parameters": {
          "type": "object",
          "required": ["path"],
          "properties": {
            "path": {"type": "string", "description": "File path to list files from, relative to the working directory (default is the working directory itself)"}}}}}

def get_file_content(working_directory, path):

    working_directory_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_directory_abs, path))

    dir_list = [working_directory_abs, target_path]

    valid_target_dir = os.path.commonpath(dir_list)

    if valid_target_dir != working_directory_abs:
        return f'Error: Cannot read "{path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{path}"'
    
    try:
        with open(target_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1) != "":
                content += f'[...File "{path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f"Error: {e}"
    
    return content