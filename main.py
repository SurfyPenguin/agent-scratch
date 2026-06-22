from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL
from core.tools import tools
from models.conversation import Conversation
from helpers.console import print_markdown

EXIT_COMMANDS = ["/exit", "/quit"]

client = genai.Client(api_key=GEMINI_API_KEY)

system_prompt = "You are a senior software developer, who specializes in design patterns and system architecture."

config = types.GenerateContentConfig(
    system_instruction=system_prompt,
    tools=tools.get_functions(),
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)


def main() -> None:
    chat = client.chats.create(
        model=GEMINI_MODEL,
        config=config,
    )

    conversation = Conversation(chat=chat)
    while True:
        user_message = input(">> ")

        if (
            user_message.strip().startswith("/")
            and user_message.strip().lower() in EXIT_COMMANDS
        ):
            return
        response = conversation.send_message(user_message)

        print_markdown(response.text)


if __name__ == "__main__":
    main()
