from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("sign in")


class PostForm(FlaskForm):
    body = StringField("body", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("post")
