import os
from app import models, db, app
from datetime import datetime
import xlsxwriter, xlrd, json

#
# item categories
#
def getItemCategories():
	categories = {}
	categories['main'] = [
		'testrun',
		'testcase_sequence',
		'testcase',
		'teststep_sequence',
		'teststep',
	]

	return categories

#
# generate choices of items
#

def getTestCaseSequences():
	choices = []
	for item in models.TestCaseSequence.query.all():
		choices.append((f'{item.id}', item.name))
	return choices

def getDataFiles():
	choices = []
	for item in models.DataFile.query.all():
		choices.append((f'{item.id}', item.filename))
	return choices

def getTestCases():
	choices = []
	for item in models.TestCase.query.all():
		choices.append((f'{item.id}', item.name))
	return choices

def getTestStepSequences():
	choices = []
	for item in models.TestStepSequence.query.all():
		choices.append((f'{item.id}', item.name))
	return choices

def getTestSteps():
	choices = []
	for item in models.TestStepExecution.query.all():
		choices.append((f'{item.id}', item.name))
	return choices

def getClassNames():
	choices = []
	for item in models.ClassName.query.all():
		choices.append((f'{item.id}', item.name))
	return choices

def getBrowserTypes():
	choices = []
	for item in models.BrowserType.query.all():
		choices.append((f'{item.id}', item.name))
	return choices

def getTestCaseTypes():
	choices = []
	for item in models.TestCaseType.query.all():
		choices.append((f'{item.id}', item.name))
	return choices

def getActivityTypes():
	choices = []
	for item in models.ActivityType.query.all():
		choices.append((f'{item.id}', item.name))
	return choices

def getLocatorTypes():
	choices = []
	for item in models.LocatorType.query.all():
		choices.append((f'{item.id}', item.name))
	return choices


#
# Comaprisions
#

COMPARISIONS = [
	'=',
	'>',
	'<',
	'>=',
	'<=',
	'<>',
]

def getComparisionChoices():
	return [('0', 'none')] + [(f'{i+1}', COMPARISIONS[i]) for i in range(len(COMPARISIONS))]

def getComparisionId(option):
	for i in range(len(COMPARISIONS)):
		if option == COMPARISIONS[i]:
			return f'{i+1}'
	return '0'

#
# Get Items By Name
#

def getBrowserTypeByName(name):
	# browser mapper
	bm = {
		'BROWSER_FIREFOX': "FF",
		'BROWSER_CHROME': "Chrome",
		'BROWSER_SAFARI': "Safari",
		'BROWSER_EDGE': "Edge",
	}
	return models.BrowserType.query.filter_by(name=bm[name.split('.')[-1]]).first()

def getTestCaseTypeByName(name):
	return models.TestCaseType.query.filter_by(name=name).first()

def getActivityTypeByName(name):
	#print('*********** Activity Type')
	#print(name)
	return models.ActivityType.query.filter_by(name=name).first()

def getLocatorTypeByName(name):
	if name:
		return models.LocatorType.query.filter_by(name=name).first()
	else:
		return None

def getBooleanValue(value):
	if value:
		return True
	else:
		return False


#
# Testrun format convertions
#

