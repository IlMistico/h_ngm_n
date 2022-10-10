import uuid
from pydantic import BaseModel, conint


class Game(BaseModel):
    game_id: uuid.UUID
    word: str
    status: str
    attempts_remaining: conint(ge=0)
