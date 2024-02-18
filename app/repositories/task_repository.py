from typing import Optional

from sqlalchemy import asc

from app import db
from app.interfaces.repository_interface import RepositoryInterface
from app.models import Task, User


class TaskRepository(RepositoryInterface):
    def get_all(self, category_id: Optional[int], current_user: User) -> list:
        if category_id:
            return (Task.query.filter_by(user_id=current_user.id, category_id=category_id).order_by(asc(Task.order))
                    .all())
        else:
            return Task.query.filter_by(user_id=current_user.id).order_by(asc(Task.order)).all()

    def get_by_id(self, id, current_user: User) -> Task | None:
        return Task.query.filter_by(id=id, user_id=current_user.id).first()

    def get_by_name(self, title: str):
        return Task.query.filter_by(title=title).first()

    def get_by_order(self, order: int, current_user: User):
        return Task.query.filter_by(order=order, user_id=current_user.id).first()

    def create(self, task: Task) -> Task:
        db.session.add(task)
        db.session.commit()
        return task

    def update(self, task):
        db.session.commit()

    def delete(self, id):
        task = Task.query.get(id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return True
        return False
