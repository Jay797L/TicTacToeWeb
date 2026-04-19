import uuid
from typing import List, Optional
from .board import Board
from .player import Player, Symbol

class Game:
    """Current game model with UUID, board, and players."""

    def __init__(self, player_x: Player, player_o: Player, game_id: uuid.UUID = None, board: Board = None):
        """
        Initialize a game.

        Args:
            player_x: Player using X symbol.
            player_o: Player using O symbol.
            game_id: UUID for the game. If None, generates a new UUID.
            board: Board instance. If None, creates an empty board.
        """
        self._id = game_id if game_id is not None else uuid.uuid4()
        self._board = board if board is not None else Board()
        self._player_x = player_x
        self._player_o = player_o
        self._current_turn = Symbol.X  # X always goes first

    @property
    def id(self) -> uuid.UUID:
        """Get game UUID."""
        return self._id

    @property
    def board(self) -> Board:
        """Get game board."""
        return self._board

    @property
    def player_x(self) -> Player:
        """Get player with X symbol."""
        return self._player_x

    @property
    def player_o(self) -> Player:
        """Get player with O symbol."""
        return self._player_o

    @property
    def current_turn(self) -> Symbol:
        """Get whose turn it is."""
        return self._current_turn

    def get_player_by_symbol(self, symbol: Symbol) -> Player:
        """Get player by their symbol."""
        if symbol == Symbol.X:
            return self._player_x
        elif symbol == Symbol.O:
            return self._player_o
        raise ValueError(f"Invalid symbol: {symbol}")

    def get_current_player(self) -> Player:
        """Get player whose turn it is."""
        return self.get_player_by_symbol(self._current_turn)

    def switch_turn(self) -> None:
        """Switch to the other player's turn."""
        if self._current_turn == Symbol.X:
            self._current_turn = Symbol.O
        else:
            self._current_turn = Symbol.X

    def update_board(self, new_board: Board) -> None:
        """Update the game board."""
        self._board = new_board

    def make_move(self, row: int, col: int, player: Player) -> bool:
        """
        Make a move on the board.

        Args:
            row: Row index (0-2).
            col: Column index (0-2).
            player: Player making the move.

        Returns:
            True if move was valid and made, False otherwise.
        """
        if player != self.get_current_player():
            return False

        if not self._board.is_empty(row, col):
            return False

        self._board.set_cell(row, col, player.symbol_value)
        self.switch_turn()
        return True

    def __eq__(self, other) -> bool:
        if not isinstance(other, Game):
            return False
        return self._id == other._id

    def __repr__(self) -> str:
        return f"Game(id={self._id}, player_x={self._player_x.name}, player_o={self._player_o.name}, board={self._board})"