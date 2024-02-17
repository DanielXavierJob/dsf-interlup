from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

from config import Config

db = SQLAlchemy()
app = Flask(__name__)


def create_app():
    app.config.from_object(Config)
    db.init_app(app)

    from .routes import auth, task
    app.register_blueprint(auth.bp)
    app.register_blueprint(task.bp)

    swagger_url = '/api/docs'
    api_url = '/api/swagger.json'
    swagger_ui_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={
            'app_name': "API Flask Todo-List"
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=swagger_url)
    api = Api(app, title='API Flask Todo-List', version='1.0', description='The Documentation of API Flask Todo-List')

    api.add_namespace(auth.api, path='/auth')
    api.add_namespace(task.api, path='/task')
    with app.app_context():
        db.create_all()

    return app
