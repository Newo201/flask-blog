from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

# Create a Comment Form for users to see posts
class CommentForm(FlaskForm):

    comment = CKEditorField(label = "Your Comment", validators=[DataRequired()])
    submit = SubmitField(label = "Submit Comment")