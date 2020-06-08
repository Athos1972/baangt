from baangt.base.SendReports import Sender
from pathlib import Path
import configparser
import requests
import json
import os


def readConfig():
    """ Read existing sendstatistic.ini file """
    globalSettings = {}
    config = configparser.ConfigParser()
    config_file = Path(os.getcwd()).joinpath("tests").joinpath("0TestInput").joinpath("sendstatistics.ini")
    print(config_file)
    config.read(config_file)
    globalSettings["TelegramBot"] = config["Default"].get("TelegramBot")
    globalSettings["TelegramChannel"] = config["Default"].get("TelegramChannel")
    return globalSettings

settings = readConfig()
send_stats = Sender(settings, "tests/0TestInput/sendstatistics.xlsx")
subject, body = send_stats.create_body()

def test_telegram():
    messages = send_stats.sendTelegram(test=True)
    text = subject + "\n\n" + body
    assert text in messages
