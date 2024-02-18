from flask import Flask


def sync_blueprints(app: Flask):
    from .routes import auth, task, task_category
    app.register_blueprint(auth.bp)
    app.register_blueprint(task_category.bp)
    app.register_blueprint(task.bp)
