from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login_manager

#
# user Model
# TODO: extend user Model
#
class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, nullable=False)
	password = db.Column(db.String(128), nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	lastlogin = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __str__(self):
		return self.username

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

#
# relation tables
#

testrun_casesequence = db.Table(
	'testrun_casesequence',
	db.Column('testrun_id', db.Integer, db.ForeignKey('testruns.id'), primary_key=True),
	db.Column('testcase_sequence_id', db.Integer, db.ForeignKey('testcase_sequences.id'), primary_key=True)
)

testcase_sequence_datafile = db.Table(
	'testcase_sequence_datafile',
	db.Column('testcase_sequence_id', db.Integer, db.ForeignKey('testcase_sequences.id'), primary_key=True),
	db.Column('datafile_id', db.Integer, db.ForeignKey('datafiles.id'), primary_key=True)
)

testcase_sequence_case = db.Table(
	'testcase_sequence_case',
	db.Column('testcase_sequence_id', db.Integer, db.ForeignKey('testcase_sequences.id'), primary_key=True),
	db.Column('testcase_id', db.Integer, db.ForeignKey('testcases.id'), primary_key=True)
)

testcase_stepsequence = db.Table(
	'testcase_stepsequence',
	db.Column('testcase_id', db.Integer, db.ForeignKey('testcases.id'), primary_key=True),
	db.Column('teststep_sequence_id', db.Integer, db.ForeignKey('teststep_sequences.id'), primary_key=True)
)


#
# main entities
#
class Testrun(db.Model):
	__tablename__ = 'testruns'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	description = db.Column(db.String(512), nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	edited = db.Column(db.DateTime, nullable=True)
	editor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
	creator = db.relationship('User', backref='created_testruns', lazy='immediate', foreign_keys=[creator_id])
	editor = db.relationship('User', backref='edited_testruns', lazy='immediate', foreign_keys=[editor_id])

	def __str__(self):
		return self.name

	def to_json(self):
		return {
			'TestCaseSequence' : [x.to_json() for x in self.testcase_sequences],
		}

class TestCaseSequence(db.Model):
	__tablename__ = 'testcase_sequences'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	description = db.Column(db.String(512), nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	edited = db.Column(db.DateTime, nullable=True)
	editor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
	classname_id = db.Column(db.Integer, db.ForeignKey('classnames.id'), nullable=False)
	creator = db.relationship('User', backref='created_testcase_sequances', lazy='immediate', foreign_keys=[creator_id])
	editor = db.relationship('User', backref='edited_testcase_sequances', lazy='immediate', foreign_keys=[editor_id])
	classname = db.relationship('ClassName', backref='testcase_sequences', lazy='immediate', foreign_keys=[classname_id])
	testrun = db.relationship(
		'Testrun',
		secondary=testrun_casesequence,
		lazy='subquery',
		backref=db.backref('testcase_sequences', lazy=True),
	)

	def __str__(self):
		return self.name

	def to_json(self):
		if len(self.datafiles) > 0:
			TestDataFileName = self.datafiles[0].filename
		else:
			TestDataFileName = ''
		return {
			'SequenceClass': self.classname.name,
			'TestDataFileName': TestDataFileName,
			'TestCase' : [x.to_json() for x in self.testcases],
		}

class DataFile(db.Model):
	__tablename__ = 'datafiles'
	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(64), nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	creator = db.relationship('User', backref='created_datafiles', lazy='immediate', foreign_keys=[creator_id])
	testcase_sequence = db.relationship(
		'TestCaseSequence',
		secondary=testcase_sequence_datafile,
		lazy='subquery',
		backref=db.backref('datafiles', lazy=True),
	)

	def __str__(self):
		return self.filename

class TestCase(db.Model):
	__tablename__ = 'testcases'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	description = db.Column(db.String(512), nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	edited = db.Column(db.DateTime, nullable=True)
	editor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
	classname_id = db.Column(db.Integer, db.ForeignKey('classnames.id'), nullable=False)
	browser_type_id = db.Column(db.Integer, db.ForeignKey('browser_types.id'), nullable=False)
	testcase_type_id = db.Column(db.Integer, db.ForeignKey('testcase_types.id'), nullable=False)
	creator = db.relationship('User', backref='created_testcases', lazy='immediate', foreign_keys=[creator_id])
	editor = db.relationship('User', backref='edited_testcases', lazy='immediate', foreign_keys=[editor_id])
	classname = db.relationship('ClassName', backref='testcases', lazy='immediate', foreign_keys=[classname_id])
	browser_type = db.relationship('BrowserType', backref='testcases', lazy='immediate', foreign_keys=[browser_type_id])
	testcase_type = db.relationship('TestCaseType', backref='testcases', lazy='immediate', foreign_keys=[testcase_type_id])
	testcase_sequence = db.relationship(
		'TestCaseSequence',
		secondary=testcase_sequence_case,
		lazy='subquery',
		backref=db.backref('testcases', lazy=True),
	)

	def __str__(self):
		return self.name

	def to_json(self):
		return {
			'TestCaseClass': self.classname.name,
			'TestCaseType': self.testcase_type.name,
			'Browser': self.browser_type.name,
			'TestStepSequences' : [x.to_json() for x in self.teststep_sequences],
		}

class TestStepSequence(db.Model):
	__tablename__ = 'teststep_sequences'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	description = db.Column(db.String(512), nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	edited = db.Column(db.DateTime, nullable=True)
	editor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
	classname_id = db.Column(db.Integer, db.ForeignKey('classnames.id'), nullable=False)
	creator = db.relationship('User', backref='created_teststep_sequences', lazy='immediate', foreign_keys=[creator_id])
	editor = db.relationship('User', backref='edited_teststep_sequences', lazy='immediate', foreign_keys=[editor_id])
	classname = db.relationship('ClassName', backref='teststep_sequences', lazy='immediate', foreign_keys=[classname_id])
	testcase = db.relationship(
		'TestCase',
		secondary=testcase_stepsequence,
		lazy='subquery',
		backref=db.backref('teststep_sequences', lazy=True),
	)

	def __str__(self):
		return self.name

	def to_json(self):
		return {
			'TestStepClass': self.classname.name,
			'TestSteps' : [x.to_json() for x in self.teststeps],
		}

class TestStepExecution(db.Model):
	__tablename__ = 'teststep_executions'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	description = db.Column(db.String(512), nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	edited = db.Column(db.DateTime, nullable=True)
	editor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
	activity_type_id = db.Column(db.Integer, db.ForeignKey('activity_types.id'), nullable=False)
	locator_type_id = db.Column(db.Integer, db.ForeignKey('locator_types.id'), nullable=False)
	teststep_sequence_id = db.Column(db.Integer, db.ForeignKey('teststep_sequences.id'), nullable=True)
	creator = db.relationship('User', backref='created_teststeps', lazy='immediate', foreign_keys=[creator_id])
	editor = db.relationship('User', backref='edited_teststeps', lazy='immediate', foreign_keys=[editor_id])
	activity_type = db.relationship('ActivityType', backref='teststeps', lazy='immediate', foreign_keys=[activity_type_id])
	locator_type = db.relationship('LocatorType', backref='teststeps', lazy='immediate', foreign_keys=[locator_type_id])
	teststep_sequence = db.relationship('TestStepSequence', backref='teststeps', lazy='immediate', foreign_keys=[teststep_sequence_id])
	# model extension
	locator = db.Column(db.String, nullable=True)
	optional = db.Column(db.Boolean, nullable=False, default=False)
	timeout = db.Column(db.Float(precision='5,2'), nullable=True)
	release = db.Column(db.String, nullable=True)
	value = db.Column(db.String, nullable=True)
	value2 = db.Column(db.String, nullable=True)
	comparision = db.Column(db.String, nullable=True)

	def __str__(self):
		return self.name

	def to_json(self):
		return {
			'Activity': self.activity_type.name,
			'LocatorType': self.locator_type.name,
			'Locator': self.locator,
			'Value': self.value,
			'Comparison': self.comparision,
			'Value2': self.value2,
			'Timeout': self.timeout,
			'Optional': self.optional,
			'Release': self.release,
		}

#
# supporting entities
#
class GlobalTestStepExecution(db.Model):
	__tablename__ = 'global_teststep_executions'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	description = db.Column(db.String(512), nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	edited = db.Column(db.DateTime, nullable=True)
	editor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
	activity_type_id = db.Column(db.Integer, db.ForeignKey('activity_types.id'), nullable=False)
	locator_type_id = db.Column(db.Integer, db.ForeignKey('locator_types.id'), nullable=False)
	teststep_sequence_id = db.Column(db.Integer, db.ForeignKey('teststep_sequences.id'), nullable=True)
	creator = db.relationship('User', backref='created_global_teststeps', lazy='immediate', foreign_keys=[creator_id])
	editor = db.relationship('User', backref='edited_global_teststeps', lazy='immediate', foreign_keys=[editor_id])
	activity_type = db.relationship('ActivityType', backref='global_teststeps', lazy='immediate', foreign_keys=[activity_type_id])
	locator_type = db.relationship('LocatorType', backref='global_teststeps', lazy='immediate', foreign_keys=[locator_type_id])
	teststep_sequence = db.relationship('TestStepSequence', backref='global_teststeps', lazy='immediate', foreign_keys=[teststep_sequence_id])
	
	def __str__(self):
		return self.name

class ClassName(db.Model):
	__tablename__ = 'classnames'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	description = db.Column(db.String(512), nullable=False)

	def __str__(self):
		return self.name

class BrowserType(db.Model):
	__tablename__ = 'browser_types'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	description = db.Column(db.String(512), nullable=False)

	def __str__(self):
		return self.name
	
class TestCaseType(db.Model):
	__tablename__ = 'testcase_types'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	description = db.Column(db.String(512), nullable=False)

	def __str__(self):
		return self.name

class ActivityType(db.Model):
	__tablename__ = 'activity_types'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	description = db.Column(db.String(512), nullable=False)

	def __str__(self):
		return self.name

class LocatorType(db.Model):
	__tablename__ = 'locator_types'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	description = db.Column(db.String(512), nullable=False)

	def __str__(self):
		return self.name
