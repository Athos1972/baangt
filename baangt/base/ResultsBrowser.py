from sqlalchemy import create_engine, desc, and_
from sqlalchemy.orm import sessionmaker
from baangt.base.DataBaseORM import DATABASE_URL, TestrunLog, GlobalAttribute, TestCaseLog, TestCaseSequenceLog, TestCaseField
from baangt.base.ExportResults.ExportResults import ExcelSheetHelperFunctions
from baangt.base.PathManagement import ManagedPaths
import baangt.base.GlobalConstants as GC
import uuid
from datetime import datetime
from xlsxwriter import Workbook
import logging
import os
import json
import re
import uuid
import time # time tracker

logger = logging.getLogger("pyC")

class QuerySet:

    # flags
    SIZE_TCS = 0
    SIZE_TC = 1

    def __init__(self):
        self.data = None

    def __del__(self):
        del self.data

    @property
    def length(self):
        return len(self.data)

    def set(self, data):
        self.data = list(data)

    def names(self):
        return {tr.testrunName for tr in self.data}

    def all(self):
        return (tr for tr in self.data)

    def filter(self, tr_name, tcs_index=None, tc_index=None):
        #
        # returns generator of filtered query_set
        #

        if tcs_index is None:
            return filter(lambda tr: tr.testrunName == tr_name, self.data)

        if tc_index is None:
            return filter(lambda tr: tr.testrunName == tr_name and len(tr.testcase_sequences) > tcs_index, self.data)

        return filter(
            lambda tr: tr.testrunName == tr_name and len(tr.testcase_sequences) > tcs_index \
                and len(tr.testcase_sequences[tcs_index].testcases) > tc_index,
            self.data,
        )

    def max_size(self, tr_name, tcs_index=None):
        #
        # returns the max number of 
        # tcs_index is None: testcase sequences within the testruns in query_set
        # tcs_index is a number: testcases within specified testcase sequence of all testruns in db
        #

        # test case sequences
        if tcs_index is None:
            return max(map(lambda tr: len(tr.testcase_sequences), self.filter(tr_name=tr_name)))

        # test cases
        return max(map(lambda tr: len(tr.testcase_sequences[tcs_index].testcases), self.filter(tr_name=tr_name, tcs_index=tcs_index)))

    def tr_avg_duration(self, tr_name):
        duration = 0
        quantity = 0
        for d in (tr.duration for tr in self.filter(tr_name) if tr.duration):
            duration += d
            quantity += 1

        if quantity > 0:
            return round(duration/quantity, 2)

        return None

    def tc_avg_duration(self, tr_name, indexes):
        durations = map(
            lambda tr: tr.testcase_sequences[indexes[0]].testcases[indexes[1]].duration,
            self.filter(tr_name, tcs_index=indexes[0], tc_index=indexes[1]),
        )

        duration = 0
        quantity = 0
        for d in durations:
            if d:
                duration += d
                quantity += 1

        if quantity > 0:
            return round(duration/quantity, 2)

        return None


class ExportSheet:

    def __init__(self, sheet, header_format):
        self.sheet = sheet
        self.line = 1 # current line
        self.column = 0
        self.header_map = {}
        self.header_format = header_format

    def set_header_format(self, header_format):
        self.header_format = header_format

    def hr(self):
        self.line += 1

    def header(self, headers):
        for header in headers:
            self.sheet.write(0, self.column, header, self.header_format)
            self.header_map[header] = self.column
            self.column += 1

    def add_header(self, header):
        if not header in self.header_map:
            self.sheet.write(0, self.column, header, self.header_format)
            self.header_map[header] = self.column
            self.column += 1

    def row(self, row_data):
        for col, data in enumerate(row_data):
            self.sheet.write(self.line, col, data.get('value'), data.get('format'))
        self.line += 1

    def new_row(self, row_data):
        self.line += 1
        for col, data in enumerate(row_data):
            self.sheet.write(self.line, col, data.get('value'), data.get('format'))

    def by_header(self, header, value):
        self.add_header(header)
        self.sheet.write(self.line, self.header_map[header], value)




