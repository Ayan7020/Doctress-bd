import asyncio
from workers.uploadDocsConsumer import start_consumer

if __name__ == "__main__":
    print("Starting RabbitMQ consumer...")
    asyncio.run(start_consumer())