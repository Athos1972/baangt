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
	return render_template("index.html", items=items)

@app.route("/testrun/<int:testrun_id>") 
def testrun(testrun_id):
	# get testrun by id
	items['testruns'] = Testrun.query.get(testrun_id)
	return render_template("testrun.html", testrun=testrun)
	

if __name__ == '__main__':
	app.run()

