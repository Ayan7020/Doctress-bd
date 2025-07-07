import aio_pika
from core.config import settings

class RabbitMqClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        
    async def connect(self):
        self.connection = await aio_pika.connect_robust(settings.REDIS_CONNECTION_URL)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)
        
    async def publish(self,queue_name: str,message: dict):
        
        if not self.channel:
            await self.connect()
            
        queue = await self.channel.declare_queue(queue_name,durable=True)
        await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=str(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=queue.name
        )
        

rabbitmq = RabbitMqClient()