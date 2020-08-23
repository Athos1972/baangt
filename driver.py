from baangt.base.ResultsBrowser import ResultsBrowser
from datetime import datetime

names = [
	'RSantragAll.json',
	'heartbeat.json',
	'kfz.xlsx',
]

q = ResultsBrowser()
q.query(name=names[0])
#q.query_set.data = q.query_set.data[:10]

#q.query()
#q.query_set.data = [i for i in q.query_set.data if i.testrunName in names[:2]]

q.export()