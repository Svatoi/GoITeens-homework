import os
import json
from flask import Blueprint, redirect, jsonify, render_template, request, flash, url_for
from flask_login import current_user

from app.forms import PostForm
from app.controllers import PostController
from app.models import Post
 
blog_bp = Blueprint("blog", __name__, url_prefix="/blog")

UPLOAD_FOLDER = os.path.join('static', 'uploads')

@blog_bp.route("/", methods=['GET', 'POST'])
def index():
    check_posts = PostController.check_posts(current_user.id)
    posts = PostController.get_post_by_user(current_user.id)
    for post in posts:
        post.created_at = post.created_at.strftime('%d.%m.%Y')
    return render_template(
        "blog/index.html", title="Блог", current_page=request.endpoint, check_posts=check_posts, posts=posts
    )

@blog_bp.route("/blog/post", methods=['GET', 'POST'])
def add_post():
    try:
        form = PostForm(request.form)
        
        if form.validate_on_submit():
            # data = request.json
            # image_data = data.get('image')
            
            PostController.create_post(
                title=form.title.data, 
                content=form.content.data, 
                # image=image_data, 
                user_id=current_user.id)
                
            flash("Пост був опублікован", "success")
            return redirect(url_for("blog.index"))
        elif form.is_submitted():
            flash("Надані дані були недійсними..", "danger")
        return render_template(
            "blog/add_post.html", 
            title="Добавити пост", 
            current_page=request.endpoint, 
            form=form
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@blog_bp.route("/post/<post_id>/<post_title>", methods=['GET', 'POST'])
def view_post(post_id, post_title):
    post = PostController.get_post_by_id(post_id)
    if post:
        post.created_at = post.created_at.strftime('%d.%m.%Y')
        return render_template(
            "blog/view_post.html", 
            title=post.title, 
            current_page=request.endpoint, 
            post=post
        )
    else:
        flash("Пост з таким названням не знайдено", "danger")
        return redirect(url_for("blog.index"))


@blog_bp.route("/post/edit/<post_id>/<post_title>", methods=['GET', 'POST'])
def edit_post(post_id, post_title):
    post = PostController.get_post_by_id(post_id)
    if not post:
        flash("Пост не знайдено", "danger")
        return redirect(url_for("blog.index"))

    form = PostForm(obj=post)
    if form.validate_on_submit():
            PostController.update_post(post_id, form.title.data, form.content.data)
            flash("Пост успішно змінено", "success")
            return redirect(url_for("blog.view_post", post_title=post.title, post_id=post_id))
    elif form.is_submitted():
        flash("Надані дані були недійсними.", "danger")
    
    return render_template(
        "blog/edit_post.html", 
        title="Редагувати пост", 
        current_page=request.endpoint, 
        form=form,
        form_action=url_for("blog.edit_post", post_id=post_id, post_title=post_title)
    )

@blog_bp.route("/post/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = PostController.get_post_by_id(post_id)

    if not post or current_user.id != post.user_id:
        flash("Не знайдено")
        return redirect(url_for("blog.index"), code=303)

    PostController.delete_post(post_id)

    flash(f"Пост {post.title} був видаленний")
    return redirect(url_for("blog.index"), code=303)