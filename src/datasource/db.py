from typing import Dict, Optional
import uuid
from src.models.game import Game

# Mimics an actual database where params are stored.
class ParamsDb:
    """
    Connects the service to a DB used to store parameters
    Currently mocked.
    """

    def __init__(self) -> None:
        self.words = [
            w.lower()
            for w in [
                "Create",
                "Credit",
                "Crisis",
                "Custom",
                "Fairly",
                "Fallen",
                "Family",
                "Famous",
                "Father",
                "Golden",
                "Ground",
                "Growth",
                "Guilty",
                "Handed",
                "Lights",
                "Likely",
                "Linked",
                "Liquid",
                "Listen",
                "Little",
                "Living",
            ]
        ]
        self.difficulty_map: Dict[str, int] = {"easy": 10, "medium": 7, "hard": 4}


class GamesDb:
    """
    Connects the service to a DB used to store games for further analysis.
    Currently mocked.
    """

    def __init__(self) -> None:
        self.games: Dict[str, Game] = {}

    def store(username: str, game: Game):
        pass

    def get(username: str, game_id: Optional[uuid.UUID]):
        pass


class UsersDb:
    """
    Connects the service to a DB used to store users for oauth.
    Currently mocked.
    """

    def __init__(self) -> None:
        self.users = {
            "johndoe": {
                "username": "johndoe",
                "full_name": "John Doe",
                "email": "johndoe@example.com",
                "hashed_password": "fakehashedsecret",
                "disabled": False,
            },
            "alice": {
                "username": "alice",
                "full_name": "Alice Wonderson",
                "email": "alice@example.com",
                "hashed_password": "fakehashedsecret2",
                "disabled": True,
            },
        }

    def get_user(self, username):
        return self.users.get(username)
