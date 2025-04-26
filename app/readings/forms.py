# app/readings/forms.py
from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired

class DailyReadingForm(FlaskForm):
    has_read = BooleanField('I read my Bible today')
    submit = SubmitField('Save')

# Minimal form for CSRF protection on actions without fields
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit') # A submit field is often expected, even if not rendered