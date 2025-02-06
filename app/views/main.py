from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required, logout_user

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html", title="Головна", current_page=request.endpoint)

@main_bp.route("/contacts")
def contacts():
    return render_template(
        "contacts.html", title="Контакти", current_page=request.endpoint
    )

@main_bp.route("/read-more")
def read_more():
    return render_template("focus.html")

@main_bp.route("/popularity")
def popularity():
    return render_template("meme/popularity.html")
