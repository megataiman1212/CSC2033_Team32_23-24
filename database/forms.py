# File written by Daniel E, Asha
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, ValidationError


def is_real(form, number):
    # Check if a number is within a specified range (0 to 99,999)
    if number.data < 0 or number.data > 99999:
        raise ValidationError('Number must be between 0 and 100000')


def validate_category(form, category):
    # Check if a category is either "food" or "hygiene"
    if category.data.lower() != "food" and category.data.lower() != "hygiene":
        raise ValidationError('category must be "food" or "hygiene"')


class ProductForm(FlaskForm):
    """
    Creates product form
    """
    name = StringField(validators=[InputRequired()])
    stock = IntegerField(validators=[InputRequired(),
                                     is_real])
    category = StringField(validators=[InputRequired(),
                                       validate_category])
    required_stock = IntegerField(validators=[InputRequired(),
                                              is_real])
    submit = SubmitField()


class RequiredStockForm(FlaskForm):
    """
    Creates required stock form
    """
    new_level = IntegerField(validators=[InputRequired(), is_real])
    submit = SubmitField()
