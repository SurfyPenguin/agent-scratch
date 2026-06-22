from models.tool_function import ToolFunction


def dummy_function(): ...


def test_tool_function():
    tool = ToolFunction(
        function=dummy_function,
        sensitive=True,
        prompt="test prompt",
    )

    assert tool.function == dummy_function
    assert tool.sensitive
    assert tool.prompt == "test prompt"


def test_get_prompt_from_args():
    tool = ToolFunction(
        function=dummy_function,
        sensitive=True,
        prompt="about to call {dummy_name}",
    )
    kwargs = {"dummy_name": "dummy function"}
    prompt = tool.get_prompt_from_args(kwargs)
    assert prompt == f"about to call {kwargs['dummy_name']}"
