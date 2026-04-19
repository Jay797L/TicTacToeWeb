import uuid
from flask import Blueprint, request, jsonify, current_app
from typing import Dict, Optional
from src.domain.model.player import Player, Symbol
from src.domain.model.board import Board
from src.domain.model.game import Game
from src.web.model.game_models import WebBoard, WebGame, ErrorResponse, CreateGameRequest
from src.web.mapper.game_mapper import GameMapper

game_bp = Blueprint('game', __name__, url_prefix='/game')

@game_bp.route('', methods=['POST'])
def create_game():
    """
    Create a new game.

    Expects JSON body with:
    - player_x_name: Name of player X
    - player_o_name: Name of player O
    - player_x_is_bot: Whether player X is a bot (default: False)
    - player_o_is_bot: Whether player O is a bot (default: False)

    Returns:
        Created game data
    """
    try:
        # Get dependencies from app config
        service = current_app.config.get('GAME_SERVICE')
        repository = current_app.config.get('GAME_REPOSITORY')

        if not service:
            return jsonify(ErrorResponse(
                error="Service unavailable",
                message="Game service not configured"
            ).__dict__), 500

        # Parse request body
        data = request.get_json()
        if not data:
            return jsonify(ErrorResponse(
                error="Invalid request",
                message="Request body is required"
            ).__dict__), 400

        # Extract request fields
        player_x_name = data.get('player_x_name')
        player_o_name = data.get('player_o_name')
        player_x_is_bot = data.get('player_x_is_bot', False)
        player_o_is_bot = data.get('player_o_is_bot', False)

        # Validate required fields
        if not player_x_name:
            return jsonify(ErrorResponse(
                error="Invalid request",
                message="player_x_name is required"
            ).__dict__), 400

        if not player_o_name:
            return jsonify(ErrorResponse(
                error="Invalid request",
                message="player_o_name is required"
            ).__dict__), 400

        # Create players
        player_x = Player(name=player_x_name, symbol=Symbol.X, is_bot=player_x_is_bot)
        player_o = Player(name=player_o_name, symbol=Symbol.O, is_bot=player_o_is_bot)

        # Create game
        game = Game(player_x=player_x, player_o=player_o)

        # Save game to repository
        if repository:
            repository.save_game(game)

        # Convert to web model and return
        web_game = GameMapper.game_to_web(game)

        return jsonify(web_game.__dict__), 201

    except Exception as e:
        return jsonify(ErrorResponse(
            error="Internal server error",
            message=str(e)
        ).__dict__), 500

@game_bp.route('/<string:game_uuid>', methods=['POST'])
def make_move(game_uuid: str):
    """
    Process a move in the game.

    Expects JSON body with:
    - player_id: UUID of the player making the move
    - row: row index (0-2)
    - col: column index (0-2)
    - updated_board: the board after the user's move

    Returns:
        Updated game state after computer move
    """
    try:
        # Validate UUID format
        try:
            game_id = uuid.UUID(game_uuid)
        except ValueError:
            return jsonify(ErrorResponse(
                error="Invalid UUID",
                message=f"'{game_uuid}' is not a valid UUID"
            ).__dict__), 400

        # Get dependencies from app config
        service = current_app.config.get('GAME_SERVICE')
        repository = current_app.config.get('GAME_REPOSITORY')

        if not service:
            return jsonify(ErrorResponse(
                error="Service unavailable",
                message="Game service not configured"
            ).__dict__), 500

        # Get game from repository
        game = None
        if repository:
            game = repository.get_game(game_id)

        if not game:
            return jsonify(ErrorResponse(
                error="Game not found",
                message=f"Game with UUID {game_uuid} does not exist"
            ).__dict__), 404

        # Parse request body
        data = request.get_json()
        if not data:
            return jsonify(ErrorResponse(
                error="Invalid request",
                message="Request body is required"
            ).__dict__), 400

        # Extract request fields
        player_id_str = data.get('player_id')
        row = data.get('row')
        col = data.get('col')

        if not all([player_id_str, row is not None, col is not None]):
            return jsonify(ErrorResponse(
                error="Invalid request",
                message="Missing required fields: player_id, row, col, updated_board"
            ).__dict__), 400

        # Validate player ID
        try:
            player_id = uuid.UUID(player_id_str)
        except ValueError:
            return jsonify(ErrorResponse(
                error="Invalid player ID",
                message=f"'{player_id_str}' is not a valid UUID"
            ).__dict__), 400

        # Find the player in the game
        player = None
        if game.player_x.id == player_id:
            player = game.player_x
        elif game.player_o.id == player_id:
            player = game.player_o
        else:
            return jsonify(ErrorResponse(
                error="Player not found",
                message=f"Player with UUID {player_id_str} is not part of this game"
            ).__dict__), 400

        # Validate row and column
        if not (0 <= row < 3 and 0 <= col < 3):
            return jsonify(ErrorResponse(
                error="Invalid move",
                message=f"Position ({row}, {col}) is out of bounds"
            ).__dict__), 400

        # Check if game is already over
        is_game_over, winner = service.check_game_over(game.board)
        if is_game_over:
            winner_name = winner.name if winner else "Draw"
            return jsonify(ErrorResponse(
                error="Game already over",
                message=f"Game has already ended. Winner: {winner_name}"
            ).__dict__), 400

        # Save previous board state
        previous_board = Board(matrix=game.board.matrix)

        # Validate the move
        is_valid = service.validate_move(game, previous_board, player, row, col)

        if not is_valid:
            return jsonify(ErrorResponse(
                error="Invalid move",
                message="The move is not valid. Check that it's the player's turn and the cell is empty"
            ).__dict__), 400

        # Apply the move to the game
        game.make_move(row, col, player)

        # Check if game is over after user's move
        is_game_over, winner = service.check_game_over(game.board)

        if is_game_over:
            # Save game state
            if repository:
                repository.save_game(game)

            # Return final game state
            web_game = GameMapper.game_to_web(game, is_game_over=True,
                                              winner_symbol=winner.value if winner else None)
            return jsonify(web_game.__dict__), 200

        # Check if it's a bot's turn now
        current_player = game.get_current_player()

        if current_player.is_bot:
            # Get bot's move
            bot_row, bot_col = service.get_next_move(game, current_player)

            # Apply bot's move
            game.make_move(bot_row, bot_col, current_player)

            # Check if game is over after bot's move
            is_game_over, winner = service.check_game_over(game.board)

        # Save updated game state
        if repository:
            repository.save_game(game)

        # Convert to web model and return
        web_game = GameMapper.game_to_web(game, is_game_over=is_game_over,
                                          winner_symbol=winner.value if winner else None)

        return jsonify(web_game.__dict__), 200

    except Exception as e:
        return jsonify(ErrorResponse(
            error="Internal server error",
            message=str(e)
        ).__dict__), 500