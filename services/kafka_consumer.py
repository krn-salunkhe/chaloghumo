import asyncio
import json
from aiokafka import AIOKafkaConsumer
from core.config import settings
from services.signals import signal_service

class KafkaSignalConsumer:
    """
    Consumer for high-velocity signals from Kafka.
    Handles real-time updates like crowd density and emergency alerts.
    """
    def __init__(self):
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.topic = "destination_signals"
        self.consumer = None

    async def start(self):
        """
        Initialize and start the Kafka consumer.
        """
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id="signal_ingestion_group",
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        await self.consumer.start()
        print(f"Kafka Consumer started on topic: {self.topic}")
        
        try:
            async for msg in self.consumer:
                await self.process_signal(msg.value)
        finally:
            await self.consumer.stop()

    async def process_signal(self, data: dict):
        """
        Process incoming signals and update Redis with aggressive caching.
        """
        destination_id = data.get("destination_id")
        signal_type = data.get("type") # e.g., 'crowd_density', 'emergency'
        value = data.get("value")
        
        if not destination_id or not signal_type:
            return

        print(f"Received Kafka signal for {destination_id}: {signal_type} = {value}")

        # Aggressive Caching: Update Redis immediately with high priority
        # We use a longer TTL for high-velocity signals if we want to ensure availability 
        # but the 'aggressiveness' usually refers to write-through or immediate propagation.
        
        if signal_type == "crowd_density":
            # Update the societal state in Redis
            current_soc = await signal_service.get_societal_state(destination_id) or {}
            current_soc["crowd_density"] = value
            await signal_service.redis.set(
                f"signal:soc:{destination_id}", 
                json.dumps(current_soc), 
                ex=300 # Shorter TTL (5 mins) for high-velocity data to ensure freshness
            )
        
        elif signal_type == "emergency":
            # Emergency signals have longer persistence to ensure safety
            await signal_service.redis.set(
                f"signal:emergency:{destination_id}", 
                json.dumps({"alert": value, "active": True}), 
                ex=3600 # 1 hour
            )

async def run_consumer():
    consumer = KafkaSignalConsumer()
    await consumer.start()

if __name__ == "__main__":
    asyncio.run(run_consumer())
