from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from application import db


#
# user Model
# TODO: extend user Model
#
class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, nullable=False)

	def __str__(self):
		return self.username

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
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.now())
	createdBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	edited = db.Column(db.DateTime, nullable=True)
	editedBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

	def get_createdBy(self):
		print(f'id = {self.createdBy}')
		user = User.query.get(self.createdBy)
		print(f'user: {user}')
		return user

class TestCaseSequence(db.Model):
	__tablename__ = 'testcase_sequences'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.now())
	createdBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	edited = db.Column(db.DateTime, nullable=True)
	editedBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
	className = db.Column(db.Integer, db.ForeignKey('classnames.id'), nullable=True)
	testrun = db.relationship(
		'Testrun',
		secondary=testrun_casesequence,
		lazy='subquery',
		backref=db.backref('testcase_sequences', lazy=True),
	)

class DataFile(db.Model):
	__tablename__ = 'datafiles'
	id = db.Column(db.Integer, primary_key=True)
	fileName = db.Column(db.String, nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.now())
	createdBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	testcase_sequence = db.relationship(
		'TestCaseSequence',
		secondary=testcase_sequence_datafile,
		lazy='subquery',
		backref=db.backref('datafiles', lazy=True),
	)

class TestCase(db.Model):
	__tablename__ = 'testcases'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.now())
	createdBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	edited = db.Column(db.DateTime, nullable=True)
	editedBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
	className = db.Column(db.Integer, db.ForeignKey('classnames.id'), nullable=False)
	browserType = db.Column(db.Integer, db.ForeignKey('browser_types.id'), nullable=False)
	testCaseType = db.Column(db.Integer, db.ForeignKey('testcase_types.id'), nullable=False)
	testcase_sequence = db.relationship(
		'TestCaseSequence',
		secondary=testcase_sequence_case,
		lazy='subquery',
		backref=db.backref('testcases', lazy=True),
	)

class TestStepSequence(db.Model):
	__tablename__ = 'teststep_sequences'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.now())
	createdBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	edited = db.Column(db.DateTime, nullable=True)
	editedBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
	className = db.Column(db.Integer, db.ForeignKey('classnames.id'), nullable=False)
	testcase = db.relationship(
		'TestCase',
		secondary=testcase_stepsequence,
		lazy='subquery',
		backref=db.backref('teststep_sequences', lazy=True),
	)

class TestStepExecution(db.Model):
	__tablename__ = 'teststep_executions'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.now())
	createdBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	edited = db.Column(db.DateTime, nullable=True)
	editedBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
	activityType = db.Column(db.Integer, db.ForeignKey('activity_types.id'), nullable=False)
	locatorType = db.Column(db.Integer, db.ForeignKey('locator_types.id'), nullable=False)
	testStepSequence = db.Column(db.Integer, db.ForeignKey('teststep_sequences.id'), nullable=False)

#
# supporting entities
#
class GlobalTestStepExecution(db.Model):
	__tablename__ = 'global_teststep_executions'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.now())
	createdBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	edited = db.Column(db.DateTime, nullable=True)
	editedBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
	activityType = db.Column(db.Integer, db.ForeignKey('activity_types.id'), nullable=False)
	locatorType = db.Column(db.Integer, db.ForeignKey('locator_types.id'), nullable=False)
	testStepSequence = db.Column(db.Integer, db.ForeignKey('teststep_sequences.id'), nullable=False)

class ClassName(db.Model):
	__tablename__ = 'classnames'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)

class BrowserType(db.Model):
	__tablename__ = 'browser_types'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	
class TestCaseType(db.Model):
	__tablename__ = 'testcase_types'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)

class ActivityType(db.Model):
	__tablename__ = 'activity_types'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)

class LocatorType(db.Model):
	__tablename__ = 'locator_types'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)




