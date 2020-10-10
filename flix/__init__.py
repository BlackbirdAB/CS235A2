"""Initialize Flask app."""

import os

from flask import Flask

import flix.adapters.repository as repo
from flix.adapters.memory_repository import MemoryRepository, load_data


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = os.path.join('datafiles')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    load_data(data_path, repo.repo_instance)

    # Build the application - these steps require an application context.
    with app.app_context():
        # Register blueprints.
        from flix.home import home
        app.register_blueprint(home.home_blueprint)

        from flix.movies import movies
        app.register_blueprint(movies.movies_blueprint)

        from flix.authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from flix.utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

        from flix.search import search
        app.register_blueprint(search.search_blueprint)

    return app
