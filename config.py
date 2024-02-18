from decouple import config


class Config:
    SECRET_KEY = config('SECRET_KEY', '004f2af45d3a4e161a7dd2d17fdae47f')
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', 'sqlite:///db.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = config('DEBUG', False)
