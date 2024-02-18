from typing import Optional

from app.models import Task, User, TaskCategory
from app.repositories.task_category_repository import TaskCategoryRepository
from app.repositories.task_repository import TaskRepository
from app.utils import move_element_and_update_order


class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()
        self.task_category_repository = TaskCategoryRepository()

    def create_init_tasks(self, tasks_categories: list[TaskCategory], current_user: User) -> list[Task]:
        tasks_created = []
        for task_category in tasks_categories:
            task = self.create(title=f"Example Task '{task_category.title}'",
                               description=f"Example for '{task_category.title}' category",
                               order=1,
                               category_id=task_category.id, current_user=current_user)
            tasks_created.append(task)
        return tasks_created

    def get_all(self, category_id: Optional[str], current_user: User) -> list:
        return self.task_repository.get_all(category_id, current_user)

    def get_by_id(self, id: int, current_user: User) -> Task | None:
        return self.task_repository.get_by_id(id, current_user)

    def create(self, title: str, description: str, order: int, category_id: str, current_user: User) -> Task:
        category = self.task_category_repository.get_by_id(category_id, True, current_user)
        task = Task(title=title, description=description, order=order, category_id=category.id, user_id=current_user.id)
        self.task_repository.create(task)
        return task

    def get_by_order(self, order: int, current_user: User):
        return self.task_repository.get_by_order(order, current_user)

    def update(self, id: int, title: Optional[str], description: Optional[str], order: Optional[int],
               category_id: Optional[str], current_user: User) -> Task | None:
        task = self.get_by_id(id, current_user)
        if task is None:
            return None

        task.title = title if title else task.title
        task.description = description if description else task.description
        if order is not None:
            task_order_older = self.get_all(task.category_id, current_user)

            task_order_reordered = move_element_and_update_order(task_order_older, task.id, order)

            for row_task_category_order in task_order_reordered:
                self.task_repository.update(row_task_category_order)
                if row_task_category_order.id == task.id:
                    task.order = row_task_category_order.order

        if category_id:
            category = self.task_category_repository.get_by_id(category_id, True, current_user)
            task.category_id = category.id

        self.task_repository.update(task)
        return task

    def delete(self, id: int, current_user: User) -> bool:
        task = self.get_by_id(id, current_user)
        if not task:
            return False
        return self.task_repository.delete(task.id)
