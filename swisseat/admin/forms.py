from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class RestaurantUpdateForm(FlaskForm):
    name = StringField('Restaurant Name', 
                      validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Beschreibung')
    address = StringField('Adresse', 
                         validators=[DataRequired(), Length(min=5, max=200)])
    cuisine_type = SelectField('Küche', 
                             choices=[('italienisch', 'Italienisch'),
                                    ('asiatisch', 'Asiatisch'),
                                    ('amerikanisch', 'Amerikanisch'),
                                    ('indisch', 'Indisch'),
                                    ('schweizerisch', 'Schweizerisch')])
    delivery_time = IntegerField('Lieferzeit (Minuten)', 
                               validators=[DataRequired(), NumberRange(min=1, max=120)])
    minimum_order = FloatField('Mindestbestellwert', 
                             validators=[DataRequired(), NumberRange(min=0)])
    delivery_fee = FloatField('Liefergebühr', 
                            validators=[DataRequired(), NumberRange(min=0)])
    accepts_cash = BooleanField('Barzahlung bei Lieferung')
    accepts_twint = BooleanField('TWINT')
    accepts_paypal = BooleanField('PayPal')
    submit = SubmitField('Aktualisieren')

class MenuItemForm(FlaskForm):
    name = StringField('Name', 
                      validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Beschreibung')
    price = FloatField('Preis', 
                      validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Kategorie',
                         choices=[('vorspeisen', 'Vorspeisen'),
                                ('hauptgerichte', 'Hauptgerichte'),
                                ('desserts', 'Desserts'),
                                ('getranke', 'Getränke')])
    is_available = BooleanField('Verfügbar')
    submit = SubmitField('Speichern')
