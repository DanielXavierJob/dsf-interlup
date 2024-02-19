from flask import Flask


def sync_blueprints(app: Flask):
    """
        Function: sync_blueprints

        Description:
        This function is responsible for synchronizing the blueprints of various routes with the Flask application. It registers the blueprints for authentication, task categories, and tasks with the provided Flask application instance.

        Parameters:
        - app (Flask): The Flask application instance to which the blueprints will be registered.

        Returns:
        None
    """

    from .routes import auth, task, task_category
    app.register_blueprint(auth.bp)
    app.register_blueprint(task_category.bp)
    app.register_blueprint(task.bp)
