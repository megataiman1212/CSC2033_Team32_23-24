from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, ValidationError, Length, EqualTo, DataRequired
import re


# Checks for not allowed characters
def character_check(form, field):
    excluded_chars = "*?!'^+%&/()=}][{$#@<>"

    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed")


# Checks for if the phone number is in the correct format
def validate_phone(self, phone):
    p = re.compile("[0-9]{4}\-[0-9]{3}\-[0-9]{4}")
    if not p.match(phone.data):
        raise ValidationError("Phone number must be in the format XXXX-XXX-XXXX")


# Looks for a digit in the password
def validate_digit(self, field):
    count = 0
    digits = "0123456789"
    for char in field.data:
        if char in digits:
            count = count + 1
    if count == 0:
        raise ValidationError("Password must contain a digit")


# Checks for a lowercase letter in the password
def lowercase_check(form, field):
    lowercase_valid = False
    for char in field.data:
        if char.islower():
            lowercase_valid = True
    if not lowercase_valid:
        raise ValidationError("Password must contain a lowercase letter")


# Check for an uppercase letter in the password
def uppercase_check(form, field):
    uppercase_valid = False
    for char in field.data:
        if char.isupper():
            uppercase_valid = True
    if not uppercase_valid:
        raise ValidationError("Password must contain an uppercase letter")


# Checks for a special character in the password
def special_character_check(self, password):
    p = re.compile(r'(?=.*\W)')
    if not p.match(password.data):
        raise ValidationError("Password must contain a special character")


# Checks the date of birth is in the correct format
def validate_DOB(self, DOB):
    p = re.compile("^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)\d{2}$")
    if not p.match(DOB.data):
        raise ValidationError("DOB must be in the format DD/MM/YYYY, and have appropriate digits")


# Checks if the postcode is in the correct format
def validate_postcode(self, postcode):
    validated = False
    p1 = re.compile("[A-Z]{1}[0-9]{1}\s[0-9]{1}[A-Z]{2}")
    p2 = re.compile("[A-Z]{1}[0-9]{2}\s[0-9]{1}[A-Z]{2}")
    p3 = re.compile("[A-Z]{2}[0-9]{1}\s[0-9]{1}[A-Z]{2}")
    if p1.match(postcode.data):
        validated = True
    if p2.match(postcode.data):
        validated = True
    if p3.match(postcode.data):
        validated = True
    if not validated:
        raise ValidationError("Postcode must be in one of these formats: D7 8SG, D78 8SG, DL7 8SG")


# Checks the pin is in the correct format
def validate_pin(self, pin):
    p = re.compile("[0-9]{6}")
    if not p.match(pin.data):
        raise ValidationError("Pin is 6 digits long")


# The register form with validators
class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    postcode = StringField(validators=[validate_postcode, DataRequired()])
    pin = StringField(validators=[DataRequired(), validate_pin])
    submit = SubmitField()
