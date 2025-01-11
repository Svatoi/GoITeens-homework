from flask import Blueprint, render_template, request
from flask_login import current_user

from app.controllers import PostController
from app.controllers import UserController
from app.models import Post

user_bp = Blueprint("user", __name__)

@user_bp.route("/profile")
def profile():
    user_info = UserController.get_user_info(id=current_user.id)
    check_posts = Post.query.filter_by(user_id=current_user.id).first()
    posts = PostController.get_post_by_user(current_user.id)

    for post in posts:
        post.created_at = post.created_at.strftime('%d.%m.%Y')

    if not user_info:
        return render_template("user/error.html", title="Профіль не знайдено"), 404
    
    return render_template("user/index.html", 
                           title="Профіль", 
                           current_page=request.endpoint, 
                           user_info=user_info,
                           check_posts=check_posts,
                           posts=posts
                           )
