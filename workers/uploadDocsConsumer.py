
import asyncio
import json
import aio_pika
from core.config import settings
from fastapi import HTTPException
from langchain_community.document_loaders import AzureBlobStorageFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.vector.VectorStore import VectorStore
from core.redis_client import redis_client

QUEUE_NAME = "uploaddocs" 

async def handle_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            print("Get Message")
            payload = json.loads(message.body.decode()) 
            
            if not payload:
                print("Received message with empty payload.")
                return 
            
            blob_url = payload.get('blob_url') 
            companyName = payload.get('companyName') 
            department = payload.get('department') 
            userId = payload.get("userId")
            
            if not blob_url:
                print("no blub url found")
                return
            
            stored_filename = payload.get('stored_filename') 
            
            loader = AzureBlobStorageFileLoader(conn_str=settings.AzureConnection_string, container="doctres-files",blob_name=stored_filename)
            print("loading file from azure")
            docs = loader.load()
            for doc in docs:
                docs[0].metadata.update({
                    "stored_filename":stored_filename,
                    "companyName":companyName,
                    "department": department                    
                })
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
            print("splitting")
            chunks = splitter.split_documents(docs)
            print("adding in vector Database")
            await VectorStore.add_documents(chunks)
            print("publishing")
            await redis_client.publish(
                f"user:{userId}",
                f"File '{stored_filename}' preprocessing completed"
            )
            print("finish")
            return 
        except Exception as e:
            print(f"Error processing message: {e}")  
            
async def start_consumer():
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    await queue.consume(handle_message, no_ack=False)
    print("Started consuming from queue:", QUEUE_NAME)
    await asyncio.Event().wait()