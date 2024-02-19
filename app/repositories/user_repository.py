from app import db
from app.interfaces.repository_interface import RepositoryInterface
from app.models import User


class UserRepository(RepositoryInterface):
    def get_all(self):
        """
             Retrieves all users.

             Returns:
             A list of User objects representing all users.
         """
        return User.query.all()

    def get_by_id(self, id: int):
        """
            Retrieves a specific user by their ID.

            Parameters:
            - id (int): The ID of the user to retrieve.

            Returns:
            The User object corresponding to the specified ID, or None if not found.
        """
        return User.query.get(id)

    def get_by_name(self, username: str):
        """
            Retrieves a user by their username.

            Parameters:
            - username (str): The username of the user.

            Returns:
            The User object corresponding to the specified username, or None if not found.
        """
        return User.query.filter_by(username=username).first()

    def get_by_order(self, order: int):
        """
             Placeholder method. Not implemented.
        """
        pass

    def create(self, user):
        """
            Creates a new user.

            Parameters:
            - user: The User object to create.
        """
        db.session.add(user)
        db.session.commit()

    def update(self, user):
        """
            Updates an existing user.

            Parameters:
            - user: The User object to update.
        """
        db.session.commit()

    def delete(self, id):
        """
            Deletes a specific user by their ID.

            Parameters:
            - id (int): The ID of the user to delete.
        """
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
