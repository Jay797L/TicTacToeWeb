from flask import Flask
from src.web.route.game_routes import game_bp

def create_app(service, repository=None):
    """
    Create and configure Flask application.

    Args:
        service: Game service instance
        repository: Game repository instance (optional)

    Returns:
        Configured Flask app
    """
    app = Flask(__name__)

    # Store dependencies in app config for access in routes
    app.config['GAME_SERVICE'] = service
    app.config['GAME_REPOSITORY'] = repository

    # Register blueprints
    app.register_blueprint(game_bp)

    return app