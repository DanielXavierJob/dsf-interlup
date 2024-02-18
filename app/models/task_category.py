from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app import db


class TaskCategory(db.Model):
    __tablename__ = "task_category"
    id = Column(String(64), primary_key=True)
    title = Column(String(128), nullable=False)
    order = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))
    tasks = relationship("Task", backref="category")

    def to_dict(self, exclude_tasks=False):
        data = {field.name: getattr(self, field.name) for field in self.__table__.c}
        if not exclude_tasks:
            data["tasks"] = [task.to_dict() for task in self.tasks]
        else:
            data["tasks"] = []

        return data
