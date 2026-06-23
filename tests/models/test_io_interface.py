from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from unittest.mock import MagicMock, patch

from models.io_interface import ConsoleIO


def test_display_prints_markdown():
    mock_console = MagicMock(spec=Console)
    io = ConsoleIO(console=mock_console)

    io.display("Hello **world**")
    mock_console.print.assert_called_once()
    (arg,), _ = mock_console.print.call_args

    assert isinstance(arg, Markdown)
    assert arg.markup == "Hello **world**"


@patch.object(Prompt, "ask")
def test_prompt_returns_input(mock_ask):
    mock_ask.return_value = "yes"
    mock_console = MagicMock(spec=Console)
    io = ConsoleIO(console=mock_console)

    response = io.prompt("**sure?**")
    assert response == "yes"

    mock_console.print.assert_called_once()

    (arg,), _ = mock_console.print.call_args
    assert isinstance(arg, Markdown)
    assert arg.markup == "**sure?**"
