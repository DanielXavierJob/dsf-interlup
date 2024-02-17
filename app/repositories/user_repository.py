from app import db
from app.interfaces.repository_interface import RepositoryInterface
from app.models import User


class UserRepository(RepositoryInterface):
    def get_all(self):
        return User.query.all()

    def get_by_id(self, id):
        return User.query.get(id)

    def get_by_name(self, username: str):
        return User.query.filter_by(username=username).first()

    def create(self, user):
        db.session.add(user)
        db.session.commit()

    def update(self, user):
        db.session.commit()

    def delete(self, id):
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
