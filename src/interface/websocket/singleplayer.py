from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from fastapi_jwt_auth import AuthJWT
from src.interface.websocket.utils import ConnectionManager
from src.service.game_manager import SinglePlayerGameManager

singleplayer_game_manager = SinglePlayerGameManager()

singleplayer_game_ws = APIRouter()

presentation = "Let's start with some introductions. Who are you?"
difficulty_phrase = "Hi {}! Please choose between 'easy', 'medium' or 'hard'."
wrong_difficulty_phrase = (
    "Let me ask again, {}. Do you want your game easy, medium or hard?"
)
guess_message = " You have {} tries. Good Luck!"

new_match_question = "{}Would you care for another round? (y/n)"
new_match_message = "Alright then, here we go!"
goodbye_message = "Very well {}, it was a pleasure playing with you. Have a good life!"

connection_manager = ConnectionManager()


@singleplayer_game_ws.websocket_route("/hangman/ws/play")
async def play_hangman(websocket: WebSocket):
    username = None
    await connection_manager.connect(websocket)
    try:
        while True:
            if not username:
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
            guesses_remaining = singleplayer_game_manager.get_status(
                username, guesses_only=True
            )

            await connection_manager.send_message(
                guess_message.format(guesses_remaining),
                websocket=websocket,
            )

            while guesses_remaining >= 0:

                letter_or_word = await websocket.receive_text()
                if len(letter_or_word) == 1 and guesses_remaining != 0:
                    await connection_manager.send_message(
                        singleplayer_game_manager.new_guess(
                            username=username, letter=letter_or_word
                        ),
                        websocket=websocket,
                    )
                    guesses_remaining -= 1
                else:
                    await connection_manager.send_message(
                        singleplayer_game_manager.submit_result(
                            username=username,
                            word=letter_or_word,
                        ),
                        websocket=websocket,
                    )
                    break

            await connection_manager.send_message(
                new_match_question.format(""),
                websocket=websocket,
            )

            while (new_match := await websocket.receive_text()) not in [
                "y",
                "n",
                "Y",
                "N",
            ]:
                await connection_manager.send_message(
                    new_match_question.format("Sorry, I'm not sure what you said. "),
                    websocket=websocket,
                )
            if new_match.lower() == "n":
                await connection_manager.send_message(
                    goodbye_message.format(username),
                    websocket=websocket,
                )
                connection_manager.disconnect(websocket)
                break

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)

        await connection_manager.broadcast("Disconnected")
