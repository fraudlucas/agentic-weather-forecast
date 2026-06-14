from fastapi import APIRouter, HTTPException

from agentic_weather_forecast.api.schemas import ChatRequest, ChatResponse
from agentic_weather_forecast.api.parser import (
    langchain_to_pydantic,
    pydantic_to_langchain,
)
from agentic_weather_forecast.graph.workflow import graph

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    inputs = {"messages": pydantic_to_langchain(request.messages)}

    try:
        result = graph.invoke(inputs)

        result_messages = langchain_to_pydantic(result["messages"])

        return ChatResponse(messages=result_messages)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
