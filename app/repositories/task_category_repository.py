from sqlalchemy import asc
from sqlalchemy.orm import joinedload

from app import db
from app.interfaces.repository_interface import RepositoryInterface
from app.models import TaskCategory, User
from app.repositories.task_repository import TaskRepository


class TaskCategoryRepository(RepositoryInterface):
    def get_all(self, exclude_tasks: bool, current_user: User) -> list[TaskCategory]:
        if not exclude_tasks:
            return (TaskCategory.query.filter_by(user_id=current_user.id).options(joinedload(TaskCategory.tasks))
                    .order_by(asc(TaskCategory.order)).all())
        else:
            return TaskCategory.query.filter_by(user_id=current_user.id).order_by(asc(TaskCategory.order)).all()

    def get_by_id(self, id: str, exclude_tasks: bool, current_user: User) -> TaskCategory:
        if not exclude_tasks:
            return TaskCategory.query.filter_by(id=id, user_id=current_user.id).options(
                joinedload(TaskCategory.tasks)).first()
        else:
            return TaskCategory.query.filter_by(id=id, user_id=current_user.id).first()

    def get_by_name(self, title: str):
        pass

    def get_by_order(self, order: int, current_user: User):
        return TaskCategory.query.filter_by(order=order, user_id=current_user.id).first()

    def create(self, category: TaskCategory) -> TaskCategory:
        db.session.add(category)
        db.session.commit()
        return category

    def update(self, category: TaskCategory):
        db.session.commit()

    def delete(self, id: str, current_user: User):
        category = self.get_by_id(id, False, current_user)
        if category:
            task_repository = TaskRepository()
            for task in category.tasks:
                task_repository.delete(task.id)

            db.session.delete(category)
            db.session.commit()
            return True
        return False
