from typing import Sequence

import pytest
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
)

from agentic_weather_forecast.api.parser import langchain_to_pydantic, pydantic_to_langchain
from agentic_weather_forecast.api.schemas import Message


class UnknownMessage(BaseMessage):
    """A message type not present in the parser mapping."""
    type: str = "unknown"


class TestLangchainToPydantic:
    def test_human_message(self):
        result = langchain_to_pydantic([HumanMessage(content="hi")])
        assert len(result) == 1
        assert result[0].role == "user"
        assert result[0].content == "hi"

    def test_ai_message(self):
        result = langchain_to_pydantic([AIMessage(content="hello")])
        assert len(result) == 1
        assert result[0].role == "assistant"
        assert result[0].content == "hello"

    def test_tool_message(self):
        result = langchain_to_pydantic(
            [ToolMessage(content="result", tool_call_id="x")]
        )
        assert len(result) == 1
        assert result[0].role == "tool"
        assert result[0].content == "result"

    def test_unknown_type_fallback_to_user(self):
        result = langchain_to_pydantic([UnknownMessage(content="fallback")])
        assert len(result) == 1
        assert result[0].role == "user"
        assert result[0].content == "fallback"

    def test_multiple_messages(self):
        msgs: Sequence[BaseMessage] = [
            HumanMessage(content="hi"),
            AIMessage(content="how can I help?"),
            ToolMessage(content="weather data", tool_call_id="t1"),
        ]
        result = langchain_to_pydantic(msgs)
        assert len(result) == 3
        assert result[0].role == "user"
        assert result[1].role == "assistant"
        assert result[2].role == "tool"

    def test_empty_sequence(self):
        result = langchain_to_pydantic([])
        assert result == []


class TestPydanticToLangchain:
    def test_user_message(self):
        result = pydantic_to_langchain([Message(role="user", content="hi")])
        assert len(result) == 1
        assert isinstance(result[0], HumanMessage)
        assert result[0].content == "hi"

    def test_assistant_message(self):
        result = pydantic_to_langchain([Message(role="assistant", content="hello")])
        assert len(result) == 1
        assert isinstance(result[0], AIMessage)
        assert result[0].content == "hello"

    def test_tool_message_missing_tool_call_id(self):
        with pytest.raises(KeyError):
            pydantic_to_langchain([Message(role="tool", content="result")])

    def test_multiple_messages(self):
        result = pydantic_to_langchain([
            Message(role="user", content="hi"),
            Message(role="assistant", content="hello"),
        ])
        assert len(result) == 2
        assert isinstance(result[0], HumanMessage)
        assert isinstance(result[1], AIMessage)
