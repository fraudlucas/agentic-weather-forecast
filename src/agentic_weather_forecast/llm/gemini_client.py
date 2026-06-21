from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI

from agentic_weather_forecast.core.settings import env_settings
from agentic_weather_forecast.tools.weather_forecast import get_weather_forecast


@lru_cache(maxsize=1)
def get_llm_agent():
    api_key = env_settings.gemini_api_key
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY before running the Gemini smoke test.")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=1.0,
        max_retries=2,
        google_api_key=api_key,
    )
    return llm.bind_tools([get_weather_forecast])
