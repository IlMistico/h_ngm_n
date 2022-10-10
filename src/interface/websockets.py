# from src.interface.utils import ConnectionManager

# connection_manager = ConnectionManager(logger=logger)

# @game_router.websocket("/play")
# async def play_hangman(
#     websocket: WebSocket,
#     cookie_or_token: str = Depends(get_cookie_or_token),
# ):
#     await connection_manager.connect(websocket)
#     try:
#         while True:
#             guess = websocket.receive_text()

#             await connection_manager.send_message(guess, websocket=websocket)
#     except WebSocketDisconnect:
#         connection_manager.disconnect(websocket)

#         await connection_manager.broadcast("Disconnected")
