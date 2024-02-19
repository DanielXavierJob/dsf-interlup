from flask import Blueprint, request
from flask_pydantic import validate
from flask_restx import Resource, Namespace, fields

from app.decorators import token_required
from app.dtos.task_dto import RegisterNewTaskModel, UpdateTaskModel
from app.services import TaskService

authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}
api = Namespace("Tasks", description="Tasks related users", authorizations=authorizations)

bp = Blueprint("task", __name__)
task_service = TaskService()

# Base Response Model
BaseResponseModel = api.model("BaseResponseModel",
                              {
                                  "message": fields.String,
                              })

# Task Model
TaskModel = api.model("TaskModel",
                      {
                          "id": fields.Integer,
                          "title": fields.String,
                          "order": fields.Integer,
                          "description": fields.String(required=False),
                          "category_id": fields.Integer,
                          "user_id": fields.Integer
                      })


# Register Model
RegisterModel = api.model("TaskRegisterModel",
                          {
                              "title": fields.String,
                              "description": fields.String,
                              "order": fields.Integer,
                              "category_id": fields.Integer,
                          })


@api.route("")
class Tasks(Resource):
    """
        Decorator: @api.route("")

        Description:
        Specifies the route "" (root) for the Tasks resource within the API.

        Class: Tasks(Resource)

        Description:
        This class represents the Tasks resource in the API. It handles HTTP GET and POST requests related to tasks.

        Method: get(self, current_user)

        Description:
        Handles HTTP GET requests to the root endpoint. It requires a valid authentication token to access the tasks.
        Uses the token_required decorator to enforce authentication. Retrieves all tasks for the authenticated user.
        Returns appropriate responses based on the authentication outcome.

        Parameters:
        - current_user: The current authenticated user obtained from the token.

        Decorators:
        - @api.response(200, "Tasks has been searched", [TaskModel]): Indicates that if the authentication is successful
          the response will have HTTP status code 200 and will be accompanied by a list of TaskModel instances.
        - @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel): Indicates that if the
          authentication fails or no token is provided, the response will have HTTP status code 401 and will be
          accompanied by a BaseResponseModel instance.
        - @api.doc(security="Bearer Auth"): Specifies the security requirements for accessing this endpoint, indicating
          that a Bearer token is required.
        - @token_required: Enforces authentication for accessing the endpoint.

        Returns:
        A dictionary containing a message indicating the success of the task search along with the tasks' information.

        Method: post(self, current_user)

        Description:
        Handles HTTP POST requests to the root endpoint. It requires a valid authentication token to create a new task.
        Uses the token_required decorator to enforce authentication. Creates a new task with the provided details.
        Returns appropriate responses based on the task creation outcome.

        Parameters:
        - current_user: The current authenticated user obtained from the token.

        Decorators:
        - @api.response(200, "Task has been created", TaskModel): Indicates that if the task creation is successful, the
          response will have HTTP status code 201 and will be accompanied by a TaskModel instance.
        - @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel): Indicates that if the
          authentication fails or no token is provided, the response will have HTTP status code 401 and will be
          accompanied by a BaseResponseModel instance.
        - @api.expect(RegisterModel): Specifies the expected JSON schema for the request body, using the RegisterModel.
        - @api.doc(security="Bearer Auth"): Specifies the security requirements for accessing this endpoint, indicating
          that a Bearer token is required.
        - @validate(body=RegisterNewTaskModel): Validates the request body against the RegisterNewTaskModel schema.
        - @token_required: Enforces authentication for accessing the endpoint.

        Returns:
        A dictionary containing a message indicating the success of the task creation along with the newly created
        task's information.
    """

    @api.response(200, "Tasks has been searched", [TaskModel])
    @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)
    @api.doc(security="Bearer Auth")
    @token_required
    def get(self, current_user):
        """
            Decorator: @api.response(200, "Tasks has been searched", [TaskModel])

            Description:
            Specifies the response format for successful retrieval of tasks. The response has HTTP status code 200 and
            is accompanied by a list of TaskModel instances.

            Decorator: @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)

            Description:
            Specifies the response format for failed authentication. The response has HTTP status code 401 and is
            accompanied by a BaseResponseModel instance indicating the authentication failure.

            Decorator: @api.doc(security="Bearer Auth")

            Description:
            Specifies the security requirements for accessing this endpoint, indicating that a Bearer token is required
            for authentication.

            Decorator: @token_required

            Description:
            Enforces authentication for accessing the endpoint by requiring a valid authentication token.

            Method: get(self, current_user)

            Description:
            Handles HTTP GET requests to the root endpoint. It retrieves all tasks for the authenticated user. Returns
            appropriate responses based on the authentication outcome.

            Parameters:
            - current_user: The current authenticated user obtained from the token.

            Returns:
            A dictionary containing a message indicating the success of the task search along with the tasks'
            information.
        """

        tasks = task_service.get_all(None, current_user=current_user)
        return {"message": "Tasks has been searched", "result": [task.to_dict() for task in tasks]}, 200

    @api.response(200, "Task has been created", TaskModel)
    @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)
    @api.expect(RegisterModel)
    @api.doc(security="Bearer Auth")
    @validate(body=RegisterNewTaskModel)
    @token_required
    def post(self, current_user):
        """
            Decorator: @api.response(200, "Task has been created", TaskModel)

            Description:
            Specifies the response format for successful creation of a task. The response has HTTP status code 200 and
            is accompanied by a TaskModel instance representing the newly created task.

            Decorator: @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)

            Description:
            Specifies the response format for failed authentication. The response has HTTP status code 401 and is
            accompanied by a BaseResponseModel instance indicating the authentication failure.

            Decorator: @api.expect(RegisterModel)

            Description:
            Specifies the expected JSON schema for the request body when creating a new task, using the RegisterModel.

            Decorator: @api.doc(security="Bearer Auth")

            Description:
            Specifies the security requirements for accessing this endpoint, indicating that a Bearer token is required
            for authentication.

            Decorator: @validate(body=RegisterNewTaskModel)

            Description:
            Validates the request body against the RegisterNewTaskModel schema before processing the request.

            Decorator: @token_required

            Description:
            Enforces authentication for accessing the endpoint by requiring a valid authentication token.

            Method: post(self, current_user)

            Description:
            Handles HTTP POST requests to the root endpoint. It creates a new task with the provided details. Returns
            appropriate responses based on the task creation outcome.

            Parameters:
            - current_user: The current authenticated user obtained from the token.

            Returns:
            A dictionary containing a message indicating the success of the task creation along with the newly created
            task's information.
        """

        title = request.body_params.title
        description = request.body_params.description
        order = request.body_params.order
        category_id = request.body_params.category_id
        task = task_service.create(title, description, order, category_id, current_user)
        return {"message": "Task has been created", "result": task.to_dict()}, 201


