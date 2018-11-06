import os


class Config(object):
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = "postgresql://<username>:<password>@<host>:5432/<dbname>"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TAX = 0.08
    LIMIT = 5
