from google import genai
from google.genai.types import GenerateContentConfig

from config import GEMINI_API_KEY, GEMINI_MODEL
from core.tools import tools

EXIT_COMMANDS = ["/exit", "/quit"]

client = genai.Client(api_key=GEMINI_API_KEY)

system_prompt = "You are a senior software developer, who specializes in design patterns and system architecture."

config = GenerateContentConfig(
    system_instruction=system_prompt,
    tools=tools.get_functions()
)

def main() -> None:
    chat = client.chats.create(
        model=GEMINI_MODEL,
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