from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app import db


class TaskCategory(db.Model):
    """
         Represents a task category in the database.

         Attributes:
         - id (str): The unique identifier for the task category.
         - title (str): The title of the task category.
         - order (int): The order of the task category.
         - user_id (int): The ID of the user who owns the task category.
         - tasks (relationship): Relationship with Task objects associated with the category.
    """
    __tablename__ = "task_category"
    id = Column(String(64), primary_key=True)
    title = Column(String(128), nullable=False)
    order = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))
    tasks = relationship("Task", backref="category")

    def to_dict(self, exclude_tasks=False):
        """
            Converts the task category object to a dictionary.

            Parameters:
            - exclude_tasks (bool): If True, tasks associated with the category will be excluded from the dictionary.

            Returns:
            A dictionary representation of the task category object.
        """
        data = {field.name: getattr(self, field.name) for field in self.__table__.c}
        if not exclude_tasks:
            data["tasks"] = [task.to_dict() for task in self.tasks]
        else:
            data["tasks"] = []

        return data
