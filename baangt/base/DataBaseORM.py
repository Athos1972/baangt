from sqlalchemy import Column, String, Integer, DateTime, Boolean, Table, ForeignKey 
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'testrun.db'

engine = create_engine(f'sqlite:///{DATABASE_URL}')
base = declarative_base()

#
# declare realtion classes
#
class TestrunToTestcase(base):
	__tablename__ = 'testrun_testcase'
	testrunLog_id = Column(Integer, ForeignKey('testrunLog.id'), primary_key=True)
	testcase_id = Column(Integer, ForeignKey('testCaseLog.id'), primary_key=True)

class TestcaseToExtra(base):
	__tablename__ = 'testcase_extras'
	testcase_id = Column(Integer, ForeignKey('testCaseLog.id'), primary_key=True)
	extrafield_id = Column(Integer, ForeignKey('extraFields.id'), primary_key=True)

#
# declare models
#
class TestrunLog(base):
	__tablename__ = "testrunLog"
	id = Column(Integer, primary_key=True)
	testrunName = Column(String, nullable=False)
	logfileName = Column(String, nullable=False)
	startTime = Column(DateTime, nullable=False)
	endTime = Column(DateTime, nullable=False)
	globalVars = Column(String, nullable=True)
	dataFile = Column(String, nullable=True)
	statusOk = Column(Integer, nullable=False)
	statusFailed = Column(Integer, nullable=False)
	statusPaused = Column(Integer, nullable=False)
	testcases = relationship('TestCaseLog', secondary='TestrunToTestcase')

class TestCaseLog(base):
	__tablename__ = 'testCaseLog'
	id = Column(Integer, primary_key=True)
	toasts = Column(String, nullable=True)
	tcErrorLog =Column(String, nullable=True)
	vigogf = Column(String, nullable=True)
	sapPolizzennr =Column(String, nullable=True)
	pramie = Column(String, nullable=True)
	polNrHost = Column(String, nullable=True)
	testCaseStatus = Column(String, nullable=True)
	duration = Column(String, nullable=True)
	screenshots = Column(String, nullable=True)
	timelog = Column(String, nullable=True)
	exportFilesBasePath = Column(String, nullable=True)
	tcLines = Column(String, nullable=True)
	tcDontCloseBrowser = Column(Boolean, nullable=True)
	tcBrowserAttributes = Column(String, nullable=True)
	tcSlowExecution = Column(Boolean, nullable=True)
	tcNetworkInfo = Column(Boolean, nullable=True)
	txDebug = Column(Boolean, nullable=True)
	screenshotPath = Column(String, nullable=True)
	exportPath = Column(String, nullable=True)
	importPath = Column(String, nullable=True)
	rootPath = Column(String, nullable=True)
	testrun = relationship('TestrunLog', secondary='TestrunToTestcase')
	extraFields = relationship('ExtraField', secondary='TestcaseToExtra')

class ExtraField(base):
	__tablename__ = 'extraFields'
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	value = Column(String, nullable=True)
	testcase = relationship('TestCaseLog', secondary='TestcaseToExtra')


# create tables
base.metadata.create_all(engine)