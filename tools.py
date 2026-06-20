from typing import Callable

tools = []

def add_tool(func: Callable) -> Callable:
    tools.append(func)
    return func

@add_tool
def read_file(file_path: str) -> str:
    """
    Use this tool when the user asks you to read or inspect the contents of a text file.
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File at `{file_path}` was not found."
    except IOError as e:
        return f"Error reading file `{file_path}`: {e}"
    
@add_tool
def write_file(file_path: str, content: str) -> str:
    """
    Use this tool when the user asks you to write, create, or edit a file.
    """
    try:
        with open(file_path, "w") as file:
            file.write(content)
        return f"Successfully wrote to `{file_path}`."
    except IOError as e:
        return f"Error writing to file `{file_path}`: {e}"