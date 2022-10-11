import sys, os
from pathlib import Path
from fastapi import FastAPI

if str(ROOT := Path(__file__).parent.parent.resolve()) not in sys.path:
    sys.path.append(str(ROOT))

from src.service.game_manager import SinglePlayerGameManager


if __name__ == "__main__":
    singleplayer_game_manager = SinglePlayerGameManager()

    print("I see youŕe here to play a game of hangman. But first, tell me something.")
    username = input("Who are you, misterious stranger?\n")
    print(
        f"{username} uh? Ok then, and tell me, what kind of game do you wish to play?"
    )
    difficulty = input("easy\tmedium\thard\n")
    if difficulty not in ["easy", "medium", "hard"]:
        input(
            f"Let me ask again, {username}. Do you want your game easy, medium or hard?\n"
        )
    else:
        print(
            f"A{'n' if difficulty == 'easy' else ''} {difficulty} game for {username} it is! Here we go!"
        )
        singleplayer_game_manager.start_game(player=username, difficulty=difficulty)
        print(singleplayer_game_manager.get_status(username=username))
        while singleplayer_game_manager.get_status(username, guesses_only=True) > 0:

            letter_or_word = input(" Guess a letter, or try the full word already: ")
            if len(letter_or_word) == 1:
                print(
                    singleplayer_game_manager.new_guess(
                        username=username, letter=letter_or_word
                    )
                )
            else:
                print(
                    singleplayer_game_manager.submit_result(
                        username=username, word=letter_or_word
                    )
                )
                break
        print(f"Well, {username}, it has been a pleasure. Now, care for another ride?")
