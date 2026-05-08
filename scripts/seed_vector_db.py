import asyncio
import json
import os
import httpx
from typing import List, Dict, Any
from services.llm import llm_service
from services.vector_store import vector_service

import csv
import io

CITY_DATA_URL = "https://raw.githubusercontent.com/opentraveldata/opentraveldata/master/opentraveldata/optd_por_public.csv"
CHECKPOINT_FILE = "seed_checkpoint.json"

async def fetch_cities() -> List[Dict[str, Any]]:
    """
    Download and parse the opentraveldata POR dataset.
    Uses '^' as delimiter.
    """
    print(f"Fetching city data from {CITY_DATA_URL}...")
    async with httpx.AsyncClient() as client:
        # Large file, we'll stream or just read it if memory allows
        response = await client.get(CITY_DATA_URL)
        response.raise_for_status()
        
        f = io.StringIO(response.text)
        reader = csv.DictReader(f, delimiter='^')
        
        cities = []
        for row in reader:
            # location_type 'C' for City, 'H' for Heliport, 'A' for Airport, 'R' for Railway...
            # We want Cities and maybe some Airports that act as city hubs
            if row.get('location_type') in ['C', 'CA', 'A']:
                cities.append({
                    "name": row.get('name') or row.get('asciiname'),
                    "country": row.get('country_code'),
                    "lat": float(row.get('latitude')) if row.get('latitude') else 0.0,
                    "lng": float(row.get('longitude')) if row.get('longitude') else 0.0,
                    "iata": row.get('iata_code')
                })
        return cities

def load_checkpoint() -> set:
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_checkpoint(completed_ids: set):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(list(completed_ids), f)

async def seed_data(limit: int = 1000):
    """
    Main seeding logic.
    """
    cities = await fetch_cities()
    completed_ids = load_checkpoint()
    
    # Filter for cities with population > some threshold or just take top N
    # For this demo, we'll sort by population if available, or just take the first N
    # The lmfmaier dataset has name, country, lat, lng
    
    count = 0
    for city in cities:
        if count >= limit:
            break
            
        city_id = city.get('iata') or f"{city['name']}_{city['country']}".replace(" ", "_").lower()
        if city_id in completed_ids:
            continue
            
        print(f"Processing {count+1}/{limit}: {city['name']}, {city['country']}...")
        
        # 1. Generate a descriptive 'vibe' for the city
        # In a real production scenario, we might use Gemini to generate this
        # For 1000 cities, to save time/cost, we'll use a template
        vibe_description = f"{city['name']} in {city['country']} is a destination known for its unique atmosphere. " \
                           f"Located at coordinates {city['lat']}, {city['lng']}, it offers a blend of local culture and geography."
        
        # 2. Generate embedding
        embedding = await llm_service.generate_embedding(vibe_description)
        
        # Fallback for testing if API key is invalid
        if all(v == 0.0 for v in embedding):
            print(f"Warning: Using mock embedding for {city['name']} (check API key)")
            import random
            embedding = [random.uniform(-1, 1) for _ in range(384)]
        
        # 3. Upsert to Qdrant
        payload = {
            "name": city["name"],
            "country": city["country"],
            "lat": city["lat"],
            "lng": city["lng"],
            "vibe_description": vibe_description
        }
        
        success = await vector_service.upsert_destination(
            destination_id=city_id,
            vector=embedding,
            payload=payload
        )
        
        if success:
            completed_ids.add(city_id)
            save_checkpoint(completed_ids)
            count += 1
        else:
            print(f"Failed to upsert {city['name']}")
            
    print(f"Seeding completed. {count} cities added.")

if __name__ == "__main__":
    # We use a smaller limit for the first run or allow user to specify
    asyncio.run(seed_data(limit=1000))
