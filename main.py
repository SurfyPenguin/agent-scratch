from google import genai
from google.genai.types import GenerateContentConfig

from models import gemini_models
from config import GEMINI_API_KEY

MODEL: gemini_models = "gemini-3.1-flash-lite"
EXIT_COMMANDS = ["/exit", "/quit"]

client = genai.Client(api_key=GEMINI_API_KEY)

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

system_prompt = "You are a senior software developer, who specializes in design patterns and system architecture."

config = GenerateContentConfig(
    system_instruction=system_prompt,
    tools=[read_file, write_file]
)

def main() -> None:
    chat = client.chats.create(
        model=MODEL,
        config=config,
    )

    while True:
        message = input(" >> ")

        if message.strip().lower() in EXIT_COMMANDS:
            return

        response = chat.send_message(message)
        print(response.text)

if __name__ == "__main__":
    main()