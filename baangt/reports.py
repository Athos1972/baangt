from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, and_
from baangt.base.DataBaseORM import engine, TestrunLog, GlobalAttribute, TestCaseLog, TestCaseSequenceLog, TestCaseField
import baangt.base.GlobalConstants as GC
from jinja2 import Environment, FileSystemLoader
import json
import os
import webbrowser
import uuid

# number of items on history charts
history_items = 10
template_dir = 'templates'

class Report:
	#
	# Parent reports class
	# defines constants and construcor
	#

	def __init__(self):
		self.created = datetime.now()
		self.generate();

	@property
	def path(self):
		return ''	

	def generate(self):
		#
		# report generator
		#

		pass

	def show(self):
		#
		# shows html report
		#

		webbrowser.open(f'file://{self.path}', new=2)


	def template(self, template_name):
		#
		# returns jinja2 template
		#

		file_loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), GC.REPORT_PATH, template_dir))
		env = Environment(loader=file_loader)

		return env.get_template(template_name)


	def chart_figures(self, log):
		#
		# builds json with log statistics
		#

		return {
			'records': log.recordCount,
			'successful': log.statusOk,
			'error': log.statusFailed,
			'paused': log.statusPaused,
		}

	def time_in_seconds(self, time):
		time_int = time.split('.')[0]
		factors = [3600, 60, 1]
		return sum(t*f for t,f in zip(map(int, time_int.split(':')), factors))

	def chart_status(self, log):
		#
		# builds json for Chart.js: log statistics
		#

		return json.dumps({
			'type': 'doughnut',
			'data': {
				'datasets': [{
					'data': [
						log.statusOk,
						log.statusFailed,
						log.statusPaused,
					],
					'backgroundColor': [
						'#52ff52',
						'#ff5252',
						'#bdbdbd',
					],
				}],
				'labels': [
					'Passed',
					'Failed',
					'Paused'
				],
			},
			'options': {
				'legend': {
					'display': False,
				},
			},
		})

	def chart_results(self, logs):
		#
		# builds json for Chart.js: history of log results
		#

		logs = logs[-history_items:]
		empty = history_items - len(logs)

		return json.dumps({
			'type': 'bar',
				'data': {
					'datasets': [
						{
							'data': [x.statusOk for x in logs] + [None]*empty,
							'backgroundColor': '#52ff52',
							'label': 'Passed',
						},
						{
							'data': [x.statusFailed for x in logs] + [None]*empty,
							'backgroundColor': '#ff5252',
							'label': 'Failed',
						},
						{
							'data': [x.statusPaused for x in logs] + [None]*empty,
							'backgroundColor': '#bdbdbd',
							'label': 'Paused',
						},
					],
					'labels': [x.startTime.strftime('%Y-%m-%d %H:%M') for x in logs] + [None]*empty,
				},
				'options': {
					'legend': {
						'display': False,
					},
					'tooltips': {
						'mode': 'index',
						'intersect': False,
					},
					'scales': {
						'xAxes': [{
							'gridLines': {
								'display': False,
								'drawBorder': False,
							},
							'ticks': {
								'display': False,
							},
							'stacked': True,
						}],
						'yAxes': [{
							'gridLines': {
								'display': False,
								'drawBorder': False,
							},
							'ticks': {
								'display': False,
							},
							'stacked': True,
						}],
					},
				},
			})

	def chart_duration(self, logs):
		#
		# builds json for Chart.js: history of log durations
		#

		logs = logs[-history_items:]
		empty = history_items - len(logs)

		return json.dumps({
			'type': 'line',
				'data': {
					'datasets': [{
						'data': [str(x.duration) for x in logs] + [None]*empty,
						'fill': False,
						'borderColor': '#cfd8dc',
						'borderWidth': 1, 
						'pointBackgroundColor': 'transparent',
						'pointBorderColor': '#0277bd',
						'pointRadius': 5,
						'lineTension': 0,
						'label': 'Duration',
					}],
					'labels': [x.startTime.strftime('%Y-%m-%d %H:%M') for x in logs] + [None]*empty,
				},
				'options': {
					'legend': {
						'display': False,
					},
					'tooltips': {
						'mode': 'index',
						'intersect': False,
					},
					'layout': {
						'padding': {
							'top': 10,
							'right': 10,
						},
					},
					'scales': {
						'xAxes': [{
							'gridLines': {
								'display': False,
								'drawBorder': False,
							},
							'ticks': {
								'display': False,
							},
						}],
						'yAxes': [{
							'gridLines': {
								'display': False,
								'drawBorder': False,
							},
							'ticks': {
								'display': False,
							},
						}],
					},
				},
			})


	def chart_testcases(self, logs):
		#
		# builds json for Chart.js: history of log results
		#

		tc = logs[-history_items:]
		empty = history_items - len(tc)

		return json.dumps({
			'type': 'bar',
				'data': {
					'datasets': [
						{
							'data': [self.time_in_seconds(t['duration']) if t['status'] == GC.TESTCASESTATUS_SUCCESS else 0 for t in tc] + [None]*empty,
							'backgroundColor': '#52ff52',
							'label': 'PASSED',
						},
						{
							'data': [self.time_in_seconds(t['duration']) if t['status'] == GC.TESTCASESTATUS_ERROR else 0 for t in tc] + [None]*empty,
							'backgroundColor': '#ff5252',
							'label': 'FAILED',
						},
						{
							'data': [self.time_in_seconds(t['duration']) if t['status'] == GC.TESTCASESTATUS_WAITING else 0 for t in tc] + [None]*empty,
							'backgroundColor': '#bdbdbd',
							'label': 'PAUSED',
						},
					],
					'labels': [t['duration'] for t in tc] + [None]*empty,
				},
				'options': {
					'legend': {
						'display': False,
					},
					'tooltips': {
						'mode': 'index',
						'intersect': False,
					},
					'scales': {
						'xAxes': [{
							'gridLines': {
								'display': False,
								'drawBorder': False,
							},
							'ticks': {
								'display': False,
							},
							'stacked': True,
						}],
						'yAxes': [{
							'gridLines': {
								'display': False,
								'drawBorder': False,
							},
							'ticks': {
								'display': False,
							},
							'stacked': True,
						}],
					},
				},
			})



