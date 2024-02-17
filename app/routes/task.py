from flask import Blueprint, request
from flask_pydantic import validate
from flask_restx import Resource, Namespace, fields

from app.decorators import token_required
from app.dtos.task_dto import RegisterNewTaskModel, UpdateTaskModel
from app.services import TaskService
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Namespace('Tasks', description='Tasks related users', authorizations=authorizations)

bp = Blueprint('task', __name__)
task_service = TaskService()

# Task Model
TaskModel = api.model('TaskModel',
                      {
                          'id': fields.Integer,
                          'title': fields.String,
                          'description': fields.String(required=False),
                          'completed': fields.Boolean(default=False)
                      })

# Task Update Model
TaskUpdateModel = api.model('TaskUpdateModel',
                      {
                          'title': fields.String(required=False),
                          'description': fields.String(required=False),
                          'completed': fields.Boolean(required=False)
                      })

# Register Model
registerModel = api.model('TaskRegisterModel',
                          {
                              'title': fields.String,
                              'description': fields.String
                          })

# Base Response Model
baseResponseModel = api.model('BaseResponseModel',
                          {
                              'message': fields.String,
                          })



@api.route('/tasks')
class Tasks(Resource):
    @api.response(200, "All tasks related to this user", [TaskModel])
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, current_user):
        tasks = task_service.get_all(current_user)
        return {"message": 'Tasks has been searched', "result": [task.to_dict() for task in tasks]}, 200

    @api.response(200, "Task has been created", TaskModel)
    @api.expect(registerModel)
    @api.doc(security='Bearer Auth')
    @validate(body=RegisterNewTaskModel)
    @token_required
    def post(self, current_user):
        title = request.body_params.title
        description = request.body_params.description
        task = task_service.create(title, description, current_user)
        return {"message": "Task has been created", "result": task.to_dict()}, 201


@api.route('/tasks/<int:id>')
class Task(Resource):
    @api.response(200, "Task found", TaskModel)
    @api.response(404, "Task not found or you don't have permission to view it", baseResponseModel)
    @api.doc(security='Bearer Auth')
    @token_required
    def get(self, id, current_user):
        task = task_service.get_by_id(id, current_user)
        if task:
            return {"message": 'Task has been searched', "result": task.to_dict()}, 200
        else:
            return {"message": "Task not found or you don't have permission to view it"}, 404

    @api.response(200, "Task has been updated", TaskModel)
    @api.response(404, "Task not found or you don't have permission to view it", baseResponseModel)
    @api.expect(TaskUpdateModel)
    @api.doc(security='Bearer Auth')
    @validate(body=UpdateTaskModel)
    @token_required
    def put(self, id, current_user):
        title = request.body_params.title
        description = request.body_params.description
        completed = request.body_params.completed
        task = task_service.update(id, title, description,completed, current_user)
        if task:
            return {"message": "Task has been updated", "result": task.to_dict()}, 200
        else:
            return {"message": "Task not found or you don't have permission to update it"}, 404

    @api.response(200, "Task has been deleted", baseResponseModel)
    @api.response(404, "Task not found or you don't have permission to delete it", baseResponseModel)
    @api.doc(security='Bearer Auth')
    @token_required
    def delete(self, id, current_user):
        success = task_service.delete(id, current_user)
        if success:
            return {"message": "Task has been deleted"}, 200
        else:
            return {"message": "Task not found or you don't have permission to delete it"}, 404
