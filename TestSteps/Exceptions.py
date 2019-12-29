import logging

logger = logging.getLogger("pyC")

class pyFETestException(Exception):
    def __init__(self, *args, **kwargs):
        logger.exception("Exception occured - aborting")
        pass