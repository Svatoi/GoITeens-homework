from app import db

class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False, unique=True)

    user = db.relationship('User', back_populates='Post')
    posts = db.relationship('Post', back_populates='user', cascade='all')

