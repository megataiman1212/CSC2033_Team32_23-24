from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError


def is_real(form, stock):
    if 0 > stock.data or stock.data > 99999:
        raise ValidationError('Stock must be between 0 and 100000')


def validate_category(form, category):
    if category.data != "food" and category.data != "hygiene":
        raise ValidationError('category must be "food" or "hygiene"')


class ProductForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    stock = IntegerField(validators=[DataRequired(),
                                     is_real])
    category = StringField(validators=[DataRequired(),
                                       validate_category])
    required_stock = IntegerField(validators=[DataRequired(),
                                              is_real])
    submit = SubmitField()
