from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    # return {"gameId": f"{game_id}", "board": f"{game.board}"}
    return jsonify(gameId = f"{game_id}", board = f"{game.board}")

@app.post("/api/score-word")
def score_word():
    """Accepts a word played by user for a specific game and determines if 
    it's a valid word"""

    word = request.json["word"].upper()
    game_id = request.json["gameId"]

    is_word_in_word_list = games[game_id].is_word_in_word_list(word)
    is_findable_on_board = games[game_id].check_word_on_board(word)

    if not is_word_in_word_list:
        return jsonify(result = "not-word")

    if not is_findable_on_board:
        return jsonify( result = "not-on-board")
    
    return jsonify( result = "ok")
