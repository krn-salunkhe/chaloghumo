from typing import Any, Dict, List
from pydantic import BaseModel, Field, UUID4

class RecommendationBase(BaseModel):
    destination_id: UUID4 = Field(..., description="Unique identifier of the recommended destination")
    match_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the match (0.0 - 1.0)")
    reasoning_chain: List[str] = Field(..., description="Logic steps explaining the match")
    context_snapshot: Dict[str, Any] = Field(..., description="The state of the three domains at generation time")

class RecommendationCreate(RecommendationBase):
    pass

class Recommendation(RecommendationBase):
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "destination_id": "550e8400-e29b-41d4-a716-446655440000",
                "match_score": 0.95,
                "reasoning_chain": [
                    "Destination matches your preference for 'Quiet' environments.",
                    "Active weather signal indicates perfect temperature (22°C).",
                    "Crowd density is currently low (0.2)."
                ],
                "context_snapshot": {
                    "environmental": {"temp": 22},
                    "societal": {"crowds": 0.2}
                }
            }
        }