class Dashboard(Report):

	def __init__(self, name=None, stage=None):
		self.name = name
		self.stage = stage
		super().__init__()


	@property
	def path(self):
		#
		# path to report
		#
		return os.path.join(
			os.path.dirname(__file__),
			GC.REPORT_PATH,
			self.created.strftime('dashboard-%Y%m%d-%H%M%S.html'),
		)


	def generate(self):
		#
		# generates HTML report
		#

		# get jinja2 template
		template = self.template('dashboard.html')

		data = self.get_data() or None
		if data is None:
			error_msg = 'No TestrunLog maches:'
			if self.name:
				error_msg = f'{error_msg} Name "{self.name}"'
				if self.stage:
					  error_msg = f'{error_msg},'
			if self.stage:
				error_msg = f'{error_msg} Stage "{self.stage}"'
			raise ValueError(error_msg)

		# generate report
		with open(self.path, 'w') as f:
			f.write(template.render(
				type='Dashboard',
				data=data,
				created=self.created.strftime('%Y-%m-%d %H:%M:%S'),
				name=self.name,
				stage=self.stage,
			))


	def get_data(self):
		#
		# get data from db for the report
		#

		db = sessionmaker(bind=engine)()
		records = []

		if self.name and self.stage:
			logs = db.query(TestrunLog).order_by(TestrunLog.startTime).filter_by(testrunName=self.name)\
				.filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==self.stage))).all()
			return {'records': [self.build_charts(logs)]}
		
		elif self.name:
			# get Testrun stages
			stages = db.query(GlobalAttribute.value).filter(GlobalAttribute.testrun.has(TestrunLog.testrunName==self.name))\
			.filter_by(name=GC.EXECUTION_STAGE).group_by(GlobalAttribute.value).order_by(GlobalAttribute.value).all()
			stages = [x[0] for x in stages]

			for stage in stages:
				logs = db.query(TestrunLog).order_by(TestrunLog.startTime).filter_by(testrunName=self.name)\
					.filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==stage))).all()
				records.append(self.build_charts(logs, stage=stage))

			return {'records': records}

		elif self.stage:
			# get Testrun names
			names = db.query(TestrunLog.testrunName)\
			.filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==self.stage)))\
			.group_by(TestrunLog.testrunName).order_by(TestrunLog.testrunName).all()
			names = [x[0] for x in names]

			for name in names:
				logs = db.query(TestrunLog).order_by(TestrunLog.startTime).filter_by(testrunName=name)\
					.filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==self.stage))).all()
				records.append(self.build_charts(logs, name=name))

			return {'records': records}

		else:
			# get Testrun names
			names = db.query(TestrunLog.testrunName)\
			.group_by(TestrunLog.testrunName).order_by(TestrunLog.testrunName).all()
			names = [x[0] for x in names]
			stage_set = set()

			for name in names:
				# get Testrun stages
				stages = db.query(GlobalAttribute.value).filter(GlobalAttribute.testrun.has(TestrunLog.testrunName==name))\
				.filter_by(name=GC.EXECUTION_STAGE).group_by(GlobalAttribute.value).order_by(GlobalAttribute.value).all()
				stages = [x[0] for x in stages]
				stage_set.update(stages)

				for stage in stages:
					logs = db.query(TestrunLog).order_by(TestrunLog.startTime).filter_by(testrunName=name)\
						.filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==stage))).all()
					records.append(self.build_charts(logs, name=name, stage=stage))

			return {
				'names': names,
				'stages': list(stage_set),
				'records': records,
			}


	def build_charts(self, logs, name=None, stage=None):
		#
		# builds Chart.js data collections
		#

		name = self.name or name
		stage = self.stage or stage
		
		if logs:
			return {
				'id': f'record-{uuid.uuid4()}',
				'name': name,
				'stage': stage,
				'figures': self.chart_figures(logs[-1]),
				'status': self.chart_status(logs[-1]),
				'results': self.chart_results(logs),
				'duration': self.chart_duration(logs),
			}
		else:
			error_msg = 'No TestrunLog maches:'
			if self.name:
				error_msg = f'{error_msg} Name "{self.name}"'
				if self.stage:
					  error_msg = f'{error_msg},'
			if self.stage:
				error_msg = f'{error_msg} Stage "{self.stage}"'
			raise ValueError(error_msg)



