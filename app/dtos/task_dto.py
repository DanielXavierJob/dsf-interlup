from typing import Optional

from pydantic import BaseModel


class RegisterNewTaskModel(BaseModel):
    title: str
    description: str


class UpdateTaskModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

