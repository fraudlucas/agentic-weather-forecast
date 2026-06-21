from fastapi import APIRouter, Query, HTTPException

from agentic_weather_forecast.api.schemas import ChatResponse
from agentic_weather_forecast.api.parser import langchain_to_pydantic
from agentic_weather_forecast.graph.workflow import build_graph

router = APIRouter()
graph = build_graph()


@router.get("/weather", response_model=ChatResponse)
async def get_weather(
    location: str = Query(..., min_length=1),
    date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
):
    inputs = {
        "messages": [
            ("user", f"What is the weather in {location} on {date} ?"),
        ]
    }

    try:
        result = graph.invoke(inputs)

        result_messages = langchain_to_pydantic(result["messages"])

        return ChatResponse(messages=result_messages)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
