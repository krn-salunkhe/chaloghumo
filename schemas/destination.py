from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator

class DestinationPayload(BaseModel):
    """
    Strict schema for Qdrant payloads to ensure filtering reliability.
    """
    name: str = Field(..., description="Name of the destination (City/Region)")
    country: str = Field(..., description="ISO Country Code")
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")
    iata: Optional[str] = Field(None, description="IATA code if applicable")
    
    # Semantic Content
    vibe_description: str = Field(..., description="Natural language description of the destination's vibe")
    
    # Hard/Soft Filters
    budget_level: str = Field(
        ..., 
        description="Categorical budget (e.g., Budget, Mid-range, Luxury)",
        pattern="^(Budget|Mid-range|Luxury)$"
    )
    climate_type: str = Field(
        ..., 
        description="Dominant climate (e.g., Tropical, Temperate, Arid, Continental, Polar)",
        pattern="^(Tropical|Temperate|Arid|Continental|Polar)$"
    )
    safety_index: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="Safety score from 0.0 to 1.0 (Higher is safer)"
    )
    
    # Tags for quick filtering
    tags: List[str] = Field(default_factory=list, description="List of feature tags (e.g., mountains, beach, nightlife)")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Paris",
                "country": "FR",
                "lat": 48.8566,
                "lng": 2.3522,
                "iata": "PAR",
                "vibe_description": "A city of lights, culture, and high fashion.",
                "budget_level": "Luxury",
                "climate_type": "Temperate",
                "safety_index": 0.85,
                "tags": ["culture", "romance", "urban"]
            }
        }
