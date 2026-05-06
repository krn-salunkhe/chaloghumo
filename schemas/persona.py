from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class UserPersona(BaseModel):
    """
    The subjective state and requirements of the traveler.
    """
    preferences: Dict[str, float] = Field(
        ..., 
        description="Map of weights (e.g., adventure: 0.8, relaxation: 0.2)",
        example={"adventure": 0.8, "relaxation": 0.2}
    )
    constraints: List[str] = Field(
        default_factory=list,
        description="List of Hard/Soft constraints (e.g., max_budget: 2000)",
        example=["max_budget: 2000", "mobility: wheelchair"]
    )
    mood: Optional[str] = Field(
        None, 
        description="Semantic string describing the current state",
        example="seeking solitude and vibrant energy"
    )

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "preferences": {"adventure": 0.8, "relaxation": 0.2},
                "constraints": ["max_budget: 2000", "wheelchair_access"],
                "mood": "seeking solitude"
            }
        }
