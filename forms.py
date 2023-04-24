from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, URL, Email
from flask_ckeditor import CKEditorField

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
    email = StringField(label='Email', validators=[DataRequired(), Email("Please enter a valid email address")])
    password = PasswordField(label='Password',  validators=[DataRequired()])
    submit = SubmitField(label='Register')

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email("Please enter a valid email address")])
    password = PasswordField(label='Password',  validators=[DataRequired()])
    submit = SubmitField(label='Login')
