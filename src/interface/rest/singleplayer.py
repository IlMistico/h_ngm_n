from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.responses import PlainTextResponse
from src.interface.auth.rest import get_current_active_user
from src.models.users import User
from src.service.game_manager import SinglePlayerGameManager

singleplayer_game_manager = SinglePlayerGameManager()

singleplayer_game_router = APIRouter(prefix="/hangman/rest/single")


@singleplayer_game_router.post("/start", response_class=PlainTextResponse)
def init_game(
    difficulty: str, current_user: User = Depends(get_current_active_user)
) -> str:
    """
    Initialize a new game for the username passed as argument, with a particular difficulty level.
    The server extracts a new word and returns the current status;
    """
    username = current_user.username
    singleplayer_game_manager.start_game(player=username, difficulty=difficulty)
    return singleplayer_game_manager.get_status(username=username)


@singleplayer_game_router.get("/status", response_class=PlainTextResponse)
def get_status(current_user: User = Depends(get_current_active_user)) -> str:
    """
    Returns the current status of the client guessing.
    The current status is represented by the remaining number of guessing and the current status of the guessing;
    """
    username = current_user.username

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
def new_guess(letter: str, current_user: User = Depends(get_current_active_user)):
    """
    Look for the letter in the word and return the
    result of guessing with the current status;
    """
    username = current_user.username

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
def submit_result(word: str, current_user: User = Depends(get_current_active_user)):
    """
    Try to guess the whole word, it returns a
    string in case of win or lose the game. Only one submit_result
    per game is admitted!
    """
    username = current_user.username
    try:
        return singleplayer_game_manager.submit_result(username=username, word=word)
    except KeyError as ke:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ke),
        )
