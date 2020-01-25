import os
from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") or 'sqlite:///testrun.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
	print('***** index')
	testruns = Testrun.query.all()
	print(testruns)
	return render_template("index.html", testruns=testruns)

if __name__ == '__main__':
	app.run()

