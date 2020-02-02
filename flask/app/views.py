
from flask import render_template, redirect, flash, request, url_for
from flask_login import login_required, current_user, login_user, logout_user
from app import app, db, models, forms
from datetime import datetime

@app.route('/')
@login_required
def index():
	# get the whole bunch of items
	items = {}
	items['testruns'] = models.Testrun.query.all()
	items['testcase_sequances'] = models.TestCaseSequence.query.all()
	#items['datafiles'] = models.DataFile.query.all()
	items['testcases'] = models.TestCase.query.all()
	items['teststep_sequences'] = models.TestStepSequence.query.all()
	items['teststeps'] = models.TestStepExecution.query.all()

	return render_template('testrun/index.html', items=items)

@app.route('/<string:item_type>/<int:item_id>', methods=['GET', 'POST'])
@login_required
def get_item(item_type, item_id):
	# get item by type and id
	if item_type == 'testrun':
		item = models.Testrun.query.get(item_id)
	elif item_type == 'testcase_sequence':
		item = models.TestCaseSequence.query.get(item_id)
	elif item_type == 'testcase':
		item = models.TestCase.query.get(item_id)
	elif item_type == 'teststep_sequence':
		item = models.TestStepSequence.query.get(item_id)
	elif item_type == 'teststep':
		item = models.TestStepExecution.query.get(item_id)
	else:
		return 'ERROR: Wrong Item'

	


	return render_template('testrun/item.html', type=item_type, item=item)


