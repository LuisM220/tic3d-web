# game.py
class TicTacToe3D:
    def __init__(self):
        self.board = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.current_player = -1  # -1 for X, 1 for O
        self.finished = False
        self.winner = None
        self.last_move = None
        self.C = [
            [1, 0, 0], [0, 1, 0], [0, 0, 1],
            [1, 1, 0], [1, 0, 1], [0, 1, 1],
            [1, -1, 0], [1, 0, -1], [0, 1, -1],
            [1, 1, 1], [1, -1, 1], [1, 1, -1], [1, -1, -1]
        ]

    def make_move(self, x, y, z, player_symbol):
        if self.finished:
            return {"valid": False, "error": "Juego finalizado"}

        if (self.current_player == -1 and player_symbol != 'X') or (self.current_player == 1 and player_symbol != 'O'):
            return {"valid": False, "error": "Turno de jugador"}

        if self.board[z][y][x] != 0:
            return {"valid": False, "error": "Casilla ocupada"}

        val = -1 if player_symbol == 'X' else 1
        self.board[z][y][x] = val
        self.last_move = (x, y, z)

        winner, cells = self.check_winner()
        if winner is not None:
            self.finished = True
            self.winner = 'X' if winner == -1 else 'O'
            return {
                "valid": True,
                "board": self.board,
                "winner": self.winner,
                "winning_cells": cells
            }

        self.current_player = 1 if self.current_player == -1 else -1
        return {
            "valid": True,
            "board": self.board,
            "winner": None,
            "next_player": 'X' if self.current_player == -1 else 'O'
        }

    def check_winner(self):
        X, Y, Z = self.last_move
        for direction in self.C:
            win, cells = self._check_line(direction, X, Y, Z)
            if win:
                s = sum(self.board[z][y][x] for (x, y, z) in cells)
                if s == -3:
                    return -1, cells
                if s == 3:
                    return 1, cells
        return None, []

    def _check_line(self, direction, X, Y, Z):
        dx, dy, dz = direction
        cells = []
        for i in range(3):
            x = X + dx * (i - 1)
            y = Y + dy * (i - 1)
            z = Z + dz * (i - 1)
            if 0 <= x < 3 and 0 <= y < 3 and 0 <= z < 3:
                cells.append((x, y, z))
            else:
                return False, []
        if len(cells) != 3:
            return False, []
        return True, cells