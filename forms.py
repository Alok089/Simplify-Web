from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, URL, Email
from flask_ckeditor import CKEditorField
from wtforms.csrf.session import SessionCSRF
from datetime import timedelta

##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class CommentForm(FlaskForm):
    comment = CKEditorField("Comments", validators=[DataRequired()])
    submit = SubmitField(label='Submit Comment')

class RegisterForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email("Please enter a valid email")])
    password = PasswordField(label='Password',  validators=[DataRequired()])
    submit = SubmitField(label='Register')
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = b'EPj00jpfj8Gx1SfdgsdsdafjQfnQ9DJYe0Ym'
        csrf_time_limit = timedelta(minutes=20)

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password',  validators=[DataRequired()])
    submit = SubmitField(label='Login')
