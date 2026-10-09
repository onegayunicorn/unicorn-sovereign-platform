"""Live job update WebSocket."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio, json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []
    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)
    async def broadcast(self, message: dict):
        for ws in list(self.active):
            try:
                await ws.send_text(json.dumps(message))
            except Exception:
                self.active.remove(ws)

manager = ConnectionManager()

@router.websocket("/jobs/{job_id}")
async def job_events(websocket: WebSocket, job_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast({"job_id": job_id, "echo": data})
    except WebSocketDisconnect:
        manager.active.remove(websocket)
