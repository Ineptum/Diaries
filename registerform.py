from flask_wtf import FlaskForm
from flask import Flask, render_template, url_for
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(message='Поле не должно быть пустым')])
    password = PasswordField('Введите пароль', [DataRequired(message='Поле не должно быть пустым'),
        EqualTo('confirm', message='Пароли должны совпадать')])
    confirm = PasswordField('Повторите пароль', validators=[DataRequired(message='Поле не должно быть пустым')])
    submit = SubmitField('Зарегистрироваться')