from typing import Callable, Any

from core.models import ToolFunction


class Registry:
    def __init__(self):
        self.registry: dict[str, ToolFunction] = {}

    def register(self, *, sensitive: bool = False) -> Callable[..., Any]:
        def decorator(func: Callable[..., Any]):
            self.registry[func.__name__] = ToolFunction(
                function=func,
                sensitive=sensitive,
            )
            return func

        return decorator

    def get_functions(self) -> list[Callable[..., Any]]:
        return [tool_func.function for tool_func in self.registry.values()]
