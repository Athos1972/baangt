from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

DATABASE_URL = 'sqlite:///testrun.db'
engine = create_engine(DATABASE_URL)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

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
