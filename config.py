import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY=os.urandom(24)
    WTF_CSRF_SECRET_KEY="a csrf secret key"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or
        "sqlite:///" + os.path.join(BASE_DIR, "blog.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_USERNAME=os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD=os.environ.get("ADMIN_PASSWORD", "admin")

