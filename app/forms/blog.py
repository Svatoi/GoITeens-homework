from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length

class PostForm(FlaskForm):
    title = StringField([DataRequired(), Length(4, 125)])
    content = TextAreaField([DataRequired(), Length(max=615)])
    image = StringField("Завантажуйте будь-які зображення/файли", [Optional()])

    submit = SubmitField("Зробити пост")