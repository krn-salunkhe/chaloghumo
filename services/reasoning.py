from typing import Any, List, Dict
from schemas.persona import UserPersona
from services.vector_store import vector_service
from services.llm import llm_service
from services.signals import signal_service

class ReasoningEngine:
    """
    The core synthesis engine for ChaloGhumo.
    Orchestrates the multi-domain recommendation flow.
    """
    
    def __init__(self):
        self.vector_store = vector_service
        self.llm = llm_service
        self.signals = signal_service

    async def generate_recommendation(self, persona: UserPersona) -> Dict[str, Any]:
        """
        Orchestrate the V1 Baseline Recommendation Flow.
        """
        # 1. Pruning: Filter candidates via SQL based on Hard Constraints
        candidate_pool = await self._prune_candidates(persona)
        
        # 2. Semantic Alignment: Rank candidates via Qdrant based on Mood/Vibe
        ranked_candidates = await self._align_semantics(persona, candidate_pool)
        
        # 3. Contextual Weighting: Incorporate real-time signals
        weighted_candidates = await self._apply_contextual_weights(ranked_candidates)
        
        # 4. Synthesis: Generate final narrative via Gemini
        top_destination = weighted_candidates[0] if weighted_candidates else None
        
        if not top_destination:
            return self._empty_response()

        # Fetch latest signals for the top destination to provide context to LLM
        env_state = await self.signals.get_environmental_state(top_destination["id"])
        soc_state = await self.signals.get_societal_state(top_destination["id"])

        reasoning_chain = await self.llm.generate_reasoning_chain(
            persona_context=persona.dict(),
            destination_context=top_destination,
            environmental_signals=env_state or {},
            societal_signals=soc_state or {}
        )

        return {
            "destination_id": top_destination.get("id", "unknown"),
            "match_score": top_destination.get("score", 0.0),
            "reasoning_chain": reasoning_chain,
            "context_snapshot": {
                "persona": persona.dict(),
                "environment": env_state or {},
                "societal": soc_state or {}
            }
        }

    async def _prune_candidates(self, persona: UserPersona) -> List[Dict[str, Any]]:
        """
        Logic for SQL-based filtering of hard constraints.
        """
        # Placeholder for DB query logic
        return []

    async def _align_semantics(self, persona: UserPersona, pool: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Logic for Vector-based similarity search and ranking.
        """
        # Convert the user's mood/vibe into a vector
        query_vector = await self.llm.generate_embedding(persona.mood or "travel")
        
        # Search the vector store
        # If pool is empty, we search the entire collection. 
        # If pool has candidates from _prune_candidates, we should ideally use them as filters,
        # but for now, we'll perform a standard search.
        results = await self.vector_store.search_by_vibe(query_vector=query_vector, limit=10)
        
        return results

    async def _apply_contextual_weights(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Logic for adjusting scores based on real-time Environmental/Societal signals.
        Implements 'Environmental Determinism' by penalizing unsafe or incompatible states.
        """
        for cand in candidates:
            env = await self.signals.get_environmental_state(cand["id"])
            if env and env.get("conditions") == "Extreme":
                cand["score"] *= 0.1 # Severe penalty for safety invariant violation
            
            soc = await self.signals.get_societal_state(cand["id"])
            if soc and soc.get("crowd_density", 0) > 0.8:
                cand["score"] *= 0.7 # Penalty for high crowding (Crowding Paradox)
                
        return sorted(candidates, key=lambda x: x["score"], reverse=True)

    def _empty_response(self) -> Dict[str, Any]:
        return {
            "destination_id": "no-match",
            "match_score": 0.0,
            "reasoning_chain": [
                {
                    "step_id": 1,
                    "logic": "Unable to find a destination matching your constraints.",
                    "domain": "System",
                    "impact_weight": 0.0
                }
            ],
            "context_snapshot": {}
        }

reasoning_engine = ReasoningEngine()
