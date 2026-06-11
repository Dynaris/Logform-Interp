import os

get_files_info_schema = {
      "type": "function",
      "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
          "type": "object",
          "required": [],
          "properties": {
            "path": {"type": "string", "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)"}}}}}

def get_files_info(working_directory, path="."):

    working_directory_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_abs, path))

    dir_list = [working_directory_abs, target_dir]

    valid_target_dir = os.path.commonpath(dir_list)

    if valid_target_dir != working_directory_abs:
        return f'Error: Cannot list "{path}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir):
        return f'Error: "{path}" is not a directory'

    result_list = []

    try:
        for item in os.listdir(target_dir):  
                item_path = os.path.join(target_dir, item)
                output = f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
                result_list.append(output)
    except Exception as e:
        return f"Error: {e}"

    return ("\n".join(result_list))