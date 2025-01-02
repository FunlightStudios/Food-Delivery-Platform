from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, FloatField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange

class RestaurantSearchForm(FlaskForm):
    query = StringField('Suche nach Restaurants oder Gerichten')
    cuisine = SelectField('Küche', choices=[
        ('', 'Alle Küchen'),
        ('italienisch', 'Italienisch'),
        ('asiatisch', 'Asiatisch'),
        ('amerikanisch', 'Amerikanisch'),
        ('indisch', 'Indisch'),
        ('schweizerisch', 'Schweizerisch'),
        ('vegetarisch', 'Vegetarisch'),
        ('vegan', 'Vegan')
    ])
    submit = SubmitField('Suchen')

class RestaurantForm(FlaskForm):
    name = StringField('Restaurant Name', 
                      validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Beschreibung')
    address = StringField('Adresse', 
                         validators=[DataRequired(), Length(min=5, max=200)])
    cuisine_type = SelectField('Küche', 
                             choices=[
                                 ('italienisch', 'Italienisch'),
                                 ('asiatisch', 'Asiatisch'),
                                 ('amerikanisch', 'Amerikanisch'),
                                 ('indisch', 'Indisch'),
                                 ('schweizerisch', 'Schweizerisch'),
                                 ('vegetarisch', 'Vegetarisch'),
                                 ('vegan', 'Vegan',)
                             ],
                             validators=[DataRequired()])
    delivery_time = IntegerField('Lieferzeit (Minuten)', 
                                validators=[DataRequired(), NumberRange(min=1, max=120)])
    minimum_order = FloatField('Mindestbestellwert (CHF)', 
                              validators=[NumberRange(min=0, max=100)])
    delivery_fee = FloatField('Liefergebühr (CHF)', 
                             validators=[NumberRange(min=0, max=50)])
    accepts_cash = BooleanField('Barzahlung akzeptieren')
    accepts_twint = BooleanField('TWINT akzeptieren')
    accepts_paypal = BooleanField('PayPal akzeptieren')
    submit = SubmitField('Restaurant registrieren')

class MenuItemForm(FlaskForm):
    name = StringField('Name', 
                      validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Beschreibung')
    price = FloatField('Preis (CHF)', 
                      validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Kategorie',
                         choices=[
                             ('vorspeisen', 'Vorspeisen'),
                             ('hauptgerichte', 'Hauptgerichte'),
                             ('desserts', 'Desserts'),
                             ('getranke', 'Getränke'),
                             ('beilagen', 'Beilagen')
                         ],
                         validators=[DataRequired()])
    submit = SubmitField('Menüeintrag hinzufügen')
