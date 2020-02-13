import logging

logger = logging.getLogger("pyC")


class baangtTestStepException(Exception):
    def __init__(self, *args, **kwargs):
        logger.exception(f"Exception occured - aborting. Args: {args}, KWARGS: {kwargs}")