from app import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(355))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False, unique=True)
    
    created_at = db.Column(db.Date, default=datetime.now())

    user = db.relationship('User', back_populates='Post')
    posts = db.relationship('Post', back_populates='user', cascade='all')

