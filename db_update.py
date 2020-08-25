from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker
from baangt.base.DataBaseORM import DATABASE_URL, TestrunLog, TestCaseLog, TestCaseSequenceLog

def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    #column_nullable = column.nullable.compile(engine.dialect)
    #column_default = column.default.compile(engine.dialect)
    sql = f'''
    	ALTER TABLE {table_name}
    	ADD COLUMN {column_name} {column_type} {"NULL" if column.nullable else "NOT NULL"}
    	{"DEFAULT " if column.default else ""}{column.default.arg if column.default else ""}
    '''
    print(f'*** CREATING new column in table {table_name}:\n{sql}')
    engine.execute(sql)

if __name__ == '__main__':
	engine = create_engine(DATABASE_URL)
	
	# add new columns
	number_column = Column('number', Integer, nullable=False, default=0)
	add_column(engine, TestCaseSequenceLog.__table__, number_column)
	add_column(engine, TestCaseLog.__table__, number_column)

	# populate with numbers
	print('\n*** POPULATING new columns')
	session = sessionmaker(bind=engine)()

	# fetch testruns
	print('\nSetting numbers of TestCaseSequeces')
	testruns = session.query(TestrunLog)
	for tr_index, tr in enumerate(testruns):
		for tcs_index, tcs in enumerate(tr.testcase_sequences, 1):
			tcs.number = tcs_index
		if tr_index and not tr_index%50:
			print(f'{tr_index} TestrunLogs processed')
	session.commit()

	# fetch testcase sequences
	print('\nSetting numbers of TestCases')
	testcase_sequences = session.query(TestCaseSequenceLog)
	for tcs_index, tcs in enumerate(testcase_sequences):
		for tc_index, tc in enumerate(tcs.testcases, 1):
			tc.number = tc_index
		if tcs_index and not tcs_index%50:
			print(f'{tcs_index} TestCaseSequenceLogs processed')
	session.commit()
