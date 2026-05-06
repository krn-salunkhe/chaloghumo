import json
from typing import Dict, Any, Optional
from redis import Redis
from core.config import settings

class SignalService:
    """
    Service for retrieving real-time Environmental and Societal signals from Redis.
    Implements the 'Environmental Determinism' logic by providing context for the Reasoning Engine.
    """

    def __init__(self):
        self.redis = Redis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT, 
            decode_responses=True
        )

    async def get_environmental_state(self, destination_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch real-time weather and climate data for a destination.
        """
        data = self.redis.get(f"signal:env:{destination_id}")
        return json.loads(data) if data else None

    async def get_societal_state(self, destination_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch real-time crowd density and infrastructure availability.
        """
        data = self.redis.get(f"signal:soc:{destination_id}")
        return json.loads(data) if data else None

signal_service = SignalService()
