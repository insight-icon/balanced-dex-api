from typing import List
from fastapi import WebSocket
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        print("send_personal_message: " + message)
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        print("broadcast:", message)
        for connection in self.active_connections:
            await connection.send_text(message)


# class WebSocketConnection:
#     def __init__(self, ws: WebSocket):
#         self.uri = ws["uri"]
