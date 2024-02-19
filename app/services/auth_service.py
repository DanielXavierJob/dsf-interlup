from datetime import datetime, timedelta, timezone
import re
import jwt

from app import app
from app.models import User
from app.repositories.user_repository import UserRepository


class AuthService:
    """
        Class: AuthService

        Description:
        This class provides authentication-related services for the Todo-List API. It includes methods for user
        registration, user login, and retrieving all users.

        Methods:
        - __init__(self): Constructor method initializing the user repository.
        - register(self, username, password): Registers a new user with the provided username and password. It checks
          if the username is alphanumeric, verifies if the username already exists, creates a new user instance, sets
          the password, and persists the user in the database. It also initializes task categories and tasks for the
          newly registered user.
        - login(self, username, password): Authenticates a user with the provided username and password. It retrieves
          the user from the repository, checks if the password matches, generates a JWT token for authentication, and
          returns the token if authentication is successful.
        - get_all(self): Retrieves all users from the repository.

        Attributes:
        - user_repository: An instance of UserRepository for accessing user data.

        Note:
        - This class assumes the existence of other services such as TaskService and TaskCategoryService for
          initializing tasks and task categories.
    """
    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, username, password):
        """
            Method: register

            Description:
            Registers a new user with the provided username and password. It validates the username to ensure it is
            alphanumeric, checks if the username already exists in the system, creates a new user instance, sets the
            password, and persists the user in the database. Additionally, it initializes task categories and tasks for
            the newly registered user.

            Parameters:
            - username (str): The username of the new user.
            - password (str): The password of the new user.

            Returns:
            dict: A dictionary containing a message confirming the user creation and the username of the created user,
            along with an HTTP status code.
        """
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
        """
            Method: login

            Description:
            Authenticates a user with the provided username and password. It retrieves the user from the repository
            based on the username provided, checks if the password matches with the stored password hash, generates a
            JWT token with a specified expiration time, and returns the token if the authentication is successful. If
            the authentication fails due to an invalid username or password, an appropriate error message is returned.

            Parameters:
            - username (str): The username of the user trying to log in.
            - password (str): The password provided by the user for authentication.

            Returns:
            dict: A dictionary containing a message indicating the result of the login attempt along with an HTTP status
            code. If successful, the token generated for the user is also included in the result.
        """

        user = self.user_repository.get_by_name(username)
        if user and user.check_password(password):
            token = jwt.encode(
                {"id": user.id, "exp": datetime.now(timezone.utc) + timedelta(minutes=45)},
                app.config["SECRET_KEY"], "HS256")
            return {"message": "User has been logged", "result": token}, 200
        else:
            return {"message": "Invalid username or password"}, 401

    def get_all(self):
        """
            Method: get_all

            Description:
            Retrieves all users from the repository.

            Returns:
            tuple: A tuple containing a list of all users retrieved from the repository and an HTTP status code
            indicating the success of the operation.
        """

        return self.user_repository.get_all(), 200
