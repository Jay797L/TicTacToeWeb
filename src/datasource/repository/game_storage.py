import threading
from typing import Dict, Optional
from uuid import UUID
from ..model.game_storage_models import StorageGame

class GameStorage:
    """Thread-safe storage class for current games."""

    def __init__(self):
        self._games: Dict[UUID, StorageGame] = {}
        self._lock = threading.RLock()

    def save(self, game: StorageGame) -> None:
        """Save a game to storage."""
        with self._lock:
            self._games[game.id] = game

    def get(self, game_id: UUID) -> Optional[StorageGame]:
        """Get a game from storage by ID."""
        with self._lock:
            return self._games.get(game_id)

    def delete(self, game_id: UUID) -> bool:
        """Delete a game from storage. Returns True if deleted, False if not found."""
        with self._lock:
            if game_id in self._games:
                del self._games[game_id]
                return True
            return False

    def exists(self, game_id: UUID) -> bool:
        """Check if a game exists in storage."""
        with self._lock:
            return game_id in self._games

    def get_all(self) -> Dict[UUID, StorageGame]:
        """Get a copy of all games."""
        with self._lock:
            return self._games.copy()

    def clear(self) -> None:
        """Clear all games from storage."""
        with self._lock:
            self._games.clear()