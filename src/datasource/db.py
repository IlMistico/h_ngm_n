from typing import Dict
from src.models.game import Game

# Mimics an actual database where params are stored.
class ParamsDb:
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
    def __init__(self) -> None:
        self.games: Dict[str, Game] = {}
