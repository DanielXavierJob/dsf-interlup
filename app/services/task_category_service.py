import hashlib
import time
from typing import Optional

from app.models import TaskCategory, User
from app.repositories.task_category_repository import TaskCategoryRepository
from app.utils import move_element_and_update_order


class TaskCategoryService:
    """
        Class: TaskCategoryService

        Description:
        This class provides services related to task categories for the Todo-List API. It includes methods for creating
        initial task categories, retrieving task categories, creating new task categories, updating existing task
        categories, and deleting task categories.

        Methods:
        - __init__(self): Constructor method initializing the task category repository.
        - create_init_tasks_categories(self, current_user: User) -> list[TaskCategory]: Creates and returns initial task
          categories ('Todo', 'In Progress', 'Done').
        - get_all(self, exclude_tasks: bool, current_user: User) -> list[TaskCategory]: Retrieves all task categories
          optionally excluding tasks associated with them.
        - get_by_id(self, id: str, exclude_tasks: Optional[bool], current_user: User) -> TaskCategory: Retrieves a task
          category by its ID optionally excluding tasks associated with it.
        - get_by_order(self, order: int, current_user: User): Retrieves a task category by its order.
        - create(self, title: str, order: int, current_user: User) -> TaskCategory: Creates a new task category with the
          provided title and order.
        - update(self, id: str, title: Optional[str], order: Optional[int], current_user: User) -> TaskCategory: Updates
          an existing task category with the provided ID, title, and/or order.
        - delete(self, id: str, current_user: User) -> bool: Deletes a task category with the provided ID.

        Attributes:
        - task_category_repository: An instance of TaskCategoryRepository for accessing task category data.

        Note:
        - This class assumes the existence of a User instance for operations that require a current user.
        - The 'move_element_and_update_order' function is utilized within the 'update' method for reordering task categories.
    """
    def __init__(self):
        self.task_category_repository = TaskCategoryRepository()

    def create_init_tasks_categories(self, current_user: User) -> list[TaskCategory]:
        """
            Method: create_init_tasks_categories

            Description:
            Creates and returns initial task categories ('Todo', 'In Progress', 'Done') for a given user. This method is
            typically used during user registration or initialization to provide default task categories.

            Parameters:
            - current_user (User): The current user for whom the task categories are created.

            Returns:
            list[TaskCategory]: A list containing the newly created task categories ('Todo', 'In Progress', 'Done').
        """

        todo = self.create(title="Todo", order=1, current_user=current_user)
        in_progress = self.create(title="In Progress", order=2, current_user=current_user)
        done = self.create(title="Done", order=3, current_user=current_user)
        return [todo, in_progress, done]

    def get_all(self,  exclude_tasks: bool, current_user: User) -> list[TaskCategory]:
        """
            Method: get_all

            Description:
            Retrieves all task categories optionally excluding tasks associated with them.

            Parameters:
            - exclude_tasks (bool): If True, tasks associated with the task categories will be excluded from the result.
            - current_user (User): The current user for whom the task categories are retrieved.

            Returns:
            list[TaskCategory]: A list containing all task categories retrieved from the repository.
        """

        return self.task_category_repository.get_all(exclude_tasks, current_user)

    def get_by_id(self, id: str, exclude_tasks: Optional[bool], current_user: User) -> TaskCategory:
        """
            Method: get_by_id

            Description:
            Retrieves a task category by its ID optionally excluding tasks associated with it.

            Parameters:
            - id (str): The ID of the task category to retrieve.
            - exclude_tasks (Optional[bool]): If True, tasks associated with the task category will be excluded from the
              result.
            - current_user (User): The current user for whom the task category is retrieved.

            Returns:
            TaskCategory: The task category retrieved based on the provided ID.
        """

        return self.task_category_repository.get_by_id(id, exclude_tasks, current_user)

    def get_by_order(self, order: int, current_user: User):
        """
            Method: get_by_order

            Description:
            Retrieves a task category by its order.

            Parameters:
            - order (int): The order of the task category to retrieve.
            - current_user (User): The current user for whom the task category is retrieved.

            Returns:
            TaskCategory: The task category retrieved based on the provided order.
        """

        return self.task_category_repository.get_by_order(order, current_user)

    def create(self, title: str, order: int, current_user: User) -> TaskCategory:
        """
            Method: create

            Description:
            Creates a new task category with the provided title and order for the current user.

            Parameters:
            - title (str): The title of the new task category.
            - order (int): The order of the new task category.
            - current_user (User): The current user for whom the task category is created.

            Returns:
            TaskCategory: The newly created task category instance.
        """

        id_task_category = hashlib.sha256(f"{title}{time.time()}".encode()).hexdigest()
        task_category = TaskCategory(id=id_task_category, title=title, order=order, user_id=current_user.id)
        self.task_category_repository.create(task_category)
        return task_category

    def update(self, id: str, title: Optional[str], order: Optional[int], current_user: User) -> TaskCategory:
        """
            Method: update

            Description:
            Updates an existing task category with the provided ID, title, and/or order for the current user. If the
            'title' parameter is provided, it updates the title of the task category. If the 'order' parameter is
            provided and different from the current order, it reorders the task category accordingly.

            Parameters:
            - id (str): The ID of the task category to update.
            - title (Optional[str]): The new title for the task category (if provided).
            - order (Optional[int]): The new order for the task category (if provided).
            - current_user (User): The current user performing the update operation.

            Returns:
            TaskCategory: The updated task category instance.
        """

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
        """
            Method: delete

            Description:
            Deletes a task category with the provided ID for the current user.

            Parameters:
            - id (str): The ID of the task category to delete.
            - current_user (User): The current user performing the delete operation.

            Returns:
            bool: True if the task category is successfully deleted, False otherwise.
        """

        task_category = self.get_by_id(id, False, current_user)
        return self.task_category_repository.delete(task_category.id, current_user)
