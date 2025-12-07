# app.py
from flask import Flask, render_template, request, redirect, url_for
from game import TicTacToe3D

app = Flask(__name__)
juego = TicTacToe3D()

@app.route("/")
def index():
    return render_template("board.html",
                           board=juego.board,
                           current="X" if juego.current_player == -1 else "O",
                           winner=juego.winner)

@app.route("/move")
def move():
    if juego.finished:
        return redirect(url_for("index"))

    x = int(request.args.get("x"))
    y = int(request.args.get("y"))
    z = int(request.args.get("z"))
    player = "X" if juego.current_player == -1 else "O"
    juego.make_move(x, y, z)
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    juego.reset()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)