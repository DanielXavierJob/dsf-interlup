from decouple import config


class Config:
    """
        Configuration class for the application.

        Attributes:
        - SECRET_KEY (str): Secret key used for cryptographic operations.
        - SQLALCHEMY_DATABASE_URI (str): Database URI.
        - SQLALCHEMY_TRACK_MODIFICATIONS (bool): Flag to enable/disable tracking modifications.
        - DEBUG (bool): Flag to enable/disable debug mode.
    """

    SECRET_KEY = config('SECRET_KEY', '004f2af45d3a4e161a7dd2d17fdae47f')
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', 'sqlite:///db.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = config('DEBUG', False)
