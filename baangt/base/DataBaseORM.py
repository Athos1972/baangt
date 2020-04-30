from sqlalchemy import Column, String, Integer, DateTime, Boolean, Table, ForeignKey, LargeBinary
#from sqlalchemy.types import Binary, TypeDecorator
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
import uuid
from baangt.base.PathManagement import ManagedPaths

#DATABASE_URL = os.getenv('BAANGT_RESULTS_DATABASE_URL') or 'sqlite:///testrun.db'

#engine = create_engine(DATABASE_URL)
managedPaths = ManagedPaths()
DATABASE_URL = str(managedPaths.derivePathForOSAndInstallationOption().joinpath('testrun.db'))

engine = create_engine(f'sqlite:///{DATABASE_URL}')

base = declarative_base()

#
# UUID as bytes
#
def uuidAsBytes():
	return uuid.uuid4().bytes

#
# Testrun models
#

class TestrunLog(base):
	#
	# summary on Testrun results
	#
	__tablename__ = "testruns"
	# columns
	id = Column(LargeBinary, primary_key=True, default=uuidAsBytes)
	testrunName = Column(String, nullable=False)
	logfileName = Column(String, nullable=False)
	startTime = Column(DateTime, nullable=False)
	endTime = Column(DateTime, nullable=False)
	dataFile = Column(String, nullable=True)
	statusOk = Column(Integer, nullable=False)
	statusFailed = Column(Integer, nullable=False)
	statusPaused = Column(Integer, nullable=False)
	# relationships
	globalVars = relationship('GlobalAttribute')
	testcase_sequences = relationship('TestCaseSequenceLog')

	def __str__(self):
		return str(uuid.UUID(bytes=self.id))

	def to_json(self):
		return {
			'id': str(self),
			'Name': self.testrunName,
			'Summary': {
				'TestRecords': sum((self.statusOk, self.statusPaused, self.statusFailed)),
				'Successful': self.statusOk,
				'Paused': self.statusPaused,
				'Error': self.statusFailed,
				'LogFile': self.logfileName,
				'StartTime': self.startTime.strftime('%H:%M:%S'),
				'EndTime': self.endTime.strftime('%H:%M:%S'),
				'Duration': str(self.endTime - self.startTime),
			},
			'GlobalSettings': {gv.name: gv.value for gv in self.globalVars},
			'TestSequences': [tsq.to_json() for tsq in self.testcase_sequences],
		}



class GlobalAttribute(base):
	#
	# global vars
	#
	__tablename__ = 'globals'
	# columns
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	value = Column(String, nullable=True)
	testrun_id = Column(LargeBinary, ForeignKey('testruns.id'), nullable=False)
	# relationships
	testrun = relationship('TestrunLog', foreign_keys=[testrun_id])


#
# Test Case Sequence models
#

class TestCaseSequenceLog(base):
	#
	# TestCase Sequence
	#

	__tablename__ = 'testCaseSequences'
	# columns
	id = Column(LargeBinary, primary_key=True, default=uuidAsBytes)
	testrun_id = Column(LargeBinary, ForeignKey('testruns.id'), nullable=False)
	# relationships
	testrun = relationship('TestrunLog', foreign_keys=[testrun_id])
	testcases = relationship('TestCaseLog')

	def __str__(self):
		return str(uuid.UUID(bytes=self.id))

	def to_json(self):
		return {
			'id': str(self),
			'TestCases': [tc.to_json() for tc in self.testcases],
		}


#
# Test Case models
#

class TestCaseLog(base):
	#
	# TestCase results
	#
	__tablename__ = 'testCases'
	# columns
	id = Column(LargeBinary, primary_key=True, default=uuidAsBytes)
	testcase_sequence_id = Column(LargeBinary, ForeignKey('testCaseSequences.id'), nullable=False)
	# relationships
	testcase_sequence = relationship('TestCaseSequenceLog', foreign_keys=[testcase_sequence_id])
	fields = relationship('TestCaseField')
	networkInfo = relationship('TestCaseNetworkInfo')

	def __str__(self):
		return str(uuid.UUID(bytes=self.id))

	def to_json(self):
		return {
			'id': str(self),
			'Parameters': {pr.name: pr.value for pr in self.fields},
			'NetworkInfo': [nw.to_json() for nw in self.networkInfo],
		}


class TestCaseField(base):
	#
	# field for a TestCase results
	#
	__tablename__ = 'testCaseFields'
	# columns
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	value = Column(String, nullable=True)
	testcase_id = Column(LargeBinary, ForeignKey('testCases.id'), nullable=False)
	# relationships
	testcase = relationship('TestCaseLog', foreign_keys=[testcase_id])

class TestCaseNetworkInfo(base):
	#
	# network info for a TestCase
	#
	__tablename__ = 'networkInfo'
	# columns
	id = Column(Integer, primary_key=True)
	browserName = Column(String, nullable=True)
	status = Column(Integer, nullable=True)
	method = Column(String, nullable=True)
	url = Column(String, nullable=True)
	contentType = Column(String, nullable=True)
	contentSize = Column(Integer, nullable=True)
	headers = Column(String, nullable=True)
	params = Column(String, nullable=True)
	response = Column(String, nullable=True)
	startDateTime = Column(DateTime, nullable=True)
	duration = Column(Integer, nullable=True)
	testcase_id = Column(LargeBinary, ForeignKey('testCases.id'), nullable=True)
	# relationships
	testcase = relationship('TestCaseLog', foreign_keys=[testcase_id])

	def to_json(self):
		return {
			'BrowserName': self.browserName,
			'Status': self.status,
			'Method': self.method,
			'URL': self.url,
			'ContentType': self.contentType,
			'ContentSize': self.contentSize,
			'Headers': self.headers,
			'Params': self.params,
			'Response': '',#self.response,
			'StartDateTime': str(self.startDateTime),
			'Duration': self.duration,
		}



# create tables
#if __name__ == '__main__':
base.metadata.create_all(engine)