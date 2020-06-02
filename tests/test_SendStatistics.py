from baangt.base.SendStatistics import Sender
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
    globalSettings["SlackWebHook"] = config["Default"].get("SlackWebHook")
    globalSettings["TelegramBot"] = config["Default"].get("TelegramBot")
    globalSettings["TelegramChannel"] = config["Default"].get("TelegramChannel")
    return globalSettings

settings = readConfig()
send_stats = Sender(settings, "tests/0TestInput/sendstatistics.xlsx")
subject, body = send_stats.create_body()

def test_slack():
    send_stats.sendSlack()
    text = subject + "\n\n" + body
    token = "xoxb-1046914962533-1180874542160-Zw0JNcKcYholZ8QLxGMliWJB"
    channel = "C014DRKRE30"
    url = f'https://slack.com/api/channels.history?token={token}&channel={channel}&count=5'
    res = requests.get(url)
    js = json.loads(res.content)
    messages = [m['text'] for m in js['messages']]
    assert text in messages

def test_telegram():
    messages = send_stats.sendTelegram(test=True)
    text = subject + "\n\n" + body
    assert text in messages
