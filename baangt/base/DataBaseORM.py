from sqlalchemy import Column, String, Integer, DateTime, Boolean, Table, ForeignKey 
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'sqlite:///testrun.db'

engine = create_engine(DATABASE_URL)
base = declarative_base()


#
# Testrun models
#

class TestrunLog(base):
	#
	# summary on Testrun results 
	#
	__tablename__ = "testruns"
	# columns
	id = Column(Integer, primary_key=True)
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
	testrun_id = Column(Integer, ForeignKey('testruns.id'), nullable=False)
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
	id = Column(Integer, primary_key=True)
	testrun_id = Column(Integer, ForeignKey('testruns.id'), nullable=False)
	# relationships
	testrun = relationship('TestrunLog', foreign_keys=[testrun_id])
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
	id = Column(Integer, primary_key=True)
	testcase_sequence_id = Column(Integer, ForeignKey('testCaseSequences.id'), nullable=False)
	# relationships
	testcase_sequence = relationship('TestCaseSequenceLog', foreign_keys=[testcase_sequence_id])
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
	testcase_id = Column(Integer, ForeignKey('testCases.id'), nullable=False)
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
	testcase_id = Column(Integer, ForeignKey('testCases.id'), nullable=True)
	# relationships
	testcase = relationship('TestCaseLog', foreign_keys=[testcase_id])




# create tables
#if __name__ == '__main__':
base.metadata.create_all(engine)