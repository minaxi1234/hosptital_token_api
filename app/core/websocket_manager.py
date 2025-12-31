from fastapi import WebSocket
from typing import Set
import json

class WebSocketManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, event: dict):
        if not self.active_connections:
            return

        message = json.dumps(event)
        dead = []

        for ws in self.active_connections:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)

        for ws in dead:
            self.disconnect(ws)

# 🔴 SINGLE INSTANCE — NEVER CREATE AGAIN
websocket_manager = WebSocketManager()
