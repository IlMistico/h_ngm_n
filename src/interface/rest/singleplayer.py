from fastapi import (
    APIRouter,
    HTTPException,
    status,
)
from fastapi.responses import PlainTextResponse
import logging

# get logger
logger = logging.getLogger("hangman")

from src.service.game_manager import SinglePlayerGameManager

singleplayer_game_manager = SinglePlayerGameManager()

singleplayer_game_router = APIRouter(prefix="/hangman/rest/single")


@singleplayer_game_router.post("/start", response_class=PlainTextResponse)
def init_game(username: str, difficulty: str) -> str:
    """
    Initialize a new game for the username passed as argument, with a particular difficulty level.
    The server extracts a new word and returns the current status;
    """
    singleplayer_game_manager.start_game(player=username, difficulty=difficulty)
    return singleplayer_game_manager.get_status(username=username)


@singleplayer_game_router.get("/status", response_class=PlainTextResponse)
def get_status(
    username: str,
    # cookie_or_token: str = Depends(get_cookie_or_token),
) -> str:
    """
    Returns the current status of the client guessing.
    The current status is represented by the remaining number of guessing and the current status of the guessing;
    """
    try:
        return singleplayer_game_manager.get_status(
            username=username,
        )
    except KeyError as ke:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ke),
        )


@singleplayer_game_router.put("/guess", response_class=PlainTextResponse)
def new_guess(
    username: str,
    letter: str,
    # cookie_or_token: str = Depends(get_cookie_or_token),
):
    """
    Look for the letter in the word and return the
    result of guessing with the current status;
    """
    if len(letter) != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New guesses must be exactly 1 (one) letter long.",
        )
    try:
        return singleplayer_game_manager.new_guess(username=username, letter=letter)
    except KeyError as ke:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ke),
        )


@singleplayer_game_router.post("/submit", response_class=PlainTextResponse)
def submit_result(
    username: str,
    word: str,
    # cookie_or_token: str = Depends(get_cookie_or_token),
):
    """
    Try to guess the whole word, it returns a
    string in case of win or lose the game. Only one submit_result
    per game is admitted!
    """
    try:
        return singleplayer_game_manager.submit_result(username=username, word=word)
    except KeyError as ke:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ke),
        )