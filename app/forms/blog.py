from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length

class PostForm(FlaskForm):
    title = StringField("Назва пост", [DataRequired(), Length(4, 125)])
    content = TextAreaField("Опис", [DataRequired(), Length(4, 256)])
    image = StringField("Завантажуйте будь-які зображення", [Optional()])

    submit = SubmitField("Зробити пост")