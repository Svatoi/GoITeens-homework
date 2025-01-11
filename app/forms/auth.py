from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo

from app.models import User


class SignInForm(FlaskForm):
    user_email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("SignIn")


class SignUpForm(FlaskForm):
    name = StringField("Name")
    email = StringField(
        "Email Address",
        [
            DataRequired(),
            Email(),
        ],
    )
    password = PasswordField("Password", [DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Confirm Password", [DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_email(form, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("This email is already signed up.")
        
class ProfileForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email Address", [DataRequired(), Email()])
    about = StringField("About")
    submit = SubmitField("Save")
