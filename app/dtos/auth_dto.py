from pydantic import BaseModel


class AuthenticationModel(BaseModel):
    """
        Represents the data model for user authentication.

        Attributes:
        - username (str): The username of the user.
        - password (str): The password of the user.
    """

    username: str
    password: str


class AuthenticationResponseModel(BaseModel):
    """
        Represents the response model for successful authentication.

        Attributes:
        - id (int): The ID of the authenticated user.
        - username (str): The username of the authenticated user.
    """

    id: int
    username: str


class RegisterNewAuthenticationModel(BaseModel):
    """
        Represents the data model for registering new users.

        Attributes:
        - username (str): The username of the new user.
        - password (str): The password of the new user.
    """

    username: str
    password: str
