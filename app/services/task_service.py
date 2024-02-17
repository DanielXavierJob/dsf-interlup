from typing import Optional

from app.models import Task, User
from app.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()

    def get_all(self, current_user: User) -> list:
        return self.task_repository.get_all(current_user)

    def get_by_id(self, id: int, current_user: User) -> Task:
        return self.task_repository.get_by_id(id, current_user)

    def create(self, title: str, description: str, current_user: User) -> Task:
        task = Task(title=title, description=description, user_id=current_user.id)
        self.task_repository.create(task)
        return task

    def update(self, id: int, title: Optional[str], description: Optional[str],completed: Optional[bool], current_user: User) -> Task:
        task = self.get_by_id(id, current_user)
        task.title = title if title else task.title
        task.description = description if description else task.description
        task.completed = completed if completed else task.completed
        self.task_repository.update(task)
        return task

    def delete(self, id: int, current_user: User) -> bool:
        task = self.get_by_id(id, current_user)
        return self.task_repository.delete(task.id)
