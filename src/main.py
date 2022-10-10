import sys, os
from pathlib import Path
from fastapi import FastAPI

if str(ROOT := Path(__file__).parent.parent.resolve()) not in sys.path:
    sys.path.append(str(ROOT))

from src.interface.singleplayer_rest import singleplayer_game_router

hangman_app = FastAPI()


# @hangman_app.get("/", response_class=HTMLResponse)
# def root():
#     return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)


# @hangman_app.get("/login", response_class=HTMLResponse)
# async def register(request: Request):

#     form_data = await request.form()

#     with open(ROOT.joinpath("src/interface/templates/users/register.html")) as f:
#         return HTMLResponse(content=f.read())


hangman_app.include_router(singleplayer_game_router)


if __name__ == "__main__":
    import uvicorn

    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 8090)

    uvicorn.run(
        "main:hangman_app",
        host=str(HOST),
        port=int(PORT),
        log_level="info",
    )
