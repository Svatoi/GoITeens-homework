from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.utils import ModelMixin
from datetime import datetime


class User(db.Model, ModelMixin, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(320), unique=True)
    created_at = db.Column(db.Date, default=datetime.now())
    password_hash = db.Column(db.String(255), nullable=False)

    posts = db.relationship("Post", back_populates="user", cascade="all, delete-orphan")

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, user_email, password):
        user = cls.query.filter(func.lower(cls.email) == func.lower(user_email)).first()
        if user is not None and check_password_hash(user.password, password):
            return user


class AnonymousUser(AnonymousUserMixin):
    pass
