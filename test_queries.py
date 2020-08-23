from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from baangt.base.DataBaseORM import DATABASE_URL, TestrunLog, GlobalAttribute, TestCaseLog, TestCaseSequenceLog, TestCaseField
import time

#{chr(746)}

#name = 'RSantragAll.json'
#name = 'heartbeat.json'
#name = 'kfz.xlsx'


class Query:

	def __init__(self, name):
		# craate session
		self.engine = create_engine(DATABASE_URL)
		self.db = sessionmaker(bind=self.engine)()
		self.name = name

	def get_logs(self):
		if self.name:
			return self.db.query(TestrunLog).filter_by(testrunName=self.name)

		return self.db.query(TestrunLog)

	def by_relationships(self):
		# time tracker
		time_start = time.time()
		# query testruns
		logs = self.get_logs()
		print(f'\nFETCHED: {logs.count()} Testruns')
		for tr_index, tr in enumerate(logs):
			print(f'** Testrun-{tr_index}')
			for tcs_index, tcs in enumerate(tr.testcase_sequences):
				print(f'**** TestCaseSequence-{tcs_index}: {len(tcs.testcases)} test cases')
				for tc_index, tc in enumerate(tcs.testcases):
					#print(f'****** TestCase-{tc_index}')
					for field in tc.fields:
						pass
		self.time = time.time()-time_start

	def by_subqueries(self):
		# time tracker
		time_start = time.time()
		# query testruns
		logs = self.get_logs()
		print(f'\nFETCHED: {logs.count()} Testruns')
		for tr_index, tr in enumerate(logs):
			print(f'** Testrun-{tr_index}')
			for tcs_index, tcs in enumerate(tr.testcase_sequences):
				# query testcases
				tc_query = self.db.query(TestCaseLog).filter_by(testcase_sequence_id=tcs.id)
				print(f'**** TestCaseSequence-{tcs_index}: {tc_query.count()} test cases')
				for tc_index, tc in enumerate(tc_query):
					for field in self.db.query(TestCaseField).filter_by(testcase_id=tc.id):
						pass
		self.time = time.time()-time_start

	def by_yield_subqueries(self):
		# time tracker
		time_start = time.time()
		# query testruns
		logs = self.get_logs()
		print(f'\nFETCHED: {logs.count()} Testruns')
		tr_index = 0
		for tr in logs.yield_per(10):
			print(f'** Testrun-{tr_index}')
			tr_index += 1
			for tcs_index, tcs in enumerate(tr.testcase_sequences):
				# query testcases
				tc_query = self.db.query(TestCaseLog).filter_by(testcase_sequence_id=tcs.id)
				print(f'**** TestCaseSequence-{tcs_index}: {tc_query.count()} test cases')
				tc_index = 0
				for tc in tc_query.yield_per(10):
					for field in self.db.query(TestCaseField).filter_by(testcase_id=tc.id).yield_per(10):
						pass
		self.time = time.time()-time_start

	def by_subqueries_fields(self):
		# time tracker
		time_start = time.time()
		# query testruns
		logs = self.get_logs()
		print(f'\nFETCHED: {logs.count()} Testruns')
		for tr_index, tr in enumerate(logs):
			print(f'** Testrun-{tr_index}')
			tcs_query = self.db.query(TestCaseSequenceLog.id).filter_by(testrun_id=tr[0])
			for tcs_index, tcs in enumerate(tcs_query):
				# query testcases
				tc_query = self.db.query(TestCaseLog.id).filter_by(testcase_sequence_id=tcs[0])
				print(f'**** TestCaseSequence-{tcs_index}: {tc_query.count()} test cases')
				for tc_index, tc in enumerate(tc_query):
					for name, value in self.db.query(TestCaseField.name, TestCaseField.value).filter_by(testcase_id=tc[0]):
						pass
		self.time = time.time()-time_start

	def by_connection(self):
		# time tracker
		time_start = time.time()
		with self.engine.connect() as conn:
			# query testruns
			logs = conn.execute(TestrunLog.__table__.select().filter_by(testrunName=self.name)).fetchall()
			print(f'\nFETCHED: {len(logs)} Testruns')
			for tr_index, tr in enumerate(logs):
				print(f'** Testrun-{tr_index}')
				for tcs_index, tcs in enumerate(tr.testcase_sequences):
					# query testcases
					tc_query = self.db.query(TestCaseLog).filter_by(testcase_sequence_id=tcs.id)
					print(f'**** TestCaseSequence-{tcs_index}: {tc_query.count()} test cases')
					for tc_index, tc in enumerate(tc_query):
						for field in self.db.query(TestCaseField).filter_by(testcase_id=tc.id):
							pass
		self.time = time.time()-time_start


	def statistics(self):
		print(f'\nEXECUTION TIME: {self.time}')

class QueryStack:

	def __init__(self):
		self.queries = []

	def add(self, query):
		self.queries.append(query)

	def statistics(self):
		fields = {
			'name': 20,
			'time': 10,
		}
		print(' '*fields.get('name') + 'Time')
		for q in self.queries:
			print(f'{q.name}{" "*(fields.get("name")-len(q.name))}{q.time}')


if __name__ == '__main__':
	name = 'RSantragAll.json'
	q = Query(name)
	q.by_relationships()

	qstack = QueryStack()
	name = None
	for i in range(1):
		q = Query(name)
		if i == 0:
			q.by_relationships()
			q.name = 'Relations'
		elif i == 1:
			q.by_subqueries()
			q.name = 'Subqueries'
		elif i == 2:
			q.by_yield_subqueries()
			q.name = 'Yielded'
		elif i == 3:
			q.by_subqueries_fields()
			q.name = 'Fields'

		qstack.add(q)

	qstack.statistics()


