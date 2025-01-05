from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import current_user

from app.forms import AddPost
from app.models import Post
 
blog_bp = Blueprint("blog", __name__, url_prefix="/blog")

@blog_bp.route("/", methods=['GET', 'POST'])
def index():
    check_posts = Post.query.filter_by(user_id=current_user.id).first()
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template(
        "blog/index.html", title="Блог", current_page=request.endpoint, check_posts=check_posts, posts=posts
    )


@blog_bp.route("/post", methods=['GET', 'POST'])
def add_post():
    form = AddPost(request.form)
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            image=form.image.data,
            user_id=current_user.id,
        )
        post.save()
        flash("Пост був опублікован", "success")
        return redirect(url_for("blog.index"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template(
        "blog/add_post.html", title="Добавити пост", current_page=request.endpoint, form=form
    )