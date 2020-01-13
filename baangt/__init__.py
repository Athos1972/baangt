import logging
from datetime import datetime
import pathlib

# fixme: Parameter für Logfile should include stage and browser()
logFilename:pathlib.Path = pathlib.Path(__file__)
logFilename = logFilename.parent.parent
logFilename = logFilename.joinpath('logs')
pathlib.Path(logFilename).mkdir(parents=True, exist_ok=True)
logFilename = logFilename.joinpath(datetime.now().strftime("%Y%m%d_%H%M%S") + '.log')

print(f"Logfile verwendet: {logFilename}")

# Bit more advanced logging
logger = logging.getLogger('pyC')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fileHandler = logging.FileHandler(logFilename, encoding ="UTF-8")
fileHandler.setLevel(level=logging.DEBUG)
# create console handler with a higher log level
channelHandler = logging.StreamHandler()
channelHandler.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s _ %(levelname)s _ %(module)s _ %(funcName)s : %(message)s')
channelHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(channelHandler)
logger.addHandler(fileHandler)