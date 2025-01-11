from app.models import User

def get_users():
    return User.query.get()