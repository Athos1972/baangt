from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'testrun.db'

engine = create_engine(f'sqlite:///{DATABASE_URL}')
base = declarative_base()

# declare models
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

# create tables
base.metadata.create_all(engine)