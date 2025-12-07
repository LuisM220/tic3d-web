# game.py
# game.py
class TicTacToe3D:
    def __init__(self):
        self.reset()
        # Direcciones base: ejes y diagonales de planos y espaciales
        self.directions = [
            (1, 0, 0), (0, 1, 0), (0, 0, 1),             # ejes X, Y, Z
            (1, 1, 0), (1, -1, 0),                        # diagonales XY
            (1, 0, 1), (1, 0, -1),                        # diagonales XZ
            (0, 1, 1), (0, 1, -1),                        # diagonales YZ
            (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1) # diagonales espaciales
        ]

    def reset(self):
        self.board = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.current_player = -1  # -1 = X, 1 = O
        self.finished = False
        self.winner = None
        self.winning_cells = []
        self.last_move = None

    def make_move(self, x, y, z, symbol_expected=None):
        # Bloquear jugadas si el juego terminó
        if self.finished:
            return {"valid": False, "error": "Juego finalizado", "board": self.board}

        # Validar coordenadas
        if not (0 <= x < 3 and 0 <= y < 3 and 0 <= z < 3):
            return {"valid": False, "error": "Coordenadas inválidas", "board": self.board}

        # Casilla ocupada
        if self.board[z][y][x] != 0:
            return {"valid": False, "error": "Casilla ocupada", "board": self.board}

        # Validar turno esperado (si el servidor indica símbolo de sesión)
        symbol_current = 'X' if self.current_player == -1 else 'O'
        if symbol_expected and symbol_expected != symbol_current:
            return {"valid": False, "error": f"No es tu turno ({symbol_current})", "board": self.board}

        # Aplicar jugada
        val = self.current_player
        self.board[z][y][x] = val
        self.last_move = (x, y, z)

        # Verificar victoria completa (todas las líneas posibles)
        winner, cells = self._find_winner_all_lines()
        if winner is not None:
            self.finished = True
            self.winner = 'X' if winner == -1 else 'O'
            self.winning_cells = cells
            return {
                "valid": True,
                "winner": self.winner,
                "winning_cells": cells,
                "board": self.board,
                "message": f"Jugada en ({x},{y},{z}). {self.winner} ha ganado."
            }

        # Cambiar turno
        self.current_player = 1 if self.current_player == -1 else -1
        next_symbol = 'X' if self.current_player == -1 else 'O'
        return {
            "valid": True,
            "winner": None,
            "next_player": next_symbol,
            "board": self.board,
            "message": f"Jugada en ({x},{y},{z}). Turno de {next_symbol}."
        }

    def _find_winner_all_lines(self):
        # Recorre todas las líneas posibles de longitud 3 partiendo de posiciones válidas
        # Para cada dirección (dx,dy,dz), el inicio (x,y,z) debe permitir x+2*dx, y+2*dy, z+2*dz dentro del tablero.
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    for dx, dy, dz in self.directions:
                        x2 = x + 2 * dx
                        y2 = y + 2 * dy
                        z2 = z + 2 * dz
                        if not (0 <= x2 < 3 and 0 <= y2 < 3 and 0 <= z2 < 3):
                            continue
                        cells = [
                            (x, y, z),
                            (x + dx, y + dy, z + dz),
                            (x + 2 * dx, y + 2 * dy, z + 2 * dz),
                        ]
                        s = sum(self.board[cz][cy][cx] for (cx, cy, cz) in cells)
                        if s == -3:
                            return -1, cells
                        if s == 3:
                            return 1, cells
        return None, []

    def get_symbol(self, val):
        return 'X' if val == -1 else ('O' if val == 1 else '')