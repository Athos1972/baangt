import pytest
import json
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
		print('ID\tName')
		for log in self.session.query(TestrunLog).all():
			print(f'{log.id}\t{log.testrunName}')

	def printTestrunSummary(self, testrun_id):
		#
		# prints summary of the specified Testrun
		#
		tr_log = self.session.query(TestrunLog).get(testrun_id)
		print(f'\n{"*"*10} Summary for Testrun #{testrun_id} {"*"*10}')
		print(f'\nName\t{tr_log.testrunName}\n')
		print(f'Testrecords\t{len(tr_log.testcase_sequences[0].testcases)}')
		print(f'Successful\t{tr_log.statusOk}')
		print(f'Paused\t\t{tr_log.statusPaused}')
		print(f'Error\t\t{tr_log.statusFailed}')
		print(f'\nLogfile:\t{tr_log.logfileName}\n')
		print(f'Start time\t{tr_log.startTime.strftime("%H:%M:%S")}')
		print(f'End time\t{tr_log.endTime.strftime("%H:%M:%S")}')
		print(f'Duration\t{tr_log.endTime - tr_log.startTime}')

	def printTestrunGlobals(self, testrun_id):
		#
		# prints global settings for specified testrun
		#
		print(f'\n{"*"*10} Global Settings for Testrun #{testrun_id} {"*"*10}\n')
		for log in self.session.query(GlobalAttribute).filter(GlobalAttribute.testrun_id == testrun_id):
			print(f'{log.name:25}{log.value}')

	def printTestrunTestcases(self, testrun_id):
		#
		# prints Testcase info of the specified Testrun
		#
		tc_counter = 0
		print(f'\n{"*"*10} Testcases of Testrun #{testrun_id} {"*"*10}')
		for tc in self.session.query(TestCaseLog).filter(TestCaseLog.testcase_sequence.has(TestCaseSequenceLog.testrun_id == testrun_id)):
			tc_counter += 1
			print(f'\n>>> Testcase #{tc_counter}')
			for log in self.session.query(TestCaseField).filter(TestCaseField.testcase_id == tc.id):
				print(f'{log.name:25}{log.value}')

# execution code
if __name__ == '__main__':
	
	# target Testrun
	testrunName = 'example_googleImages.xlsx'

	# interface object
	db = dbTestrun(f'sqlite:///{DATABASE_URL}')

	# get target testrun
	item = db.session.query(TestrunLog.id).filter(TestrunLog.testrunName == testrunName).first()
	if item is None:
		print(f'ERROR. Testrun \'{testrunName}\' does not exist in DB')
		print('\nAvailable Testruns in DB:')
		db.printTestrunList()
		exit()
	
	# print Testrun Report
	db.printTestrunSummary(item.id)
	db.printTestrunGlobals(item.id)
	db.printTestrunTestcases(item.id)
