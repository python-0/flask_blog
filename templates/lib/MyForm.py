from flask.ext.wtf import Form
class NameForm(Form):
	name = StringFiled("What is your name?", validators=[Required()] )
	submt = SubmitField('submt')
