from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

	def validate_username(self, username):
		if User.query.filter_by(username=username.data).count() == 0:
			raise ValidationError('Wrong username')

	def validate_password(self, password):
		user = User.query.filter_by(username=self.username.data).first()
		if user and not user.verify_password(password.data):
			raise ValidationError('Wrong password')


class SingupForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Password again', validators=[DataRequired(), EqualTo('password')])

	def validate_username(self, username):
		if User.query.filter_by(username=username.data).count() > 0:
			raise ValidationError('This username is in use. Please try another username.')