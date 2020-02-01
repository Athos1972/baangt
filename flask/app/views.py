
from flask import render_template, redirect, flash, request, url_for
from flask_login import login_required, current_user, login_user, logout_user
from app import app, db, models, forms

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

	# delete item
	if request.method == 'POST':
		db.session.delete(item)
		db.session.commit()
		flash(f"Item '{item.name}' successfully deleted.")
		return redirect(url_for('index'))


	return render_template('testrun/item.html', type=item_type, item=item)

@app.route('/<string:item_type>/new', methods=['GET', 'POST'])
@login_required
def new_item(item_type):
	# get form by item type
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
	
