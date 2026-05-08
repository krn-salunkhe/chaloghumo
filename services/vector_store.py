from typing import List, Optional, Dict, Any
from qdrant_client.http import models
from qdrant_client import QdrantClient
from core.config import settings
from schemas.destination import DestinationPayload

class VectorService:
    """
    Service for interacting with the Qdrant Vector Store.
    Focuses on semantic similarity search for destination 'vibes'.
    """

    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST, 
            port=settings.QDRANT_PORT
        )
        self.collection_name = "destinations"
        self.vector_size = 384  # Matches all-MiniLM-L6-v2

    def _ensure_collection(self):
        """
        Ensure the Qdrant collection exists with the correct configuration.
        """
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)
        
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                ),
                hnsw_config=models.HnswConfigDiff(
                    m=16,
                    ef_construct=100,
                    full_scan_threshold=10000
                )
            )

    async def upsert_destination(
        self, 
        destination_id: str, 
        vector: List[float], 
        payload: Dict[str, Any]
    ) -> bool:
        """
        Synchronize a destination's semantic representation with the vector store.
        Validates the payload against the DestinationPayload schema.
        """
        self._ensure_collection()
        try:
            # Enforce schema validation
            validated_payload = DestinationPayload(**payload)
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=destination_id,
                        vector=vector,
                        payload=validated_payload.model_dump()
                    )
                ]
            )
            return True
        except Exception as e:
            print(f"Error upserting to Qdrant (Validation/Connection): {e}")
            return False

    async def search_by_vibe(
        self, 
        query_vector: List[float], 
        limit: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform a semantic similarity search based on a user's 'mood' or 'vibe'.
        Supports pre-filtering via Qdrant payload filters.
        """
        self._ensure_collection()
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=models.Filter(**filters) if filters else None,
                limit=limit
            )
            return [
                {
                    "id": hit.id,
                    "score": hit.score,
                    "payload": hit.payload
                } for hit in search_result
            ]
        except Exception as e:
            print(f"Error searching Qdrant: {e}")
            return []

    async def get_destination_vector(self, destination_id: str) -> Optional[List[float]]:
        """
        Retrieve the high-dimensional vector for a specific destination.
        """
        try:
            result = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[destination_id],
                with_vectors=True
            )
            if result:
                return result[0].vector
            return None
        except Exception as e:
            print(f"Error retrieving from Qdrant: {e}")
            return None

    async def delete_destination(self, destination_id: str) -> bool:
        """
        Remove a destination from the vector store.
        """
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.PointIdsList(
                    points=[destination_id]
                )
            )
            return True
        except Exception as e:
            print(f"Error deleting from Qdrant: {e}")
            return False

vector_service = VectorService()
