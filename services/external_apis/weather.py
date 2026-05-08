import httpx
from typing import Dict, Any
from core.config import settings

class WeatherClient:
    """
    Client for fetching weather data.
    Currently stubbed for OpenWeatherMap.
    """
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"

    async def get_weather(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        Fetch current weather for coordinates.
        Returns a mock response if no API key is provided.
        """
        if not self.api_key or self.api_key == "your_openweather_key":
            return {
                "temp": 22.5,
                "conditions": "Clear",
                "humidity": 45,
                "wind_speed": 5.2,
                "source": "mock"
            }
        
        # Real implementation would go here
        async with httpx.AsyncClient() as client:
            params = {
                "lat": lat,
                "lon": lng,
                "appid": self.api_key,
                "units": "metric"
            }
            # response = await client.get(f"{self.base_url}/weather", params=params)
            # return response.json()
            return {"status": "real_api_call_not_executed_in_stub"}

weather_client = WeatherClient()
