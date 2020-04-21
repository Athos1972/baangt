from sqlalchemy import Column, String, Integer, DateTime, Boolean, Table, ForeignKey, LargeBinary
#from sqlalchemy.types import Binary, TypeDecorator
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from uuid import uuid4

DATABASE_URL = os.getenv('BAANGT_RESULTS_DATABASE_URL') or 'sqlite:///testrun.db'

engine = create_engine(DATABASE_URL)
base = declarative_base()

#
# UUID as bytes
#
def getUuidBytes():
	return uuid4().bytes

#
# Testrun models
#

class TestrunLog(base):
	#
	# summary on Testrun results 
	#
	__tablename__ = "testruns"
	# columns
	uuid = Column(LargeBinary, primary_key=True, default=getUuidBytes)
	testrunName = Column(String, nullable=False)
	logfileName = Column(String, nullable=False)
	startTime = Column(DateTime, nullable=False)
	endTime = Column(DateTime, nullable=False)
	#globalVars = Column(String, nullable=True)
	dataFile = Column(String, nullable=True)
	statusOk = Column(Integer, nullable=False)
	statusFailed = Column(Integer, nullable=False)
	statusPaused = Column(Integer, nullable=False)
	# relationships
	globalVars = relationship('GlobalAttribute')
	testcase_sequences = relationship('TestCaseSequenceLog')


class GlobalAttribute(base):
	#
	# global vars
	#
	__tablename__ = 'globals'
	# columns
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	value = Column(String, nullable=True)
	testrun_uuid = Column(LargeBinary, ForeignKey('testruns.uuid'), nullable=False)
	# relationships
	testrun = relationship('TestrunLog', foreign_keys=[testrun_uuid])


#
# Test Case Sequence models
#

class TestCaseSequenceLog(base):
	#
	# TestCase Sequence
	#

	__tablename__ = 'testCaseSequences'
	# columns
	uuid = Column(LargeBinary, primary_key=True, default=getUuidBytes)
	testrun_uuid = Column(LargeBinary, ForeignKey('testruns.uuid'), nullable=False)
	# relationships
	testrun = relationship('TestrunLog', foreign_keys=[testrun_uuid])
	testcases = relationship('TestCaseLog')


#
# Test Case models
#

class TestCaseLog(base):
	#
	# TestCase results
	#
	__tablename__ = 'testCases'
	# columns
	uuid = Column(LargeBinary, primary_key=True, default=getUuidBytes)
	testcase_sequence_uuid = Column(LargeBinary, ForeignKey('testCaseSequences.uuid'), nullable=False)
	# relationships
	testcase_sequence = relationship('TestCaseSequenceLog', foreign_keys=[testcase_sequence_uuid])
	fields = relationship('TestCaseField')
	networkInfo = relationship('TestCaseNetworkInfo')


class TestCaseField(base):
	#
	# field for a TestCase results 
	#
	__tablename__ = 'testCaseFields'
	# columns
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	value = Column(String, nullable=True)
	testcase_uuid = Column(LargeBinary, ForeignKey('testCases.uuid'), nullable=False)
	# relationships
	testcase = relationship('TestCaseLog', foreign_keys=[testcase_uuid])

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
	testcase_uuid = Column(LargeBinary, ForeignKey('testCases.uuid'), nullable=True)
	# relationships
	testcase = relationship('TestCaseLog', foreign_keys=[testcase_uuid])




# create tables
#if __name__ == '__main__':
base.metadata.create_all(engine)