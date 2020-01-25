from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

DATABASE_URL = 'sqlite:///testrun.db'
engine = create_engine(DATABASE_URL)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

# create supports
browsers = {
	'FF': 'Mozilla Firefox',
	'Chrome': 'Google Chrome',
	'IE': 'MS Internet Exploer',
	'Safari': 'Safari',
	'Edge': 'MS Edge',
}
for key, value in browsers.items():
	browser = BrowserType(name=key, description=value)
	session.add(browser)

testcases = {
	'Browser': 'Browser',
	'API-Rest': 'API-Rest',
	'API-SOAP': 'API-SOAP',
	'API-oDataV2': 'API-oDataV2',
	'API-oDataV4': 'API-oDataV4',
}
for key, value in testcases.items():
	testcase = TestCaseType(name=key, description=value)
	session.add(testcase)

activities = {
	'GOTOURL': 'Go to an URL',
	'SETTEXT': 'Set Text of an Element',
	'CLICK': 'Click on an Element',
}
for key, value in activities.items():
	activity = ActivityType(name=key, description=value)
	session.add(activity)

locators = {
	'xpath': 'Locate via XPATH-Expression',
	'css': 'Locate via CSS-Path of the Element',
	'id': 'Locate via ID of the Element',
}
for key, value in locators.items():
	locator = LocatorType(name=key, description=value)
	session.add(locator)

session.commit()

# create users
user = User(username='admin')
session.add(user)
session.commit()

# create testruns
testrun  = Testrun(
	name='Testrun #1',
	description='some description goes here',
	createdBy=user.id,
)
session.add(testrun)
session.commit()

# create testrun sequences
seq_1 = TestCaseSequence(
	name='Testrun Sequance #1',
	description='About sequence #1',
	createdBy=user.id,
)
seq_2 = TestCaseSequence(
	name='Testrun Sequance #2',
	description='About sequence #2',
	createdBy=user.id,
)
seq_1.testrun.append(testrun)

session.add(seq_1)
session.add(seq_2)
session.commit()
