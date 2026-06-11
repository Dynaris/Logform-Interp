import os

write_file_schema = {
      "type": "function",
      "function": {
        "name": "write_file",
        "description": "Writes files in a specified directory relative to the working directory.",
        "parameters": {
          "type": "object",
          "required": ["path", "content"],
          "properties": {
            "path": {"type": "string", "description": "File path to list files from, relative to the working directory (default is the working directory itself)"},
            "content": {"type": "string", "description": "The text content to write to the file"}}}}}

def write_file(working_directory, path, content):

    working_directory_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_abs, path))

    dir_list = [working_directory_abs, target_dir]

    valid_target_dir = os.path.commonpath(dir_list)

    parent_directory = os.path.dirname(target_dir)

    if valid_target_dir != working_directory_abs:
        return f'Error: Cannot write to "{path}" as it is outside the permitted working directory'
    
    if os.path.isdir(target_dir):
        return f'Error: Cannot write to "{path}" as it is a directory'
    
    try:
        os.makedirs(parent_directory, exist_ok=True)
        with open(target_dir, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    