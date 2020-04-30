import pytest
import json
import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from baangt.base.DataBaseORM import DATABASE_URL, TestrunLog, GlobalAttribute, TestCaseSequenceLog
from baangt.base.DataBaseORM import TestCaseLog, TestCaseField, TestCaseNetworkInfo

# db interface object
class dbTestrun:
	def __init__(self, db_url):
		engine = create_engine(db_url)
		self.session = sessionmaker(bind=engine)()

	def printTestrunList(self):
		#
		# prints the list odf Testruns in DB
		#
		print(f'{"UUID":40}Name')
		for log in self.session.query(TestrunLog).all():
			print(f'{str(uuid.UUID(bytes=log.uuid)):40}{log.testrunName}')

	def printTestrunSummary(self, testrun_uuid):
		#
		# prints summary of the specified Testrun
		#
		tr_log = self.session.query(TestrunLog).get(testrun_uuid)
		print(f'\n{"*"*10} Summary for Testrun {uuid.UUID(bytes=testrun_uuid)} {"*"*10}')
		print(f'\nUUID\t{uuid.UUID(bytes=testrun_uuid)}')
		print(f'Name\t{tr_log.testrunName}\n')
		print(f'Testrecords\t{len(tr_log.testcase_sequences[0].testcases)}')
		print(f'Successful\t{tr_log.statusOk}')
		print(f'Paused\t\t{tr_log.statusPaused}')
		print(f'Error\t\t{tr_log.statusFailed}')
		print(f'\nLogfile:\t{tr_log.logfileName}\n')
		print(f'Start time\t{tr_log.startTime.strftime("%H:%M:%S")}')
		print(f'End time\t{tr_log.endTime.strftime("%H:%M:%S")}')
		print(f'Duration\t{tr_log.endTime - tr_log.startTime}')

		print(type(tr_log.startTime))
		print(type(tr_log.uuid))

	def printTestrunGlobals(self, testrun_uuid):
		#
		# prints global settings for specified testrun
		#
		print(f'\n{"*"*10} Global Settings for Testrun {uuid.UUID(bytes=testrun_uuid)} {"*"*10}\n')
		for log in self.session.query(GlobalAttribute).filter(GlobalAttribute.testrun_uuid == testrun_uuid):
			print(f'{log.name:25}{log.value}')

	def printTestrunTestcases(self, testrun_uuid):
		#
		# prints Testcase info of the specified Testrun
		#
		tc_counter = 0
		print(f'\n{"*"*10} Testcases of Testrun {uuid.UUID(bytes=testrun_uuid)} {"*"*10}')
		for tc in self.session.query(TestCaseLog).filter(TestCaseLog.testcase_sequence.has(TestCaseSequenceLog.testrun_uuid == testrun_uuid)):
			tc_counter += 1
			print(f'\n>>> Testcase #{tc_counter}')
			print(f'\nUUID\t{uuid.UUID(bytes=tc.uuid)}')
			for log in self.session.query(TestCaseField).filter(TestCaseField.testcase_uuid == tc.uuid):
				print(f'{log.name:25}{log.value}')

# execution code
if __name__ == '__main__':
	
	# target Testrun
	testrunName = 'example_googleImages.xlsx_'

	# interface object
	db = dbTestrun(DATABASE_URL)

	# get target testrun
	item = db.session.query(TestrunLog).filter(TestrunLog.testrunName == testrunName).first()
	if item is None:
		print(f'ERROR. Testrun \'{testrunName}\' does not exist in DB')
		print('\nAvailable Testruns in DB:')
		db.printTestrunList()
		exit()
	
	# print Testrun Report
	db.printTestrunSummary(item.uuid)
	db.printTestrunGlobals(item.uuid)
	db.printTestrunTestcases(item.uuid)
