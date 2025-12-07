from flask import Flask, render_template, request, redirect, url_for, session
from game import TicTacToe3D

app = Flask(__name__)
app.secret_key = "cambia_esta_clave_en_produccion"
juego = TicTacToe3D()

# Registro global de jugadores
assigned_roles = []

def assign_player():
    if "player" in session:
        return session["player"]

    # Asignar X si no está ocupado
    if "X" not in assigned_roles:
        session["player"] = "X"
        assigned_roles.append("X")
    # Asignar O si no está ocupado
    elif "O" not in assigned_roles:
        session["player"] = "O"
        assigned_roles.append("O")
    else:
        session["player"] = "Spectator"

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
    session.pop("player", None)
    assigned_roles.clear()  # 🔥 Reinicia roles globales
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)