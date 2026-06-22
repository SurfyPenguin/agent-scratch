from typing import Callable, Any

from pydantic import BaseModel


class ToolFunction(BaseModel):
    function: Callable[..., Any]
    sensitive: bool = False
    prompt: str | None = None

    def get_prompt_from_args(self, kwargs: dict[str, Any]) -> str:
        return self.prompt.format(**kwargs)
