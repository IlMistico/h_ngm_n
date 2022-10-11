from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from src.interface.websocket.utils import ConnectionManager, get_cookie_or_token
from src.service.game_manager import SinglePlayerGameManager

connection_manager = ConnectionManager()
singleplayer_game_manager = SinglePlayerGameManager()

singleplayer_game_router = APIRouter(prefix="/hangman/ws")

presentation = "Let's start with some introductions. Who are you?"
difficulty_phrase = "Well, welcome {}. How hard do you like to play? Choose between 'easy', 'medium' or 'hard'."
wrong_difficulty_phrase = (
    "Let me ask again, {}. Do you want your game easy, medium or hard?"
)


@singleplayer_game_router.websocket("/play")
async def play_hangman(
    websocket: WebSocket,
    cookie_or_token: str = Depends(get_cookie_or_token),
):
    await connection_manager.connect(websocket)
    try:
        while cookie_or_token:
            await connection_manager.send_message(presentation, websocket=websocket)
            username = await websocket.receive_text()

            await connection_manager.send_message(
                difficulty_phrase.format(username), websocket=websocket
            )
            difficulty = await websocket.receive_text()
            while difficulty not in ["easy", "medium", "hard"]:
                await connection_manager.send_message(
                    wrong_difficulty_phrase.format(username), websocket=websocket
                )
                difficulty = await websocket.receive_text()
            singleplayer_game_manager.start_game(username, difficulty)

            await connection_manager.send_message(
                singleplayer_game_manager.get_status(username=username),
                websocket=websocket,
            )

            while singleplayer_game_manager.get_status(username, guesses_only=True) > 0:

                await connection_manager.send_message(
                    " Guess a letter, or try the full word already: "
                )
                letter_or_word = await websocket.receive_text()
                if len(letter_or_word) == 1:
                    await connection_manager.send_message(
                        singleplayer_game_manager.new_guess(
                            username=username, letter=letter_or_word
                        )
                    )
                else:
                    await connection_manager.send_message(
                        singleplayer_game_manager.submit_result(
                            username=username, word=letter_or_word
                        )
                    )
                    break

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)

        await connection_manager.broadcast("Disconnected")
