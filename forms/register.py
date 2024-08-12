from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired

# Create a Registration Form for new users
class RegisterForm(FlaskForm):

    email = EmailField(label = "Your Email", validators=[DataRequired()])
    password = PasswordField(label = "Your Password", validators=[DataRequired()])
    name = StringField(label = "Your Name", validators=[DataRequired()])
    submit = SubmitField(label = "Register Now")