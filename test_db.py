import pytest
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

path_to_db = 'test.db'
path_to_globals = 'tests/jsons/globals.json'
path_to_results = 'tests/jsons/results.json'
path_to_network = 'tests/jsons/network.json'

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
	with open(path_to_globals, 'r') as f:
		return json.load(f)


@pytest.fixture(scope='function')
def results_google():
	#
	# returns presaved Testrun results as dict
	#
	with open(path_to_results, 'r') as f:
		return json.load(f)

@pytest.fixture(scope='function')
def network_google():
	#
	# returns presaved Testrun network results as dict
	#
	with open(path_to_network, 'r') as f:
		return json.load(f)

#
# TestrunLog test
#

def test_testrunlog(session_db, tr_log):
	#
	# creata a TestrunLog instance
	#
	
	session_db.add(tr_log)
	session_db.commit()
	# assertions
	assert len(tr_log.testcase_sequences) == 0
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
	assert len(tr_log.testcase_sequences) == 0
	assert len(tr_log.globalVars) == 7


#
# TestCaseSequenceLog tests
#

def test_single_testcasesequencelog(session_db):
	#
	# fails to create a TestCaseSequenceLog instance without TestrunLog
	#
	from baangt.base.DataBaseORM import TestCaseSequenceLog

	tcs_log = TestCaseSequenceLog()
	session_db.add(tcs_log)
	with pytest.raises(Exception) as e_info:
		session_db.commit()

def test_testcasesequencelog(session_db, tr_log):
	#
	# create a TestCaseSequenceLog instance
	#
	from baangt.base.DataBaseORM import TestCaseSequenceLog

	tcs_log = TestCaseSequenceLog(testrun=tr_log)
	session_db.add(tr_log)
	session_db.add(tcs_log)
	session_db.commit()
	# assertions
	assert len(tr_log.testcase_sequences) == 1
	assert len(tcs_log.testcases) == 0


#
# TestCaseLog tests
#

def test_single_testcaselog(session_db):
	#
	# fails to create a TestCaseLog instance without TestCaseSequenceLog
	#
	from baangt.base.DataBaseORM import TestCaseLog

	tc_log = TestCaseLog()
	session_db.add(tc_log)
	with pytest.raises(Exception) as e_info:
		session_db.commit()


def test_testcaselog(session_db, tr_log):
	#
	# create a TestCaseLog instance
	#
	from baangt.base.DataBaseORM import TestCaseSequenceLog, TestCaseLog

	tcs_log = TestCaseSequenceLog(testrun=tr_log)
	tc_log = TestCaseLog(testcase_sequence=tcs_log)
	session_db.add(tr_log)
	session_db.add(tcs_log)
	session_db.add(tc_log)
	session_db.commit()
	# assertions
	assert len(tr_log.testcase_sequences) == 1
	assert len(tcs_log.testcases) == 1
	assert len(tc_log.fields) == 0
	assert len(tc_log.networkInfo) == 0

def test_testcase_field(session_db, tr_log):
	#
	# create a TestCaseField instance
	#
	from baangt.base.DataBaseORM import TestCaseSequenceLog, TestCaseLog, TestCaseField

	tcs_log = TestCaseSequenceLog(testrun=tr_log)
	tc_log = TestCaseLog(testcase_sequence=tcs_log)
	field = TestCaseField(name='Name', value='Value', testcase=tc_log)
	session_db.add(tr_log)
	session_db.add(tcs_log)
	session_db.add(tc_log)
	session_db.add(field)
	session_db.commit()
	# assertions
	assert len(tc_log.fields) == 1
	assert len(tc_log.networkInfo) == 0

def test_networkinfo(session_db, tr_log):
	#
	# create a TestCaseNetworkInfo instance
	#
	from baangt.base.DataBaseORM import TestCaseSequenceLog, TestCaseLog, TestCaseNetworkInfo

	tcs_log = TestCaseSequenceLog(testrun=tr_log)
	tc_log = TestCaseLog(testcase_sequence=tcs_log)
	info = TestCaseNetworkInfo(testcase=tc_log)
	session_db.add(tr_log)
	session_db.add(tcs_log)
	session_db.add(tc_log)
	session_db.add(info)
	session_db.commit()
	# assertions
	assert len(tc_log.fields) == 0
	assert len(tc_log.networkInfo) == 1


def test_sampletestcases(session_db, tr_log, results_google, network_google):
	#
	# create sample TestCaseLog instances
	#
	from baangt.base.DataBaseORM import TestCaseSequenceLog, TestCaseLog, TestCaseField, TestCaseNetworkInfo

	tcs_log = TestCaseSequenceLog(testrun=tr_log)
	session_db.add(tr_log)
	session_db.add(tcs_log)

	for result in results_google.values():
		# create TestCaseLog per a record
		tc_log = TestCaseLog(testcase_sequence=tcs_log)
		session_db.add(tc_log)
		# add TestCaseLog attributes
		for key, value in result.items():
			field = TestCaseField(name=key, value=str(value), testcase=tc_log)
			session_db.add(field)
	session_db.commit()

	# create network infos
	for info in network_google:
		for entry in info['log']['entries']:
			ni = TestCaseNetworkInfo(
				browserName = entry.get('pageref'),
				status = entry['response'].get('status'),
				method = entry['request'].get('method'),
				url = entry['request'].get('url'),
				contentType = entry['response']['content'].get('mimeType'),
				contentSize = entry['response']['content'].get('size'),
				headers = str(entry['response']['headers']),
				params = str(entry['request']['queryString']),
				response = entry['response']['content'].get('text'),
				startDateTime = datetime.strptime(entry['startedDateTime'][:19], '%Y-%m-%dT%H:%M:%S'), 
				duration = entry.get('time'),
				testcase = tcs_log.testcases[0],
			)
			session_db.add(ni)

	session_db.commit()

	# assertions
	assert len(tcs_log.testcases) == 4
	assert len(tcs_log.testcases[0].fields) == 23
	assert len(tcs_log.testcases[1].fields) == 23
	assert len(tcs_log.testcases[2].fields) == 23
	assert len(tcs_log.testcases[3].fields) == 23
	assert len(tcs_log.testcases[0].networkInfo) == 171


