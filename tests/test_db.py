import pytest
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

path_to_db = 'test.db'

#
# fixtures
#

@pytest.fixture(scope='function')
def session_db():
	#
	# creats test session
	#
	from baangt.base.DataBaseORM import base
	engine = create_engine(f'sqlite:///{path_to_db}')#, echo = True)
	base.metadata.create_all(engine)
	Session = sessionmaker(bind=engine)
	session = Session()
	yield session
	session.close()
	base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def tr_log():
	#
	# creates a sample TestrunLog instance
	#
	from baangt.base.DataBaseORM import TestrunLog

	log = TestrunLog(
		testrunName = 'Test Testrun',
		logfileName = 'Test Filename',
		startTime = datetime.strptime('00:00:00', '%H:%M:%S'),
		endTime = datetime.strptime('00:01:00', '%H:%M:%S'),
		statusOk = 1,
		statusFailed = 1,
		statusPaused = 1,
		dataFile = 'Test DataFile name',
	)

	return log

@pytest.fixture(scope='function')
def global_vars():
	#
	# returns presaved global attributes as dict
	#
	with open('examples/globals_grid4.json', 'r') as f:
		return json.load(f)


@pytest.fixture(scope='function')
def results_google():
	#
	# returns presaved Testrun results as dict
	#
	with open('jsons/results_example_googleImages.json', 'r') as f:
		return json.load(f)


#
# Tests
#

def test_testrunlog(session_db, tr_log):
	#
	# creata a TestrunLog instance
	#
	
	session_db.add(tr_log)
	session_db.commit()
	# assertions
	assert len(tr_log.testcases) == 0
	assert len(tr_log.globalVars) == 0

def test_globalvars(session_db, tr_log, global_vars):
	#
	# create a TestrunLog instance with global attributes
	#
	from baangt.base.DataBaseORM import GlobalAttribute

	session_db.add(tr_log)
	for key, value in global_vars.items():
		ga = GlobalAttribute(
			name=key,
			value=str(value),
			testrun=tr_log,
		)
		session_db.add(ga)
	session_db.commit()
	# assertions
	assert len(tr_log.testcases) == 0
	assert len(tr_log.globalVars) == 7



def test_testcaselog(session_db, tr_log):
	#
	# create a TestCaseLog instance
	#
	from baangt.base.DataBaseORM import TestCaseLog

	tc_log = TestCaseLog(testrun=tr_log)
	session_db.add(tr_log)
	session_db.add(tc_log)
	session_db.commit()
	# assertions
	assert len(tr_log.testcases) == 1
	assert len(tc_log.extraFields) == 0

def test_extrafield(session_db, tr_log):
	#
	# create a TestCaseExtraField instance
	#
	from baangt.base.DataBaseORM import TestCaseLog, TestCaseExtraField

	tc_log = TestCaseLog(testrun=tr_log)
	extra = TestCaseExtraField(name='Name', value='Value', testcase=tc_log)
	session_db.add(tr_log)
	session_db.add(tc_log)
	session_db.add(extra)
	session_db.commit()
	# assertions
	assert len(tr_log.testcases) == 1
	assert len(tc_log.extraFields) == 1


def test_sampletestrun(session_db, tr_log, results_google):
	#
	# create sample TestCaseLog instances
	#
	from baangt.base.DataBaseORM import TestCaseLog, TestCaseExtraField
	
	# predefined fields of TestCaseLog object
	predefinedFields = [
		'Toasts',
		'TCErrorLog',
		'VIGOGF#',
		'SAP Polizzennr',
		'Prämie',
		'PolNR Host',
		'TestCaseStatus',
		'Duration',
		'Screenshots',
		'timelog',
		'exportFilesBasePath',
		'TC.Lines',
		'TC.dontCloseBrowser',
		'TC.slowExecution',
		'TC.NetworkInfo',
		'TX.DEBUG',
		'ScreenshotPath',
		'ExportPath',
		'ImportPath',
		'RootPath',
	]

	session_db.add(tr_log)
	for result in results_google.values():
		# create TestCaseLog with predefined attributes
		tc_log = TestCaseLog(
			testrun=tr_log,
			toasts=result.get('Toasts'),
			tcErrorLog=result.get('TCErrorLog'),
			vigogf=result.get('VIGOGF#'),
			sapPolizzennr=result.get('SAP Polizzennr'),
			pramie=result.get('Prämie'),
			polNrHost=result.get('PolNR Host'),
			testCaseStatus=result.get('TestCaseStatus'),
			duration=result.get('Duration'),
			screenshots=result.get('Screenshots'),
			timelog=result.get('timelog'),
			exportFilesBasePath=result.get('exportFilesBasePath'),
			tcLines=result.get('TC.Lines'),
			tcDontCloseBrowser=result.get('TC.dontCloseBrowser'),
			tcSlowExecution=result.get('TC.slowExecution'),
			tcNetworkInfo=result.get('TC.NetworkInfo'),
			txDebug=result.get('TX.DEBUG'),
			screenshotPath=result.get('ScreenshotPath'),
			exportPath=result.get('ExportPath'),
			importPath=result.get('ImportPath'),
			rootPath=result.get('RootPath'),
		)
		session_db.add(tc_log)
		# add other attributes as TestCaseExtraField instances
		for key, value in result.items():
			if not key in predefinedFields:
				extra = TestCaseExtraField(name=key, value=str(value), testcase=tc_log)
				session_db.add(extra)

	session_db.commit()

	# assertions
	assert len(tr_log.testcases) == 4
	assert len(tr_log.testcases[0].extraFields) == 3
