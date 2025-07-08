from fastapi import APIRouter, WebSocket
from core.redis_client import redis_client

router = APIRouter() 

@router.websocket("/ws/notifications/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(f"user:{user_id}")

    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=30.0)
            if message:
                await websocket.send_text(message['data'].decode())
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await pubsub.unsubscribe(f"user:{user_id}")
        await websocket.close()
