import uuid
from typing import Optional
from src.domain.model.board import Board
from src.domain.model.game import Game
from src.domain.model.player import Player, Symbol
from src.web.model.game_models import WebBoard, WebGame, WebPlayer

class GameMapper:
    """Mapper between domain and web models."""

    @staticmethod
    def board_to_web(board: Board) -> WebBoard:
        """Convert domain Board to WebBoard."""
        return WebBoard(matrix=board.matrix)

    @staticmethod
    def board_from_web(web_board: WebBoard) -> Board:
        """Convert WebBoard to domain Board."""
        return Board(matrix=web_board.matrix)

    @staticmethod
    def player_to_web(player: Player) -> WebPlayer:
        """Convert domain Player to WebPlayer."""
        return WebPlayer(
            id=str(player.id),
            name=player.name,
            symbol=player.symbol_value,
            is_bot=player.is_bot
        )

    @staticmethod
    def player_from_web(web_player: WebPlayer) -> Player:
        """Convert WebPlayer to domain Player."""
        symbol = Symbol.X if web_player.symbol == 1 else Symbol.O
        return Player(
            name=web_player.name,
            symbol=symbol,
            is_bot=web_player.is_bot,
            player_id=uuid.UUID(web_player.id)
        )

    @staticmethod
    def game_to_web(game: Game, is_game_over: bool = False, winner_symbol: Optional[int] = None) -> WebGame:
        """Convert domain Game to WebGame."""
        return WebGame(
            id=str(game.id),
            board=GameMapper.board_to_web(game.board),
            player_x=GameMapper.player_to_web(game.player_x),
            player_o=GameMapper.player_to_web(game.player_o),
            current_turn_symbol=game.current_turn.value,
            is_game_over=is_game_over,
            winner_symbol=winner_symbol
        )

    @staticmethod
    def game_from_web(web_game: WebGame) -> Game:
        """Convert WebGame to domain Game."""
        player_x = GameMapper.player_from_web(web_game.player_x)
        player_o = GameMapper.player_from_web(web_game.player_o)
        board = GameMapper.board_from_web(web_game.board)

        game = Game(
            player_x=player_x,
            player_o=player_o,
            game_id=uuid.UUID(web_game.id),
            board=board
        )

        # Set current turn if needed
        if web_game.current_turn_symbol == 2:
            # If web says it's O's turn but default is X, switch
            if game.current_turn.value != web_game.current_turn_symbol:
                game.switch_turn()

        return game