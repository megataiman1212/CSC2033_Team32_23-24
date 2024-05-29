#File written by Daniel E, Asha
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, ValidationError


def is_real(form, number):
    if number.data < 0 or number.data > 99999:
        raise ValidationError('Number must be between 0 and 100000')


def validate_category(form, category):
    if category.data.lower != "food" and category.data.lower != "hygiene":
        raise ValidationError('category must be "food" or "hygiene"')


class ProductForm(FlaskForm):
    name = StringField(validators=[InputRequired()])
    stock = IntegerField(validators=[InputRequired(),
                                     is_real])
    category = StringField(validators=[InputRequired(),
                                       validate_category])
    required_stock = IntegerField(validators=[InputRequired(),
                                              is_real])
    submit = SubmitField()


class RequiredStockForm(FlaskForm):
    new_level = IntegerField(validators=[InputRequired(),
                                              is_real])
    submit = SubmitField()
