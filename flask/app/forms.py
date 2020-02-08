from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SelectMultipleField, SelectField
from wtforms.widgets import TextArea, ListWidget, CheckboxInput
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User
from app import utils

#
# fields
#

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


#
# authantication forms
#

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

#
# testrun items forms
#

class TestrunCreateForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()], widget=TextArea())
	testcase_sequences = SelectMultipleField('Test Case Sequences', option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))

	@classmethod
	def new(cls):
		# update choices
		form = cls()
		form.testcase_sequences.choices = utils.getTestCaseSequences()
		return form


class TestCaseSequenceCreateForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()], widget=TextArea())
	classname = SelectField('Class Name')
	datafiles = SelectMultipleField('Data Files')
	testcases = SelectMultipleField('Test Cases')

	@classmethod
	def new(cls):
		# update choices
		form = cls()
		form.classname.choices = utils.getClassNames()
		form.datafiles.choices = utils.getDataFiles()
		form.testcases.choices = utils.getTestCases()
		return form


class TestCaseCreateForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()], widget=TextArea())
	classname = SelectField('Class Name')
	browser_type = SelectField('Browser Type')
	testcase_type = SelectField('Test Case Type')
	testcase_stepsequences = SelectMultipleField('Step Sequences')

	@classmethod
	def new(cls):
		# update choices
		form = cls()
		form.classname.choices = utils.getClassNames()
		form.browser_type.choices = utils.getBrowserTypes()
		form.testcase_type.choices = utils.getTestCaseTypes()
		form.testcase_stepsequences.choices = utils.getTestStepSequences()
		return form


class TestStepSequenceCreateForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()], widget=TextArea())
	classname = SelectField('Class Name')
	teststeps = SelectMultipleField('Test Steps')

	@classmethod
	def new(cls):
		# update choices
		form = cls()
		form.classname.choices = utils.getClassNames()
		form.teststeps.choices = utils.getTestSteps()
		return form


class TestStepCreateForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()], widget=TextArea())
	activity_type = SelectField('Activity Type')
	locator_type = SelectField('Locator Type')

	@classmethod
	def new(cls):
		# update choices
		form = cls()
		form.activity_type.choices = utils.getActivityTypes()
		form.locator_type.choices = utils.getLocatorTypes()
		return form
	