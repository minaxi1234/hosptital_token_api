from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import websocket_manager


router = APIRouter()

@router.websocket("/ws/tokens")
async def websocket_token_updates(websocket: WebSocket):
  print("🔄 WebSocket connection attempt received")
  await websocket_manager.connect(websocket)
  print("✅ WebSocket connected successfully") 
  try:
    while True:
      data = await websocket.receive_text()
      print(f"📨 Received message: {data}")
  except WebSocketDisconnect:
    websocket_manager.disconnect(websocket)

