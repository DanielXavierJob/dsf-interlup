from typing import Optional

from sqlalchemy import asc

from app import db
from app.interfaces.repository_interface import RepositoryInterface
from app.models import Task, User


class TaskRepository(RepositoryInterface):
    def get_all(self, category_id: Optional[int], current_user: User) -> list:
        """
            Retrieves all tasks associated with the current user.

            Parameters:
            - category_id (Optional[int]): The ID of the category to filter tasks by (optional).
            - current_user (User): The current authenticated user.

            Returns:
            A list of Task objects representing all tasks associated with the current user.
        """
        if category_id:
            return (Task.query.filter_by(user_id=current_user.id, category_id=category_id).order_by(asc(Task.order))
                    .all())
        else:
            return Task.query.filter_by(user_id=current_user.id).order_by(asc(Task.order)).all()

    def get_by_id(self, id, current_user: User) -> Task | None:
        """
            Retrieves a specific task by its ID.

            Parameters:
            - id (str): The ID of the task to retrieve.
            - current_user (User): The current authenticated user.

            Returns:
            The Task object corresponding to the specified ID, or None if not found.
        """
        return Task.query.filter_by(id=id, user_id=current_user.id).first()

    def get_by_name(self, title: str):
        """
            Retrieves a task by its title.

            Parameters:
            - title (str): The title of the task.

            Returns:
            The Task object corresponding to the specified title, or None if not found.
        """
        return Task.query.filter_by(title=title).first()

    def get_by_order(self, order: int, current_user: User):
        """
            Retrieves a task by its order for the current user.

            Parameters:
            - order (int): The order of the task.
            - current_user (User): The current authenticated user.

            Returns:
            The Task object corresponding to the specified order, or None if not found.
        """
        return Task.query.filter_by(order=order, user_id=current_user.id).first()

    def create(self, task: Task) -> Task:
        """
            Creates a new task.

            Parameters:
            - task (Task): The Task object to create.

            Returns:
            The created Task object.
        """
        db.session.add(task)
        db.session.commit()
        return task

    def update(self, task):
        """
            Updates an existing task.

            Parameters:
            - task: The Task object to update.
        """
        db.session.commit()

    def delete(self, id):
        """
            Deletes a specific task by its ID.

            Parameters:
            - id (str): The ID of the task to delete.

            Returns:
            True if deletion was successful, False otherwise.
        """
        task = Task.query.get(id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return True
        return False
