from dataclasses import dataclass

import threading

lock = threading.Lock()

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class Statistic(metaclass=Singleton):
    testcases_total: int = 0
    testcases_executed: int = 0
    testcases_remaining: int = 0
    testcases_paused: int = 0
    testcases_success: int = 0
    testcases_failed: int = 0
    teststep_executed: int = 0
    testcase_sequence_executed: int = 0
    teststep_sequence_executed: int = 0

    def __str__(self):
        string = [f"{key.split('_')[0]+' '+key.split('_')[1]}: {self.__dict__[key]}" for key in self.__dict__]
        return "\n".join(string)

    def total_testcases(self, number):
        self.testcases_total = number

    def update_all(self, success, error, waiting):
        self.testcases_executed = success+error
        self.testcases_remaining = self.testcases_total - self.testcases_executed
        self.testcases_paused = waiting
        self.testcases_success = success
        self.testcases_failed = error

    def update_teststep(self):
        self.teststep_executed += 1

    def update_testcase_sequence(self):
        self.testcase_sequence_executed += 1

    def update_teststep_sequence(self):
        self.teststep_sequence_executed += 1

    @staticmethod
    def get_update():
        return Statistic().__str__()


