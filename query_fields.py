from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from baangt.base.DataBaseORM import DATABASE_URL, TestrunLog, GlobalAttribute, TestCaseLog, TestCaseSequenceLog, TestCaseField
import time


class QueryFields:

    def __init__(self):
        # craate session
        engine = create_engine(DATABASE_URL)
        self.session = sessionmaker(bind=engine)

    def by_objects(self, name=None):
        db = self.session()
        print('Fields fetching started')
        time_start = time.time()
        time_mid = time_start
        # fetch fields
        fields = db.query(
            TestCaseField.name,
            TestCaseField.value,
            TestCaseLog.number,
        )\
            .join(TestCaseField.testcase).join(TestCaseLog.testcase_sequence).join(TestCaseSequenceLog.testrun)\
            .filter(and_(TestrunLog.testrunName == name, TestCaseSequenceLog.number == 1))\
            .order_by(TestrunLog.startTime).order_by(TestCaseLog.number)
        counter = 0
        for fname, fvalue, tc in fields.yield_per(1000):
            counter += 1
            v = fvalue.replace("\n", " ")[:30]
            print(f'{counter}\t{name}{tc:4} {fname:32}{v}')
            
            #if not counter%100000:
            #   time_cur = time.time()
            #   print(f'** {counter:,} records fetched in {time_cur-time_mid} seconds'.replace(',', ' '))
            #   print(field)
            #   time_mid = time_cur
        time_elapsed = time.time() - time_start

        print(f'\n*** FETCHED: {counter:,} fields'.replace(',', ' '))
        print(f'*** EXECUTION TIME: {time_elapsed}')


if __name__ == '__main__':
    q = QueryFields()
    q.by_objects(name='kfz.xlsx')