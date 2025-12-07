# game.py
# game.py
class TicTacToe3D:
    def __init__(self):
        self.reset()
        # Direcciones para líneas de 3 celdas (todas las horizontales, verticales, profundidad y diagonales 3D)
        self.C = [
            [1,0,0],[0,1,0],[0,0,1],        # ejes principales: x, y, z
            [1,1,0],[1,-1,0],               # diagonales en plano XY
            [1,0,1],[1,0,-1],               # diagonales en plano XZ
            [0,1,1],[0,1,-1],               # diagonales en plano YZ
            [1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1]  # diagonales espaciales
        ]

    def reset(self):
        self.board = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.current_player = -1  # -1 = X, 1 = O
        self.finished = False
        self.winner = None
        self.last_move = None

    def make_move(self, x, y, z):
        # Bloquear jugadas si el juego terminó
        if self.finished:
            return {"valid": False, "error": "Juego finalizado", "board": self.board}

        # Validar coordenadas
        if not (0 <= x < 3 and 0 <= y < 3 and 0 <= z < 3):
            return {"valid": False, "error": "Coordenadas inválidas", "board": self.board}

        # Casilla ocupada
        if self.board[z][y][x] != 0:
            return {"valid": False, "error": "Casilla ocupada", "board": self.board}

        # Aplicar jugada del jugador actual
        val = self.current_player
        self.board[z][y][x] = val
        self.last_move = (x, y, z)

        # Verificar victoria
        winner, cells = self.check_winner()
        if winner is not None:
            self.finished = True
            self.winner = 'X' if winner == -1 else 'O'
            return {
                "valid": True,
                "winner": self.winner,
                "winning_cells": cells,
                "board": self.board
            }

        # Cambiar turno
        self.current_player = 1 if self.current_player == -1 else -1
        return {
            "valid": True,
            "winner": None,
            "next_player": 'X' if self.current_player == -1 else 'O',
            "board": self.board
        }

    def check_winner(self):
        # Debe existir una última jugada que sirva de centro de la línea
        if not self.last_move:
            return None, []
        X, Y, Z = self.last_move

        # Revisar todas las direcciones posibles
        for direction in self.C:
            win, cells = self._check_line(direction, X, Y, Z)
            if win:
                s = sum(self.board[z][y][x] for (x, y, z) in cells)
                if s == -3:  # X gana
                    return -1, cells
                if s == 3:   # O gana
                    return 1, cells
        return None, []

    def _check_line(self, direction, X, Y, Z):
        # Construye una línea de 3 celdas centrada en la última jugada,
        # avanzando -1, 0, +1 pasos en la dirección dada (dx,dy,dz)
        dx, dy, dz = direction
        cells = []
        for i in range(3):
            x = X + dx * (i - 1)
            y = Y + dy * (i - 1)
            z = Z + dz * (i - 1)
            if 0 <= x < 3 and 0 <= y < 3 and 0 <= z < 3:
                cells.append((x, y, z))
            else:
                return False, []  # Se sale del tablero: no es línea válida
        return True, cells