class ResultsBrowser:

    def __init__(self, db_url=None):
        # setup db engine
        if db_url:
            engine = create_engine(db_url)
        else:
            engine = create_engine(DATABASE_URL)
        self.db = sessionmaker(bind=engine)()
        # result query set
        self.query_set = QuerySet()
        # query filters
        self.filters = {}
        # path management
        self.managedPaths = ManagedPaths()
        logger.info(f'Initiated with DATABASE_URL: {db_url if db_url else DATABASE_URL}')

    def __del__(self):
        self.db.close()

    def name_list(self):
        names = self.db.query(TestrunLog.testrunName).group_by(TestrunLog.testrunName).order_by(TestrunLog.testrunName)
        return [x[0] for x in names]

    def stage_list(self):
        stages = self.db.query(GlobalAttribute.value).filter_by(name=GC.EXECUTION_STAGE)\
            .group_by(GlobalAttribute.value).order_by(GlobalAttribute.value)
        return [x[0] for x in stages]

    def globals_names(self):
        names = self.db.query(GlobalAttribute.name).group_by(GlobalAttribute.name).order_by(GlobalAttribute.name)
        return [x[0] for x in names]

    def globals_values(self, name):
        values = self.db.query(GlobalAttribute.value).filter_by(name=name).group_by(GlobalAttribute.value).order_by(GlobalAttribute.value)
        return [x[0] for x in values]

    def query(self, name=None, stage=None, start_date=None, end_date=None, global_settings={}):
        #
        # get TestrunLogs from db
        #

        # store filters
        self.filters = {
            'name': name,
            'stage': stage,
            'start_date': start_date,
            'end_date': end_date,
            'globals': global_settings,
        }

        # get records
        logger.info(f'Quering: name={name}, stage={stage}, dates=[{start_date} - {end_date}], globals={global_settings}')
        records = self.db.query(TestrunLog).order_by(TestrunLog.startTime)

        # filter by name
        if name:
            records = records.filter_by(testrunName=name)

        # filter bay dates
        if start_date:
            records = records.filter(TestrunLog.startTime >= start_date)

        if end_date:
            records = records.filter(TestrunLog.endTime <= end_date)

        # filter by globals
        if stage:
            records = records.filter(TestrunLog.globalVars.any(and_(
                GlobalAttribute.name == GC.EXECUTION_STAGE,
                GlobalAttribute.value == stage,
            )))

        for key, value in global_settings.items():
            records = records.filter(TestrunLog.globalVars.any(and_(
                GlobalAttribute.name == key,
                GlobalAttribute.value == value,
            )))

        self.query_set.set(records)

        logger.info(f'Number of found records: {self.query_set.length}')

    def filter_to_str(self, key):
        #
        # get filter value as str
        #

        value = self.filters.get(key)
        if value:
            return str(value)

        # undefined values
        if key == 'end_date':
            return datetime.now().strftime('%Y-%m-%d')
        if key == 'start_date':
            return 'None'
        return 'All'

    def filename(self, extention):
        #
        # generate filename for exports
        #

        filename = '_'.join([
            'TestrunLogs',
            self.filter_to_str('name'),
            self.filter_to_str('stage'),
            self.filter_to_str('start_date'),
            self.filter_to_str('end_date'),
            'globals' if self.filters.get('globals') else 'None',
        ])
        return f'{filename}.{extention}'
            
    def export(self):
        #
        # exports the query set to xlsx
        #

        # initialize workbook
        path_to_file = self.managedPaths.getOrSetDBExportPath().joinpath(self.filename('xlsx'))
        workbook = Workbook(str(path_to_file))

        # set labels
        labels = {
            'testrun': 'TestRun',
            'testcase_sequence': 'Test Case Sequence',
            'testcase': 'Test Case',
            'stage': 'Stage',
            'duration': 'Avg. Duration',
            'globals': 'Global Settings',
        }

        # set output headers
        base_headers = [
            'Testrun ID',
            'TestCase ID',
            'TestCase Number',
        ]

        base_fields = [
            GC.EXECUTION_STAGE,
            GC.TESTCASESTATUS,
            GC.TIMING_DURATION,
        ]
       
        # define cell formats
        cformats = {
            'bg_red': workbook.add_format({'bg_color': 'red'}),
            'bg_green': workbook.add_format({'bg_color': 'green'}),
            'bg_yellow': workbook.add_format({'bg_color': 'yellow'}),
            'font_bold': workbook.add_format({'bold': True}),
            'font_bold_italic': workbook.add_format({'bold': True, 'italic': True}),
        }

        # map status styles
        status_style = {
            GC.TESTCASESTATUS_SUCCESS: cformats.get('bg_green'),
            GC.TESTCASESTATUS_ERROR: cformats.get('bg_red'),
            GC.TESTCASESTATUS_WAITING: None,
        }

        # create sheets
        sheets = {
            'summary': ExportSheet(workbook.add_worksheet('Summary'), cformats.get('font_bold')),
            'output': ExportSheet(workbook.add_worksheet('Output'), cformats.get('font_bold')),
        }

        # write summary titles
        time_start = time.time() # -------------------------> time tracker
        # title
        sheets['summary'].sheet.set_column(first_col=0, last_col=0, width=18)
        sheets['summary'].sheet.set_column(first_col=1, last_col=1, width=10)
        sheets['summary'].header([f'{labels.get("testrun")}s Summary'])
        
        # parameters
        for key in self.filters:
            if key != 'globals':
                sheets['summary'].row([
                    {
                        'value': key,
                        'format': cformats.get('font_bold'),
                    },
                    {
                        'value': self.filter_to_str(key),
                    },
                ])
        # global settings
        if self.filters.get('globals'):
            sheets['summary'].hr()
            sheets['summary'].row([
                {
                    'value': f"{labels.get('globals')}:",
                    'format': cformats.get('font_bold'),
                },
            ])
            for name, value in self.filters.get('globals').items():
                sheets['summary'].row([
                    {
                        'value': name,
                    },
                    {
                        'value': value,
                    },
                ])

        # write output titles
        sheets['output'].header(base_headers + base_fields)

        # write items
        # testruns
        for tr_name in self.query_set.names():
            logger.info(f'Exporting Tetsrun "{tr_name}": {len(list(self.query_set.filter(tr_name)))} records')
            # testrun name
            sheets['summary'].hr()
            sheets['summary'].row([
                {
                    'value': labels.get('testrun'),
                    'format': cformats.get('font_bold'),
                },
                {
                    'value': tr_name,
                }
            ])
            
            # average duration
            sheets['summary'].row([
                {
                    'value': labels.get('duration'),
                    'format': cformats.get('font_bold'),
                },
                {
                    'value': self.query_set.tr_avg_duration(tr_name),
                }
            ])

            #

            # testcase sequences
            for tcs_index in range(self.query_set.max_size(tr_name)):
                tcs_number = tcs_index+1
                # testcase sequence
                sheets['summary'].hr()
                sheets['summary'].row([
                    {
                        'value': labels.get('testcase_sequence'),
                        'format': cformats.get('font_bold'),
                    },
                    {
                        'value': tcs_number,
                    }
                ])

                # test cases
                # header
                tc_num_max = self.query_set.max_size(tr_name, tcs_index=tcs_index)
                sheets['summary'].hr()
                sheets['summary'].row(
                    [
                        {
                            'value': 'Run Date',
                            'format': cformats.get('font_bold_italic'),
                        },
                        {
                            'value': labels.get('testcase'),
                            'format': cformats.get('font_bold_italic'),
                        },
                    ] + [{} for i in range(1, tc_num_max)] +[
                        {
                            'value': labels.get('stage'),
                            'format': cformats.get('font_bold_italic'),
                        },
                        {
                            'value': f'{labels.get("testrun")} ID',
                            'format': cformats.get('font_bold_italic'),
                        },
                    ]
                )
                sheets['summary'].row(
                    [{}] + [{'value': i} for i in range(tc_num_max)]
                )

                durations =  [[.0,0] for i in range(tc_num_max)]
                for tr_index, tr in enumerate(self.query_set.filter(tr_name, tcs_index)):
                    tc_num = len(tr.testcase_sequences[tcs_index].testcases)
                    status_row = [{'value': tr.startTime.strftime('%Y-%m-%d %H:%M:%S')}]

                    # query fields
                    data = self.db.query(
                        TestCaseField.name,
                        TestCaseField.value,
                        TestCaseLog.number,
                        TestCaseLog.id,
                    ).join(TestCaseField.testcase).join(TestCaseLog.testcase_sequence).join(TestCaseSequenceLog.testrun)\
                    .filter(and_(TestrunLog.id == tr.id, TestCaseSequenceLog.number == tcs_number)).order_by(TestCaseLog.number)
                    tc_id_cur = None
                    tr_stage = None
                    for name, value, tc_index, tc_id in data.yield_per(500):
                        # summary data
                        if name == GC.TESTCASESTATUS:
                            status_row.append({
                                'value': value,
                                'format': status_style.get(value),
                            })
                        elif name == GC.EXECUTION_STAGE:
                            tr_stage = value
                        elif name == GC.TIMING_DURATION:
                            m = re.search(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', value)
                            if m:
                                factors = {
                                    'hours': 3600,
                                    'minutes': 60,
                                    'seconds': 1,
                                }
                                durations[tc_index-1][0] += sum([factors[key]*float(value) for key, value in m.groupdict().items()])
                                durations[tc_index-1][1] += 1
                            
                        # write to output
                        # write testcase
                        if tc_id != tc_id_cur:
                            tc_id_cur = tc_id
                            sheets['output'].new_row([
                                {
                                    'value': str(tr),
                                },
                                {
                                    'value': str(uuid.UUID(bytes=tc_id)),
                                },
                                {
                                    'value': tc_index,
                                },
                            ])

                        #field
                        sheets['output'].by_header(name, value)

                    # write state row to summary sheet
                    sheets['summary'].row(
                        status_row + [{} for i in range(tc_num, tc_num_max)] + [
                            {
                                'value': tr_stage,
                            },
                            {
                                'value': str(tr),
                            },
                        ]
                    )

                # avg durations
                sheets['summary'].row(
                    [
                        {
                            'value': labels.get('duration'),
                            'format': cformats.get('font_bold_italic'),
                        },
                    ] + [{'value': d} for d in map(lambda d: round(d[0]/d[1], 2) if d[1] > 0 else .0, durations)]
                )
        
        # autowidth output columns
        for col in range(len(base_headers)+len(base_fields)):
            ExcelSheetHelperFunctions.set_column_autowidth(sheets['output'].sheet, col)

        workbook.close()

        execution_time = round(time.time()-time_start, 2)
        logger.info(f'Query successfully exported to {path_to_file} in {execution_time} seconds')

        return path_to_file
    

    def export_txt(self):
        #
        # export to txt
        #

        path_to_file = self.managedPaths.getOrSetDBExportPath().joinpath(self.filename('txt'))

        # set labels
        labels = {
            'testrun': 'TestRun',
            'testcase_sequence': 'Test Case Sequence',
            'testcase': 'Test Case',
            'stage': 'Stage',
            'duration': 'Avg. Duration',
        }

        # write data
        with open(path_to_file, 'w') as f:
            # title
            f.write(f'{labels.get("testrun")}s Summary\n\n')
            
            # parameters
            for key in self.filters:
                f.write(f'{key}\t{self.filter_to_str(key)}\n')

            # testruns
            for tr_name in self.query_set.names():
                print(f'*** Tetsrun "{tr_name}"')
                # testrun name
                f.write(f'\n{labels.get("testrun")}: {tr_name}\n')
                
                # average duration
                f.write(f'{labels.get("duration")}: {self.query_set.tr_avg_duration(tr_name)}\n')

                # testcase sequences
                for tcs_index in range(self.query_set.max_size(tr_name)):
                    print(f'**** TestCaseSequence-{tcs_index}')
                    # testcase sequence
                    f.write(f'\n{labels.get("testcase_sequence")}: {tcs_index}\n\n')

                    # test cases
                    # header
                    tc_num = self.query_set.max_size(tr_name, tcs_index=tcs_index)
                    f.write(f'{"Run Date":20}{labels.get("testcase"):8}')
                    f.write(' '*7)
                    f.write((' '*8)*(tc_num-2))
                    f.write(f'{labels.get("stage"):8}{labels.get("testcase")} ID\n')
                    f.write(' '*20)            
                    for tc_index in range(tc_num):
                        f.write(f'{tc_index:<8}')
                    f.write('\n')

                    # testcase status
                    tr_counter = 1 
                    for tr in self.query_set.filter(tr_name, tcs_index):
                        print(f'***** TestRun {tr_counter}: {len(tr.testcase_sequences[tcs_index].testcases)} testcases')
                        tr_counter += 1
                        f.write(f'{tr.startTime.strftime("%Y-%m-%d %H:%M:%S"):20}')
                        for tc in tr.testcase_sequences[tcs_index].testcases:
                            f.write(f'{tc.status:8}')
                        # tail
                        print(f'{tc_num} - {len(tr.testcase_sequences[tcs_index].testcases)} = {(tc_num-len(tr.testcase_sequences[tcs_index].testcases))}')
                        f.write((' '*8)*(tc_num-len(tr.testcase_sequences[tcs_index].testcases)))
                        f.write(f'{tr.stage:8}{tr}\n')

                    # average durations
                    f.write(f'{labels.get("duration"):20}')
                    for tc_index in range(tc_num):
                        f.write(f'{self.query_set.tc_avg_duration(tr_name, (tcs_index, tc_index)):8}')

        logger.info(f'Query successfully exported to {path_to_file}')

        return path_to_file



