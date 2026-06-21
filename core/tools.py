import subprocess

from core.registry import Registry

tools = Registry()

@tools.register()
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
    
@tools.register(sensitive=True)
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
    
@tools.register(sensitive=True)
def run_shell_command(command: str) -> str:
    """
    Execute a shell command and return its stdout, stderr, and exit code.
    Use this to run tests, compile code, list directory trees, or check system status.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            text=True,
            capture_output=True,
            timeout=10,
        )
        output = [f"Exit code: {result.returncode}"]
        if result.stdout:
            output.append(f"STDOUT: {result.stdout.strip()}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr.strip()}")

        return "\n".join(output)
    except subprocess.TimeoutExpired:
        return "Error: Command timed out"
    except Exception as e:
        return f"Error executing command: {e}"