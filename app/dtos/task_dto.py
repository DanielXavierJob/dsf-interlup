from typing import Optional

from pydantic import BaseModel


class RegisterNewTaskModel(BaseModel):
    """
        Represents the data model for registering a new task.

        Attributes:
        - title (str): The title of the new task.
        - description (str): The description of the new task.
        - category_id (str): The ID of the category to which the new task belongs.
        - order (int): The order of the new task.
    """

    title: str
    description: str
    category_id: str
    order: int


class UpdateTaskModel(BaseModel):
    """
        Represents the data model for updating an existing task.

        Attributes:
        - title (Optional[str]): The updated title of the task.
        - description (Optional[str]): The updated description of the task.
        - category_id (Optional[str]): The updated category ID of the task.
        - order (Optional[int]): The updated order of the task.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    order: Optional[int] = None
