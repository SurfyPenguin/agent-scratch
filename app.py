from google import genai
from google.genai import types
from fastapi import FastAPI
from pydantic import BaseModel

from helpers.config import GEMINI_API_KEY, GEMINI_MODEL
from core.tools import tools

client = genai.Client(api_key=GEMINI_API_KEY)

system_prompt = "You are a senior software developer, who specializes in design patterns and system architecture."

config = types.GenerateContentConfig(
    system_instruction=system_prompt,
    tools=tools.get_functions(),
    # automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)

chat = client.chats.create(
    model=GEMINI_MODEL,
    config=config,
)


class ChatRequest(BaseModel):
    text: str


class ChatResponse(BaseModel):
    reply: str


app = FastAPI()


@app.post("/chat")
def get_text(request: ChatRequest):
    user_text = request.text
    response = chat.send_message(user_text)
    return ChatResponse(reply=response.text)
