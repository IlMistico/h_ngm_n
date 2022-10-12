# The hangman game server

This is an implementation of the hangman game in Python.

## Step 0: CLI game - COMPLETED
Write the game engine and a simple `main_cli.py` for a single player to play the game from command line.

## Step 1. REST single-player game - COMPLETED
Expose the game via REST endpoints to support single player games. 

Many player can play indipendently at the same time: each will be handled asynchronously.

Launch `main_webserver.py` to start the server. If necessary, set env variables `HOST` and `PORT` to use custom values.

## Step 2. Websockets - COMPLETED
Use websockets (persistent connection) to handle each game. 

## Step 3. Secure communications - TODO
Add cryptography to both REST and Websocket versions of the game, to encrypt/decrypt messages.
### Step 3.1 Add SSL certificates - TODO WITH CONDITION
Real implementation requires real certificates

### 3.2 Add OAuth2 - TODO

## Step 4. PvP game - TODO
The same as step 1, but allows two players to compete in the same game. 

## Step 5. Cool UI - WILL NOT DO
Out of scope.