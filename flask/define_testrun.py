import pandas as pd
import json

path_to_excel = '../DropsTestRunDefinition.xlsx'
path_to_json = 'testrun.json'

xl = pd.ExcelFile(path_to_excel)

# parse TestCaseSequence
df = xl.parse('TestCaseSequence')

for name in df:
	print(name)

'''
testrun = {}
for i in range(len(df)):
	step = {
		'name': df['Name'][i],
		'description': df['Description'][i],
		'activity_type': df['ActivityType'][i],
		'locator_type': 'xpath',
	}
	steps.append(step)

# dump to json
with open(path_to_json, 'w') as f:
	json.dump(steps, f)
'''