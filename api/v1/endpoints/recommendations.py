from typing import Any
from fastapi import APIRouter, HTTPException

from schemas.recommendation import Recommendation
from schemas.persona import UserPersona
from services.reasoning import reasoning_engine

router = APIRouter()

@router.post("/", response_model=Recommendation)
async def create_recommendation(
    *,
    persona_in: UserPersona,
) -> Any:
    """
    Generate a next-generation AI travel recommendation based on hyper-personalized context.
    
    This endpoint orchestrates the multi-domain reasoning flow:
    1. Prunes candidates using objective constraints.
    2. Aligns semantic 'vibes' via vector similarity.
    3. Synthesizes a natural language ReasoningChain using Gemini 1.5 Pro.
    """
    try:
        recommendation = await reasoning_engine.generate_recommendation(persona_in)
        
        if recommendation["destination_id"] == "no-match":
            raise HTTPException(
                status_code=404, 
                detail="No destinations found matching your current constraints and mood."
            )
            
        return recommendation
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occurred in the Reasoning Engine: {str(e)}"
        )
