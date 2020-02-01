from app import models

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
	print(models.TestStepExecution.query.all())
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