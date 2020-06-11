import os
import csv
import xlrd
import json
import xlsxwriter
import logging
import requests
import pymsteams
import configparser
from slack_webhook import Slack
from baangt.base.PathManagement import ManagedPaths
from baangt.base.SendReports.mailer import SendMail

logger = logging.getLogger('pyC')


class Sender:
    def __init__(self, settings, filename, attach_file=""):
        self.defaultSettings = settings
        self.xlsx_file = filename
        self.attach_file = attach_file
        self.subject, self.body = self.create_body()

    def sendMail(self):
        self.set_globalSettings(self.defaultSettings, "SendMailTo")
        if len(self.globalSettings.get("SendMailTo")) > 0:
            SendMail(self.globalSettings, self.xlsx_file, self.subject, self.body, self.attach_file)

    def sendMsTeam(self):
        self.set_globalSettings(self.defaultSettings, "MsWebHook")
        if len(self.globalSettings.get("MsWebHook")) > 0:
            lis = self.get_list(self.globalSettings.get("MsWebHook"))
            try:
                for hooks in lis:
                    text = "<pre>" + self.subject + "\n\n" + self.body + "</pre>"
                    text.replace('\n', '<br>')
                    msg = pymsteams.connectorcard(hooks)
                    msg.text(text)
                    msg.send()
                    logger.info(f"MsTeam sent to: {hooks}")
            except Exception as ex:
                logger.info(ex)

    def sendSlack(self):
        self.set_globalSettings(self.defaultSettings, "SlackWebHook")
        if len(self.globalSettings.get("SlackWebHook")) > 0:
            lis = self.get_list(self.globalSettings.get("SlackWebHook"))
            try:
                for hooks in lis:
                    text = self.subject+"\n\n"+self.body
                    slack = Slack(url=hooks)
                    slack.post(text=text)
                    logger.info(f"Slack sent to: {hooks}")
            except Exception as ex:
                logger.info(ex)

    def sendTelegram(self, test=False):
        self.set_globalSettings(self.defaultSettings, "TelegramBot")
        bot = self.globalSettings.get("TelegramBot")
        if len(bot) > 0 and len(self.globalSettings.get("TelegramChannel")):
            lis = self.get_list(self.globalSettings.get("TelegramChannel"))
            messages = []
            for channel in lis:
                try:
                    text = self.subject + "\n\n" + self.body
                    if channel[0] != '@':
                        channel = '@' + channel
                    url = f"https://api.telegram.org/bot{bot}/sendMessage?chat_id={channel}&text={text}"
                    res = requests.get(url)
                    js = json.loads(res.content)
                    if res.status_code == 200:
                        logger.info(f"Sent to {channel} telegram channel")
                        if js['ok']:
                            messages.append(js["result"]["text"])
                    else:
                        logger.info(res.content)
                except Exception as ex:
                    logger.info(ex)
            if test:
                return messages

    def set_globalSettings(self, setting, word_to_look):
        if word_to_look in setting:
            self.globalSettings = setting
        else:
            self.readConfig()

    def readConfig(self):
        """ Read existing mail.ini file if not exist then will write one with empty values"""
        self.globalSettings = {}
        config = configparser.ConfigParser()
        managedPaths = ManagedPaths()
        config_file = managedPaths.getOrSetIni().joinpath("mail.ini")
        if not os.path.exists(config_file):
            self.write_config(config_file)
        config.read(config_file)
        self.globalSettings["SendMailTo"] = config["Default"].get("SendMailTo"
                                            ) or self.write_config(config_file, "SendMailTo", "")
        self.globalSettings["NotificationWithAttachment"] = config["Default"].get("NotificationWithAttachment"
                                            ) or self.write_config(config_file, "NotificationWithAttachment", False)
        self.globalSettings["MsWebHook"] = config["Default"].get("MsWebHook"
                                            ) or self.write_config(config_file, "MsWebHook", "")
        self.globalSettings["SlackWebHook"] = config["Default"].get("SlackWebHook"
                                            ) or self.write_config(config_file, "SlackWebHook", "")
        self.globalSettings["TelegramBot"] = config["Default"].get("TelegramBot"
                                                                    ) or self.write_config(config_file, "TelegramBot",
                                                                                           "")
        self.globalSettings["TelegramChannel"] = config["Default"].get("TelegramChannel"
                                                                    ) or self.write_config(config_file, "TelegramChannel",
                                                                                           "")

    def write_config(self, config_file, key=None, value=None):
        if key:
            config_write = configparser.ConfigParser()
            config_write["Default"] = {key: value}
            for keys in self.globalSettings:
                config_write["Default"][keys] = self.globalSettings[keys]
            with open(config_file, "w") as configFile:
                config_write.write(configFile)
            return value
        config_write = configparser.ConfigParser()
        config_write["Default"] = {
            "SendMailTo": "",
            "NotificationWithAttachment": 'False',
            "MsWebHook": "",
            "SlackWebHook": "",
            "TelegramBot": "",
            "TelegramChannel": ""
        }
        with open(config_file, "w") as configFile:
            config_write.write(configFile)

    def create_body(self):
        """
        Will create body from mail by using summary tab of xlsx output file.
        Any changes in body structure should be made in this function.
        :return:
        """
        wb = xlrd.open_workbook(self.xlsx_file)
        sheet = wb.sheet_by_name("Summary")
        data = []
        for x in range(2, sheet.nrows):
            lis = []
            for cell in sheet.row(x):
                value = cell.value
                if type(value) == float:
                    value = str(value)
                    if value[-2:] == '.0':
                        value = value[:-2]
                else:
                    value = str(value).strip()
                lis.append(value)
            while "" in lis:
                lis.remove("")
            if lis != []:
                data.append(' = '.join(lis))
        subject = sheet.row(0)[0].value.strip()
        body = '\n'.join(data)
        return subject, body

    def get_list(self, string):
        lis = string.split(',')
        lis = [data.strip() for data in lis]
        return lis

    @staticmethod
    def send_all(results, globalSettings):
        if ".csv" in results.fileName:
            # If output file is of CSV Format then we are creating a temporary xlsx file which is just used to
            # send reports and get deleted after that.
            temp_file = results.fileName + ".xlsx"
            results.workbook = xlsxwriter.Workbook(temp_file)
            results.summarySheet = results.workbook.add_worksheet("Summary")
            results.cellFormatGreen = results.workbook.add_format()
            results.cellFormatGreen.set_bg_color('green')
            results.cellFormatRed = results.workbook.add_format()
            results.cellFormatRed.set_bg_color('red')
            results.cellFormatBold = results.workbook.add_format()
            results.cellFormatBold.set_bold(bold=True)
            results.summaryRow = 0
            results.makeSummaryExcel()
            results.closeExcel()
            send_stats = Sender(globalSettings, temp_file, results.fileName)
            os.remove(temp_file)
        else:
            send_stats = Sender(globalSettings, results.fileName)
        try:
            send_stats.sendMail()
        except Exception as ex:
            logger.debug(ex)
        try:
            send_stats.sendMsTeam()
        except Exception as ex:
            logger.debug(ex)
        try:
            send_stats.sendSlack()
        except Exception as ex:
            logger.debug(ex)
        try:
            send_stats.sendTelegram()
        except Exception as ex:
            logger.debug(ex)


