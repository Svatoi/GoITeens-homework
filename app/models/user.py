from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.utils import ModelMixin
from datetime import datetime

class User(db.Model, ModelMixin, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(120))
    created_at = db.Column(db.Date, default=datetime.now())
    password_hash = db.Column(db.String(255), nullable=False)

    posts = db.relationship('Post', back_populates='user', cascade='all')

    @hybrid_property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)