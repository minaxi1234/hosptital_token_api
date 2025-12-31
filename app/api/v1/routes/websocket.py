from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import websocket_manager

router = APIRouter()

@router.websocket("/ws/tokens")
async def websocket_token_updates(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
