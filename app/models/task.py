from sqlalchemy import Column, Integer, String, ForeignKey

from app import db


class Task(db.Model):
    """
        Represents a task in the database.

        Attributes:
        - id (int): The unique identifier for the task.
        - title (str): The title of the task.
        - description (str): The description of the task.
        - order (int): The order of the task.
        - category_id (str): The ID of the category to which the task belongs.
        - user_id (int): The ID of the user who owns the task.
    """

    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    description = Column(String)
    order = Column(Integer)
    category_id = Column(String, ForeignKey("task_category.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    def to_dict(self):
        """
            Converts the task object to a dictionary.

            Returns:
            A dictionary representation of the task object.
        """
        return {field.name: getattr(self, field.name) for field in self.__table__.c}
