from os import environ


class Config:
    SECRET_KEY = environ.get('SECRET_KEY') or '004f2af45d3a4e161a7dd2d17fdae47f'
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or 'sqlite:////Users\\daniel\\PycharmProjects\\dsf-interlup\\dbb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
