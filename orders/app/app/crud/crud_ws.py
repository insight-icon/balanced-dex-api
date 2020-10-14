from fastapi import WebSocket


class CrudWS:

    @staticmethod
    async def send_text(websocket: WebSocket, message: str):
        print("CrudWS - send_text : " + message)
        try:
            await websocket.send_text(message)
        except:
            await websocket.close()
