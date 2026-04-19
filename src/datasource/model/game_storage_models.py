import uuid
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class StorageBoard:
    """Datasource model for game board."""
    matrix: List[List[int]] = field(default_factory=lambda: [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def __post_init__(self):
        """Ensure matrix is a copy to prevent reference issues."""
        if self.matrix:
            self.matrix = [row[:] for row in self.matrix]

    @classmethod
    def empty(cls) -> 'StorageBoard':
        """Create an empty board."""
        return cls(matrix=[[0, 0, 0], [0, 0, 0], [0, 0, 0]])

@dataclass
class StoragePlayer:
    """Datasource model for player."""
    id: uuid.UUID
    name: str
    symbol: int  # 1 for X, 2 for O
    is_bot: bool

@dataclass
class StorageGame:
    """Datasource model for current game."""
    id: uuid.UUID
    board: StorageBoard
    player_x_id: uuid.UUID
    player_o_id: uuid.UUID
    players: List[StoragePlayer] = field(default_factory=list)
    current_turn_symbol: int = 1  # 1 for X, 2 for O