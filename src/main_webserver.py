import sys, os
from pathlib import Path
from fastapi import FastAPI

if str(ROOT := Path(__file__).parent.parent.resolve()) not in sys.path:
    sys.path.append(str(ROOT))

from src.interface.singleplayer_rest import singleplayer_game_router

hangman_app = FastAPI()


hangman_app.include_router(singleplayer_game_router)


if __name__ == "__main__":
    import uvicorn

    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 8765)

    uvicorn.run(
        "main:hangman_app",
        host=str(HOST),
        port=int(PORT),
        log_level="info",
    )
