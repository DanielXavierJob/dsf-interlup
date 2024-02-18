import hashlib
import time
from typing import Optional

from app.models import TaskCategory, User
from app.repositories.task_category_repository import TaskCategoryRepository
from app.utils import move_element_and_update_order


class TaskCategoryService:
    def __init__(self):
        self.task_category_repository = TaskCategoryRepository()

    def create_init_tasks_categories(self, current_user: User) -> list[TaskCategory]:
        todo = self.create(title="Todo", order=1, current_user=current_user)
        in_progress = self.create(title="In Progress", order=2, current_user=current_user)
        done = self.create(title="Done", order=3, current_user=current_user)
        return [todo, in_progress, done]

    def get_all(self,  exclude_tasks: bool, current_user: User) -> list[TaskCategory]:
        return self.task_category_repository.get_all(exclude_tasks, current_user)

    def get_by_id(self, id: str, exclude_tasks: Optional[bool], current_user: User) -> TaskCategory:
        return self.task_category_repository.get_by_id(id, exclude_tasks, current_user)

    def get_by_order(self, order: int, current_user: User):
        return self.task_category_repository.get_by_order(order, current_user)

    def create(self, title: str, order: int, current_user: User) -> TaskCategory:
        id_task_category = hashlib.sha256(f"{title}{time.time()}".encode()).hexdigest()
        task_category = TaskCategory(id=id_task_category, title=title, order=order, user_id=current_user.id)
        self.task_category_repository.create(task_category)
        return task_category

    def update(self, id: str, title: Optional[str], order: Optional[int], current_user: User) -> TaskCategory:
        task_category = self.get_by_id(id, True, current_user=current_user)
        task_category.title = title if title else task_category.title
        if order and task_category.order != order:

            task_category_order_older = self.get_all(exclude_tasks=True, current_user=current_user)
            task_category_reordered = move_element_and_update_order(task_category_order_older, task_category.id, order)

            def filter_without_task(tasks_category_filter):
                return tasks_category_filter.id != task_category.id

            for task_category_order in filter(filter_without_task, task_category_reordered):
                self.task_category_repository.update(task_category_order)

        self.task_category_repository.update(task_category)
        return task_category

    def delete(self, id: str, current_user: User) -> bool:
        task_category = self.get_by_id(id, False, current_user)
        return self.task_category_repository.delete(task_category.id, current_user)
