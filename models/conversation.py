from google.genai.chats import Chat
from google.genai import types
from pydantic import BaseModel, ConfigDict

from helpers.response import is_function_call, get_function_call, get_tool
from .io_interface import IOInterface


class Conversation(BaseModel):
    chat: Chat
    io: IOInterface

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def parse_approval(
        self,
        content: str,
    ) -> bool | None:
        content = content.strip().lower()
        if content in ["yes", "y"]:
            return True

        if content in ["no", "n"]:
            return False
        return None

    def get_user_approval(
        self,
        function_call: types.FunctionCall,
    ) -> bool:
        while True:
            tool = get_tool(function_call)
            approval = self.parse_approval(
                self.io.prompt(tool.get_prompt_from_args(function_call.args))
            )

            if approval is not None:
                return approval

    def send_function_response(
        self,
        function_call: types.FunctionCall,
        response: str,
    ):
        response = self.chat.send_message(
            message=types.Part.from_function_response(
                name=function_call.name, response={"output": response}
            )
        )

        return response

    def send_message(self, message):
        response = self.chat.send_message(message)

        while is_function_call(response):
            function_call = get_function_call(response)
            tool = get_tool(function_call)

            if tool.sensitive and not self.get_user_approval(function_call):
                response = self.send_function_response(
                    function_call, "user denied request."
                )

            else:
                tool_result = tool.function(**function_call.args)
                response = self.send_function_response(function_call, tool_result)
        return response
