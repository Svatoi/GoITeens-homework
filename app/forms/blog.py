from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional

class AddPost(FlaskForm):
    title = StringField("Назва пост", [DataRequired()])
    content = StringField("Опис", [DataRequired()])
    image = StringField("Добавте фото або відео", [Optional()])

    submit = SubmitField("Зробити пост")