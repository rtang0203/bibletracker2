# app/groups/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from ..models import Group

class CreateGroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    is_data_public = BooleanField('Make reading data visible to all members')
    submit = SubmitField('Create Group')

class JoinGroupForm(FlaskForm):
    group_code = StringField('Group Code', validators=[DataRequired(), Length(min=8, max=8)])
    submit = SubmitField('Join Group')

    def validate_group_code(self, group_code):
        group = Group.query.filter_by(group_code=group_code.data.upper()).first()
        if not group:
            raise ValidationError('Invalid group code. Please check and try again.')