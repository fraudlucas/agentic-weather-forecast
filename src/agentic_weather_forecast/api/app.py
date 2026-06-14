from fastapi import FastAPI

from agentic_weather_forecast.api.routes import health, chat, weather

app = FastAPI(
    title="Agentic Weather Forecast",
    version="0.1.0",
    description="REST API for the agentic weather forecast system",
)

app.include_router(health.router, tags=["health"])
app.include_router(chat.router, tags=["chat"])
app.include_router(weather.router, tags=["weather"])
