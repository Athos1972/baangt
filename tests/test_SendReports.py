from baangt.base.SendReports import Sender
from pathlib import Path
import configparser
import os
from unittest.mock import patch
from atlassian import Confluence


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


def fake_response(text):
    return '{"test@pytest": "Success"}'

@patch.object(Confluence, "create_page")
@patch.object(Confluence, "attach_file")
def test_confluence(mock_attach, mock_create):
    send_stats.globalSettings["Confluence-Base-Url"] = "xxxx"
    send_stats.globalSettings["Confluence-Space"] = "xxxx"
    send_stats.globalSettings["Confluence-Pagetitle"] = "xxxx"
    send_stats.globalSettings["Confluence-Username"] = "xxxx"
    send_stats.globalSettings["Confluence-Password"] = "xxxx"
    send_stats.globalSettings["Confluence-Rootpage"] = "xxxx"
    send_stats.globalSettings["Confluence-Remove_Headers"] = "xxxx"
    send_stats.globalSettings["Confluence-Uploadoriginalfile"] = "xxxx"
    send_stats.globalSettings["Confluence-Createsubpagesforeachxxentries"] = 11
    send_stats.sendConfluence()
    assert 1 == 1


@patch("json.loads", fake_response)
@patch("requests.post")
def test_SendMail(mock_request):
    send_stats.defaultSettings["SendMailTo"] = "test@pytest"
    send_stats.sendMail()
    assert mock_request.call_count == 1


@patch("pymsteams.connectorcard")
def test_SendMsTeams(mock_conn):
    send_stats.defaultSettings["MsWebHook"] = "xxxx"
    send_stats.sendMsTeam()
    assert mock_conn.call_count == 1


@patch("slack_webhook.Slack")
def test_SendSlack(mock_conn):
    send_stats.defaultSettings["SlackWebHook"] = "xxxx"
    send_stats.sendSlack()
    assert 1 == 1