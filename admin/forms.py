from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class RegisterForm (FlaskForm):
    email = StringField(validators= [DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()