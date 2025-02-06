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
            flash("Вхід успішний.", "success")
            return redirect(url_for("main.index"))
        flash("Неправильний логін або пароль.", "danger")
    return render_template("auth/signin.html", form=form)


@auth_bp.route("/sign-out", methods=["GET"])
def signout():
    logout_user()
    flash("Вихід успішний.", "success")
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
        flash("Реєстрація успішна. Ви увійшли в систему.", "success")
        return redirect(url_for("main.index"))
    elif form.is_submitted():
        flash("Надані дані були недійсними.", "danger")
    return render_template("auth/signup.html", form=form)

@auth_bp.route('/logout')
def logout():
    logout_user() 
    return redirect(url_for('index'))