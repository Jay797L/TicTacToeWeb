from typing import Optional
from uuid import UUID
from src.domain.model.game import Game
from src.datasource.model.game_storage_models import StorageGame
from src.datasource.mapper.storage_mapper import StorageMapper
from src.datasource.repository.game_storage import GameStorage

class GameRepository:
    """Repository for working with game storage."""

    def __init__(self, storage: GameStorage):
        self._storage = storage
        self._mapper = StorageMapper()

    def save_game(self, game: Game) -> None:
        """
        Save a current game to storage.

        Args:
            game: Domain game model to save.
        """
        storage_game = self._mapper.game_to_storage(game)
        self._storage.save(storage_game)

    def get_game(self, game_id: UUID) -> Optional[Game]:
        """
        Get a current game from storage by ID.

        Args:
            game_id: UUID of the game to retrieve.

        Returns:
            Domain game model if found, None otherwise.
        """
        storage_game = self._storage.get(game_id)
        if storage_game is None:
            return None
        return self._mapper.game_from_storage(storage_game)

    def delete_game(self, game_id: UUID) -> bool:
        """
        Delete a game from storage.

        Args:
            game_id: UUID of the game to delete.

        Returns:
            True if deleted, False if not found.
        """
        return self._storage.delete(game_id)

    def game_exists(self, game_id: UUID) -> bool:
        """
        Check if a game exists in storage.

        Args:
            game_id: UUID of the game to check.

        Returns:
            True if exists, False otherwise.
        """
        return self._storage.exists(game_id)