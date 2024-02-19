from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    """
        Represents a user in the database.

        Attributes:
        - id (int): The unique identifier for the user.
        - username (str): The username of the user.
        - password_hash (str): The hashed password of the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))

    def set_password(self, password):
        """
            Sets the password for the user.

            Parameters:
            - password (str): The password to set.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
            Checks if the provided password matches the user's password.

            Parameters:
            - password (str): The password to check.

            Returns:
            True if the provided password matches the user's password, False otherwise.
        """
        return check_password_hash(self.password_hash, password)
