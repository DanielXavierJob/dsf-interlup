from typing import Optional

from app.models import Task, User, TaskCategory
from app.repositories.task_category_repository import TaskCategoryRepository
from app.repositories.task_repository import TaskRepository
from app.utils import move_element_and_update_order


class TaskService:
    """
        Class: TaskService

        Description:
        This class provides services related to tasks for the Todo-List API. It includes methods for creating initial
        tasks, retrieving tasks, creating new tasks, updating existing tasks, and deleting tasks.

        Methods:
        - __init__(self): Constructor method initializing task repositories.
        - create_init_tasks(self, tasks_categories: list[TaskCategory], current_user: User) -> list[Task]: Creates and
          returns initial example tasks for each provided task category.
        - get_all(self, category_id: Optional[str], current_user: User) -> list: Retrieves all tasks optionally filtered
          by category ID.
        - get_by_id(self, id: int, current_user: User) -> Task | None: Retrieves a task by its ID.
        - create(self, title: str, description: str, order: int, category_id: str, current_user: User) -> Task: Creates
          a new task with the provided title, description, order, and category ID.
        - get_by_order(self, order: int, current_user: User): Retrieves a task by its order.
        - update(self, id: int, title: Optional[str], description: Optional[str], order: Optional[int], category_id:
          Optional[str], current_user: User) -> Task | None: Updates an existing task with the provided ID, title,
          description, order, and/or category ID.
        - delete(self, id: int, current_user: User) -> bool: Deletes a task with the provided ID.

        Attributes:
        - task_repository: An instance of TaskRepository for accessing task data.
        - task_category_repository: An instance of TaskCategoryRepository for accessing task category data.

        Note:
        - This class assumes the existence of a User instance for operations that require a current user.
        - The 'move_element_and_update_order' function is utilized within the 'update' method for reordering tasks.
    """

    def __init__(self):
        self.task_repository = TaskRepository()
        self.task_category_repository = TaskCategoryRepository()

    def create_init_tasks(self, tasks_categories: list[TaskCategory], current_user: User) -> list[Task]:
        """
            Method: create_init_tasks

            Description:
            Creates and returns initial example tasks for each provided task category. These example tasks are created
            with a default title and description, and each task belongs to its respective task category.

            Parameters:
            - tasks_categories (list[TaskCategory]): A list of TaskCategory instances for which initial example tasks
              will be created.
            - current_user (User): The current user for whom the example tasks are created.

            Returns:
            list[Task]: A list containing the newly created example tasks.
        """

        tasks_created = []
        for task_category in tasks_categories:
            task = self.create(title=f"Example Task '{task_category.title}'",
                               description=f"Example for '{task_category.title}' category",
                               order=1,
                               category_id=task_category.id, current_user=current_user)
            tasks_created.append(task)
        return tasks_created

    def get_all(self, category_id: Optional[str], current_user: User) -> list:
        """
            Method: get_all

            Description:
            Retrieves all tasks optionally filtered by category ID for the given current user.

            Parameters:
            - category_id (Optional[str]): The ID of the task category to filter tasks by. If None, all tasks are
              retrieved.
            - current_user (User): The current user for whom the tasks are retrieved.

            Returns:
            list: A list containing all tasks retrieved from the repository.
        """

        return self.task_repository.get_all(category_id, current_user)

    def get_by_id(self, id: int, current_user: User) -> Task | None:
        """
            Method: get_by_id

            Description:
            Retrieves a task by its ID for the given current user.

            Parameters:
            - id (int): The ID of the task to retrieve.
            - current_user (User): The current user for whom the task is retrieved.

            Returns:
            Task | None: The task retrieved based on the provided ID. Returns None if no task is found.
        """

        return self.task_repository.get_by_id(id, current_user)

    def create(self, title: str, description: str, order: int, category_id: str, current_user: User) -> Task:
        """
            Method: create

            Description:
            Creates a new task with the provided title, description, order, and category ID for the given current user.

            Parameters:
            - title (str): The title of the new task.
            - description (str): The description of the new task.
            - order (int): The order of the new task.
            - category_id (str): The ID of the task category to which the new task belongs.
            - current_user (User): The current user creating the task.

            Returns:
            Task: The newly created task instance.
        """

        category = self.task_category_repository.get_by_id(category_id, True, current_user)
        task = Task(title=title, description=description, order=order, category_id=category.id, user_id=current_user.id)
        self.task_repository.create(task)
        return task

    def get_by_order(self, order: int, current_user: User):
        """
            Method: get_by_order

            Description:
            Retrieves a task by its order for the given current user.

            Parameters:
            - order (int): The order of the task to retrieve.
            - current_user (User): The current user for whom the task is retrieved.

            Returns:
            Task: The task retrieved based on the provided order.
        """

        return self.task_repository.get_by_order(order, current_user)

    def update(self, id: int, title: Optional[str], description: Optional[str], order: Optional[int],
               category_id: Optional[str], current_user: User) -> Task | None:
        """
            Method: update

            Description:
            Updates an existing task with the provided ID, title, description, order, and/or category ID for the given
            current user.

            Parameters:
            - id (int): The ID of the task to update.
            - title (Optional[str]): The new title for the task (if provided).
            - description (Optional[str]): The new description for the task (if provided).
            - order (Optional[int]): The new order for the task (if provided).
            - category_id (Optional[str]): The new category ID for the task (if provided).
            - current_user (User): The current user updating the task.

            Returns:
            Task | None: The updated task instance if the update is successful. Returns None if no task is found.
        """

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
        """
            Method: delete

            Description:
            Deletes a task with the provided ID for the given current user.

            Parameters:
            - id (int): The ID of the task to delete.
            - current_user (User): The current user deleting the task.

            Returns:
            bool: True if the task is successfully deleted, False otherwise.
        """

        task = self.get_by_id(id, current_user)
        if not task:
            return False
        return self.task_repository.delete(task.id)
