from baangt.base.Faker import Faker
import random
import datetime
import logging

logger = logging.getLogger("pyC")

class RandomValues:
    def __init__(self):
        self.fake = Faker().faker

    def retrieveRandomValue(self, RandomizationType="string", mini=None, maxi=None, format=None):
        '''
        updates attribute then calls another function to generate random value and return it to the caller.
        :param RandomizationType:
        :param mini:
        :param maxi:
        :param format:
        :return:
        '''
        self.RandomizationType = RandomizationType
        self.min = mini
        self.max = maxi
        self.format = format
        return self.generateValue()

    def generateValue(self):
        '''
        Generates random value as per input type and other parameters
        :return:
        '''
        if self.RandomizationType.lower() == "string":
            self.min = self.min or 3  # If value is none than change it to 3. We can do this in parameter but as we have
            self.max = self.max or 10 # multiple types and we need different default value for each of them, this is used.
            return self.fake.pystr(self.min, self.max)  # used faker module of baangt to generate string name

        elif self.RandomizationType.lower() == "name":
            return self.fake.name()  # used faker module of baangt to generate fake name

        elif self.RandomizationType.lower() == "int":
            self.min = self.min or 0
            self.max = self.max or 1000000
            return random.randint(self.min, self.max)

        elif self.RandomizationType.lower() == "float":
            self.min = self.min or 0
            self.max = self.max or 1000
            flt = random.uniform(self.min, self.max)
            return flt

        elif self.RandomizationType.lower() == "date":
            self.format = self.format or "%d/%m/%Y"
            if self.min:
                try:
                    self.min = datetime.datetime.strptime(self.min, self.format).timestamp()
                except Exception as ex:
                    logger.info(f"Minimum date's structure or format is incorrect - {str(ex)}")
                    self.min = 86400
            else:
                self.min = 86400
            if self.max:
                try:
                    self.max = datetime.datetime.strptime(self.max, self.format).timestamp()
                except Exception as ex:
                    logger.info(f"Maximum date's structure or format is incorrect - {str(ex)}")
                    self.max = datetime.datetime.now().timestamp()
            else:
                self.max = datetime.datetime.now().timestamp()
            return datetime.datetime.fromtimestamp(random.randint(self.min, self.max)).strftime(self.format)

        elif self.RandomizationType.lower() == "time":
            self.format = self.format or "%H:%M:%S"
            base = datetime.datetime(2000, 1, 1)
            if self.min:
                try:
                    time = datetime.datetime.strptime(self.min, self.format)
                    mini = base.replace(hour=time.hour, minute=time.minute, second=time.second).timestamp()
                except Exception as ex:
                    logger.info(f"Minimum time's structure or format is incorrect - {str(ex)}")
                    mini = base.replace(hour=0, minute=0, second=0).timestamp()
            else:
                mini = base.replace(hour=0, minute=0, second=0).timestamp()
            if self.max:
                try:
                    time = datetime.datetime.strptime(self.max, self.format)
                    maxi = base.replace(hour=time.hour, minute=time.minute, second=time.second).timestamp()
                except Exception as ex:
                    logger.info(f"Maximum time's structure or format is incorrect - {str(ex)}")
                    maxi = base.replace(hour=11, minute=59, second=59).timestamp()
            else:
                maxi = base.replace(hour=11, minute=59, second=59).timestamp()
            return datetime.datetime.fromtimestamp(random.uniform(mini, maxi)).strftime(self.format)

        else:  # if type is not valid this statement will be executed
            raise BaseException(
                f"Incorrect type {self.RandomizationType}. Please use string, name, int, float, date, time.")

