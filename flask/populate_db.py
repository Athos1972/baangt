import json
from app import db
from app.models import *

#DATABASE_URL = 'sqlite:///testrun.db'
#engine = create_engine(DATABASE_URL)

# create a db.session
#db.session = db.sessionmaker(bind=engine)
#db.session = db.session()

# recreate db structure
db.drop_all()
db.create_all()

# create users
print('Creating users...')
admin = User(username='admin')
admin.set_password('12345')
user = User(username='simple_user')
user.set_password('12345')
db.session.add(admin)
db.session.add(user)
db.session.commit()
print('Done.')

# create supports
print('Creating supports...')
browsers = {
	'FF': 'Mozilla Firefox',
	'Chrome': 'Google Chrome',
	'IE': 'MS Internet Exploer',
	'Safari': 'Safari',
	'Edge': 'MS Edge',
}
for key, value in browsers.items():
	browser = BrowserType(name=key, description=value)
	db.session.add(browser)

testcases = {
	'Browser': 'Browser',
	'API-Rest': 'API-Rest',
	'API-SOAP': 'API-SOAP',
	'API-oDataV2': 'API-oDataV2',
	'API-oDataV4': 'API-oDataV4',
}
for key, value in testcases.items():
	testcase = TestCaseType(name=key, description=value)
	db.session.add(testcase)

activities = {
	'GOTOURL': 'Go to an URL',
	'SETTEXT': 'Set Text of an Element',
	'CLICK': 'Click on an Element',
}
for key, value in activities.items():
	activity = ActivityType(name=key, description=value)
	db.session.add(activity)

locators = {
	'xpath': 'Locate via XPATH-Expression',
	'css': 'Locate via CSS-Path of the Element',
	'id': 'Locate via ID of the Element',
}
for key, value in locators.items():
	locator = LocatorType(name=key, description=value)
	db.session.add(locator)

classnames = {
	'Class A': 'A Simple Class Name',
	'Class B': 'One more Simple Class Name',
	'Class C': 'A Complex Class Name',
}
for key, value in classnames.items():
	classname = ClassName(name=key, description=value)
	db.session.add(classname)

db.session.commit()
print('Done.')

# create mains
print('Creating mains...')
for i in range(5):
	testrun  = Testrun(
		name=f'Testrun #{i}',
		description=f'Testrun #{i} is intended for testing the application UI. There are several features wich are described here.',
		creator=admin,
	)
	db.session.add(testrun)

db.session.commit()

for i in range(5):
	if i < 3:
		u = admin
	else:
		u = user
	testseq  = TestCaseSequence(
		name=f'Test Case Sequence #{i}',
		description=f'Test Case Sequence #{i} is intended for testing the application UI. There are several features wich are described here.',
		creator=u,
		classname=classname,
	)
	testseq.testrun.append(testrun)
	if i == 2 or i == 3:
		another_testrun = Testrun.query.get(i)
		testseq.testrun.append(another_testrun)
	db.session.add(testseq)
	
db.session.commit()

for i in range(5):
	if i < 3:
		u = admin
	else:
		u = user
	datafile  = DataFile(
		filename=f'data_file_{i}.xlsx',
		creator=u,
	)
	testseq = TestCaseSequence.query.get(i+1)
	datafile.testcase_sequence.append(testseq)
	db.session.add(datafile)
	
db.session.commit()

# get supports
browsers = BrowserType.query.all()
testtypes = TestCaseType.query.all()
activities = ActivityType.query.all()
locators = LocatorType.query.all()

for i in range(12):
	if i%3 == 0:
		u = admin
	else:
		u = user
	testcase  = TestCase(
		name=f'Test Case #{i}',
		description=f'Test Case #{i} is intended for testing the application UI. There are several features wich are described here.',
		creator=u,
		classname=classname,
		browser_type=browsers[i%len(browsers)],
		testcase_type=testtypes[i%len(testtypes)], 
	)
	testseq = TestCaseSequence.query.get(i%5 + 1)
	testcase.testcase_sequence.append(testseq)
	db.session.add(testcase)

db.session.commit()

for i in range(7):
	if i%3 == 0:
		u = admin
	else:
		u = user
	teststepseq  = TestStepSequence(
		name=f'Test Step Sequence #{i}',
		description=f'Test Step Sequence #{i} is intended for testing the application UI. There are several features wich are described here.',
		creator=u,
		classname=classname,
	)
	teststepseq.testcase.append(testcase)
	db.session.add(testcase)

db.session.commit()

'''
for i in range(4):
	if i%3 == 0:
		u = admin
	else:
		u = user
	teststepex  = TestStepExecution(
		name=f'Test Step Execution #{i}',
		description=f'Test Step Execution #{i} is intended for testing the application UI. There are several features wich are described here.',
		creator=u,
		activity_type=activities[i%len(activities)],
		locator_type=locators[i%len(locators)],
		teststep_sequence=TestStepSequence.query.get(i%2 + 1),
	)
	db.session.add(testcase)
'''
# get teststeps from json
path_to_json = 'teststeps.json'
with open(path_to_json, 'r') as f:
	steps = json.load(f)
# populate teststeps
for step in steps:
	# get activity type
	for a in activities:
		if a.name.upper() == step.get('activity_type').upper():
			activity = a
			break
	# get locator type
	for l in locators:
		if l.name.upper() == step.get('locator_type').upper():
			locator = l
			break
	# create Test Step
	teststepex  = TestStepExecution(
		name=step.get('name'),
		description=step.get('description'),
		creator=admin,
		activity_type=activity,
		locator_type=locator,
	)
	db.session.add(testcase)


db.session.commit()
print('Done.')