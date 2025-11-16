from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.database import save_message, load_messages_for_today
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["Chat"])

class ConnectionManager:
    def __init__(self):
        self.connections = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.append(ws)
        # Send today's history
        # await ws.send_json({"type": "history", "messages": load_messages_for_today()})
        try:
            await ws.send_json({"type": "history", "messages": load_messages_for_today()})
        except Exception as e:
            print(f"⚠️ Failed to send history: {e}")
            self.disconnect(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.connections:
            self.connections.remove(ws)

    async def broadcast(self, message: dict):
        dead = []
        for conn in self.connections:
            try:
                await conn.send_json(message)
            except:
                dead.append(conn)
        for conn in dead:
            self.disconnect(conn)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_json()
            username = data.get("username", "Anonymous")
            text = data.get("message", "").strip()
            if not text:
                continue

            msg = {"username": username, "message": text, "timestamp": datetime.utcnow().isoformat() + "Z",
}
            save_message(username, text)
            await manager.broadcast({"type": "chat", "message": msg})

    except WebSocketDisconnect:
        manager.disconnect(ws)
