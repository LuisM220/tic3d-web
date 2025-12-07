from flask import Flask, render_template, request, redirect, url_for, session
from game import TicTacToe3D

app = Flask(__name__)
app.secret_key = "cambia_esta_clave_en_produccion"
juego = TicTacToe3D()

# Variables globales para roles
roles_ocupados = {"X": False, "O": False}

def assign_player():
    if "player" in session:
        return session["player"]

    # Asignar X si está libre
    if not roles_ocupados["X"]:
        session["player"] = "X"
        roles_ocupados["X"] = True
    # Asignar O si está libre
    elif not roles_ocupados["O"]:
        session["player"] = "O"
        roles_ocupados["O"] = True
    else:
        # 🔥 En lugar de espectador, volvemos a asignar X
        session["player"] = "X"

    return session["player"]

@app.route("/")
def index():
    player = assign_player()
    current_symbol = 'X' if juego.current_player == -1 else 'O'
    is_turn = (player == current_symbol) and not juego.finished
    return render_template(
        "board.html",
        board=juego.board,
        current=current_symbol,
        winner=juego.winner,
        winning_cells=juego.winning_cells,
        player=player,
        is_turn=is_turn
    )

@app.route("/move")
def move():
    if juego.finished:
        return redirect(url_for("index"))

    player = assign_player()
    current_symbol = 'X' if juego.current_player == -1 else 'O'
    if player != current_symbol:
        return redirect(url_for("index"))

    try:
        x = int(request.args.get("x"))
        y = int(request.args.get("y"))
        z = int(request.args.get("z"))
    except (TypeError, ValueError):
        return redirect(url_for("index"))

    juego.make_move(x, y, z, symbol_expected=player)
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    juego.reset()
    # Reinicia roles para que se reasignen en la próxima entrada
    roles_ocupados["X"] = False
    roles_ocupados["O"] = False
    session.pop("player", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)