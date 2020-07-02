from sqlalchemy import create_engine, desc, and_
from sqlalchemy.orm import sessionmaker
from baangt.base.DataBaseORM import DATABASE_URL, engine, TestrunLog, GlobalAttribute, TestCaseLog, TestCaseSequenceLog, TestCaseField
import baangt.base.GlobalConstants as GC
import uuid

class ResultsBrowser:

	def __init__(self, db_url=None):
		if db_url:
			self.engine = create_engine(db_url)
		else:
			self.engine = create_engine(DATABASE_URL)

	def get(self, id):
		#
		# get TestrunLog by id (uuid string)
		#

		db = sessionmaker(bind=self.engine)()
		return db.query(TestrunLog).get(uuid.UUID(id).bytes)

	def getResults(self, name=None, stage=None, start_date=None, end_date=None):
		#
		# get TestrunLogs by name, stage and dates
		#

		db = sessionmaker(bind=self.engine)()
		records = []

		# filter by name and stage
		if name and stage:
			records = db.query(TestrunLog).order_by(TestrunLog.startTime).filter_by(testrunName=name)\
				.filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==stage))).all()
		
		# filter by name
		elif name:
			# get Testrun stages
			stages = db.query(GlobalAttribute.value).filter(GlobalAttribute.testrun.has(TestrunLog.testrunName==name))\
			.filter_by(name=GC.EXECUTION_STAGE).group_by(GlobalAttribute.value).order_by(GlobalAttribute.value).all()
			stages = [x[0] for x in stages]

			for s in stages:
				logs = db.query(TestrunLog).order_by(TestrunLog.startTime).filter_by(testrunName=name)\
					.filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==s))).all()
				records.extend(logs)

		# filter by stage
		elif stage:
			# get Testrun names
			names = db.query(TestrunLog.testrunName)\
			.filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==stage)))\
			.group_by(TestrunLog.testrunName).order_by(TestrunLog.testrunName).all()
			names = [x[0] for x in names]

			for n in names:
				logs = db.query(TestrunLog).order_by(TestrunLog.startTime).filter_by(testrunName=n)\
					.filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==stage))).all()
				records.extend(logs)

		# get all testruns ordered by name and stage
		else:
			# get Testrun names
			names = db.query(TestrunLog.testrunName).group_by(TestrunLog.testrunName).order_by(TestrunLog.testrunName).all()
			names = [x[0] for x in names]
			
			for n in names:
				# get Testrun stages
				stages = db.query(GlobalAttribute.value).filter(GlobalAttribute.testrun.has(TestrunLog.testrunName==n))\
				.filter_by(name=GC.EXECUTION_STAGE).group_by(GlobalAttribute.value).order_by(GlobalAttribute.value).all()
				stages = [x[0] for x in stages]

				for s in stages:
					logs = db.query(TestrunLog).order_by(TestrunLog.startTime).filter_by(testrunName=n)\
						.filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==s))).all()
					records.extend(logs)
			

		# filter by dates
		if start_date and end_date:
			return [log for log in records if log.startTime > start_date and log.startTime < end_date]
		elif start_date:
			return [log for log in records if log.startTime > start_date]
		elif end_date:
			return [log for log in records if log.startTime < end_date]

		return records

	def getTestCases(self, name, stage, start_date=None, end_date=None):
		#
		# retuns data on the specified testrun stages
		#

		# get records
		records = self.getResults(name, stage, start_date, end_date)

		print(f'Records read: {len(records)}')
		for r in records:
			for tc in r.testcase_sequences[0].testcases:
				print(f'{tc.duration}:\t{tc.status}\t{tc}')

		#return [{'duration': tc.duration, 'status': tc.status for tc in r.testcase_sequences[0].testcases} for r in records]
		



