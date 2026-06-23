import pytest
from google.genai.chats import Chat
from google.genai import types
from unittest.mock import MagicMock, patch

from models.conversation import Conversation, IOInterface

PATCH_TARGET = "models.conversation.get_tool"


@pytest.fixture
def mock_io():
    return MagicMock(spec=IOInterface)


@pytest.fixture
def conversation(mock_io):
    return Conversation(chat=MagicMock(spec=Chat), io=mock_io)


@pytest.fixture
def mock_fc():
    return types.FunctionCall(name="my_tool", args={"x": 1})


@pytest.mark.parametrize(
    "user_input, expected_output",
    [
        ("yes", True),
        ("   Y  ", True),
        ("no  ", False),
        ("N", False),
        ("maybe", None),
    ],
)
def test_parse_approval(user_input: str, expected_output: bool | None):
    mock_conv = Conversation(chat=MagicMock(spec=Chat), io=MagicMock(spec=IOInterface))
    assert mock_conv.parse_approval(user_input) == expected_output


@pytest.fixture
def mock_tool():
    mt = MagicMock()
    mt.function = MagicMock(return_value="mock function")
    mt.get_prompt_from_args.return_value = "Run this?"
    return mt


# ------------ TESTS for Conversation.get_user_approval ------------


@patch(PATCH_TARGET)
def test_approval_yes(mock_get_tool, conversation, mock_io, mock_tool, mock_fc):
    mock_get_tool.return_value = mock_tool

    mock_io.prompt.return_value = "y"

    assert conversation.get_user_approval(mock_fc) is True


@patch(PATCH_TARGET)
def test_approval_no(mock_get_tool, conversation, mock_io, mock_tool, mock_fc):
    mock_get_tool.return_value = mock_tool

    mock_io.prompt.return_value = "n"

    assert conversation.get_user_approval(mock_fc) is False


@patch(PATCH_TARGET)
def test_reprompts_until_valid_input(
    mock_get_tool, conversation, mock_io, mock_tool, mock_fc
):
    mock_get_tool.return_value = mock_tool

    mock_io.prompt.side_effect = ["maybe", "sure", "yes"]

    assert conversation.get_user_approval(mock_fc) is True
    assert mock_io.prompt.call_count == 3


# ------------ TESTS for Conversation.send_function_response ------------


def test_send_function_response(conversation, mock_fc):
    conversation.chat.send_message.return_value = "chat response"
    result = conversation.send_function_response(mock_fc, "tool output")

    assert result == "chat response"

    expected_part = types.Part.from_function_response(
        name="my_tool",
        response={"output": "tool output"},
    )

    conversation.chat.send_message.assert_called_once_with(message=expected_part)


@patch("models.conversation.is_function_call")
def test_send_message_has_no_function_call(mock_is_function_call, conversation):
    mock_is_function_call.return_value = False
    mock_part = types.Part(text="mock test")
    conversation.chat.send_message.return_value = mock_part

    result = conversation.send_message("input text")
    assert result.text == "mock test"

    conversation.chat.send_message.assert_called_once_with("input text")


@patch.object(Conversation, "send_function_response")
@patch.object(Conversation, "get_user_approval")
@patch("models.conversation.get_tool")
@patch("models.conversation.get_function_call")
@patch("models.conversation.is_function_call")
def test_send_message_has_function_call_user_allowed(
    mock_is_function_call,
    mock_get_function_call,
    mock_get_tool,
    mock_get_user_approval,
    mock_send_function_response,
    conversation,
    mock_fc,
    mock_tool,
):
    mock_is_function_call.side_effect = [True, False]
    mock_get_function_call.return_value = mock_fc

    mock_tool.sensitive = True
    mock_get_user_approval.return_value = True
    mock_get_tool.return_value = mock_tool
    mock_part = types.Part(text="mock test")
    conversation.chat.send_message.return_value = mock_part
    mock_send_function_response.return_value = mock_part

    assert conversation.send_message("input message").text == "mock test"
