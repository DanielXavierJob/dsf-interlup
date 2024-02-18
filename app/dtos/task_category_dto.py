from typing import Optional

from pydantic import BaseModel


class RegisterNewTaskCategoryModel(BaseModel):
    title: str
    order: int


class UpdateTaskCategoryModel(BaseModel):
    title: Optional[str] = None
    order: Optional[int] = None
