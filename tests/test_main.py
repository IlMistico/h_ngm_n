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

from src.interface.websocket.singleplayer import singleplayer_game_router


HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", 8765)
base_url = f"ws://{HOST}:{PORT}/hangman"


client = TestClient(app=hangman_app, base_url=base_url)
difficulty_map: Dict[str, int] = {"easy": 10, "medium": 7, "hard": 4}


@pytest.mark.skip
@pytest.mark.parametrize(
    "difficulty",
    list(difficulty_map.keys()),
)
def test_singleplayer_game_rest(difficulty, username="Jackster"):

    base_url_single = base_url + "/single"

    # Test the single endpoints
    start_response = client.post(
        base_url_single + "/start",
        params={"username": username, "difficulty": difficulty},
    )

    status_response = client.get(
        base_url_single + "/status",
        params={
            "username": username,
        },
    )

    guess_response = client.put(
        base_url_single + "/guess",
        params={"username": username, "letter": "a"},
    )

    invalid_guess_response = client.put(
        base_url_single + "/guess",
        params={"username": username, "letter": "argwer"},
    )

    submit_response = client.post(
        base_url_single + "/submit",
        params={"username": username, "word": "family"},
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
            base_url_single + "/guess",
            params={
                "username": username,
                "letter": random.choice(string.ascii_lowercase),
            },
        )
        for _ in range(limit * 2)
    ]

    assert len(set([resp.text for resp in guesses_responses])) <= limit


def test_singleplayer_game_websocket(username="Jackster"):
    # client = TestClient(singleplayer_game_router)
    with client.websocket_connect("ws/play") as websocket:
        presentation = websocket.receive_text()
        websocket.send_text(username)
