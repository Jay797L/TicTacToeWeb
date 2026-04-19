import uuid
from typing import Optional
from enum import IntEnum

class Symbol(IntEnum):
    """Player symbols for Tic-Tac-Toe."""
    EMPTY = 0
    X = 1
    O = 2

class Player:
    """Player model for Tic-Tac-Toe game."""

    def __init__(self, name: str, symbol: Symbol, is_bot: bool = False, player_id: uuid.UUID = None):
        """
        Initialize a player.

        Args:
            name: Player's display name.
            symbol: Player's symbol (X or O).
            is_bot: True if AI-controlled, False for human player.
            player_id: UUID for the player. If None, generates a new UUID.
        """
        self._id = player_id if player_id is not None else uuid.uuid4()
        self._name = name
        self._symbol = symbol
        self._is_bot = is_bot

    @property
    def id(self) -> uuid.UUID:
        """Get player UUID."""
        return self._id

    @property
    def name(self) -> str:
        """Get player name."""
        return self._name

    @property
    def symbol(self) -> Symbol:
        """Get player symbol."""
        return self._symbol

    @property
    def is_bot(self) -> bool:
        """Check if player is AI-controlled."""
        return self._is_bot

    @property
    def symbol_value(self) -> int:
        """Get symbol as integer (1 for X, 2 for O)."""
        return self._symbol.value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        return self._id == other._id

    def __repr__(self) -> str:
        return f"Player(id={self._id}, name='{self._name}', symbol={self._symbol.name}, is_bot={self._is_bot})"