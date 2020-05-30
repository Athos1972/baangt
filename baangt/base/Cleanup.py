import os
import logging
from time import sleep
from pathlib import Path
from datetime import datetime
from baangt.base.PathManagement import ManagedPaths
from baangt.base.DownloadFolderMonitoring import DownloadFolderMonitoring

logger = logging.getLogger("pyC")


class Cleanup:
    def __init__(self, days: float = 31):
        self.managedPaths = ManagedPaths()
        self.threshold = days

    def clean_logs(self):
        logger.info(f"Removing logs older than {str(self.threshold)} days")
        logs_dir = self.managedPaths.getLogfilePath()
        files = Path(logs_dir).glob('**/*')
        removed = []
        for file in files:
            timedelta = datetime.now() - datetime.fromtimestamp(DownloadFolderMonitoring.creation_date(file))
            if timedelta.total_seconds()/86400 > self.threshold:
                try:
                    os.remove(str(file))
                    removed.append(file)
                except:
                    logger.debug(f"Cannot remove {str(file)}")
                    continue
                logger.debug(f"{str(file)} deleted")
        if len(removed) == 0:
            logger.info(f"No log file older than {str(self.threshold)} days found")
        else:
            logger.info(f"{str(len(removed))} Log file deleted")

    def clean_screenshots(self):
        logger.info(f"Removing screenshots older than {str(self.threshold)} days")
        ss_dir = self.managedPaths.getOrSetScreenshotsPath()
        files = Path(ss_dir).glob('**/*')
        removed = []
        for file in files:
            timedelta = datetime.now() - datetime.fromtimestamp(DownloadFolderMonitoring.creation_date(file))
            if timedelta.total_seconds()/86400 > self.threshold:
                try:
                    os.remove(str(file))
                    removed.append(file)
                except:
                    logger.debug(f"Cannot remove {str(file)}")
                    continue
                logger.debug(f"{str(file)} deleted")
        if len(removed) == 0:
            logger.info(f"No Screenshot older than {str(self.threshold)} days found")
        else:
            logger.info(f"{str(len(removed))} Screenshot deleted")

    def clean_downloads(self):
        logger.info(f"Removing downloads older than {str(self.threshold)} days")
        downloads_dir = self.managedPaths.getOrSetAttachmentDownloadPath()
        files = Path(downloads_dir).glob('**/*')
        removed = []
        for file in files:
            if file.is_file():
                timedelta = datetime.now() - datetime.fromtimestamp(DownloadFolderMonitoring.creation_date(file))
                if timedelta.total_seconds()/86400 > self.threshold:
                    try:
                        os.remove(str(file))
                        removed.append(file)
                    except:
                        logger.debug(f"Cannot remove {str(file)}")
                        continue
                    logger.debug(f"{str(file)} deleted")
        if len(removed) == 0:
            logger.info(f"No downloads older than {str(self.threshold)} days found")
        else:
            logger.info(f"{str(len(removed))} downloads deleted")
        sleep(1)
        logger.info("Removing empty folders inside download folder.")
        files = Path(downloads_dir).glob('**/*')
        removed = []
        for file in files:
            if file.is_dir():
                if len(os.listdir(str(file))) == 0:
                    try:
                        os.rmdir(str(file))
                        removed.append(file)
                    except:
                        logger.debug(f"Cannot remove folder {str(file)}")
                        continue
                    logger.debug(f"{str(file)} folder deleted")
        if len(removed) == 0:
            logger.info(f"No empty folder found inside downloads")
        else:
            logger.info(f"{str(len(removed))} empty folder deleted")

    def clean_all(self):
        self.clean_logs()
        self.clean_screenshots()
        self.clean_downloads()
