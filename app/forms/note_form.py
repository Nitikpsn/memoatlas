from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    subject = StringField('Subject', validators=[Length(max=100)])
    tags = StringField('Tags (comma-separated)')
    submit = SubmitField('Save Note')