@app.route('/<string:item_type>/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_type, item_id):
	#
	# delete item
	#
	if request.method == 'POST':
		# get item by type and id
		if item_type == 'testrun':
			item = models.Testrun.query.get(item_id)
		elif item_type == 'testcase_sequence':
			item = models.TestCaseSequence.query.get(item_id)
		elif item_type == 'testcase':
			item = models.TestCase.query.get(item_id)
		elif item_type == 'teststep_sequence':
			item = models.TestStepSequence.query.get(item_id)
		elif item_type == 'teststep':
			item = models.TestStepExecution.query.get(item_id)
		else:
			return 'ERROR: Wrong Item'

		db.session.delete(item)
		db.session.commit()
		flash(f"Item '{item.name}' successfully deleted.")
		return redirect(url_for('index'))

	return 'ERROR: Wring request method'


@app.route('/<string:item_type>/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_type, item_id):
	#
	# edit item
	#
	if item_type == 'testrun':
		item = models.Testrun.query.get(item_id)
		form = forms.TestrunCreateForm.new()
		if request.method == 'GET':
			form.testcase_sequences.data = [f'{x.id}' for x in item.testcase_sequences]
	elif item_type == 'testcase_sequence':
		item = models.TestCaseSequence.query.get(item_id)
		form = forms.TestCaseSequenceCreateForm.new()
		if request.method == 'GET':
			form.classname.data = f'{item.classname.id}'
			form.datafiles.data = [f'{x.id}' for x in item.datafiles]
			form.testcases.data = [f'{x.id}' for x in item.testcases]
	elif item_type == 'testcase':
		item = models.TestCase.query.get(item_id)
		form = forms.TestCaseCreateForm.new()
		if request.method == 'GET':
			form.classname.data = f'{item.classname.id}'
			form.browser_type.data = f'{item.browser_type.id}'
			form.testcase_type.data = f'{item.testcase_type.id}'
			form.testcase_stepsequences.data = [f'{x.id}' for x in item.teststep_sequences]
	elif item_type == 'teststep_sequence':
		item = models.TestStepSequence.query.get(item_id)
		form = forms.TestStepSequenceCreateForm.new()
		if request.method == 'GET':
			form.classname.data = f'{item.classname.id}'
			form.teststeps.data =[f'{x.id}' for x in item.teststeps]
	elif item_type == 'teststep':
		item = models.TestStepExecution.query.get(item_id)
		form = forms.TestStepCreateForm.new()
		if request.method == 'GET':
			form.activity_type.data = f'{item.activity_type.id}'
			form.locator_type.data = f'{item.locator_type.id}'
	else:
		flash('ERROR: Wrong Item Type')
		return None

	if request.method == 'GET':
		form.name.data = item.name
		form.description.data = item.description

	if  form.validate_on_submit():
		# update item data
		item.name = form.name.data
		item.description = form.description.data
		# testrun
		if item_type == 'testrun':
			item.editor = current_user
			item.edited = datetime.utcnow()
			item.testcase_sequences=[models.TestCaseSequence.query.get(int(x)) for x in form.testcase_sequences.data]
		# testcase sequence
		elif item_type == 'testcase_sequence':
			item.editor = current_user
			item.edited = datetime.utcnow()
			item.classname = models.ClassName.query.get(int(form.classname.data))
			item.datafiles = [models.DataFile.query.get(int(x)) for x in form.datafiles.data]
			item.testcases = [models.TestCase.query.get(int(x)) for x in form.testcases.data]
		# testcase
		elif item_type == 'testcase':
			item.editor = current_user
			item.edited = datetime.utcnow()
			item.classname = models.ClassName.query.get(int(form.classname.data))
			item.browser_type = models.BrowserType.query.get(int(form.browser_type.data))
			item.testcase_type = models.TestCaseType.query.get(int(form.testcase_type.data))
			item.teststep_sequences = [models.TestStepSequence.query.get(int(x)) for x in form.testcase_stepsequences.data]
		# step sequence
		elif item_type == 'teststep_sequence':
			item.editor = current_user
			item.edited = datetime.utcnow()
			item.classname = models.ClassName.query.get(int(form.classname.data))
			item.teststeps = [models.TestStepExecution.query.get(int(x)) for x in form.teststeps.data]
		# test step
		elif item_type == 'teststep':
			item.editor = current_user
			item.edited = datetime.utcnow()
			item.activity_type = models.ActivityType.query.get(int(form.activity_type.data))
			item.locator_type = models.LocatorType.query.get(int(form.locator_type.data))
			

		# update item in db
		db.session.commit()
		flash(f"Item '{item.name}' successfully updated.")
		return redirect(url_for('index'))


	return render_template('testrun/edit_item.html', type=item_type, item=item, form=form)





@app.route('/<string:item_type>/new', methods=['GET', 'POST'])
@login_required
def new_item(item_type):
	#
	# create new item
	#
	if item_type == 'testrun':
		form = forms.TestrunCreateForm.new()
	elif item_type == 'testcase_sequence':
		form = forms.TestCaseSequenceCreateForm.new()
	elif item_type == 'testcase':
		form = forms.TestCaseCreateForm.new()
	elif item_type == 'teststep_sequence':
		form = forms.TestStepSequenceCreateForm.new()
	elif item_type == 'teststep':
		form = forms.TestStepCreateForm.new()
	else:
		flash('ERROR: Wrong Item Type')
		return None

	if form.validate_on_submit():
		# create new item
		# testrun
		if item_type == 'testrun':
			item = models.Testrun(
				name=form.name.data,
				description=form.description.data,
				creator=current_user,
				testcase_sequences=[models.TestCaseSequence.query.get(int(x)) for x in form.testcase_sequences.data],
			)
		# testcase sequence
		elif item_type == 'testcase_sequence':
			item = models.TestCaseSequence(
				name=form.name.data,
				description=form.description.data,
				creator=current_user,
				classname=models.ClassName.query.get(int(form.classname.data)),
				datafiles=[models.DataFile.query.get(int(x)) for x in form.datafiles.data],
				testcases=[models.TestCase.query.get(int(x)) for x in form.testcases.data],
			)
		# testcase
		elif item_type == 'testcase':
			item = models.TestCase(
				name=form.name.data,
				description=form.description.data,
				creator=current_user,
				classname=models.ClassName.query.get(int(form.classname.data)),
				browser_type=models.BrowserType.query.get(int(form.browser_type.data)),
				testcase_type=models.TestCaseType.query.get(int(form.testcase_type.data)),
				teststep_sequences=[models.TestStepSequence.query.get(int(x)) for x in form.testcase_stepsequences.data],
			)
		# step sequence
		elif item_type == 'teststep_sequence':
			item = models.TestStepSequence(
				name=form.name.data,
				description=form.description.data,
				creator=current_user,
				classname=models.ClassName.query.get(int(form.classname.data)),
				teststeps=[models.TestStepExecution.query.get(int(x)) for x in form.teststeps.data],
			)
		# test step
		elif item_type == 'teststep':
			item = models.TestStepExecution(
				name=form.name.data,
				description=form.description.data,
				creator=current_user,
				activity_type=models.ActivityType.query.get(int(form.activity_type.data)),
				locator_type=models.LocatorType.query.get(int(form.locator_type.data)),
			)

		# save item to db
		db.session.add(item)
		db.session.commit()
		flash(f"Item '{item.name}' successfully created.")
		return redirect(url_for('index'))

	return render_template('testrun/create_item.html', type=item_type, form=form)

#
# user authentication
#

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = forms.SingupForm()
	if form.validate_on_submit():
		# create user
		user = models.User(username=form.username.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		# login
		login_user(user, remember=True)
		flash(f'User {user.username.capitalize()} successfully created!')
		return redirect(url_for('index'))

	return render_template('testrun/signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = forms.LoginForm()
	if form.validate_on_submit():
		user = models.User.query.filter_by(username=form.username.data).first()
		if user and user.verify_password(form.password.data):
			login_user(user, remember=True)
			flash(f'Welcome {user.username.capitalize()}!')
			return redirect(url_for('index'))

	return render_template('testrun/login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()

	return redirect(url_for('login'))
	
