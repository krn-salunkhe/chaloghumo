import json
from typing import Dict, Any, Optional
import redis.asyncio as redis
from core.config import settings
from services.external_apis.weather import weather_client
from services.external_apis.safety import safety_client
from services.external_apis.events import events_client

class SignalService:
    """
    Service for retrieving and refreshing real-time Environmental and Societal signals.
    Orchestrates ingestion from external APIs and Kafka into the Redis cache.
    """

    def __init__(self):
        self.redis = redis.Redis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT, 
            decode_responses=True
        )

    async def get_environmental_state(self, destination_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch cached weather and climate data.
        """
        data = await self.redis.get(f"signal:env:{destination_id}")
        return json.loads(data) if data else None

    async def get_societal_state(self, destination_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch cached crowd density and infrastructure availability.
        """
        data = await self.redis.get(f"signal:soc:{destination_id}")
        return json.loads(data) if data else None

    async def get_emergency_alerts(self, destination_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch high-priority emergency alerts.
        """
        data = await self.redis.get(f"signal:emergency:{destination_id}")
        return json.loads(data) if data else None

    async def refresh_signals(self, destination_id: str, lat: float, lng: float):
        """
        Trigger ingestion from external APIs and update Redis cache with aggressive TTLs.
        """
        # 1. Fetch from Weather API
        weather_data = await weather_client.get_weather(lat, lng)
        await self.redis.set(f"signal:env:{destination_id}", json.dumps(weather_data), ex=3600)

        # 2. Fetch from Safety and Events
        safety_data = await safety_client.get_safety_score(lat, lng)
        events_data = await events_client.get_nearby_events(lat, lng)
        
        soc_data = {
            "safety": safety_data,
            "events": events_data,
            "crowd_density": 0.4 
        }
        await self.redis.set(f"signal:soc:{destination_id}", json.dumps(soc_data), ex=3600)


signal_service = SignalService()
