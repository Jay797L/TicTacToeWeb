from typing import List, Tuple, Optional
from src.domain.model.board import Board
from src.domain.model.player import Symbol

class Minimax:
    """Minimax algorithm implementation for Tic-Tac-Toe."""

    def __init__(self):
        self._computer_symbol = None
        self._human_symbol = None

    def find_best_move(self, board: Board, computer_symbol: Symbol) -> Tuple[int, int]:
        """
        Find the best move for the computer using Minimax.

        Args:
            board: Current board state.
            computer_symbol: Symbol for computer (Symbol.X or Symbol.O).

        Returns:
            Tuple of (row, col) for the best move.
        """
        self._computer_symbol = computer_symbol.value
        # Human is the opposite symbol
        if computer_symbol == Symbol.X:
            self._human_symbol = Symbol.O.value
        else:
            self._human_symbol = Symbol.X.value

        best_score = float('-inf')
        best_move = None

        for row, col in board.get_empty_cells():
            # Try the move
            board.set_cell(row, col, computer_symbol.value)

            # Evaluate the move
            score = self._minimax(board, 0, False)

            # Undo the move
            board.set_cell(row, col, 0)

            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move if best_move is not None else (0, 0)

    def _minimax(self, board: Board, depth: int, is_maximizing: bool) -> int:
        """
        Minimax recursive algorithm.

        Args:
            board: Current board state.
            depth: Current depth in the game tree.
            is_maximizing: True if maximizing player (computer), False if minimizing (human).

        Returns:
            Score for the position.
        """
        winner = self._check_winner(board)

        # Terminal states
        if winner == self._computer_symbol:
            return 10 - depth
        elif winner == self._human_symbol:
            return depth - 10
        elif board.is_full():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for row, col in board.get_empty_cells():
                board.set_cell(row, col, self._computer_symbol)
                score = self._minimax(board, depth + 1, False)
                board.set_cell(row, col, 0)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row, col in board.get_empty_cells():
                board.set_cell(row, col, self._human_symbol)
                score = self._minimax(board, depth + 1, True)
                board.set_cell(row, col, 0)
                best_score = min(score, best_score)
            return best_score

    def _check_winner(self, board: Board) -> Optional[int]:
        """Check if there's a winner on the board."""
        matrix = board.matrix

        # Check rows
        for i in range(3):
            if matrix[i][0] != 0 and matrix[i][0] == matrix[i][1] == matrix[i][2]:
                return matrix[i][0]

        # Check columns
        for j in range(3):
            if matrix[0][j] != 0 and matrix[0][j] == matrix[1][j] == matrix[2][j]:
                return matrix[0][j]

        # Check diagonals
        if matrix[0][0] != 0 and matrix[0][0] == matrix[1][1] == matrix[2][2]:
            return matrix[0][0]
        if matrix[0][2] != 0 and matrix[0][2] == matrix[1][1] == matrix[2][0]:
            return matrix[0][2]

        return None