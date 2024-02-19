from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.blueprints import sync_blueprints
from app.swagger import create_swagger
from config import Config

db = SQLAlchemy()
app = Flask(__name__)
CORS(app)


def create_app():
    """
        Function: create_app

        Description:
        This function serves as a factory for creating instances of the Flask application for the
        Todo-List API. It configures the application with the provided configuration object, initializes the database,
        synchronizes the blueprints of various routes, sets up Swagger documentation, creates all necessary database
        tables within the application context, and finally returns the configured Flask application instance.

        Returns:
        Flask: The configured Flask application instance.
    """
    app.config.from_object(Config)
    db.init_app(app)

    sync_blueprints(app)
    create_swagger(app)

    with app.app_context():
        db.create_all()

    return app
