import logging
from typing import List, Union
from fastapi import WebSocket, Cookie, Query, status


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Union[str, None] = Cookie(default=None),
    token: Union[str, None] = Query(default=None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


# Websocket handling
class ConnectionManager:
    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger()
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.logger.info("Connecting websocket")

        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.logger.info("Disconnecting websocket")

        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        self.logger.info(f"Sending message: {message}")

        await websocket.send_text(message)

    async def broadcast(self, message: str):
        self.logger.info(f"Broadcasting to all connections. Message: {message}")
        for connection in self.active_connections:
            await connection.send_text(message)
