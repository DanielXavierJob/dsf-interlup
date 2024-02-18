from sqlalchemy import Column, Integer, String, ForeignKey

from app import db


class Task(db.Model):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    description = Column(String)
    order = Column(Integer)
    category_id = Column(String, ForeignKey("task_category.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}
