import random
import string
import sys, os
import pytest
from typing import Dict
from pathlib import Path

from http import HTTPStatus
from fastapi.testclient import TestClient

if str(ROOT := Path(__file__).parent.parent.resolve()) not in sys.path:
    sys.path.append(str(ROOT))


from src.main import hangman_app

from src.interface.websocket.singleplayer import singleplayer_game_ws


HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", 8765)
client = TestClient(app=hangman_app)
base_url = f"http://{HOST}:{PORT}"


difficulty_map: Dict[str, int] = {"easy": 10, "medium": 7, "hard": 4}


# @pytest.mark.skip
@pytest.mark.parametrize(
    "difficulty",
    list(difficulty_map.keys()),
)
def test_singleplayer_game_rest(difficulty, username="johndoe", password="johndoe"):

    url = base_url + "/hangman/rest/single"

    token_request = client.post(
        base_url + "/login",
        data={"grant_type": "password", "username": username, "password": password},
    )

    assert token_request.status_code == 200
    token = token_request.json().get("access_token")
    assert bool(token)
    assert token == "johndoe"

    auth_header = {"Authorization": f"Bearer {token}"}

    # Test the single endpoints
    start_response = client.post(
        url + "/start", params={"difficulty": difficulty}, headers=auth_header
    )

    status_response = client.get(url + "/status", headers=auth_header)

    guess_response = client.put(
        url + "/guess", params={"letter": "a"}, headers=auth_header
    )

    invalid_guess_response = client.put(
        url + "/guess", params={"letter": "argwer"}, headers=auth_header
    )

    submit_response = client.post(
        url + "/submit", params={"word": "family"}, headers=auth_header
    )

    # Map each response with the expected status code
    expected_codes_map = {
        **dict(
            zip(
                [
                    start_response,
                    status_response,
                    guess_response,
                    submit_response,
                ],
                [HTTPStatus.OK] * 4,
            )
        ),
        **dict(
            zip(
                [invalid_guess_response],
                [HTTPStatus.BAD_REQUEST] * 1,
            )
        ),
    }
    # Check each response has the expected status code
    assert all(
        [
            response.status_code == expected_code
            for response, expected_code in expected_codes_map.items()
        ]
    )
    # TODO test string responses

    # Test if "status" and "guess" functions stop allowing new guesses once limit has been reached
    limit = difficulty_map[difficulty]

    guesses_responses = [
        client.put(
            url + "/guess",
            params={
                "letter": random.choice(string.ascii_lowercase),
            },
            headers=auth_header,
        )
        for _ in range(limit * 2)
    ]

    assert len(set([resp.text for resp in guesses_responses])) <= limit


@pytest.mark.skip()
@pytest.mark.parametrize(
    "difficulty",
    list(difficulty_map.keys()),
)
async def test_singleplayer_game_websocket(difficulty, username="Jackster"):
    url = f"ws://{HOST}:{PORT}/hangman/ws/play"
    with client.websocket_connect(url) as websocket:
        presentation = websocket.receive_text()
        await websocket.send_text(username)
        difficulty_selection = await websocket.receive_text()
        await websocket.send_text(difficulty)
        difficulty_selection = await websocket.receive_text()
        await websocket.send_text("a")
        await websocket.send_text("e")
        await websocket.send_text("tellar")
