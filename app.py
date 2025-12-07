from flask import Flask, render_template, request, redirect, url_for, session

from game import TicTacToe3D

app = Flask(__name__)
app.secret_key = "cambia_esta_clave_en_produccion"  # Necesario para sesiones
juego = TicTacToe3D()

# Variables globales para asignar roles fijos
assigned_roles = {"X": None, "O": None}

def assign_player():
    if "player" not in session:
        # Si no hay jugador X asignado, este navegador será X
        if assigned_roles["X"] is None:
            session["player"] = "X"
            assigned_roles["X"] = True
        # Si ya existe X, asigna O
        elif assigned_roles["O"] is None:
            session["player"] = "O"
            assigned_roles["O"] = True
        else:
            # Si ya hay dos jugadores, asigna espectador
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
    # 🔥 Reinicia roles para que se vuelvan a asignar en la próxima entrada
    assigned_roles["X"] = None
    assigned_roles["O"] = None
    session.pop("player", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)