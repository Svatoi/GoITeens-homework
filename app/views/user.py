from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user

from app.forms import ProfileForm

from app.controllers import PostController
from app.controllers import UserController
from app.models import Post, User

user_bp = Blueprint("user", __name__)

@user_bp.route("/settings", methods=["GET", "POST"])
def settings():
    user = User.query.get(current_user.id)
    form = ProfileForm()

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.about = form.about.data
        user.save()

        flash("Профіль успішно оновлено", "info")
        return redirect(url_for("user.profile"))
    elif form.is_submitted():
        flash("Надані дані були недійсними.", "danger")
    elif request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.about.data = user.about
    return render_template("auth/settings.html", form=form)

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
