import os
from flask import Flask
from flask import render_template
from flask import session, redirect,url_for,flash

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.script import Shell
from flask.ext.migrate import Migrate,MigrateCommand
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.mail import Message
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'keeporder@163.com'
app.config['MAIL_PASSWORD'] = 'Aa1234567'

manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
mail = Mail(app)
manager.add_command('db',MigrateCommand)

class NameForm(Form):
	name = StringField("What is your name?", validators=[Required()] )
	submt = SubmitField('submt')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

def make_shell_context():
	return dict(app=app,db=db,User=User,Role=Role)
manager.add_command("shell",Shell(make_context=make_shell_context))

def send_async_email(app,msg):
	with app.app_context():
		mail.send(msg)

app.config['FLASKY_MAIL_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <zi.long-1986@163.com>'
app.config['FLASKY_ADMIN'] = 'li.dinglong@163.com'
def send_mail(to,subject,template,**kwargs):
	msg = Message(app.config['FLASKY_MAIL_PREFIX'] + subject,
		sender=app.config['MAIL_USERNAME'], recipients=[to])
	msg.body = render_template(template + '.txt',**kwargs )
	msg.html = render_template(template + '.html',**kwargs )
	thr = Thread(target=send_async_email,args=[app, msg])
	thr.start()
	return thr
#如果发送大量邮件，可以用send_async_email发给Celery任务队列

@app.route('/',methods=['GET','Post'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username = form.name.data)
			db.session.add(user)
			session['known'] = False
			if app.config['FLASKY_ADMIN']:
				send_mail(app.config['FLASKY_ADMIN'],'New User', 'mail/user',user=user)
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html',form = form, name = session.get('name'),
		known = session.get('known', False) )

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

@app.errorhandler(500)
def internal_err(e):
	return render_template('500.html'),500


if __name__ == '__main__':
	manager.run()