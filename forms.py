from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.fields.html5 import URLField, EmailField


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = URLField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UserEditForm(FlaskForm):
    """Form for editing user."""

    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()])
    image_url = URLField('(Optional) Image URL')
    header_image_url = URLField('(Optional) Header Image URL')
    bio = StringField('Bio', validators=[Optional()])
    password = PasswordField('Password', validators=[Length(min=6)])
