from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from typing import Sequence

from agentic_weather_forecast.api.schemas import Message


def langchain_to_pydantic(messages: Sequence[BaseMessage]) -> list[Message]:
    mapping = {
        HumanMessage: "user",
        AIMessage: "assistant",
        ToolMessage: "tool",
    }

    return [
        Message(role=mapping.get(type(message), "user"), content=str(message.content))
        for message in messages
    ]


def pydantic_to_langchain(messages: list[Message]) -> list[BaseMessage]:
    mapping = {
        "user": HumanMessage,
        "assistant": AIMessage,
        "tool": ToolMessage,
    }

    return [mapping[message.role](content=message.content) for message in messages]
