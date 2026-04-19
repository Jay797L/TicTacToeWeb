import sys
import os
from typing import Optional

# Add parent directory to path if needed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datasource.repository.game_storage import GameStorage
from datasource.repository.game_repository import GameRepository
from domain.service.game_service_impl import GameServiceImpl
from domain.service.game_service_interface import IGameService

class Container:
    """
    Dependency injection container.
    Manages the dependency graph for the application.
    """

    def __init__(self):
        """Initialize the container with lazy-loaded dependencies."""
        self._storage: Optional[GameStorage] = None
        self._repository: Optional[GameRepository] = None
        self._service: Optional[IGameService] = None

    @property
    def storage(self) -> GameStorage:
        """
        Get GameStorage instance (singleton).

        Returns:
            GameStorage singleton instance
        """
        if self._storage is None:
            self._storage = GameStorage()
        return self._storage

    @property
    def repository(self) -> GameRepository:
        """
        Get GameRepository instance.
        Depends on storage.

        Returns:
            GameRepository instance
        """
        if self._repository is None:
            self._repository = GameRepository(self.storage)
        return self._repository

    @property
    def service(self) -> IGameService:
        """
        Get GameService instance.
        Depends on repository.

        Returns:
            GameService instance
        """
        if self._service is None:
            self._service = GameServiceImpl(repository=self.repository)
        return self._service

    def reset(self) -> None:
        """
        Reset all dependencies.
        Useful for testing or clearing state.
        """
        if self._storage is not None:
            self._storage.clear()

        self._storage = None
        self._repository = None
        self._service = None

    def get_all_dependencies(self) -> dict:
        """
        Get all initialized dependencies.

        Returns:
            Dictionary with dependency names and instances
        """
        deps = {}

        if self._storage is not None:
            deps['storage'] = self._storage

        if self._repository is not None:
            deps['repository'] = self._repository

        if self._service is not None:
            deps['service'] = self._service

        return deps