from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddNewsForm(FlaskForm):
    title = StringField('News title', validators=[DataRequired()])
    content = TextAreaField('Text of news', validators=[DataRequired()])
    submit = SubmitField('Add news')
