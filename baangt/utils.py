from datetime import datetime
import traceback

class utils:
    def __init__(self):
        self.__perf_trace = {}

    @staticmethod
    def datetime_return():
        # needed, so that the datetime-module is called newly
        t = datetime.now().strftime("%Y%m%d_%H%M%S")
        return t
