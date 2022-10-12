from typing import Dict, List, Optional
import uuid
from pydantic import BaseModel, conint
import random

from src.datasource.db import ParamsDb, GamesDb
from src.models.game import Game


def window(arr, window_size):
    for i in range(len(arr) - window_size + 1):
        yield arr[i : i + window_size]


class UniqueUsernameException(Exception):
    def __init__(self, *args: object) -> None:
        self.message = "User already exists."
        super().__init__(*args)


class SinglePlayerGameManager:
    def __init__(self) -> None:
        params_db = ParamsDb()
        self.games_db = GamesDb()

        self.words = params_db.words
        self.games: Dict[str, Game] = {}
        self.difficulty_map: Dict[str, int] = params_db.difficulty_map

    def start_game(self, player: str, difficulty: str) -> str:
        if difficulty not in self.difficulty_map.keys():
            raise KeyError(f"Difficulty {difficulty} unknown.")
        word = random.choice(self.words)
        game_id = uuid.uuid1()
        if player in self.games.keys():
            # raise UniqueUsernameException()
            return False
        new_game = Game(
            game_id=game_id,
            word=word,
            status="".join(["_"] * len(word)),
            attempts_remaining=self.difficulty_map[difficulty],
        )
        self.games[player] = new_game
        self.games_db.store(new_game)

        return self.get_status(player)

    def get_status(self, username: str, guesses_only: bool = False) -> str:
        if not (game := self.games.get(username)):
            raise KeyError(f"{username} does not have an active game.")

        remaining_attemps_message = (
            f"{attempts_remaining} guess{'' if attempts_remaining == 1 else 'es'} remaining!"
            if (attempts_remaining := game.attempts_remaining) > 0
            else f"Sorry {username}, you have {attempts_remaining} remaining guesses! Try your luck or start a new game!"
        )
        if guesses_only:
            return game.attempts_remaining
        else:
            return f"{' '.join(list(game.status))}.\n" + remaining_attemps_message

    def new_guess(self, username: str, letter: str) -> str:
        if not (game := self.games.get(username)):
            raise KeyError(f"{username} does not have an active game.")
        new_status = "".join(
            [
                game.word[i] if game.word[i] == letter else c
                for i, c in enumerate(list(game.status))
            ]
        )
        if game.attempts_remaining > 0:
            self.games[username] = Game(
                game_id=game.game_id,
                word=game.word,
                status=new_status,
                attempts_remaining=game.attempts_remaining - 1,
            )

        return self.get_status(username)

    def submit_result(self, username: str, word: str) -> bool:
        if not (game := self.games.get(username)):
            raise KeyError(f"Player {username} unknown.")
        del self.games[username]
        return (
            f"{username} wins! The word was indeed {game.word}!"
            if word == game.word
            else f"Aaaaah, too bad {username}, the word was actually {game.word}. Best of luck next time!"
        )
