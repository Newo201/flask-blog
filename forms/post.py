from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class PostForm(FlaskForm):

    title = StringField(label = "Blog Title", validators=[DataRequired()])
    subtitle = StringField(label = "Blog Subtitle", validators=[DataRequired()])
    img_url = StringField(label = "Blog Image URL", validators=[DataRequired()])
    body = CKEditorField(label = "Blog Content", validators=[DataRequired()])
    submit = SubmitField(label = "Make Post")