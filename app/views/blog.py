import os
from flask import Blueprint, redirect, jsonify, render_template, request, flash, url_for
from flask_login import current_user

from app.forms import PostForm
from app.controllers import PostController
from app.models import Post
 
blog_bp = Blueprint("blog", __name__, url_prefix="/blog")

UPLOAD_FOLDER = os.path.join('static', 'uploads')

@blog_bp.route("/", methods=['GET', 'POST'])
def index():
    check_posts = Post.query.filter_by(user_id=current_user.id).first()
    posts = PostController.get_post_by_user(current_user.id)
    for post in posts:
        post.created_at = post.created_at.strftime('%d.%m.%Y')
    return render_template(
        "blog/index.html", title="Блог", current_page=request.endpoint, check_posts=check_posts, posts=posts
    )

@blog_bp.route("/post", methods=['GET', 'POST'])
def add_post():
    form = PostForm(request.form)
    if form.validate_on_submit():
        image_url = request.form.get('image_url')
        PostController.create_post(
            title=form.title.data, 
            content=form.content.data, 
            image=image_url, 
            user_id=current_user.id)
        
        flash("Пост був опублікован", "success")
        return redirect(url_for("blog.index"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template(
        "blog/add_post.html", title="Добавити пост", current_page=request.endpoint, form=form
    )
