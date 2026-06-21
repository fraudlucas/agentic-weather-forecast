import pytest
from pydantic import ValidationError

from agentic_weather_forecast.api.schemas import Message, ChatRequest, ChatResponse


class TestMessage:
    def test_valid_roles(self):
        for role in ("user", "assistant", "tool"):
            msg = Message(role=role, content="hello")
            assert msg.role == role
            assert msg.content == "hello"

    def test_invalid_role(self):
        with pytest.raises(ValidationError):
            Message(role="system", content="hello")

    def test_content_required(self):
        with pytest.raises(ValidationError):
            Message(role="user")  # type: ignore[call-arg]

    def test_content_empty_string(self):
        msg = Message(role="user", content="")
        assert msg.content == ""


class TestChatRequest:
    def test_with_messages(self):
        req = ChatRequest(messages=[Message(role="user", content="hi")])
        assert len(req.messages) == 1
        assert req.messages[0].role == "user"
        assert req.messages[0].content == "hi"

    def test_empty_messages(self):
        req = ChatRequest(messages=[])
        assert req.messages == []

    def test_roundtrip_serialization(self):
        original = ChatRequest(
            messages=[
                Message(role="user", content="hello"),
                Message(role="assistant", content="world"),
            ]
        )
        data = original.model_dump()
        restored = ChatRequest.model_validate(data)
        assert restored == original


class TestChatResponse:
    def test_roundtrip_serialization(self):
        original = ChatResponse(
            messages=[
                Message(role="assistant", content="Hi there"),
            ]
        )
        data = original.model_dump()
        restored = ChatResponse.model_validate(data)
        assert restored == original
