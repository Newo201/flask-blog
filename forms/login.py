from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired

# Create a Login Form for existing users
class LoginForm(FlaskForm):

    email = EmailField(label = "Your Email", validators=[DataRequired()])
    password = PasswordField(label = "Your Password", validators=[DataRequired()])
    submit = SubmitField(label = "Register Now")