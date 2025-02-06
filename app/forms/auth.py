from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo

from app.models import User


class SignInForm(FlaskForm):
    user_email = StringField("Почта", [DataRequired()])
    password = PasswordField("Пароль", [DataRequired()])
    submit = SubmitField("Війти")


class SignUpForm(FlaskForm):
    name = StringField("Ім'я")
    email = StringField(
        "Електронна адреса",
        [
            DataRequired(),
            Email(),
        ],
    )
    password = PasswordField("Пароль", [DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Підтвердити пароль", [DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Реєстрація")

    def validate_email(form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Ця електронна адреса вже зареєстрована.")
        
class ProfileForm(FlaskForm):
    name = StringField("Ім'я")
    email = StringField("Електронна адреса", [DataRequired(), Email()])
    about = StringField("Про себе")
    submit = SubmitField("Зберегти")
