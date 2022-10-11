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