def exportXLSX(testrun_id):
	#
	# Exports Testrun to XLSX
	#

	# get testrun
	testrun = models.Testrun.query.get(testrun_id)
	testrun_json = testrun.to_json()

	# create workbook
	headers = {
		'TestRun': [
			'Attribute',
			'Value',
		],

		'TestCaseSequence': [
			'Number',
			'SequenceClass',
			'TestDataFileName',
		],
		
		'TestCase': [
			'TestCaseSequenceNumber',
			'TestCaseNumber',
			'TestCaseClass'
			'TestCaseType',
			'Browser',
		],
		
		'TestStep': [
			'TestCaseSequenceNumber',
			'TestCaseNumber',
			'TestStepNumber',
			'TestStepClass',
		],
		
		'TestStepExecution': [
			'TestCaseSequenceNumber',
			'TestCaseNumber',
			'TestStepNumber',
			'TestStepExecutionNumber',
			'Activity',
			'LocatorType',
			'Locator',
			'Value',
			'Comparison',
			'Value2',
			'Timeout',
			'Optional',
			'Release',
		],
	}

	xlsx_file = f'Testrun_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
	workbook = xlsxwriter.Workbook(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/files', xlsx_file))
	worksheets = {}
	for sheet in headers:
		worksheets[sheet] = workbook.add_worksheet(sheet)

	# write headers
	for key, items in headers.items():
		for col in range(len(items)):
			worksheets[key].write(0, col, items[col])

	# write data
	# to TestRun
	worksheets['TestRun'].write(1, 0, 'Export Format')
	worksheets['TestRun'].write(1, 1, 'XLSX')

	# to TestCaseSequence
	i = 1 # i for TestCaseSequence Number
	for testcase_sequence in testrun.testcase_sequences: 
		worksheets['TestCaseSequence'].write(i, 0, i)
		worksheets['TestCaseSequence'].write(i, 1, testcase_sequence.classname.name)
		worksheets['TestCaseSequence'].write(i, 2, testcase_sequence.datafiles[0].filename)

		# to TestCase
		j = 1 # j for TestCase 
		for testcase in testcase_sequence.testcases:
			worksheets['TestCase'].write(j, 0, i)
			worksheets['TestCase'].write(j, 1, j)
			worksheets['TestCase'].write(j, 2, testcase.classname.name)
			worksheets['TestCase'].write(j, 3, testcase.testcase_type.name)
			worksheets['TestCase'].write(j, 4, testcase.browser_type.name)

			# to TestStep
			k = 1 # k for TestStep
			for teststep_sequence in testcase.teststep_sequences:
				worksheets['TestStep'].write(k, 0, i)
				worksheets['TestStep'].write(k, 1, j)
				worksheets['TestStep'].write(k, 2, k)
				worksheets['TestStep'].write(k, 3, teststep_sequence.classname.name)

				# to TestStepExecution
				m = 1 # m for TestStepExecution
				for teststep in teststep_sequence.teststeps:
					worksheets['TestStepExecution'].write(m, 0, i)
					worksheets['TestStepExecution'].write(m, 1, j)
					worksheets['TestStepExecution'].write(m, 2, k)
					worksheets['TestStepExecution'].write(m, 3, m)
					worksheets['TestStepExecution'].write(m, 4, teststep.activity_type.name)
					worksheets['TestStepExecution'].write(m, 5, teststep.locator_type.name)
					worksheets['TestStepExecution'].write(m, 6, teststep.locator)
					worksheets['TestStepExecution'].write(m, 7, teststep.value)
					worksheets['TestStepExecution'].write(m, 8, teststep.comparision)
					worksheets['TestStepExecution'].write(m, 9, teststep.value2)
					worksheets['TestStepExecution'].write(m, 10, teststep.timeout)
					worksheets['TestStepExecution'].write(m, 11, teststep.optional)
					worksheets['TestStepExecution'].write(m, 12, teststep.release)

					m += 1
				k += 1
			j += 1
		i += 1

	workbook.close()
	return xlsx_file


def importXLSX(user, xlsx_file):
	#
	# imports testrun from xlsx file
	#

	app.logger.info(f'Importing a Testrun from {xlsx_file.filename} by {user}.')
	# open xlsx
	try:
		xl = xlrd.open_workbook(file_contents=xlsx_file.read())
	except XLRDError:
		return 0

	# create Testrun object
	file_name = os.path.basename(xlsx_file.filename)
	testrun  = models.Testrun(
		name=file_name,
		description=f'Imported from "{file_name}"',
		creator=user,
	)
	db.session.add(testrun)
	db.session.commit()
	app.logger.info(f'Created Testrun id {testrun.id} by {user}.')

	# create TestCaseSequences
	testcase_sequences = {}
	if 'TestCaseSequence' in xl.sheet_names():
		# get sheet
		testcase_sequence_sheet = xl.sheet_by_name('TestCaseSequence')
		# get headers as dict
		headers = {h[1]: h[0] for h in enumerate(testcase_sequence_sheet.row_values(0))}
		# get TestCaseSequences
		for row in range(1, testcase_sequence_sheet.nrows):
			n = int(testcase_sequence_sheet.cell(row, headers['Number']).value)
			# ClassName
			classname = models.ClassName(
				name=testcase_sequence_sheet.cell(row, headers['SequenceClass']).value,
				description=f'Imported from "{file_name}"',
			)
			db.session.add(classname)
			# DataFile
			datafile  = models.DataFile(
				filename=testcase_sequence_sheet.cell(row, headers['TestDataFileName']).value,
				creator=user,
			)
			db.session.add(datafile)
			db.session.commit()
			app.logger.info(f'Created ClassName id {classname.id} by {user}.')
			app.logger.info(f'Created DataFile id {datafile.id} by {user}.')
			# TestCaseSequence
			testcase_sequences[n] = models.TestCaseSequence(
				name=f'{file_name}_{row}',
				description=f'Imported from "{file_name}"',
				creator=user,
				classname=classname,
				datafiles=[datafile],
				testrun=[testrun],
			)
			db.session.add(testcase_sequences[n])
			db.session.commit()
			app.logger.info(f'Created TestCaseSequence id {testcase_sequences[n].id} by {user}.')
			
	else:
		# create default TestCaseSequence
		# ClassName
		classname = models.ClassName(
			name='GC.CLASSES_TESTCASESEQUENCE',
			description=f'Default for TestCaseSequence',
		)
		db.session.add(classname)
		# DataFile
		datafile  = models.DataFile(
			filename=file_name,
			creator=user,
		)
		db.session.add(datafile)
		db.session.commit()
		app.logger.info(f'Created ClassName id {classname.id} by {user}.')
		app.logger.info(f'Created DataFile id {datafile.id} by {user}.')
		# TestCaseSequence
		testcase_sequences[1] = models.TestCaseSequence(
			name=f'{file_name}_1',
			description=f'Default for "{file_name}"',
			creator=user,
			classname=classname,
			datafiles=[datafile],
			testrun=[testrun],
		)
		db.session.add(testcase_sequences[1])
		db.session.commit()
		app.logger.info(f'Created TestCaseSequence id {testcase_sequences[1].id} by {user}.')

	# create TestCases
	testcases = {}
	if 'TestCase' in xl.sheet_names():
		# get sheet
		testcase_sheet = xl.sheet_by_name('TestCase')
		# get headers as dict
		headers = {h[1]: h[0] for h in enumerate(testcase_sheet.row_values(0))}
		# get TestCases
		for row in range(1, testcase_sheet.nrows):
			n = int(testcase_sheet.cell(row, headers['TestCaseNumber']).value)
			# ClassName
			classname = models.ClassName(
				name=testcase_sheet.cell(row, headers['TestCaseClass']).value,
				description=f'Imported from "{file_name}"',
			)
			db.session.add(classname)
			db.session.commit()
			app.logger.info(f'Created ClassName id {classname.id} by {user}.')
			# TestCase
			testcases[n]  = models.TestCase(
				name=f'{file_name}_{row}',
				description=f'Imported from "{file_name}"',
				creator=user,
				classname=classname,
				browser_type=getBrowserTypeByName(testcase_sheet.cell(row, headers['Browser']).value),
				testcase_type=getTestCaseTypeByName(testcase_sheet.cell(row, headers['TestCaseType']).value),
				testcase_sequence=[testcase_sequences[int(testcase_sheet.cell(row, headers['TestCaseSequenceNumber']).value)]]
			)
			db.session.add(testcases[n])
			db.session.commit()
			app.logger.info(f'Created TestCase id {testcases[n].id} by {user}.')
	else:
		# create default TestCase
		# ClassName
		classname = models.ClassName(
			name='GC.CLASSES_TESTCASE',
			description='Default for TestCase',
		)
		db.session.add(classname)
		db.session.commit()
		app.logger.info(f'Created ClassName id {classname.id} by {user}.')
		# TestCase
		testcases[1]  = models.TestCase(
			name=f'{file_name}_1',
			description=f'Default for "{file_name}"',
			creator=user,
			classname=classname,
			browser_type=getBrowserTypeByName('GC.BROWSER_FIREFOX'),
			testcase_type=getTestCaseTypeByName('Browser'),
			testcase_sequence=[testcase_sequences[1]]
		)
		db.session.add(testcases[1])
		db.session.commit()
		app.logger.info(f'Created TestCase id {testcases[1].id} by {user}.')

	# create TestSteps
	teststeps = {}
	if 'TestStep' in xl.sheet_names():
		# get sheet
		teststep_sheet = xl.sheet_by_name('TestStep')
		# get headers as dict
		headers = {h[1]: h[0] for h in enumerate(teststep_sheet.row_values(0))}
		# get TestSteps
		for row in range(1, teststep_sheet.nrows):
			n = int(teststep_sheet.cell(row, headers['TestStepNumber']).value)
			# ClassName
			classname = models.ClassName(
				name=teststep_sheet.cell(row, headers['TestStepClass']).value,
				description=f'Imported from "{file_name}"',
			)
			db.session.add(classname)
			db.session.commit()
			app.logger.info(f'Created ClassName id {classname.id} by {user}.')
			# TestCase
			teststeps[n]  = models.TestStepSequence(
				name=f'{file_name}_{row}',
				description=f'Imported from "{file_name}"',
				creator=user,
				classname=classname,
				testcase=[testcases[int(teststep_sheet.cell(row, headers['TestCaseNumber']).value)]],
			)
			db.session.add(teststeps[n])
			db.session.commit()
			app.logger.info(f'Created TestStepSequence id {teststeps[n].id} by {user}.')
	else:
		# create default TestStep
		# ClassName
		classname = models.ClassName(
			name='GC.CLASSES_TESTSTEPMASTER',
			description='Default for TestStep',
		)
		db.session.add(classname)
		db.session.commit()
		app.logger.info(f'Created ClassName id {classname.id} by {user}.')
		# TestStep
		teststeps[1]  = models.TestStepSequence(
			name=f'{file_name}_1',
			description=f'Default for "{file_name}"',
			creator=user,
			classname=classname,
			testcase=[testcases[1]]
		)
		db.session.add(teststeps[1])
		db.session.commit()
		app.logger.info(f'Created TestStepSequence id {teststeps[1].id} by {user}.')

	# create TestStepsExecutions
	if 'TestStepExecution' in xl.sheet_names():
		# get sheet
		teststep_execution_sheet = xl.sheet_by_name('TestStepExecution')
		# get headers as dict
		headers = {h[1]: h[0] for h in enumerate(teststep_execution_sheet.row_values(0))}
		# get TestStepExecutions
		for row in range(1, teststep_execution_sheet.nrows):
			if headers.get('TestStepExecutionNumber'):
				n = int(teststep_execution_sheet.cell(row, headers['TestStepExecutionNumber']).value)
			else:
				# simple format
				n = row
			if headers.get('TestStepNumber'):
				teststep_sequence=teststeps[int(teststep_execution_sheet.cell(row, headers['TestStepNumber']).value)]
			else:
				# simple format
				teststep_sequence=teststeps[1]

			# TestStepExecution
			teststepex  = models.TestStepExecution(
				name=f'{file_name}_{row}',
				description=f'Imported from "{file_name}"',
				creator=user,
				teststep_sequence=teststep_sequence,
				activity_type=getActivityTypeByName(teststep_execution_sheet.cell(row, headers['Activity']).value),
				locator_type=getLocatorTypeByName(teststep_execution_sheet.cell(row, headers['LocatorType']).value),
				locator=teststep_execution_sheet.cell(row, headers['Locator']).value or None,
				value=teststep_execution_sheet.cell(row, headers['Value']).value or None,
				comparision=teststep_execution_sheet.cell(row, headers['Comparison']).value or None,
				value2=teststep_execution_sheet.cell(row, headers['Value2']).value or None,
				timeout=teststep_execution_sheet.cell(row, headers['Timeout']).value or None,
				optional=getBooleanValue(teststep_execution_sheet.cell(row, headers['Optional']).value),
				release=teststep_execution_sheet.cell(row, headers['Release']).value or None,
			)
			db.session.add(teststepex)
			db.session.commit()
			app.logger.info(f'Created TestStepExecution id {teststepex.id} by {user}.')

	return 1













