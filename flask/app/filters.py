from . import app

@app.template_filter('name_by_type')
def item_name(item_type, plural=True):
	#
	# get name of the item_type
	#
	
	# categories
	if item_type == 'main':
		name = 'Main Item'

	# main items 
	elif item_type == 'testrun':
		name = 'Testrun'
	elif item_type == 'testcase_sequence':
		name = 'Test Case Sequence'
	elif item_type == 'testcase':
		name = 'Test Case'
	elif item_type == 'teststep_sequence':
		name = 'Test Step Sequence'
	elif item_type == 'teststep':
		name = 'Test Step'
	else:
		# wrong item_type
		return ''

	# check for plurals
	if plural:
		name += 's'

	return name