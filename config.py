import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRED_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + os.path.join(BASE_DIR, 'blog.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

