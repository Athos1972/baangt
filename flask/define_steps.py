import pandas as pd
import json

path_to_excel = '../BaangtDBFill.xlsx'
path_to_json = 'teststeps.json'

xl = pd.ExcelFile(path_to_excel)

df = xl.parse('data')

#print(df)
steps = []
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