class Summary(Report):

	def __init__(self, id):
		self.id = id
		super().__init__()

	@property
	def path(self):
		#
		# path to report
		#
		return os.path.join(
			os.path.dirname(__file__),
			GC.REPORT_PATH,
			self.created.strftime('summary-%Y%m%d-%H%M%S.html'),
		)

	def generate(self):
		#
		# generates HTML report
		#

		# get jinja2 template
		template = self.template('summary.html')

		# generate report
		with open(self.path, 'w') as f:
			f.write(template.render(
				type='Report',
				data=self.get_data(),
				created=self.created.strftime('%Y-%m-%d %H:%M:%S'),
			))

	def get_data(self):
		#
		# get data from db for the report
		#

		db = sessionmaker(bind=engine)()

		log = db.query(TestrunLog).get(uuid.UUID(self.id).bytes)
		if log is None:
			raise ValueError(f'TestrunLog {self.id} does not exist')

		# collect TestCases and screenshots
		testcases = []
		screenshots = []
		for index, tc in enumerate(db.query(TestCaseLog).filter(TestCaseLog.testcase_sequence.has(TestCaseSequenceLog.testrun_id == log.id))):
			testcases.append({
				'status': db.query(TestCaseField.value).filter_by(name=GC.TESTCASESTATUS).filter(TestCaseField.testcase_id == tc.id).first()[0],
				'duration': db.query(TestCaseField.value).filter_by(name=GC.TIMING_DURATION).filter(TestCaseField.testcase_id == tc.id).first()[0],
			})
			tc_screenshots = db.query(TestCaseField.value).filter_by(name=GC.SCREENSHOTS).filter(TestCaseField.testcase_id == tc.id).first()[0]
			if tc_screenshots:
				for shot in json.loads(tc_screenshots.replace("'", '"')):
					screenshots.append({
						'index': index + 1,
						'path': shot,
					})

		# collect files
		files = [
			{
				'name': 'Log',
				'path': log.logfileName,
			},
			{
				'name': 'Results',
				'path': log.dataFile,
			}
		]

		data = {
			'id': self.id,
			'time': log.startTime.strftime('%Y-%m-%d %H:%M:%S'),
			'name': log.testrunName,
			'figures': self.chart_figures(log),
			'status': self.chart_status(log),
			'testcases': self.chart_testcases(testcases),
			'screenshots': screenshots,
			'files': files,
		}

		return data




		