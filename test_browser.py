from baangt.base.ResultsBrowser import ResultsBrowser
from datetime import datetime

#DATABASE_URL = 'sqlite:///testrun_my.db'

# filter parameters
name = 'heartbeat.json'
stage = 'HF'
start_time = datetime.strptime("2020-06-10 00:00", "%Y-%m-%d %H:%M")
end_time = datetime.strptime("2020-06-11 00:00", "%Y-%m-%d %H:%M")

def print_logs(logs):
	for index, log in enumerate(logs):
		#data = log.to_json()
		print(f"{index:^4}{log.testrunName:20}{log.stage:10}{log.startTime}\t{log}")


#r = ResultsBrowser(db_url=DATABASE_URL)
r = ResultsBrowser()

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

id = 'eff78fa9-83b7-484a-a8ab-5e30cf0f12cf'
print(f'\n****** GET BY ID: {id}')
print_logs([r.get(id)])