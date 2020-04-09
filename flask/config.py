import os


#
# configuration settings
#

class Config(object):
	#
	# secret 
	#
	SECRET_KEY = os.getenv('SECRET_KEY') or 'secret!key'

	#
	# SQL Alchemy
	#
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
    	'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/testrun.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	#
	# Testrun web-service
	#
	TESTRUN_SERVICE_HOST = os.getenv('TESTRUN_SERVICE_HOST') or 'http://127.0.0.1:6000'
	TESTRUN_SERVICE_URI = 'api/json/json'


	
