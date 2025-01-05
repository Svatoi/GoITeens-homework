from flask import Blueprint, render_template, request

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html", title="Головна", current_page=request.endpoint)


@main_bp.route("/contacts")
def contacts():
    return render_template(
        "index.html", title="Контакти", current_page=request.endpoint
    )

@main_bp.route("/read-more")
def read_more():
    return render_template("focus.html")
