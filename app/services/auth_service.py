from datetime import datetime, timedelta, timezone
import re
import jwt

from app import app
from app.models import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, username, password):
        if not re.match("^[a-zA-Z0-9_]*$", username):
            return {"message": "username must be alphanumeric"}

        user_check = self.user_repository.get_by_name(username)
        if user_check:
            return {"message": "Username already exists"}, 409

        user = User(username=username)
        user.set_password(password)
        self.user_repository.create(user)

        from app.services import TaskService, TaskCategoryService
        task_category_service = TaskCategoryService()
        task_service = TaskService()
        tasks_categories = task_category_service.create_init_tasks_categories(current_user=user)
        task_service.create_init_tasks(tasks_categories=tasks_categories, current_user=user)
        return {"message": "User has been created", "result": {"username": user.username}}, 201

    def login(self, username, password):
        user = self.user_repository.get_by_name(username)
        if user and user.check_password(password):
            token = jwt.encode(
                {"id": user.id, "exp": datetime.now(timezone.utc) + timedelta(minutes=45)},
                app.config["SECRET_KEY"], "HS256")
            return {"message": "User has been logged", "result": token}, 200
        else:
            return {"message": "Invalid username or password"}, 401

    def get_all(self):
        return self.user_repository.get_all(), 200
