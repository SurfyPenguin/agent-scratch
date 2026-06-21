from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL
from core.tools import tools

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

    while True:
        message = input(" >> ")

        if message.strip().lower() in EXIT_COMMANDS:
            return

        response = chat.send_message(message)
        part = response.parts[0]

        while part.function_call is not None:
            print(f"> calling: {part.function_call.name}")
            tool = tools.registry[part.function_call.name]
            result = tool.function(**part.function_call.args)

            response = chat.send_message(
                message=types.Part.from_function_response(
                    name=part.function_call.name, response={"output": result}
                )
            )
            part = response.parts[0]

        print(response.text)


if __name__ == "__main__":
    main()
