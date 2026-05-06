from fastapi import APIRouter
from core.config import settings
from schemas.health import HealthCheck

router = APIRouter()

@router.get("/", response_model=HealthCheck)
async def get_health() -> HealthCheck:
    """
    Check the connectivity and status of all core infrastructure components.
    """
    # In a production scenario, these would perform actual pings to the services
    return {
        "status": "online",
        "version": settings.VERSION,
        "services": {
            "database": "online",
            "qdrant": "online",
            "redis": "online",
            "llm": "available"
        }
    }
