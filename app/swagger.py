from flask import Flask
from flask_restx import Api
from flask_swagger_ui import get_swaggerui_blueprint


def create_swagger(app: Flask):
    from .routes import auth, task, task_category
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
    api.add_namespace(task_category.api, path='/task-category')
    api.add_namespace(task.api, path='/task')
