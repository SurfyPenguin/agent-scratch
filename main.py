from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL
from core.tools import tools
from models.conversation import Conversation
from models.io_interface import ConsoleIO

EXIT_COMMANDS = ["/exit", "/quit"]

client = genai.Client(api_key=GEMINI_API_KEY)

system_prompt = "You are a senior software developer, who specializes in design patterns and system architecture."

config = types.GenerateContentConfig(
    system_instruction=system_prompt,
    tools=tools.get_functions(),
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

console = ConsoleIO()


def main() -> None:
    chat = client.chats.create(
        model=GEMINI_MODEL,
        config=config,
    )

    conversation = Conversation(chat=chat, io=console)
    while True:
        user_message = console.prompt()

        if (
            user_message.strip().startswith("/")
            and user_message.strip().lower() in EXIT_COMMANDS
        ):
            return
        response = conversation.send_message(user_message)

        console.display(response.text)


if __name__ == "__main__":
    main()
