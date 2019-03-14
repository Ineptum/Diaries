from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from werkzeug.datastructures import MultiDict



class NewsForm(FlaskForm):
	title = StringField('Заголовок новости', validators=[DataRequired()])
	content = TextAreaField('Текст новости', validators=[DataRequired()])
	submit = SubmitField('Добавить')
	def __init__(self, edit=None):
		super().__init__()
		try:
			self.title.label = edit[1]
			self.content.label = edit[2]
		except:
			pass
	