# The hangman game server

This is an implementation of the hangman game in Python. It contains a lot of useful concepts to use FastAPI (endpoints, OAuth2, websockets...)

# Instructions to play
## Launch the server
The easiest way is to use docker: build the image with the provided Dockerfile and launch a container. By default the server listens on port 8765, edit the PORT env variable in the Dockerfile to change it.
In alternative, install `requirements.txt` in a virtual environment, activate it and launch `python src/main.py`. Again, default port is 8765.
## Play
There are two ways to play: 
### REST with Oauth2: 
- POST to http://www.HOST:PORT/login with form = {"grant_type": "password", "username": "johndoe", "password": johndoe"}, you will receive a (fake) token ("johndoe"). You can skip this step as the token is fake and always the same. 
Now add the following header to further requests: {"Authorization": "Bearer johndoe"}
- POST to http://www.HOST:PORT/hangman/rest/single/start?difficulty=choose between easy, medium and hard
- PUT to http://www.HOST:PORT/hangman/rest/single/guess?letter=choose letter
- keep doing PUT requests to http://www.HOST:PORT/hangman/rest/single/guess?letter=choose letter. Keep in mind, if you run out of guesses, further requests will be accepted but will not add further letters, even if you are correct.
- POST to http://www.HOST:PORT/hangman/rest/single/submit?word=choose word. You will receive a message to tell you if you won or not, then the game will end.
### Websocket unauthenticated:
- connect to the websocket on the url ws://HOST:PORT/hangman/ws/play
- follow the messages. You will be requested to insert a username and a difficulty level. 
- keep guessing. If you run out of guesses, your next guess will be treated as a solution attempt, even if it's only 1 letter long!
- when the game ends, you will be asked if you want to play again with the same username or close the game (and the connection).

# Dev diary

## Step 0: CLI game - COMPLETED
Write the game engine and a simple `main_cli.py` for a single player to play the game from command line.

## Step 1. REST single-player game - COMPLETED
Expose the game via REST endpoints to support single player games. 

Many player can play indipendently at the same time: each will be handled asynchronously.

Launch `src/main_cli.py` to start the server. If necessary, set env variables `HOST` and `PORT` to use custom values.

## Step 2. Websockets - COMPLETED
Use websockets (persistent connection) to handle each game. 

## Step 3. Secure communications - COMPLETED 
Add cryptography to both REST and Websocket versions of the game, to encrypt/decrypt messages.
### Step 3.1 Add SSL certificates - COMPLETED
Set the values for the env variables `SSL_KEYFILE = /path/to/privkey.pem` and `SSL_CERTFILE = /path/to/fullchain.pem`. Requires to setup domain and certificates.

### 3.2 (EXTRA) Add authentication - COMPLETED (partially, naive)
Allow a couple of predetermined users and use OAuth2 to login and play

To keep things simple, this service stores the users db and provides the token. A real OAuth2 flow would have separate entities for that.

TODO:
- add a registration UI and flow to add more users
- add scopes and roles (bit redundant for this game maybe :-D )
- handle auth flow for Websockets (need more "manual" handling)

## Step 4. PvP game - TODO
The same as step 1, but allows two players to compete in the same game. 

## Step 5. Cool UI - WILL NOT DO
Out of scope.

## Step 6. (EXTRA) Dockerize
Added Dockerfile and .dockerignore
