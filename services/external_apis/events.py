from typing import List, Dict, Any

class EventsClient:
    """
    Client for fetching local events and cultural signals.
    """
    async def get_nearby_events(self, lat: float, lng: float) -> List[Dict[str, Any]]:
        """
        Fetch upcoming events for a location.
        """
        return [
            {
                "name": "Local Music Festival",
                "type": "Music",
                "date": "2026-06-15",
                "vibe": "Vibrant"
            },
            {
                "name": "Art Gallery Opening",
                "type": "Culture",
                "date": "2026-06-18",
                "vibe": "Sophisticated"
            }
        ]

events_client = EventsClient()
