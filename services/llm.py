from typing import List, Dict, Any
import json
from sentence_transformers import SentenceTransformer
from core.config import settings

class LLMService:
    """
    Service for semantic processing.
    Uses SentenceTransformers for local embeddings and Gemini for reasoning.
    """

    def __init__(self):
        # Local Embedding Model (384-D)
        # Using a small, efficient model suitable for travel vibes
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Reasoning Model (Gemini via API)
        # We keep this as an option for narrative synthesis
        try:
            import google.generativeai as genai
            if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY != "your_api_key_here":
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.genai_client = genai
                self.reasoning_model = "gemini-1.5-pro"
            else:
                self.genai_client = None
        except ImportError:
            self.genai_client = None

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Convert a natural language string into a 384-D vector using all-MiniLM-L6-v2.
        Runs locally without API calls.
        """
        try:
            # sentence-transformers encode is synchronous
            embedding = self.embedding_model.encode(text)
            return embedding.tolist()
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return [0.0] * 384

    async def generate_reasoning_chain(
        self, 
        persona_context: Dict[str, Any], 
        destination_context: Dict[str, Any],
        environmental_signals: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Synthesize the final 'ReasoningChain' as a list of structured steps.
        Uses prompt engineering to force JSON output from the LLM.
        """
        prompt = self._build_reasoning_prompt(persona_context, destination_context, environmental_signals)
        
        if self.genai_client:
            try:
                model = self.genai_client.GenerativeModel(self.reasoning_model)
                response = await model.generate_content_async(prompt)
                return self._parse_structured_output(response.text)
            except Exception as e:
                print(f"LLM Synthesis Error: {e}")
        
        # Heuristic fallback if LLM fails or is unavailable
        return [
            {
                "step_id": 1,
                "logic": f"Destination {destination_context.get('id')} aligns with your vibe.",
                "domain": "Persona",
                "impact_weight": 0.3
            }
        ]

    def _build_reasoning_prompt(self, persona: dict, dest: dict, signals: dict) -> str:
        return f"""
        Analyze the match between this user persona and destination.
        User: {json.dumps(persona)}
        Destination: {json.dumps(dest)}
        Signals: {json.dumps(signals)}

        Return a JSON array of reasoning steps. Each step must have:
        - step_id: integer
        - logic: string
        - domain: one of [Persona, Environmental, Societal]
        - impact_weight: float between -1.0 and 1.0

        OUTPUT ONLY VALID JSON.
        """

    def _parse_structured_output(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract and validate JSON from raw LLM text.
        """
        try:
            # Clean up potential markdown formatting
            clean_text = text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            # Basic validation: ensure it's a list
            if isinstance(data, list):
                return data
            return []
        except Exception:
            return []

    async def parse_mood_intent(self, mood_text: str) -> Dict[str, Any]:
        """
        Analyze raw user mood strings.
        """
        return {"mood": mood_text}

llm_service = LLMService()
