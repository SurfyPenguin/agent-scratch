from rich.console import Console
from rich.markdown import Markdown


console = Console()


def print_markdown(content: Markdown | str) -> None:
    if not isinstance(content, Markdown):
        content = Markdown(content)
    console.print(content)
