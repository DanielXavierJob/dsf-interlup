from app import db
from app.interfaces.repository_interface import RepositoryInterface
from app.models import Task, User


class TaskRepository(RepositoryInterface):
    def get_all(self, current_user: User) -> list:
        return Task.query.filter_by(user_id=current_user.id).all()

    def get_by_id(self, id, current_user: User) -> Task:
        return Task.query.filter_by(id=id, user_id=current_user.id).first_or_404("Task not found")

    def get_by_name(self, title: str):
        return Task.query.filter_by(title=title).first()

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
