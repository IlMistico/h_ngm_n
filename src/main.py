from subprocess import Popen
import sys, os
from pathlib import Path
from fastapi import FastAPI

if str(ROOT := Path(__file__).parent.parent.resolve()) not in sys.path:
    sys.path.append(str(ROOT))

from src.interface.rest.singleplayer import singleplayer_game_router as rest_router
from src.interface.websocket.singleplayer import singleplayer_game_ws as ws_router

hangman_app = FastAPI()


hangman_app.include_router(rest_router)
hangman_app.include_router(ws_router)


if __name__ == "__main__":
    import uvicorn

    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("HOST", 8765)

    if (SSL_KEYFILE := os.getenv("SSL_KEYFILE")) and (
        SSL_CERTFILE := os.getenv("SSL_CERTFILE")
    ):

        Popen(["python", "-m", "https_redirect"])

        uvicorn.run(
            "main:hangman_app",
            host=HOST,
            port=443,
            log_level="info",
            ssl_keyfile=SSL_KEYFILE,
            ssl_certfile=SSL_CERTFILE,
        )
    else:
        uvicorn.run(
            "main:hangman_app",
            host=str(HOST),
            port=int(PORT),
            log_level="info",
        )
