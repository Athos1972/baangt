
from flask import render_template, redirect, request, url_for
from flask_login import login_required, current_user, login_user, logout_user
from app import app, db, models, forms

@app.route("/")
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
	return render_template("testrun/index.html", items=items)

@app.route("/<string:item_type>/<int:item_id>")
@login_required
def testrun(item_type, item_id):
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

	return render_template("testrun/item.html", type=item_type, item=item)

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
			return redirect(url_for('index'))

	return render_template('testrun/login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()

	return redirect(url_for('login'))
	
