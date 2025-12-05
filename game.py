# game.py

class TicTacToe3D:
    def __init__(self):
        self.board = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
        self.current_player = -1  # -1 = X, 1 = O
        self.finished = False
        self.winner = None
        self.last_move = (0, 0, 0)
        # Reglas de líneas (basadas en tu programa original)
        self.C = [
            [1, 1, 0], [1, 0, 1], [0, 1, 1],
            [1, 0, 0], [1, -1, 0], [0, 0, 1],
            [-1, 0, 1], [0, 1, 0], [0, 1, -1],
            [0, -1, -1], [0, -1, 0], [0, 0, -1],
            [0, 0, 0]
        ]

    def reset(self):
        self.board = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
        self.current_player = -1
        self.finished = False
        self.winner = None

    def make_move(self, x, y, z, player_symbol):
        if self.finished:
            return {"valid": False, "error": "Juego finalizado"}

        expected_symbol = 'X' if self.current_player == -1 else 'O'
        if player_symbol != expected_symbol:
            return {"valid": False, "error": f"Turno de {expected_symbol}"}

        if self.board[z][y][x] != 0:
            return {"valid": False, "error": "Casilla ocupada"}

        val = -1 if player_symbol == 'X' else 1
        self.board[z][y][x] = val
        self.last_move = (x, y, z)

        winner, cells = self.check_winner()
        if winner is not None:
            self.finished = True
            self.winner = 'X' if winner == -1 else 'O'
            return {"valid": True, "board": self.board, "winner": self.winner, "winning_cells": cells}

        # Cambiar turno
        self.current_player = 1 if self.current_player == -1 else -1
        return {"valid": True, "board": self.board, "winner": None, "next_player": 'X' if self.current_player == -1 else 'O'}

    def check_winner(self):
        X, Y, Z = self.last_move
        for c in range(13):
            win, cells = self._check_line(c, X, Y, Z)
            if win:
                s = sum(self.board[z][y][x] for (x, y, z) in cells)
                if s == -4:
                    return -1, cells
                if s == 4:
                    return 1, cells
        return None, []

    def _check_line(self, c, X, Y, Z):
        tz, ty, tx = self.C[c]
        z1 = Z if tz > 0 else -1
        y1 = Y if ty > 0 else -1
        x1 = X if tx > 0 else -1
        cells = []
        s = 0
        for i in range(4):
            z = Z if z1 >= 0 else (3 - i if tz < 0 else i)
            y = Y if y1 >= 0 else (3 - i if ty < 0 else i)
            x = X if x1 >= 0 else (3 - i if tx < 0 else i)
            s += self.board[z][y][x]
            cells.append((x, y, z))
        if s == -4 or s == 4:
            return True, cells
        return False, []