from flask import Blueprint, request
from flask_pydantic import validate
from flask_restx import Resource, Namespace, fields, reqparse

from app.decorators import token_required
from app.dtos.task_category_dto import RegisterNewTaskCategoryModel, UpdateTaskCategoryModel
from app.routes.task import TaskModel
from app.services.task_category_service import TaskCategoryService

authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}
api = Namespace("Tasks Categories", description="Tasks categories", authorizations=authorizations)

bp = Blueprint("task_category", __name__)
task_category_service = TaskCategoryService()

# Base Response Model
BaseResponseModel = api.model("BaseResponseModel",
                              {
                                  "message": fields.String,
                              })

# Task Model
TaskCategoryModel = api.model("TaskCategoryModel",
                              {
                                  "id": fields.String,
                                  "title": fields.String,
                                  "order": fields.Integer,
                                  "user_id": fields.Integer,
                                  "tasks": fields.Nested(TaskModel, as_list=True),
                              })


# Register Model
TaskCategoryRegisterModel = api.model("TaskCategoryRegisterModel",
                                      {
                                          "title": fields.String,
                                          "order": fields.Integer
                                      })


@api.route("")
class TasksCategory(Resource):
    """
        Endpoint: /tasks-category

        Description:
        Handles operations related to task categories.

        Method: get(self, current_user)

        Description:
        Handles HTTP GET requests to retrieve all task categories related to the current user. Returns appropriate
        responses based on the query parameters.

        Parameters:
        - current_user: User object representing the current authenticated user.

        Responses:
        - 200: All tasks categories related to this user.
          Body: List[TaskCategoryModel]
        - 401: Invalid or missing Authentication token.
          Body: BaseResponseModel

        Security:
        Requires a Bearer Authentication token.

        Authorization:
        Requires a valid access token obtained through authentication.

        Request Parameters:
        - exclude_tasks (string, optional): If set to "true", tasks within the categories will be excluded from the
          result.

        Method: post(self, current_user)

        Description:
        Handles HTTP POST requests to create a new task category. Returns appropriate responses based on the creation
        outcome.

        Parameters:
        - current_user: User object representing the current authenticated user.

        Request Body:
        Expects a JSON object with the following properties:
        - title (string): Title of the task category.
        - order (integer): Order of the task category.

        Responses:
        - 200: Task Category has been successfully created.
          Body: TaskCategoryModel
        - 401: Invalid or missing Authentication token.
          Body: BaseResponseModel

        Security:
        Requires a Bearer Authentication token.

        Validation:
        The request body is validated using the RegisterNewTaskCategoryModel schema.

        Authorization:
        Requires a valid access token obtained through authentication.

        Returns:
        A JSON object containing the following keys:
        - message (string): Confirmation message.
        - result (object): Details of the created task category.
          - exclude_tasks (boolean, optional): If the exclude_tasks query parameter is set to "true",
          tasks within the category will be excluded from the result.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("exclude_tasks", type=str, default="false", help="Return tasks in tasks categories")

    @api.response(200, "All tasks categories related to this user", [TaskCategoryModel])
    @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)
    @api.doc(security="Bearer Auth")
    @token_required
    def get(self, current_user):
        """
            Handles HTTP GET requests to retrieve all task categories related to the current user.
            Returns appropriate responses based on the query parameters.

            Parameters:
            - current_user: User object representing the current authenticated user.

            Responses:
            - 200: All tasks categories related to this user.
              Body: List[TaskCategoryModel]
            - 401: Invalid or missing Authentication token.
              Body: BaseResponseModel

            Security:
            Requires a Bearer Authentication token.

            Authorization:
            Requires a valid access token obtained through authentication.

            Returns:
            A JSON object containing a message indicating the success of the search operation,
            along with the list of task categories.
        """
        args = self.parser.parse_args()
        exclude_tasks = True if args["exclude_tasks"] == "true" else False
        tasks_categories = task_category_service.get_all(exclude_tasks, current_user)
        return {"message": "Tasks Categories has been searched", "result": [categories.to_dict(exclude_tasks=
                                                                                               exclude_tasks) for
                                                                            categories in
                                                                            tasks_categories]}, 200

    @api.response(200, "Task Category has been created", TaskCategoryModel)
    @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)
    @api.expect(TaskCategoryRegisterModel)
    @api.doc(security="Bearer Auth")
    @validate(body=RegisterNewTaskCategoryModel)
    @token_required
    def post(self, current_user):
        """
            Handles HTTP POST requests to create a new task category.
            Returns appropriate responses based on the creation outcome.

            Parameters:
            - current_user: User object representing the current authenticated user.

            Request Body:
            Expects a JSON object with the following properties:
            - title (string): Title of the task category.
            - order (integer): Order of the task category.

            Responses:
            - 200: Task Category has been successfully created.
              Body: TaskCategoryModel
            - 401: Invalid or missing Authentication token.
              Body: BaseResponseModel

            Security:
            Requires a Bearer Authentication token.

            Validation:
            The request body is validated using the RegisterNewTaskCategoryModel schema.

            Authorization:
            Requires a valid access token obtained through authentication.

            Returns:
            A JSON object containing the following keys:
            - message (string): Confirmation message.
            - result (object): Details of the created task category.
              - exclude_tasks (boolean, optional): If the exclude_tasks query parameter is set to "true",
              tasks within the category will be excluded from the result.
        """
        title = request.body_params.title
        order = request.body_params.order
        task_category = task_category_service.create(title, order, current_user)
        args = self.parser.parse_args()
        exclude_tasks = True if args["exclude_tasks"] == "true" else False
        return {"message": "Task Category has been created",
                "result": task_category.to_dict(exclude_tasks=exclude_tasks)}, 201


# Task Update Model
TaskCategoryUpdateModel = api.model("TaskCategoryUpdateModel",
                                    {
                                        "title": fields.String(required=False),
                                        "order": fields.Integer(required=False)
                                    })


@api.route("/<string:id>")
class TaskCategory(Resource):
    """
        Endpoint: /tasks-category/<string:id>

        Description:
        Handles operations related to individual task categories identified by their IDs.

        Method: get(self, id, current_user)

        Description:
        Handles HTTP GET requests to retrieve a specific task category by its ID.
        Returns appropriate responses based on the query parameters.

        Parameters:
        - id (string): The ID of the task category to retrieve.
        - current_user: User object representing the current authenticated user.

        Responses:
        - 200: Task Category found.
          Body: TaskCategoryModel
        - 401: Invalid or missing Authentication token.
          Body: BaseResponseModel
        - 404: Task Category not found or you don't have permission to view it.
          Body: BaseResponseModel

        Security:
        Requires a Bearer Authentication token.

        Authorization:
        Requires a valid access token obtained through authentication.

        Request Parameters:
        - exclude_tasks (boolean, optional): If set to true, tasks within the category will be excluded from the result.

        Method: put(self, id, current_user)

        Description:
        Handles HTTP PUT requests to update a specific task category by its ID.
        Returns appropriate responses based on the update outcome.

        Parameters:
        - id (string): The ID of the task category to update.
        - current_user: User object representing the current authenticated user.

        Request Body:
        Expects a JSON object with the following properties:
        - title (string): Title of the task category.
        - order (integer): Order of the task category.

        Responses:
        - 200: Task Category has been updated.
          Body: TaskCategoryModel
        - 401: Invalid or missing Authentication token.
          Body: BaseResponseModel
        - 404: Task Category not found or you don't have permission to update it.
          Body: BaseResponseModel

        Security:
        Requires a Bearer Authentication token.

        Validation:
        The request body is validated using the UpdateTaskCategoryModel schema.

        Authorization:
        Requires a valid access token obtained through authentication.

        Returns:
        A JSON object containing a message indicating the success of the update operation,
        along with the updated task category details.

        Method: delete(self, id, current_user)

        Description:
        Handles HTTP DELETE requests to delete a specific task category by its ID.
        Returns appropriate responses based on the deletion outcome.

        Parameters:
        - id (string): The ID of the task category to delete.
        - current_user: User object representing the current authenticated user.

        Responses:
        - 200: Task Category has been deleted.
          Body: BaseResponseModel
        - 401: Invalid or missing Authentication token.
          Body: BaseResponseModel
        - 404: Task Category not found or you don't have permission to delete it.
          Body: BaseResponseModel

        Security:
        Requires a Bearer Authentication token.

        Authorization:
        Requires a valid access token obtained through authentication.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("exclude_tasks", type=bool, default=False, help="Return tasks in tasks categories")

    @api.response(200, "Task Category found", TaskCategoryModel)
    @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)
    @api.response(404, "Task Category not found or you don't have permission to view it", BaseResponseModel)
    @api.doc(security="Bearer Auth")
    @token_required
    def get(self, id, current_user):
        """
            Handles HTTP GET requests to retrieve a specific task category by its ID.
            Returns appropriate responses based on the query parameters.

            Parameters:
            - id (string): The ID of the task category to retrieve.
            - current_user: User object representing the current authenticated user.

            Responses:
            - 200: Task Category found.
              Body: TaskCategoryModel
            - 401: Invalid or missing Authentication token.
              Body: BaseResponseModel
            - 404: Task Category not found or you don't have permission to view it.
              Body: BaseResponseModel

            Security:
            Requires a Bearer Authentication token.

            Authorization:
            Requires a valid access token obtained through authentication.

            Request Parameters:
            - exclude_tasks (boolean, optional): If set to true, tasks within the category will be excluded from the
              result.
        """
        args = self.parser.parse_args()
        exclude_tasks = True if args["exclude_tasks"] == "true" else False
        task_category = task_category_service.get_by_id(id, exclude_tasks, current_user)
        if task_category:
            return {"message": "Task Category has been searched", "result": task_category.to_dict(exclude_tasks=
                                                                                                  exclude_tasks)}, 200
        else:
            return {"message": "Task Category not found or you don't have permission to view it"}, 404

    @api.response(200, "Task Category has been updated", TaskCategoryModel)
    @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)
    @api.response(404,  "Task Category not found or you don't have permission to view it", BaseResponseModel)
    @api.expect(TaskCategoryUpdateModel)
    @api.doc(security="Bearer Auth")
    @validate(body=UpdateTaskCategoryModel)
    @token_required
    def put(self, id, current_user):
        """
            Handles HTTP PUT requests to update a specific task category by its ID.
            Returns appropriate responses based on the update outcome.

            Parameters:
            - id (string): The ID of the task category to update.
            - current_user: User object representing the current authenticated user.

            Request Body:
            Expects a JSON object with the following properties:
            - title (string): Title of the task category.
            - order (integer): Order of the task category.

            Responses:
            - 200: Task Category has been updated.
              Body: TaskCategoryModel
            - 401: Invalid or missing Authentication token.
              Body: BaseResponseModel
            - 404: Task Category not found or you don't have permission to view it.
              Body: BaseResponseModel

            Security:
            Requires a Bearer Authentication token.

            Validation:
            The request body is validated using the UpdateTaskCategoryModel schema.

            Authorization:
            Requires a valid access token obtained through authentication.

            Returns:
            A JSON object containing a message indicating the success of the update operation,
            along with the updated task category details.
        """
        title = request.body_params.title
        order = request.body_params.order
        task_category = task_category_service.update(id, title, order, current_user)
        if task_category:
            return {"message": "Task Category has been updated", "result": task_category.to_dict(exclude_tasks=
                                                                                                 True)}, 200
        else:
            return {"message":  "Task Category not found or you don't have permission to update it"}, 404

    @api.response(200, "Task Category has been deleted", BaseResponseModel)
    @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)
    @api.response(404, "Task Category not found or you don't have permission to delete it", BaseResponseModel)
    @api.doc(security="Bearer Auth")
    @token_required
    def delete(self, id, current_user):
        """
            Handles HTTP DELETE requests to delete a specific task category by its ID.
            Returns appropriate responses based on the deletion outcome.

            Parameters:
            - id (string): The ID of the task category to delete.
            - current_user: User object representing the current authenticated user.

            Responses:
            - 200: Task Category has been deleted.
              Body: BaseResponseModel
            - 401: Invalid or missing Authentication token.
              Body: BaseResponseModel
            - 404: Task Category not found or you don't have permission to delete it.
              Body: BaseResponseModel

            Security:
            Requires a Bearer Authentication token.

            Authorization:
            Requires a valid access token obtained through authentication.
        """
        success = task_category_service.delete(id, current_user)
        if success:
            return {"message": "Task Category has been deleted"}, 200
        else:
            return {"message": "Task Category not found or you don't have permission to delete it"}, 404
