from typing import Dict, Any
from core.config import settings

class SafetyClient:
    """
    Client for fetching safety and risk signals.
    Currently stubbed for Amadeus Safety API or GDELT.
    """
    def __init__(self):
        self.api_key = settings.AMADEUS_API_KEY

    async def get_safety_score(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        Fetch safety scores for a location.
        """
        # Mock logic
        return {
            "overall_safety": 85,
            "lgbtq_safety": 90,
            "medical_safety": 80,
            "political_stability": 95,
            "source": "mock_amadeus"
        }

safety_client = SafetyClient()
