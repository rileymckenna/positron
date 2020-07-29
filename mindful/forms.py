from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from mindful.models import User

class CheckIn(FlaskForm):
    text = TextAreaField(label="Share something positive.")
    mood0 = SubmitField(label='🙂')
    mood1 = SubmitField(label='😐')
    mood2 = SubmitField(label='☹️')