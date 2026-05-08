from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ReasoningStep(BaseModel):
    """
    A single step in the AI's logical deduction.
    """
    step_id: int
    logic: str = Field(..., description="The reasoning statement")
    domain: str = Field(..., description="The domain this logic belongs to (Environmental, Societal, Persona)")
    impact_weight: float = Field(..., ge=-1.0, le=1.0, description="How much this step influenced the final score")

class RecommendationBase(BaseModel):
    destination_id: str = Field(..., description="IATA code or unique identifier of the destination")
    match_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0 - 1.0)")
    reasoning_chain: List[ReasoningStep] = Field(..., description="Structured logic steps explaining the match")
    context_snapshot: Dict[str, Any] = Field(..., description="Snapshot of signals used during generation")

class RecommendationCreate(RecommendationBase):
    pass

class Recommendation(RecommendationBase):
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "destination_id": "LHR",
                "match_score": 0.92,
                "reasoning_chain": [
                    {
                        "step_id": 1,
                        "logic": "Matches 'Urban Explorer' preference.",
                        "domain": "Persona",
                        "impact_weight": 0.4
                    },
                    {
                        "step_id": 2,
                        "logic": "Current weather is 'Clear' and temperate.",
                        "domain": "Environmental",
                        "impact_weight": 0.3
                    }
                ],
                "context_snapshot": {
                    "environmental": {"temp": 22},
                    "societal": {"safety": 0.85}
                }
            }
        }
