from typing import Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field
from rich.prompt import Prompt
from rich.console import Console
from rich.markdown import Markdown


@runtime_checkable
class IOInterface(Protocol):
    def display(self, content: str) -> None: ...
    def prompt(self, message: str = "") -> str: ...


class ConsoleIO(BaseModel):
    console: Console = Field(default_factory=Console)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def display(self, content: str) -> None:
        self.console.print(Markdown(content))

    def prompt(self, message: str = "") -> str:
        self.console.print(Markdown(message), end="")
        return Prompt.ask(console=self.console)
