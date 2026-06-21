from typing import Callable, Any

from pydantic import BaseModel


class ToolFunction(BaseModel):
    function: Callable[..., Any]
    sensitive: bool = False
    prompt: str | None = None
