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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("exclude_tasks", type=str, default="false", help="Return tasks in tasks categories")

    @api.response(200, "All tasks categories related to this user", [TaskCategoryModel])
    @api.response(401, "Invalid or missing Authentication token!", BaseResponseModel)
    @api.doc(security="Bearer Auth")
    @token_required
    def get(self, current_user):
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
        success = task_category_service.delete(id, current_user)
        if success:
            return {"message": "Task Category has been deleted"}, 200
        else:
            return {"message": "Task Category not found or you don't have permission to delete it"}, 404
