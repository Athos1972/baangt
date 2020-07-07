from baangt.base.ResultsBrowser import ResultsBrowser
from datetime import datetime
import json

#DATABASE_URL = 'sqlite:///testrun_my.db'

# filter parameters
name = 'heartbeat.json'
#name = 'RSantragAll.json'
stage = 'HF'
#stage = 'PQA'
start_time = datetime.strptime("2020-06-10 00:00", "%Y-%m-%d %H:%M")
end_time = datetime.strptime("2020-07-11 00:00", "%Y-%m-%d %H:%M")

def print_logs(logs):
	for index, log in enumerate(logs):
		#data = log.to_json()
		print(f"{index:^4}{log.testrunName:20}{log.stage:10}{log.startTime}\t{log}")


#r = ResultsBrowser(db_url=DATABASE_URL)
r = ResultsBrowser()
#r.getTestCases(name=name, stage=stage)

'''
print('\n***** Get All Records')
logs = r.getResults()
print_logs(logs)

print('\n***** Filter By Name')
logs = r.getResults(name=name)
print_logs(logs)

print('\n***** Filter By Stage')
logs = r.getResults(stage=stage)
print_logs(logs)

print('\n***** Filter By Name & Stage')
logs = r.getResults(name=name, stage=stage)
print_logs(logs)

print('\n***** Filter By Name and Date')
logs = r.getResults(name=name, start_date=start_time, end_date=end_time)
print_logs(logs)
'''
'''
id = 'eff78fa9-83b7-484a-a8ab-5e30cf0f12cc'
print(f'\n****** GET BY ID: {id}')
print_logs([r.get(id)])
'''
'''
def draw_seconds(t):
	if t is None:
		return '\033[35mnan\033[0m'

	n = t.seconds
	if n < 20:
		return f'\033[45m{n:3}\033[0m'
	elif n < 50:
		return f'\033[44m{n:3}\033[0m'
	elif n < 100:
		return f'\033[42m{n:3}\033[0m'
	elif n < 150:
		return f'\033[43m{n:3}\033[0m'
	else:
		return f'\033[41m{n:3}\033[0m'

print(f'\n****** TestCase details for {name}')
status = {
	"OK": '\033[92mK\033[0m',
	"Failed": '\033[91mF\033[0m',
	"Paused": '\033[90mP\033[0m',
}
logs = r.getResults(name=name, stage=stage)

print(f'\n{"Date":^20}\tTest Case Status')
for log in logs:
	print(log.startTime, end='\t')
	for tc in log.testcase_sequences[0].testcases:
		print(status[tc.status], end=' ')
	print()

print(f'\n{"Date":^20}\tTest Case Duration (s)')
for log in logs:
	print(log.startTime, end='\t')
	for tc in log.testcase_sequences[0].testcases:
		print(draw_seconds(tc.duration), end=' ')
	print()
'''

r.query(name=name, stage=stage, start_date=start_time, end_date=end_time)
#r.query(name=name, start_date=start_time)
f = r.export()


#print(f'Exported to: {f}')




