from app import db
from app.models import User

class UserRepository:
    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def create(self, user):
        db.session.add(user)
        db.session.commit()
