# app.py
import os
from flask import Flask
from flask_socketio import SocketIO, emit
from game import TicTacToe3D

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
sio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

game = TicTacToe3D()

@app.route("/")
def index():
    return "Servidor TicTacToe 3D en Render"

@sio.on("connect")
def on_connect():
    emit("update", {"board": game.board, "winner": game.winner, "next_player": 'X'})

@sio.on("move")
def on_move(data):
    x, y, z, player = data["x"], data["y"], data["z"], data["player"]
    res = game.make_move(x, y, z, player)
    if not res["valid"]:
        emit("error", {"msg": res["error"]})
    else:
        sio.emit("update", res, broadcast=True)

@sio.on("reset")
def on_reset():
    game.reset()
    sio.emit("update", {"board": game.board, "winner": None, "next_player": 'X'}, broadcast=True)
    if __name__ == "__main__":
        sio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
