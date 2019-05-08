from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    userName = StringField("Username", validators=[DataRequired()])
    passWord = PasswordField("Password", validators=[DataRequired()])
    rememberMe = BooleanField("Remember me")
    submit = SubmitField("SignIn")




