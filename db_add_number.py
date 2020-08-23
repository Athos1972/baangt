from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from baangt.base.DataBaseORM import DATABASE_URL, TestrunLog, TestCaseLog, TestCaseSequenceLog

if __name__ == '__main__':
	engine = create_engine(DATABASE_URL)
	session = sessionmaker(bind=engine)()

	# fetch testruns
	print('\nSetting numbers od TestCaseSequeces')
	testruns = session.query(TestrunLog)
	for tr_index, tr in enumerate(testruns):
		for tcs_index, tcs in enumerate(tr.testcase_sequences, 1):
			tcs.number = tcs_index
			if not tr_index%50:
				print(f'{tr_index} TestrunLogs processed')
	session.commit()

	# fetch testcase sequences
	print('\nSetting numbers od TestCases')
	testcase_sequences = session.query(TestCaseSequenceLog)
	for tcs_index, tcs in enumerate(testcase_sequences):
		for tc_index, tc in enumerate(tcs.testcases, 1):
			tc.number = tc_index
			if not tcs_index%50:
				print(f'{tcs_index} TestCaseSequenceLogs processed')
	session.commit()
