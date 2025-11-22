from fastapi import WebSocket
from typing import List
import json

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_message(self, message: dict):
      print(f"🔄 WEBSOCKET: Starting broadcast to {len(self.active_connections)} connections")
      
      message_json = json.dumps(message)
      print(f"🔄 WEBSOCKET: Message JSON: {message_json}")
      
      send_tasks = []
      for connection in self.active_connections:
          send_tasks.append(connection.send_text(message_json))
      
      if send_tasks:
          import asyncio
          try:
              await asyncio.gather(*send_tasks, return_exceptions=True)
              print("✅ WEBSOCKET: Broadcast completed successfully!")
          except Exception as e:
              print(f"❌ WEBSOCKET: Broadcast failed: {e}")

websocket_manager = WebSocketManager()