from flask import render_template, session, redirect, url_for, current_app
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_mail


@main.route('/', methods=['GET', 'Post'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user_db = User.query.filter_by(username=form.name.data).first()
		if user_db is None:
			user_form = User(username=form.name.data)
			db.session.add(user_form)
			session['known'] = False
			if current_app.config['FLASKY_ADMIN']:
				send_mail(current_app.config['FLASKY_ADMIN'], 'New User', 'mail/user', user=user)
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('.index'))
	return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))


@main.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)
