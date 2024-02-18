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
    app.config.from_object(Config)
    db.init_app(app)

    sync_blueprints(app)
    create_swagger(app)

    with app.app_context():
        db.create_all()

    return app
