from typing import Tuple, Optional
from src.domain.model.game import Game
from src.domain.model.board import Board
from src.domain.model.player import Player, Symbol
from src.domain.service.game_service_interface import IGameService
from src.domain.service.minimax import Minimax

class GameServiceImpl(IGameService):
    """Concrete implementation of game service with repository support."""

    def __init__(self, repository=None):
        """
        Initialize game service.

        Args:
            repository: GameRepository instance for persistent storage (optional).
        """
        self._minimax = Minimax()
        self._repository = repository

    def get_next_move(self, game: Game, player: Player) -> Tuple[int, int]:
        """
        Determine the next move using Minimax algorithm.

        Args:
            game: Current game state.
            player: Player for whom to calculate the next move (must be a bot).

        Returns:
            Tuple of (row, col) for the best move.
        """
        if not player.is_bot:
            raise ValueError("get_next_move should only be called for bot players")

        return self._minimax.find_best_move(game.board, player.symbol)

    def validate_move(self, game: Game, previous_board: Board, player: Player, row: int, col: int) -> bool:
        """
        Validate that a move is legal and board state is consistent.

        Args:
            game: Current game state.
            previous_board: Previous board state before the move.
            player: Player making the move.
            row: Row of the move.
            col: Column of the move.

        Returns:
            True if move is valid, False otherwise.
        """
        current_board = game.board
        prev_matrix = previous_board.matrix
        curr_matrix = current_board.matrix

        # Check that it's the player's turn
        if game.get_current_player() != player:
            return False
        
        # Check that the move is within bounds
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        
        # Check that exactly one cell changed at the specified position
        for i in range(3):
            for j in range(3):
                if i == row and j == col:
                    # This cell should have changed from empty to player's symbol
                    if prev_matrix[i][j] != 0:
                        return False
                else:
                    # All other cells must remain unchanged
                    if prev_matrix[i][j] != curr_matrix[i][j]:
                        return False

        return True

    def check_game_over(self, board: Board) -> Tuple[bool, Optional[Symbol]]:
        """
        Check if the game has ended.

        Args:
            board: Current board state.

        Returns:
            Tuple of (is_game_over, winner).
            winner is Symbol.X, Symbol.O, or None for draw.
        """
        matrix = board.matrix

        # Check rows
        for i in range(3):
            if matrix[i][0] != 0 and matrix[i][0] == matrix[i][1] == matrix[i][2]:
                return True, Symbol(matrix[i][0])

        # Check columns
        for j in range(3):
            if matrix[0][j] != 0 and matrix[0][j] == matrix[1][j] == matrix[2][j]:
                return True, Symbol(matrix[0][j])

        # Check diagonals
        if matrix[0][0] != 0 and matrix[0][0] == matrix[1][1] == matrix[2][2]:
            return True, Symbol(matrix[0][0])
        if matrix[0][2] != 0 and matrix[0][2] == matrix[1][1] == matrix[2][0]:
            return True, Symbol(matrix[0][2])

        # Check for draw (board full with no winner)
        if board.is_full():
            return True, None

        return False, None

    def get_current_player_by_board(self, board: Board) -> Symbol:
        """
        Determine whose turn it is based on board state.

        Args:
            board: Current board state.

        Returns:
            Symbol.X or Symbol.O. X always goes first.
        """
        x_count = 0
        o_count = 0

        matrix = board.matrix
        for i in range(3):
            for j in range(3):
                if matrix[i][j] == Symbol.X.value:
                    x_count += 1
                elif matrix[i][j] == Symbol.O.value:
                    o_count += 1

        # X goes first, so if equal counts, it's X's turn
        if x_count == o_count:
            return Symbol.X
        else:
            return Symbol.O