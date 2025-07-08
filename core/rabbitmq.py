import aio_pika
from core.config import settings
import json
import time 

class RabbitMqClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queues = {}
        
    async def connect(self):
        self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)
        
    async def publish(self,queue_name: str,message: dict):
        
        if not self.channel:
            await self.connect()
        
        if queue_name not in self.queues:
            queue = await self.channel.declare_queue(queue_name, durable=True)
            self.queues[queue_name] = queue
        else:
            queue = self.queues[queue_name] 
            
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=queue.name
        )
        

rabbitmq = RabbitMqClient()