# Task Update Model
TaskUpdateModel = api.model("TaskUpdateModel",
                            {
                                "title": fields.String(required=False),
                                "description": fields.String(required=False),
                                "order": fields.Integer(required=False),
                                "category_id": fields.Integer(required=False),
                            })


@api.route("/<int:id>")
class Task(Resource):
    """
        Decorator: @api.route("/<int:id>")

        Description:
        Specifies the route "/<int:id>" for the Task resource within the API. The "<int:id>" part represents the task ID
        in the URL.

        Class: Task(Resource)

        Description:
        This class represents the Task resource in the API. It handles HTTP GET, PUT, and DELETE requests related to
        individual tasks.

        Method: get(self, id, current_user)

        Description:
        Handles HTTP GET requests to the "/<int:id>" endpoint. It retrieves the task with the provided ID for the
        authenticated user. Returns appropriate responses based on the task retrieval outcome.

        Parameters:
        - id (int): The ID of the task to retrieve.
        - current_user: The current authenticated user obtained from the token.

        Returns:
        A dictionary containing a message indicating the success of the task search along with the task's information,
        or a message indicating that the task was not found or the user doesn't have permission to view it.

        Method: put(self, id, current_user)

        Description:
        Handles HTTP PUT requests to the "/<int:id>" endpoint. It updates the task with the provided ID using the
        details provided in the request body. Returns appropriate responses based on the task update outcome.

        Parameters:
        - id (int): The ID of the task to update.
        - current_user: The current authenticated user obtained from the token.

        Returns:
        A dictionary containing a message indicating the success of the task update along with the updated task's
        information, or a message indicating that the task was not found or the user doesn't have permission to update
        it.

        Method: delete(self, id, current_user)

        Description:
        Handles HTTP DELETE requests to the "/<int:id>" endpoint. It deletes the task with the provided ID for the
        authenticated user. Returns appropriate responses based on the task deletion outcome.

        Parameters:
        - id (int): The ID of the task to delete.
        - current_user: The current authenticated user obtained from the token.

        Returns:
        A dictionary containing a message indicating the success of the task deletion, or a message indicating that the
        task was not found or the user doesn't have permission to delete it.

        Decorators:
        - @api.response(200, "Task has been searched", TaskModel): Indicates the response format for successful task
          retrieval, accompanied by a TaskModel instance.
        - @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel): Indicates the response
          format for failed authentication.
        - @api.response(404, "Task not found or you don't have permission to view it", BaseResponseModel): Indicates the
          response format when the task is not found or the user doesn't have permission to view it.
        - @api.expect(TaskUpdateModel): Specifies the expected JSON schema for the request body when updating a task,
          using the TaskUpdateModel.
        - @api.doc(security="Bearer Auth"): Specifies the security requirements for accessing this endpoint, indicating
          that a Bearer token is required for authentication.
        - @validate(body=UpdateTaskModel): Validates the request body against the UpdateTaskModel schema when updating a
          task.
        - @token_required: Enforces authentication for accessing the endpoint by requiring a valid authentication token.
    """

    @api.response(200, "Task has been searched", TaskModel)
    @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)
    @api.response(404, "Task not found or you don't have permission to view it", BaseResponseModel)
    @api.doc(security="Bearer Auth")
    @token_required
    def get(self, id, current_user):
        """
            Decorator: @api.response(200, "Task has been searched", TaskModel)

            Description:
            Specifies the response format for successful retrieval of a task. The response has HTTP status code 200 and
            is accompanied by a TaskModel instance representing the retrieved task.

            Decorator: @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)

            Description:
            Specifies the response format for failed authentication. The response has HTTP status code 401 and is
            accompanied by a BaseResponseModel instance indicating the authentication failure.

            Decorator: @api.response(404, "Task not found or you don't have permission to view it", BaseResponseModel)

            Description:
            Specifies the response format when the task is not found or the user doesn't have permission to view it. The
            response has HTTP status code 404 and is accompanied by a BaseResponseModel instance.

            Decorator: @api.doc(security="Bearer Auth")

            Description:
            Specifies the security requirements for accessing this endpoint, indicating that a Bearer token is required
            for authentication.

            Decorator: @token_required

            Description:
            Enforces authentication for accessing the endpoint by requiring a valid authentication token.

            Method: get(self, id, current_user)

            Description:
            Handles HTTP GET requests to the "/<int:id>" endpoint. It retrieves the task with the provided ID for the
            authenticated user. Returns appropriate responses based on the task retrieval outcome.

            Parameters:
            - id (int): The ID of the task to retrieve.
            - current_user: The current authenticated user obtained from the token.

            Returns:
            A dictionary containing a message indicating the success of the task search along with the task's
            information, or a message indicating that the task was not found or the user doesn't have permission to view
            it.
        """

        task = task_service.get_by_id(id, current_user)
        if task:
            return {"message": "Task has been searched", "result": task.to_dict()}, 200
        else:
            return {"message": "Task not found or you don't have permission to view it"}, 404

    @api.response(200, "Task has been updated", TaskModel)
    @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)
    @api.response(404, "Task not found or you don't have permission to view it", BaseResponseModel)
    @api.expect(TaskUpdateModel)
    @api.doc(security="Bearer Auth")
    @validate(body=UpdateTaskModel)
    @token_required
    def put(self, id, current_user):
        """
            Decorator: @api.response(200, "Task has been updated", TaskModel)

            Description:
            Specifies the response format for successful update of a task. The response has HTTP status code 200 and is
            accompanied by a TaskModel instance representing the updated task.

            Decorator: @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)

            Description:
            Specifies the response format for failed authentication. The response has HTTP status code 401 and is
            accompanied by a BaseResponseModel instance indicating the authentication failure.

            Decorator: @api.response(404, "Task not found or you don't have permission to view it", BaseResponseModel)

            Description:
            Specifies the response format when the task is not found or the user doesn't have permission to view it. The
            response has HTTP status code 404 and is accompanied by a BaseResponseModel instance.

            Decorator: @api.expect(TaskUpdateModel)

            Description:
            Specifies the expected JSON schema for the request body when updating a task, using the TaskUpdateModel.

            Decorator: @api.doc(security="Bearer Auth")

            Description:
            Specifies the security requirements for accessing this endpoint, indicating that a Bearer token is required
            for authentication.

            Decorator: @validate(body=UpdateTaskModel)

            Description:
            Validates the request body against the UpdateTaskModel schema before processing the request.

            Decorator: @token_required

            Description:
            Enforces authentication for accessing the endpoint by requiring a valid authentication token.

            Method: put(self, id, current_user)

            Description:
            Handles HTTP PUT requests to the "/<int:id>" endpoint. It updates the task with the provided ID using the
            details provided in the request body. Returns appropriate responses based on the task update outcome.

            Parameters:
            - id (int): The ID of the task to update.
            - current_user: The current authenticated user obtained from the token.

            Returns:
            A dictionary containing a message indicating the success of the task update along with the updated task's
            information, or a message indicating that the task was not found or the user doesn't have permission to
            update it.
        """

        title = request.body_params.title
        description = request.body_params.description
        category_id = request.body_params.category_id
        order = request.body_params.order

        task = task_service.update(id, title, description, order, category_id, current_user)
        if task:
            return {"message": "Task has been updated", "result": task.to_dict()}, 200
        else:
            return {"message": "Task not found or you don't have permission to update it"}, 404

    @api.response(200, "Task has been deleted", BaseResponseModel)
    @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)
    @api.response(404, "Task not found or you don't have permission to delete it", BaseResponseModel)
    @api.doc(security="Bearer Auth")
    @token_required
    def delete(self, id, current_user):
        """
            Decorator: @api.response(200, "Task has been deleted", BaseResponseModel)

            Description:
            Specifies the response format for successful deletion of a task. The response has HTTP status code 200 and
            is accompanied by a BaseResponseModel instance indicating the success of the task deletion.

            Decorator: @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)

            Description:
            Specifies the response format for failed authentication. The response has HTTP status code 401 and is
            accompanied by a BaseResponseModel instance indicating the authentication failure.

            Decorator: @api.response(404, "Task not found or you don't have permission to delete it", BaseResponseModel)

            Description:
            Specifies the response format when the task is not found or the user doesn't have permission to delete it.
            The response has HTTP status code 404 and is accompanied by a BaseResponseModel instance.

            Decorator: @api.doc(security="Bearer Auth")

            Description:
            Specifies the security requirements for accessing this endpoint, indicating that a Bearer token is required
            for authentication.

            Decorator: @token_required

            Description:
            Enforces authentication for accessing the endpoint by requiring a valid authentication token.

            Method: delete(self, id, current_user)

            Description:
            Handles HTTP DELETE requests to the "/<int:id>" endpoint. It attempts to delete the task with the provided
            ID for the authenticated user. Returns appropriate responses based on the task deletion outcome.

            Parameters:
            - id (int): The ID of the task to delete.
            - current_user: The current authenticated user obtained from the token.

            Returns:
            A dictionary containing a message indicating the success of the task deletion, or a message indicating that
            the task was not found or the user doesn't have permission to delete it.
        """

        success = task_service.delete(id, current_user)
        if success:
            return {"message": "Task has been deleted"}, 200
        else:
            return {"message": "Task not found or you don't have permission to delete it"}, 404
