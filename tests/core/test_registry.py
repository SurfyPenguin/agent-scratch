import pytest

from core.registry import Registry
from models.tool_function import ToolFunction


@pytest.fixture
def registry():
    return Registry()


def test_register_adds_function_to_registry(registry):
    @registry.register()
    def my_tool(x: int):
        return x + 1

    assert "my_tool" in registry.registry
    tool = registry.registry["my_tool"]
    assert isinstance(tool, ToolFunction)

    assert tool.function is my_tool
    assert tool.sensitive is False
    assert tool.prompt is None


def test_register_with_sensitive_and_prompt(registry):
    @registry.register(
        sensitive=True,
        prompt="execute tool with value: {x}?",
    )
    def my_tool(x: int):
        return x + 1

    tool = registry.registry["my_tool"]
    assert tool.function is my_tool
    assert tool.sensitive is True
    assert tool.prompt == "execute tool with value: {x}?"


def test_register_returns_original_function_unmodified(registry):
    @registry.register()
    def my_tool(x: int):
        return x + 1

    assert my_tool(2) == 3


def test_register_multiple_functions(registry):
    @registry.register()
    def func_a(): ...

    @registry.register()
    def func_b(): ...

    assert set(registry.registry.keys()) == {"func_a", "func_b"}


def test_functions_return_callables(registry):
    @registry.register()
    def func_a(): ...

    @registry.register()
    def func_b(): ...

    functions = registry.get_functions()
    assert set(functions) == {func_a, func_b}


def test_get_functions_empty_registry(registry):
    assert registry.get_functions() == []
