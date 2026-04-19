from typing import List

class Board:
    """Tic-Tac-Toe board represented as an integer matrix."""

    def __init__(self, matrix: List[List[int]] = None):
        """
        Initialize the board.

        Args:
            matrix: 3x3 integer matrix where 0=empty, 1=X, 2=O.
                   If None, creates an empty board.
        """
        if matrix is None:
            self._matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        else:
            self._matrix = [row[:] for row in matrix]

    @property
    def matrix(self) -> List[List[int]]:
        """Get a copy of the board matrix."""
        return [row[:] for row in self._matrix]

    def get_cell(self, row: int, col: int) -> int:
        """Get value at specific cell."""
        return self._matrix[row][col]

    def set_cell(self, row: int, col: int, value: int) -> None:
        """Set value at specific cell."""
        if value not in (0, 1, 2):
            raise ValueError("Value must be 0 (empty), 1 (X), or 2 (O)")
        self._matrix[row][col] = value

    def is_empty(self, row: int, col: int) -> bool:
        """Check if cell is empty."""
        return self._matrix[row][col] == 0

    def get_empty_cells(self) -> List[tuple]:
        """Return list of (row, col) tuples for empty cells."""
        empty = []
        for i in range(3):
            for j in range(3):
                if self._matrix[i][j] == 0:
                    empty.append((i, j))
        return empty

    def is_full(self) -> bool:
        """Check if board has no empty cells."""
        return len(self.get_empty_cells()) == 0

    def __eq__(self, other) -> bool:
        if not isinstance(other, Board):
            return False
        return self._matrix == other._matrix

    def __repr__(self) -> str:
        return f"Board({self._matrix})"