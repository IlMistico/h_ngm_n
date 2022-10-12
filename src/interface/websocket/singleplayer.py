from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from src.interface.websocket.utils import ConnectionManager, get_cookie_or_token
from src.service.game_manager import SinglePlayerGameManager

singleplayer_game_manager = SinglePlayerGameManager()

singleplayer_game_ws = APIRouter()

presentation = "Let's start with some introductions. Who are you?"
difficulty_phrase = "Ok then/ Tell me, {}, how hard do you like to play? Choose between 'easy', 'medium' or 'hard'."
wrong_difficulty_phrase = (
    "Let me ask again, {}. Do you want your game easy, medium or hard?"
)
guess_message = " Guess a letter, or try the full word already: "

new_match_question = "Would you care for another round? (y/n)"
new_match_message = "Alright then, here we go!"
goodbye_message = "Very well {}, it was a pleasure playing with you. Have a good life!"

connection_manager = ConnectionManager()


@singleplayer_game_ws.websocket_route("/hangman/ws/play")
async def play_hangman(
    websocket: WebSocket,
    cookie_or_token: str = Depends(get_cookie_or_token),
):
    username = None
    await connection_manager.connect(websocket)
    try:
        while cookie_or_token:
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

            while (
                guesses_remaining := singleplayer_game_manager.get_status(
                    username, guesses_only=True
                )
                >= 0
            ):

                await connection_manager.send_message(
                    guess_message,
                    websocket=websocket,
                )
                letter_or_word = await websocket.receive_text()
                if len(letter_or_word) == 1:
                    await connection_manager.send_message(
                        singleplayer_game_manager.new_guess(
                            username=username, letter=letter_or_word
                        ),
                        websocket=websocket,
                    )
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
                new_match_question,
                websocket=websocket,
            )
            new_match = await websocket.receive_text()
            if new_match.lower() in ["y", "yes", "of course"]:
                await connection_manager.send_message(
                    new_match_question,
                    websocket=websocket,
                )
            else:
                await connection_manager.send_message(
                    goodbye_message.format(username),
                    websocket=websocket,
                )
                connection_manager.disconnect(websocket)
                break

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)

        await connection_manager.broadcast("Disconnected")
