from google.genai import types

from models.tool_function import ToolFunction
from core.tools import tools


def _get_part(response: types.GenerateContentResponse) -> types.Part:
    return response.parts[0]


def is_function_call(response: types.GenerateContentResponse) -> bool:
    return _get_part(response).function_call is not None


def get_function_call(
    response: types.GenerateContentResponse,
) -> types.FunctionCall | None:
    return _get_part(response).function_call


def get_tool(function_call: types.FunctionCall) -> ToolFunction:
    return tools.registry[function_call.name]
