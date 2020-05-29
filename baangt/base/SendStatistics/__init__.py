from baangt.base.SendStatistics.mailer import SendMail
import configparser
from baangt.base.PathManagement import ManagedPaths
import os


class Sender:
    def __init__(self, settings, filename):
        self.globalSettings = {}
        self.set_globalSettings(settings)
        self.xlsx_file = filename
        self.sendMail()

    def sendMail(self):
        if len(self.globalSettings.get("SendMailTo")) > 0:
            SendMail(self.globalSettings, self.xlsx_file)

    def set_globalSettings(self, setting):
        if "SendMailTo" in setting:
            self.globalSettings = setting
        else:
            self.readConfig()

    def readConfig(self):
        """ Read existing baangt.ini file """
        config = configparser.ConfigParser()
        managedPaths = ManagedPaths()
        config_file = managedPaths.getOrSetIni().joinpath("mail.ini")
        if not os.path.exists(config_file):
            config_write = configparser.ConfigParser()
            config_write["Default"] = {
                "SendMailTo": "",
                "NotificationWithAttachment": 'False'
            }
            with open(config_file, "w" ) as configFile:
                config_write.write(configFile)
        config.read(config_file)
        self.globalSettings["SendMailTo"] = config["Default"].get("SendMailTo") or ""
        self.globalSettings["NotificationWithAttachment"] = config["Default"].get("NotificationWithAttachment") or False

