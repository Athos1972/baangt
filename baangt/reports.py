from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from baangt.base.DataBaseORM import engine, TestrunLog
from jinja2 import Environment, FileSystemLoader
import json
import os
import webbrowser


class Reports:

	path_to_reports = 'reports'


	def __init__(self):
		self.created = datetime.now()
		
	@property
	def data(self):
		#
		# fetches TestrunLogs data
		#

		db = sessionmaker(bind=engine)()

		data = {}

		# get Testrun names
		testrun_names = [item.testrunName for 
			item in db.query(TestrunLog).order_by(TestrunLog.testrunName).group_by(TestrunLog.testrunName).all()]

		for name in testrun_names:
			# build items by testruns
			logs = db.query(TestrunLog).order_by(desc(TestrunLog.startTime)).filter_by(testrunName=name).all()[-10:]
			empty = max(0, 10-len(logs))

			# build charts
			charts = {}

			charts['figures'] = {
				'records': logs[-1].recordCount,
				'successful': logs[-1].statusOk,
				'error': logs[-1].statusFailed,
				'paused': logs[-1].statusPaused,
			}

			# status chart
			charts['status'] = json.dumps({
				'type': 'doughnut',
				'data': {
					'datasets': [{
						'data': [
							logs[-1].statusOk,
							logs[-1].statusFailed,
							logs[-1].statusPaused,
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

			# results chart
			charts['results'] = json.dumps({
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

			# duration chart
			charts['duration'] = json.dumps({
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


			data['-'.join(name.split('.'))] = charts

		db.close()

		return data


	def show_dashboard(self):
		#
		# shows html dashboard
		#

		filename = os.path.join(os.path.dirname(__file__), self.path_to_reports, self.created.strftime('dashboard-%Y%m%d-%H%M%S.html'))
		self.generate_dashboard(filename)
		url = f'file://{filename}'
		webbrowser.open(url, new=2)

	def generate_dashboard(self, filename):
		file_loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), self.path_to_reports, 'templates'))
		env = Environment(loader=file_loader)

		template = env.get_template('dashboard.html')

		with open(filename, 'w') as f:
			f.write(template.render(data=self.data, created=self.created.strftime('%Y-%m-%d %H:%M:%S')))