from typing import Optional

from pydantic import BaseModel


class RegisterNewTaskModel(BaseModel):
    title: str
    description: str
    category_id: str
    order: int


class UpdateTaskModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    order: Optional[int] = None
