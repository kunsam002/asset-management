__author__ = 'stikks & kunsam002'
from flask_wtf import Form
from wtforms import Field, TextField, PasswordField, StringField, FieldList, FormField, \
    DateTimeField, DateField, BooleanField, DecimalField, validators, HiddenField, FloatField, \
    IntegerField, TextAreaField, SelectField, RadioField, SelectMultipleField, FileField
from wtforms.validators import DataRequired, Optional, Email, EqualTo, ValidationError
from datetime import datetime, date
from flask_wtf.html5 import EmailField


class LoginForm(Form):
    username = TextField('Username or Email Address', validators = [DataRequired()], description = "Please enter a registered username or email")
    password = PasswordField('Password', validators = [DataRequired()], description = "Please enter your valid password")
    

class SignupForm(Form):
    full_name = StringField('Your Full Name', validators=[DataRequired()])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    verify_password = PasswordField('Verify Password', validators=[DataRequired(), EqualTo('password')])
    merchant_request = BooleanField('I also want to be a merchant', validators=[Optional()])
    terms = BooleanField('Terms and conditions', validators=[DataRequired()])


class AddressForm(Form):
    phone = StringField('Phone', validators=[DataRequired()])
    line1 = StringField('Address', validators=[DataRequired()])
    line2 = StringField('Landmark')
    city_id = SelectField('City', coerce=int, validators=[DataRequired()])
    state_id = SelectField('State', coerce=int, validators=[DataRequired()])
    country_id = SelectField('Country', coerce=int, validators=[DataRequired()])
    longitude = StringField('Longitude', validators=[Optional()])
    latitude = StringField('Latitude', validators=[Optional()])


class DeviceForm(Form):
    reference_id = StringField('Reference ID', validators=[DataRequired()])
    meter_reference_id = StringField('Meter Reference ID', validators=[DataRequired()])
    utitlity_provider_id = SelectField('Utility Provider', validators=[DataRequired()])
    is_master = BooleanField('Master', default=False)
    is_slave = BooleanField('Slave', default=False)
    consumer_id = SelectField('Consumer', validators=[Optional()])
    transformer_id = SelectField('Transformer', validators=[Optional()])


class TransformerForm(Form):
    model_number = StringField('Model Number', validators=[DataRequired()])
    capacity = FloatField('Capacity', validators=[DataRequired()])


class TempeartureReadingForm(Form):
    degree = FloatField('Degree', validators=[DataRequired()])
    humidity = FloatField('Humidity', validators=[Optional()])
    device_code = StringField('Device Reference', validators=[DataRequired()])


class UtilityProvider(Form):
    name = StringField('Name', validators=[DataRequired()])
    url = StringField('Url', validators=[DataRequired()])

