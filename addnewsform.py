from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, optional


class NewsForm(Form):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    picture = FileField("Приложите картинку")
    submit = SubmitField('Добавить')

    def __init__(self, edit=None):
        super().__init__()
        try:
            self.title.label = edit[1]
            self.title.validators = [optional()]
            self.content.label = edit[2]
            self.content.validators = [optional()]
        except:
            pass
