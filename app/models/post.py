from app import db
from datetime import datetime
from app.models.utils import ModelMixin


class Post(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(3500), nullable=True)
    image = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    user = db.relationship("User", back_populates="posts")
