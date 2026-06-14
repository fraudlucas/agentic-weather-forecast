from langchain_core.tools import tool
from geopy.geocoders import Nominatim
from pydantic import BaseModel, Field
from functools import lru_cache

import requests


@lru_cache(maxsize=1)
def _get_geolocator():
    return Nominatim(user_agent="weather-app")


class SearchInput(BaseModel):
    location: str = Field(description="The city and state, e.g., San Francisco")
    date: str = Field(
        description="the forecasting date for when to get the weather format (yyyy-mm-dd)"
    )


@tool("get_weather_forecast", args_schema=SearchInput, return_direct=True)
def get_weather_forecast(location: str, date: str):
    """Retrieves the weather using Open-Meteo API.

    Takes a given location (city) and a date (yyyy-mm-dd).

    Returns:
        A dict with the time and temperature for each hour.
    """
    geolocator = _get_geolocator()

    location_point  = geolocator.geocode(location)

    if location_point:
        try:
            response = requests.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={location_point.latitude}&longitude={location_point.longitude}&hourly=temperature_2m&start_date={date}&end_date={date}"
            )
        
            data = response.json()

            return dict(zip(data["hourly"]["time"], data["hourly"]["temperature_2m"]))
        
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "Location not found"}


tools = [get_weather_forecast]
