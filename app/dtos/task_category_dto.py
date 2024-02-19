from typing import Optional

from pydantic import BaseModel


class RegisterNewTaskCategoryModel(BaseModel):
    """
        Represents the data model for registering a new task category.

        Attributes:
        - title (str): The title of the new task category.
        - order (int): The order of the new task category.
    """

    title: str
    order: int


class UpdateTaskCategoryModel(BaseModel):
    """
        Represents the data model for updating an existing task category.

        Attributes:
        - title (Optional[str]): The updated title of the task category.
        - order (Optional[int]): The updated order of the task category.
    """

    title: Optional[str] = None
    order: Optional[int] = None
