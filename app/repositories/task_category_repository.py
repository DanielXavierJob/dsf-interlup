from sqlalchemy import asc
from sqlalchemy.orm import joinedload

from app import db
from app.interfaces.repository_interface import RepositoryInterface
from app.models import TaskCategory, User
from app.repositories.task_repository import TaskRepository


class TaskCategoryRepository(RepositoryInterface):
    def get_all(self, exclude_tasks: bool, current_user: User) -> list[TaskCategory]:
        """
            Retrieves all task categories associated with the current user.

            Parameters:
            - exclude_tasks (bool): If true, tasks within the categories will be excluded from the result.
            - current_user (User): The current authenticated user.

            Returns:
            A list of TaskCategory objects representing all task categories associated with the current user.
        """
        if not exclude_tasks:
            return (TaskCategory.query.filter_by(user_id=current_user.id).options(joinedload(TaskCategory.tasks))
                    .order_by(asc(TaskCategory.order)).all())
        else:
            return TaskCategory.query.filter_by(user_id=current_user.id).order_by(asc(TaskCategory.order)).all()

    def get_by_id(self, id: str, exclude_tasks: bool, current_user: User) -> TaskCategory:
        """
           Retrieves a specific task category by its ID.

           Parameters:
           - id (str): The ID of the task category to retrieve.
           - exclude_tasks (bool): If true, tasks within the category will be excluded from the result.
           - current_user (User): The current authenticated user.

           Returns:
           The TaskCategory object corresponding to the specified ID, or None if not found.
        """
        if not exclude_tasks:
            return TaskCategory.query.filter_by(id=id, user_id=current_user.id).options(
                joinedload(TaskCategory.tasks)).first()
        else:
            return TaskCategory.query.filter_by(id=id, user_id=current_user.id).first()

    def get_by_name(self, title: str):
        """
            Placeholder method. Not implemented.
        """
        pass

    def get_by_order(self, order: int, current_user: User):
        """
           Retrieves a task category by its order for the current user.

           Parameters:
           - order (int): The order of the task category.
           - current_user (User): The current authenticated user.

           Returns:
           The TaskCategory object corresponding to the specified order, or None if not found.
        """
        return TaskCategory.query.filter_by(order=order, user_id=current_user.id).first()

    def create(self, category: TaskCategory) -> TaskCategory:
        """
            Creates a new task category.

            Parameters:
            - category (TaskCategory): The TaskCategory object to create.

            Returns:
            The created TaskCategory object.
        """
        db.session.add(category)
        db.session.commit()
        return category

    def update(self, category: TaskCategory):
        """
            Updates an existing task category.

            Parameters:
            - category (TaskCategory): The TaskCategory object to update.
        """
        db.session.commit()

    def delete(self, id: str, current_user: User):
        """
            Deletes a specific task category by its ID.

            Parameters:
            - id (str): The ID of the task category to delete.
            - current_user (User): The current authenticated user.

            Returns:
            True if deletion was successful, False otherwise.
        """
        category = self.get_by_id(id, False, current_user)
        if category:
            task_repository = TaskRepository()
            for task in category.tasks:
                task_repository.delete(task.id)

            db.session.delete(category)
            db.session.commit()
            return True
        return False
