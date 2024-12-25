from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length

class ReviewForm(FlaskForm):
    rating = RadioField('Bewertung', 
                       choices=[(5, '★★★★★'), 
                               (4, '★★★★☆'),
                               (3, '★★★☆☆'),
                               (2, '★★☆☆☆'),
                               (1, '★☆☆☆☆')],
                       validators=[DataRequired()],
                       coerce=int)
    comment = TextAreaField('Kommentar',
                          validators=[DataRequired(),
                                    Length(min=10, max=500)])
    submit = SubmitField('Bewertung abschicken')
