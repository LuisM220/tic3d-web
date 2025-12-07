# app.py
from flask import Flask, render_template, request, redirect, url_for
from game import TicTacToe3D

app = Flask(__name__)
juego = TicTacToe3D()

@app.route("/")
def index():
    return render_template(
        "board.html",
        board=juego.board,
        current="X" if juego.current_player == -1 else "O",
        winner=juego.winner
    )

@app.route("/move")
def move():
    # Bloquear jugadas si ya hay ganador
    if juego.finished:
        return redirect(url_for("index"))

    # Leer coordenadas
    x = int(request.args.get("x"))
    y = int(request.args.get("y"))
    z = int(request.args.get("z"))

    # El servidor decide el símbolo según turno; no se permite elegir X/O
    juego.make_move(x, y, z)

    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    juego.reset()
    return redirect(url_for("index"))

if __name__ == "__main__":
    # En Render, este puerto puede variar. Si necesitas otro, cámbialo aquí.
    app.run(host="0.0.0.0", port=10000)