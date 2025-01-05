from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from app.forms import SignInForm, SignUpForm, ProfileForm
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/sign-in", methods=["GET", "POST"])
def signin():
    form = SignInForm(request.form)
    if form.validate_on_submit():
        user = User.authenticate(form.user_email.data, form.password.data)
        if user:
            login_user(user)
            flash("SignIn successful.", "success")
            return redirect(url_for("main.index"))
        flash("Wrong username or password.", "danger")
    return render_template("auth/signin.html", form=form)


@auth_bp.route("/sign-out", methods=["GET"])
def signout():
    logout_user()
    flash("Sign Out successful.", "success")
    return redirect(url_for("main.index"))


@auth_bp.route("/sign-up", methods=["GET", "POST"])
def signup():
    form = SignUpForm(request.form)
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
        )
        user.save()
        login_user(user)
        flash("Registration successful. You are logged in.", "success")
        return redirect(url_for("main.index"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("auth/signup.html", form=form)

@auth_bp.route("/settings", methods=["GET", "POST"])
def settings():
    user = User.query.get(current_user.id)
    form = ProfileForm()

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.save()

        flash("Profile has been successfully updated", "info")
        return redirect(url_for("main.index"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    elif request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
    return render_template("auth/settings.html", form=form)