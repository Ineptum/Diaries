from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(message='Поле не должно быть пустым')])
    password = PasswordField('Введите пароль', [DataRequired(message='Поле не должно быть пустым'),
                                                EqualTo('confirm', message='Пароли должны совпадать')])
    confirm = PasswordField('Повторите пароль', validators=[DataRequired(message='Поле не должно быть пустым')])
    submit = SubmitField('Зарегистрироваться')
