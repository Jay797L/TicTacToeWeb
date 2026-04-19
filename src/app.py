#!/usr/bin/env python3
"""
Tic-Tac-Toe Web Application Entry Point.

This module initializes the dependency injection container,
creates the Flask application, and starts the web server.
"""

import sys
import os

# Add parent directory to path for proper imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.di.container import Container
from src.web.module.web_module import create_app


def main():
    """
    Main entry point for the Tic-Tac-Toe web application.

    Initializes dependencies, creates Flask app, and starts the server.
    """
    print("=" * 50)
    print("Tic-Tac-Toe Web Application")
    print("=" * 50)

    # Initialize dependency injection container
    print("Initializing dependency container...")
    container = Container()

    # Get dependencies from container
    storage = container.storage
    repository = container.repository
    service = container.service

    print(f"  - GameStorage: {'initialized' if storage else 'failed'}")
    print(f"  - GameRepository: {'initialized' if repository else 'failed'}")
    print(f"  - GameService: {'initialized' if service else 'failed'}")

    # Create Flask application with dependencies
    print("Creating Flask application...")
    app = create_app(service=service, repository=repository)

    # Configure Flask
    app.config['JSON_SORT_KEYS'] = False  # Preserve field order
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Pretty print JSON

    # Get host and port from environment variables or use defaults
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    print(f"\nStarting server...")
    print(f"  - Host: {host}")
    print(f"  - Port: {port}")
    print(f"  - Debug mode: {debug}")
    print("\nAvailable endpoints:")
    print("  POST /game                           - Create a new game")
    print("  POST /game/{game_uuid}               - Make a move in a game")
    print("\nExample game creation:")
    print('  curl -X POST http://localhost:5000/game \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"player_x_name": "Human", "player_o_name": "AI", "player_o_is_bot": true}\'')
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)

    # Run Flask application
    try:
        app.run(host=host, port=port, debug=debug, threaded=True)
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()