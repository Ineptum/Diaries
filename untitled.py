import json
import sqlite3
from datetime import datetime
from flask import Flask, session, redirect, request, flash, render_template
from flask_wtf import FlaskForm
from db import DB, UsersModel, NewsModel
from addnewsform import NewsForm
from loginform import LoginForm
from registerform import RegisterForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, PasswordField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
edit = None
db = DB()

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	login_error = ''
	if form.validate_on_submit():
		users = UsersModel(db.get_connection())
		user = users.exists(form.username.data, form.password.data)
		if user[0]:
			session['userid'] = users.get(user[1])[0]
			session['username'] = users.get(user[1])[1]
			session['admin'] = users.get(user[1])[3]
			session['sort'] = 0
			return redirect('/')
		else:
			login_error = 'Неправильный логин или пароль'
	return render_template('login.html', title='Личные дневники', form=form, login_error=login_error)

@app.route('/')
def index():
	if "username" not in session:
		return redirect('/login')
	news = NewsModel(db.get_connection())
	all_news = []
	for i in news.get_all(session['userid'], session['sort']):
		all_news.append({'pub_date': datetime.fromtimestamp(i[4]).strftime('%d.%m.%Y %H:%M'),
						 'title': i[1], 'content': i[2], 'nid': i[0]})
	return render_template('index.html', title='Личные дневники', news=all_news)

@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
	if "username" not in session:
		return redirect('/login')
	news = NewsModel(db.get_connection())
	global edit
	if not edit:
		form = NewsForm()
	else:
		form = NewsForm(news.get(edit))

	if form.validate_on_submit():
		news = NewsModel(db.get_connection())
		news.insert(form.title.data, form.content.data, session['userid'])
		if edit:
			redirect('/delete/{}'.format(edit))
		return redirect('/')
	return render_template('addNews.html', title='Личные дневники', form=form)

@app.route('/delete_news/<nid>')
def delete(nid):
	if "username" not in session:
		return redirect('/login')
	news = NewsModel(db.get_connection())
	news.delete(nid)
	return redirect('/')

@app.route('/edit_news/<nid>')
def editNews(nid):
	if "username" not in session:
		return redirect('/login')
	news = NewsModel(db.get_connection())
	global edit
	edit = nid
	return redirect("/add_news")

@app.route('/registration', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		users = UsersModel(db.get_connection())
		users.insert(form.username.data, form.password.data)
		flash('Вы успешно зарегистрировались', 'success')
		return redirect('/login')
	return render_template('register.html', title='Личные дневники', form=form)

@app.route('/admin')
def admin():
	if "username" not in session or session['admin'] != 1:
		flash('Доступ запрещен', 'danger')
		return redirect('/')
	news, users = NewsModel(db.get_connection()), UsersModel(db.get_connection())
	names, amount = {}, {}
	for n in news.get_all():
		if n[3] in amount:
			amount[n[3]] += 1
		else:
			names[n[3]] = users.get(n[3])[1]
			amount[n[3]] = 1
	return render_template('admin.html', title='Статистика пользователей',
						   amount=amount, names=names)

@app.route('/sort/<sort>')
def sortednews(sort):
	if not "username" in session:
		return redirect('/login')
	session['sort'] = int(sort)
	return redirect('/')

@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('userid', None)
	session.pop('admin', None)
	return redirect('/')


if __name__ == '__main__':
	app.run(port=8079, host='127.0.0.1')
