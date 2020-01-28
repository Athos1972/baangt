import os
from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") or 'sqlite:///testrun.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
	# get the whole bunch of items
	items = {}
	items['testruns'] = Testrun.query.all()
	items['testcase_sequances'] = TestCaseSequence.query.all()
	items['datafiles'] = DataFile.query.all()
	items['testcases'] = TestCase.query.all()
	items['teststep_sequences'] = TestStepSequence.query.all()
	items['teststeps'] = TestStepExecution.query.all()
	return render_template("testrun/index.html", items=items)

@app.route("/<string:item_type>/<int:item_id>") 
def testrun(item_type, item_id):
	# get item by type and id
	if item_type == 'testrun':
		item = Testrun.query.get(item_id)
	elif item_type == 'testcase_sequence':
		item = TestCaseSequence.query.get(item_id)
	elif item_type == 'testcase':
		item = TestCase.query.get(item_id)
	elif item_type == 'teststep_sequences':
		item = TestStepSequence.query.get(item_id)
	elif item_type == 'teststep':
		item = TestStepExecution.query.get(item_id)
	else:
		return 'ERROR: Wrong Item'

	return render_template("testrun/item.html", type=item_type, item=item)


	

if __name__ == '__main__':
	app.run()

