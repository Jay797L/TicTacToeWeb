from abc import ABC, abstractmethod
from typing import Optional, Tuple
from src.domain.model.game import Game
from src.domain.model.board import Board
from src.domain.model.player import Player, Symbol

class IGameService(ABC):
    """Interface for game service."""

    @abstractmethod
    def get_next_move(self, game: Game, player: Player) -> Tuple[int, int]:
        """
        Determine the next move using Minimax algorithm.

        Args:
            game: Current game state.
            player: Player for whom to calculate the next move (must be a bot).

        Returns:
            Tuple of (row, col) for the best move.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def check_game_over(self, board: Board) -> Tuple[bool, Optional[Symbol]]:
        """
        Check if the game has ended.

        Args:
            board: Current board state.

        Returns:
            Tuple of (is_game_over, winner).
            winner is Symbol.X, Symbol.O, or None for draw.
        """
        pass

    @abstractmethod
    def get_current_player_by_board(self, board: Board) -> Symbol:
        """
        Determine whose turn it is based on board state.

        Args:
            board: Current board state.

        Returns:
            Symbol.X or Symbol.O. X always goes first.
        """
        pass