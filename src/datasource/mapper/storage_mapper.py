from uuid import UUID
from typing import List
from src.domain.model.board import Board
from src.domain.model.game import Game
from src.domain.model.player import Player, Symbol
from src.datasource.model.game_storage_models import StorageBoard, StorageGame, StoragePlayer

class StorageMapper:
    """Mapper between domain and datasource models."""

    @staticmethod
    def board_to_storage(board: Board) -> StorageBoard:
        """Convert domain Board to StorageBoard."""
        return StorageBoard(matrix=board.matrix)

    @staticmethod
    def board_from_storage(storage_board: StorageBoard) -> Board:
        """Convert StorageBoard to domain Board."""
        return Board(matrix=storage_board.matrix)

    @staticmethod
    def player_to_storage(player: Player) -> StoragePlayer:
        """Convert domain Player to StoragePlayer."""
        return StoragePlayer(
            id=player.id,
            name=player.name,
            symbol=player.symbol_value,
            is_bot=player.is_bot
        )

    @staticmethod
    def player_from_storage(storage_player: StoragePlayer) -> Player:
        """Convert StoragePlayer to domain Player."""
        symbol = Symbol.X if storage_player.symbol == 1 else Symbol.O
        return Player(
            name=storage_player.name,
            symbol=symbol,
            is_bot=storage_player.is_bot,
            player_id=storage_player.id
        )

    @staticmethod
    def game_to_storage(game: Game) -> StorageGame:
        """Convert domain Game to StorageGame."""
        return StorageGame(
            id=game.id,
            board=StorageMapper.board_to_storage(game.board),
            player_x_id=game.player_x.id,
            player_o_id=game.player_o.id,
            players=[
                StorageMapper.player_to_storage(game.player_x),
                StorageMapper.player_to_storage(game.player_o)
            ],
            current_turn_symbol=game.current_turn.value
        )

    @staticmethod
    def game_from_storage(storage_game: StorageGame) -> Game:
        """Convert StorageGame to domain Game."""
        # Find players by ID
        player_x = None
        player_o = None

        for storage_player in storage_game.players:
            if storage_player.id == storage_game.player_x_id:
                player_x = StorageMapper.player_from_storage(storage_player)
            elif storage_player.id == storage_game.player_o_id:
                player_o = StorageMapper.player_from_storage(storage_player)

        if player_x is None or player_o is None:
            raise ValueError("Players not found in storage game")

        board = StorageMapper.board_from_storage(storage_game.board)
        game = Game(player_x=player_x, player_o=player_o, game_id=storage_game.id, board=board)

        # Set current turn based on stored value
        if storage_game.current_turn_symbol == 2:
            game.switch_turn()  # Switch to O if needed

        return game