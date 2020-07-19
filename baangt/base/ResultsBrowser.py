from sqlalchemy import create_engine, desc, and_
from sqlalchemy.orm import sessionmaker
from baangt.base.DataBaseORM import DATABASE_URL, engine, TestrunLog, GlobalAttribute, TestCaseLog, TestCaseSequenceLog, TestCaseField
from baangt.base.ExportResults.ExportResults import ExcelSheetHelperFunctions
from baangt.base.PathManagement import ManagedPaths
import baangt.base.GlobalConstants as GC
import uuid
from datetime import datetime
from xlsxwriter import Workbook
import logging
import os

logger = logging.getLogger("pyC")

class ResultsBrowser:

    def __init__(self, db_url=None):
        # setup db engine
        if db_url:
            engine = create_engine(db_url)
        else:
            engine = create_engine(DATABASE_URL)
        self.db = sessionmaker(bind=engine)()
        # result query set
        self.query_set = []
        # tag of the current query set
        self.tag = None
        # set of stages
        self.stages = None
        # path management
        self.managedPaths = ManagedPaths()
        logger.info(f'Initiated with DATABASE_URL: {db_url if db_url else DATABASE_URL}')

    def __del__(self):
        self.db.close()


    def average_duration(self, testcase_sequence=None, testcase=None):
        #
        # average durationof the testruns or particular testcases within the query set
        # testcase values:
        #   None: the whole testrun
        #   integer: the specified testcase 
        #

        if testcase_sequence is None:
            # whole testrun
            durations = [tr.duration for tr in self.query_set]
        elif testcase is None:
            # specified testcase sequence
            durations = [tr.testcase_sequences[testcase_sequence].duration for tr in self.query_set if testcase_sequence < len(tr.testcase_sequences)]
        else:
            # specific testcase
            durations = [
                tr.testcase_sequences[testcase_sequence].testcases[testcase].duration for tr in self.query_set \
                if testcase_sequence < len(tr.testcase_sequences) and testcase < len(tr.testcase_sequences[testcase_sequence].testcases)
            ]

        return round(sum(durations) / len(durations), 2)


    def size(self, testcase_sequence=None):
        #
        # the maximum number of testcase sequences
        #

        # test case sequences
        if testcase_sequence is None:
            return max([len(tr.testcase_sequences) for tr in self.query_set])

        # test cases
        return max([len(tr.testcase_sequences[testcase_sequence].testcases) for tr in self.query_set])


    def name_list(self):
        names = self.db.query(TestrunLog.testrunName).group_by(TestrunLog.testrunName).order_by(TestrunLog.testrunName).all()
        return [x[0] for x in names]


    def stage_list(self):
        stages = self.db.query(GlobalAttribute.value).filter_by(name=GC.EXECUTION_STAGE)\
            .group_by(GlobalAttribute.value).order_by(GlobalAttribute.value).all()
        return [x[0] for x in stages]


    def get(self, ids):
        #
        # get TestrunLogs by id (list of uuid string)
        #

        # set the tag
        self.tag = {
            'Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        # get records by id
        records = []
        for id in ids:
            records.append(self.db.query(TestrunLog).get(uuid.UUID(id).bytes))

        self.query_set = records


    def query(self, name=None, stage=None, start_date=None, end_date=None):
        #
        # get TestrunLogs by name, stage and dates
        #

        # set the tag
        self.tag = {
            'Name': name,
            'Stage': stage,
            'Date from': start_date.strftime('%Y-%m-%d') if start_date else None,
            'Date to': end_date.strftime('%Y-%m-%d') if end_date else None,
        }

        # get records
        records = []
        logger.info(f'Quering: name={self.tag.get("Name")}, stage={self.tag.get("Stage")}, dates=({self.tag.get("Date from")}, {self.tag.get("Date to")})')

        # filter by name and stage
        if name and stage:
            self.stages = {stage}
            records = self.db.query(TestrunLog).order_by(TestrunLog.startTime).filter_by(testrunName=name)\
                .filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==stage))).all()
        
        # filter by name
        elif name:
            # get Testrun stages
            stages = self.db.query(GlobalAttribute.value).filter(GlobalAttribute.testrun.has(TestrunLog.testrunName==name))\
            .filter_by(name=GC.EXECUTION_STAGE).group_by(GlobalAttribute.value).order_by(GlobalAttribute.value).all()
            self.stages = {x[0] for x in stages}

            for s in self.stages:
                logs = self.db.query(TestrunLog).order_by(TestrunLog.startTime).filter_by(testrunName=name)\
                    .filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==s))).all()
                records.extend(logs)

        # filter by stage
        elif stage:
            self.stages = {stage}
            # get Testrun names
            names = self.db.query(TestrunLog.testrunName)\
            .filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==stage)))\
            .group_by(TestrunLog.testrunName).order_by(TestrunLog.testrunName).all()
            names = [x[0] for x in names]

            for n in names:
                logs = self.db.query(TestrunLog).order_by(TestrunLog.startTime).filter_by(testrunName=n)\
                    .filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==stage))).all()
                records.extend(logs)

        # get all testruns ordered by name and stage
        else:
            # get Testrun names
            names = self.db.query(TestrunLog.testrunName).group_by(TestrunLog.testrunName).order_by(TestrunLog.testrunName).all()
            names = [x[0] for x in names]
            
            self.stages = set()
            for n in names:
                # get Testrun stages
                stages = self.db.query(GlobalAttribute.value).filter(GlobalAttribute.testrun.has(TestrunLog.testrunName==n))\
                .filter_by(name=GC.EXECUTION_STAGE).group_by(GlobalAttribute.value).order_by(GlobalAttribute.value).all()
                stages = [x[0] for x in stages]
                self.stages.update(stages)

                for s in stages:
                    logs = self.db.query(TestrunLog).order_by(TestrunLog.startTime).filter_by(testrunName=n)\
                        .filter(TestrunLog.globalVars.any(and_(GlobalAttribute.name==GC.EXECUTION_STAGE, GlobalAttribute.value==s))).all()
                    records.extend(logs)
            
        # filter by dates
        if start_date and end_date:
            self.query_set = [log for log in records if log.startTime > start_date and log.startTime < end_date]
        elif start_date:
            self.query_set = [log for log in records if log.startTime > start_date]
        elif end_date:
            self.query_set = [log for log in records if log.startTime < end_date]
        else:
            self.query_set = records

        logger.info(f'Number of found records: {len(self.query_set)}')


    def export(self):
        #
        # export the query set to xlsx
        #

        # set labels
        labelTetsrun = 'TestRun'
        labelTestCaseSequence = 'Test Case Sequence'
        labelTestCase = 'Test Case'
        labelAvgDuration = 'Avg. Duration'

        # initialize workbook
        path_to_file = self.managedPaths.getOrSetDBExportPath().joinpath(f'TestrunLogs_{"_".join(list(map(str, self.tag.values())))}.xlsx')
        workbook = Workbook(str(path_to_file))
        
        # define cell formats
        # green background
        cellFormatGreen = workbook.add_format({'bg_color': 'green'})
        #cellFormatGreen.set_bg_color('green')
        # red background
        cellFormatRed = workbook.add_format({'bg_color': 'red'})
        #cellFormatRed.set_bg_color('red')
        # bold font
        cellFormatBold = workbook.add_format({'bold': True})
        # bold and italic font
        cellFormatBoldItalic = workbook.add_format({'bold': True, 'italic': True})

        # summary tab
        sheet = workbook.add_worksheet('Summary')
        sheet.set_column(first_col=0, last_col=0, width=18)
        #sheet.set_column(first_col=1, last_col=1, width=12)
        # title
        sheet.write(0, 0, f'{labelTetsrun}s Summary', cellFormatBold)
        # parameters
        line = 1
        for key, value in self.tag.items():
            line += 1
            sheet.write(line, 0, key)#, cellFormatBold)
            sheet.write(line, 1, value)

        # average duration
        line += 2
        sheet.write(line, 0, labelAvgDuration, cellFormatBold)
        sheet.write(line, 1, self.average_duration())

        # testcases
        line += 2
        sheet.write(line, 0, f'{labelTestCase}s', cellFormatBold)
        status_style = {
            GC.TESTCASESTATUS_SUCCESS: cellFormatGreen,
            GC.TESTCASESTATUS_ERROR: cellFormatRed,
            GC.TESTCASESTATUS_WAITING: None,
        }
        for tcs_index in range(self.size()):
            # testcase sequence
            line += 1
            sheet.write(line, 0, labelTestCaseSequence)
            sheet.write(line, 1, tcs_index)
            line += 1
            sheet.write(line, 0, labelAvgDuration)
            sheet.write(line, 1, self.average_duration(testcase_sequence=tcs_index))
            # test cases
            # header
            line += 2
            sheet.write(line, 0, f'{labelTetsrun} Date', cellFormatBoldItalic)
            sheet.write(line, 1, labelTestCase, cellFormatBoldItalic)
            line += 1            
            for i in range(self.size(testcase_sequence=tcs_index)):
                sheet.write(line, 1 + i, i)
            id_col = i + 3
            sheet.write(line - 1, id_col, f'{labelTetsrun} ID', cellFormatBoldItalic)
            # status
            for tr in self.query_set:
                line += 1
                sheet.write(line, 0, tr.startTime.strftime('%Y-%m-%d %H:%M:%S'))
                col = 1
                for tc in tr.testcase_sequences[tcs_index].testcases:
                    sheet.write(line, col, tc.status, status_style.get(tc.status))
                    #sheet.write(line, col, tc.duration, status_style.get(tc.status))
                    col += 1
                #sheet.write(line, col, tr.duration)
                #sheet.write(line, col+1, tr.testcase_sequences[0].duration)
                sheet.write(line, id_col, str(tr))

            line += 1
            sheet.write(line, 0, labelAvgDuration, cellFormatBoldItalic)
            for tc_index in range(self.size(testcase_sequence=tcs_index)):
                sheet.write(line, tc_index+1, self.average_duration(testcase_sequence=tcs_index, testcase=tc_index))

        # test case tabs
        for stage in self.stages:
            sheet = workbook.add_worksheet(f'{stage}_JSON')
            # write headers
            headers = [
                'Stage',
                f'{labelTetsrun} ID',
                f'{labelTestCase} ID',
                'Attribute',
                'Value',
            ]
            for index, label in enumerate(headers):
                sheet.write(0, index, label, cellFormatBold)
            # write data
            line = 1
            for tr in self.query_set:
                # check the stage
                if tr.stage == stage:
                    for tcs in tr.testcase_sequences:
                        for tc in tcs.testcases:
                            for field in tc.fields:
                                sheet.write(line, 0, stage)
                                sheet.write(line, 1, str(tr))
                                sheet.write(line, 2, str(tc))
                                sheet.write(line, 3, field.name)
                                sheet.write(line, 4, field.value)
                                line += 1

            # autowidth
            for i in range(len(headers)):
                ExcelSheetHelperFunctions.set_column_autowidth(sheet, i)

        workbook.close()

        logger.info(f'Query successfully exported to {path_to_file}')

        return path_to_file

