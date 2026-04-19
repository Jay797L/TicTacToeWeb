import uuid
from typing import List, Optional
from dataclasses import dataclass, field
from enum import IntEnum

class WebSymbol(IntEnum):
    """Symbol representation for web layer."""
    EMPTY = 0
    X = 1
    O = 2

@dataclass
class WebBoard:
    """Web model for game board."""
    matrix: List[List[int]] = field(default_factory=lambda: [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def __post_init__(self):
        if self.matrix:
            self.matrix = [row[:] for row in self.matrix]

@dataclass
class WebPlayer:
    """Web model for player."""
    id: str  # UUID as string
    name: str
    symbol: int  # 1 for X, 2 for O
    is_bot: bool

@dataclass
class WebGame:
    """Web model for current game."""
    id: str  # UUID as string
    board: WebBoard
    player_x: WebPlayer
    player_o: WebPlayer
    current_turn_symbol: int  # 1 for X, 2 for O
    is_game_over: bool = False
    winner_symbol: Optional[int] = None

@dataclass
class MakeMoveRequest:
    """Request model for making a move."""
    game_id: str
    player_id: str
    row: int
    col: int
    updated_board: WebBoard

@dataclass
class CreateGameRequest:
    """Request model for creating a new game."""
    player_x_name: str
    player_o_name: str
    player_x_is_bot: bool = False
    player_o_is_bot: bool = False

@dataclass
class ErrorResponse:
    """Error response model."""
    error: str
    message: str