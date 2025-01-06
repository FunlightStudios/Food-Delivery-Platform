from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from swisseat.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Benutzername',
                         validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-Mail',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    confirm_password = PasswordField('Passwort bestätigen',
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Dieser Benutzername ist bereits vergeben.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Diese E-Mail-Adresse wird bereits verwendet.')

class RestaurantRegistrationForm(FlaskForm):
    username = StringField('Benutzername',
                         validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-Mail',
                       validators=[DataRequired(), Email()])
    phone = StringField('Telefon',
                       validators=[DataRequired(), Length(min=12, max=12)])
    address = StringField('Adresse',
                       validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField('Passwort', validators=[DataRequired()])
    confirm_password = PasswordField('Passwort bestätigen',
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Als Restaurant registrieren')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Dieser Benutzername ist bereits vergeben.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Diese E-Mail-Adresse wird bereits verwendet.')

class LoginForm(FlaskForm):
    email = StringField('E-Mail',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember = BooleanField('Angemeldet bleiben')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Benutzername',
                         validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-Mail',
                       validators=[DataRequired(), Email()])
    street = StringField('Straße')
    city = StringField('Stadt')
    zipcode = StringField('PLZ')
    country = StringField('Land')
    phone = StringField('Telefon')
    submit = SubmitField('Aktualisieren')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Dieser Benutzername ist bereits vergeben.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Diese E-Mail-Adresse wird bereits verwendet.')
