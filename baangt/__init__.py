import logging
from datetime import datetime
import pathlib
import sys
import os
from pathlib import Path
from pluggy import HookspecMarker, HookimplMarker, PluginManager
from baangt.base.PathManagement import ManagedPaths

hook_spec = HookspecMarker("baangt")
hook_impl = HookimplMarker("baangt")
plugin_manager = PluginManager("baangt")

from baangt.hookSpecs import baangtHookSpec

plugin_manager.add_hookspecs(baangtHookSpec)

from baangt.base.TestRun.hookImpls import TestRunHookImpl
from baangt.base.BrowserHandling.hookImpls import BrowserDriverHookImpl
from baangt.base.Timing.hookImpls import TimingHookImpl
from baangt.base.ExportResults.hookImpls import \
    (ExportResultsHookImpl, ExcelSheetHelperFunctionsHookImpl, ExportTimingHookImpl)

plugin_manager.register(plugin=TestRunHookImpl())
plugin_manager.register(plugin=BrowserDriverHookImpl())
plugin_manager.register(plugin=TimingHookImpl())
plugin_manager.register(plugin=ExportResultsHookImpl())
plugin_manager.register(plugin=ExcelSheetHelperFunctionsHookImpl())
plugin_manager.register(plugin=ExportTimingHookImpl())

# fixme: Parameter für Logfile should include stage and browser()
managedPaths = ManagedPaths()
logFilename:pathlib.Path = Path(managedPaths.getLogfilePath())
pathlib.Path(logFilename).mkdir(parents=True, exist_ok=True)
logFilename = logFilename.joinpath(datetime.now().strftime("%Y%m%d_%H%M%S") + '.log')

print(f"Logfile used: {logFilename}")

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

# Some general debug info:
logger.debug(f"Value of sys._MEIPASS {getattr(sys, '_MEIPASS', 'None')}")
logger.debug(f"Value of __file__: {__file__}")
logger.debug(f"Value of sys.executable: {sys.executable}")
logger.debug(f"Value of sys.argv[0]: {sys.argv[0]}")
logger.debug(f"Value of sys.path: {sys.path}")
logger.debug(f"Value of os.path: {os.path}")
logger.debug(f"Value of os.getcwd(): {os.getcwd()}")
logger.debug(f"Value of Path.cwd(): {Path.cwd()}")

if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
    logger.debug('running in a PyInstaller bundle')
else:
    logger.debug('running in a normal Python process')

